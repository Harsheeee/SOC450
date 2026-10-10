#!/usr/bin/env python3
"""
Step 07 (v2, Protocol Amendment 1): Rebuild analysis dataset.
Fixes: skip-aware cognition scoring (no fillna(0)), memory+orientation primary outcome (A1),
weighted 10th-percentile cut-off (A2), strict orientation / mh045 outliers / caste 'Other' (A3).
Reads v1 clean file for already-validated covariates; re-derives cognition from raw items.
"""
import numpy as np
import pandas as pd
import pyreadstat

RAW = "dataset/3_LASI_W1_Individual_v4.dta"
V1 = "data_analysis/lasi_clean_analysis.parquet"
OUT = "data_analysis/lasi_clean_v2.parquet"

cols = ['prim_key', 'dm013', 'dm005', 'ht235',
        'mh002', 'mh003', 'mh004', 'mh005', 'mh006', 'mh007', 'mh008', 'mh009',
        'mh012', 'mh056', 'mh019', 'mh020', 'mh038', 'mh045', 'mh046', 'mh047', 'mh050', 'mh051']
raw, _ = pyreadstat.read_dta(RAW, usecols=cols)
v1 = pd.read_parquet(V1)
df = v1.merge(raw.drop(columns=['dm005']), on='prim_key', how='left', validate='1:1')
assert len(df) == 66606

# A3: caste 'Other' (5) kept as own category instead of missing
caste_map = {1: 'SC', 2: 'ST', 3: 'OBC', 4: 'General/None', 5: 'Other'}
df['caste'] = df['dm013'].map(caste_map)

# A3: age >= 100 flag
df['age_ge100'] = (df['age'] >= 100).astype(int)

# Priority 1: Recode childhood health using the published study's definition
# Original paper: Poor/Very poor = 1; Very good/Good/Fair = 0
df['childhood_health_poor_original'] = np.where(
    df['childhood_health_5cat'].isna(),
    np.nan,
    df['childhood_health_5cat'].isin(['Poor', 'Very poor']).astype(float)
)

# 'Varied' SES retained for sensitivity (v1 file had it as 'Varied')
direct = df['direct_interview'] == 1

# ---- Memory (0-20) ; Orientation (0-8, all 8 items required) ----
df['memory_score'] = df['mh012'] + df['mh056']
ocols = ['mh002', 'mh003', 'mh004', 'mh005', 'mh006', 'mh007', 'mh008', 'mh009']
op = pd.DataFrame({c: df[c].map({1: 1.0, 2: 0.0}) for c in ocols})
df['orientation_score'] = np.where(op.notna().all(axis=1), op.sum(axis=1), np.nan)
df['mem_orient'] = np.where(direct, df['memory_score'] + df['orientation_score'], np.nan)  # 0-28

# ---- Skip-aware full battery: domain proportions on items actually asked ----
def prop(parts):
    """parts: list of (series_points, max_points). Proportion on asked items; NaN if none asked."""
    pts = pd.concat([p for p, _ in parts], axis=1)
    mx = pd.DataFrame({i: np.where(p.notna(), m, 0) for i, (p, m) in enumerate(parts)})
    mx.index = pts.index
    num = pts.sum(axis=1, min_count=1)
    den = mx.sum(axis=1)
    return np.where(den > 0, num / den.replace(0, np.nan), np.nan)

mh045 = df['mh045'].where(df['mh045'] <= 5)  # A3: outliers (6-68) -> missing
arith = prop([
    (df['mh038'].map({1: 2.0, 2: 1.0, 3: 0.0}), 2),
    (mh045, 5),
    (df['mh046'].map({1: 1.0, 2: 0.0}), 1),
    (df['mh047'].map({1: 1.0, 2: 0.0}), 1)])
exe = prop([
    (df['mh050'].map({1: 1.0, 2: 2.0, 3: 3.0, 4: 0.0}), 3),
    (df['mh051'].map({1: 1.0, 2: 0.0}), 1)])  # 'Not applicable' (3) -> not asked/missing
nam = prop([(df['mh019'].map({1: 1.0, 2: 0.0}), 1), (df['mh020'].map({1: 1.0, 2: 0.0}), 1)])
dom = pd.DataFrame({'mem': df['memory_score'] / 20, 'ori': df['orientation_score'] / 8,
                    'ari': arith, 'exe': exe, 'nam': nam})
ok = direct & dom['mem'].notna() & dom['ori'].notna()
df['battery_pct'] = np.where(ok, dom.mean(axis=1) * 100, np.nan)  # mean of available domains (0-100)

# ---- Weighted 10th percentile (A2) ----
def wquantile(x, w, q):
    o = np.argsort(x); x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = np.cumsum(w) / w.sum()
    return x[np.searchsorted(c, q)]

def add_impairment(score, name):
    m = df[score].notna()
    cut = wquantile(df.loc[m, score].values, df.loc[m, 'survey_weight'].values, 0.10)
    df[name] = np.where(m, (df[score] <= cut).astype(float), np.nan)
    wprev = np.average(df.loc[m, name], weights=df.loc[m, 'survey_weight'])
    print(f"{score}: weighted p10 cutoff <= {cut:.2f}; weighted prevalence {wprev*100:.1f}%; n={m.sum():,}")
    return cut

cut_mo = add_impairment('mem_orient', 'low_memory_orientation')
cut_bat = add_impairment('battery_pct', 'imp_battery')

# Education-stratum-specific cut-offs for mem_orient (sensitivity)
df['edu3'] = df['education'].map({'No formal education': 'None', 'Less than primary': 'Low',
                                  'Primary completed': 'Low', 'Middle completed': 'Mid',
                                  'Secondary completed': 'Mid', 'Higher secondary/Diploma': 'High',
                                  'Graduate and above': 'High'})
df['low_memory_orientation_edustrat'] = np.nan
for g, sub in df[df['mem_orient'].notna() & df['edu3'].notna()].groupby('edu3'):
    cut = wquantile(sub['mem_orient'].values, sub['survey_weight'].values, 0.10)
    df.loc[sub.index, 'low_memory_orientation_edustrat'] = (sub['mem_orient'] <= cut).astype(float)
    print(f"  edu stratum {g}: cutoff <= {cut:.1f}, n={len(sub):,}")

# Response indicator for IPW (A8): direct interview but mem_orient missing
df['cog_observed'] = np.where(direct, df['mem_orient'].notna().astype(float), np.nan)

# Education / schooling descriptive check
print(df[df['mem_orient'].notna()].groupby('education')[['mem_orient', 'low_memory_orientation']].mean().round(3))
print("mem_orient missing among direct:", int(direct.sum() - df['mem_orient'].notna().sum()))

df.to_parquet(OUT, index=False)
print("saved", OUT, df.shape)
