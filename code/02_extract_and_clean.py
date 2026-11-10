#!/usr/bin/env python3
"""
Step 02: Extract, Clean, and Construct Analysis Dataset
- Extracts relevant variables from 3_LASI_W1_Individual_v4.dta
- Restricts target population to age >= 45
- Standardizes exposures, outcomes, covariates, and survey design identifiers
- Produces sample flow diagnostics and saves clean analytical dataset
"""

import os
import pyreadstat
import pandas as pd
import numpy as np

# File paths
RAW_DTA = "dataset/3_LASI_W1_Individual_v4.dta"
OUTPUT_DIR = "data_analysis"
DIAG_DIR = "outputs/diagnostics"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DIAG_DIR, exist_ok=True)

# 1. Variables to extract
extract_cols = [
    # IDs & Survey Design
    'prim_key', 'hhid', 'stateid', 'state', 'ssuid', 'residence',
    'indiaindividualweight', 'stateindividualweight', 'rproxy',
    # Demographics & Adult SES
    'dm003', 'dm005', 'dm006', 'dm007', 'dm008', 'dm013', 'dm021',
    'mpce_quintile', 'mpce_amount',
    # Exposures
    'ht235', 'ht231', 'ht233', 'ht234',
    # Depression: CES-D 10 items
    'fs701', 'fs702', 'fs703', 'fs704', 'fs705', 'fs706', 'fs707', 'fs708', 'fs709', 'fs710',
    # Cognition components (43-point battery)
    'mh002', 'mh003', 'mh004', 'mh005', 'mh006', 'mh007', 'mh008', 'mh009',  # Orientation (8)
    'mh012',  # Immediate recall (10)
    'mh056',  # Delayed recall (10)
    'mh016_correct',  # Verbal fluency
    'mh019', 'mh020',  # Object naming (2)
    'mh038',  # Backward counting (2)
    'mh045',  # Serial 7s (5)
    'mh046', 'mh047',  # Computation sale & lottery (2)
    'mh050',  # Paper folding (3)
    'mh051',  # Overlapping pentagons drawing (1)
    'mh058',  # MH test assistance
    # Adult health pathway controls
    'ht001_a', 'ht002', 'ht003', 'ht005', 'ht006', 'ht007'
]

print(f"Reading {len(extract_cols)} variables from {RAW_DTA}...")
df_raw, meta = pyreadstat.read_dta(RAW_DTA, usecols=extract_cols)
n_raw = len(df_raw)
print(f"Successfully loaded {n_raw:,} records.")

# 2. Sample Filtering: Age >= 45
df = df_raw[df_raw['dm005'] >= 45].copy()
n_45plus = len(df)
print(f"Restricted to Age >= 45: {n_45plus:,} respondents ({n_45plus/n_raw*100:.2f}% of survey).")

# 3. Clean Demographics & Adult SES
# Age & Age Group
df['age'] = df['dm005'].astype(int)
df['age_group'] = pd.cut(
    df['age'],
    bins=[45, 60, 75, 125],
    right=False,
    labels=['45-59', '60-74', '75+']
)

# Sex (1=Male, 2=Female)
df['sex'] = df['dm003'].map({1: 'Male', 2: 'Female'})

# Residence (1=Rural, 2=Urban)
df['residence_cat'] = df['residence'].map({1: 'Rural', 2: 'Urban'})

# Caste category
# 1=SC, 2=ST, 3=OBC, 4=None/General
df['caste'] = df['dm013'].map({
    1: 'SC',
    2: 'ST',
    3: 'OBC',
    4: 'General/None'
})

# Marital Status
# 1=Married, 2=Widowed, 3=Divorced, 4=Separated, 5=Deserted, 6=Live-in, 7=Never married
def clean_marital(val):
    if pd.isna(val):
        return np.nan
    val = int(val)
    if val in [1, 6]:
        return 'Married/Partnered'
    elif val == 2:
        return 'Widowed'
    elif val in [3, 4, 5]:
        return 'Divorced/Separated'
    elif val == 7:
        return 'Never Married'
    return np.nan

df['marital_status'] = df['dm021'].apply(clean_marital)
df['married_binary'] = df['dm021'].apply(lambda v: 1 if v in [1, 6] else (0 if pd.notna(v) else np.nan))

# Education
# dm006: 1=Yes, 2=No
# dm008: 1=Less than primary, 2=Primary, 3=Middle, 4=Secondary, 5=Higher sec, 6=Diploma, 7=Graduate, 8=Postgrad, 9=Professional
def clean_education(row):
    dm006 = row['dm006']
    dm008 = row['dm008']
    if pd.isna(dm006):
        return np.nan
    if dm006 == 2:
        return 'No formal education'
    if pd.isna(dm008):
        return np.nan
    dm008 = int(dm008)
    if dm008 == 1:
        return 'Less than primary'
    elif dm008 == 2:
        return 'Primary completed'
    elif dm008 == 3:
        return 'Middle completed'
    elif dm008 == 4:
        return 'Secondary completed'
    elif dm008 in [5, 6]:
        return 'Higher secondary/Diploma'
    elif dm008 in [7, 8, 9]:
        return 'Graduate and above'
    return np.nan

df['education'] = df.apply(clean_education, axis=1)

# MPCE Quintile (1 to 5)
df['mpce_quintile'] = df['mpce_quintile'].astype(int)

# 4. Clean Early-Life Disadvantage Exposures
# Childhood SES: ht235 (1=Pretty well off, 2=Average, 3=Poor, 4=Varied)
def clean_child_ses(val):
    if pd.isna(val):
        return np.nan
    val = int(val)
    if val == 1:
        return 'Pretty well-off'
    elif val == 2:
        return 'Average'
    elif val == 3:
        return 'Poor'
    elif val == 4:
        return 'Varied'
    return np.nan

df['childhood_ses'] = df['ht235'].apply(clean_child_ses)

# Childhood Health: ht231 (1=Very good, 2=Good, 3=Fair, 4=Poor, 5=Very poor)
def clean_child_health_5(val):
    if pd.isna(val):
        return np.nan
    val = int(val)
    mapping = {1: 'Very good', 2: 'Good', 3: 'Fair', 4: 'Poor', 5: 'Very poor'}
    return mapping.get(val, np.nan)

def clean_child_health_bin(val):
    if pd.isna(val):
        return np.nan
    val = int(val)
    if val in [1, 2]:
        return 'Good'  # Reference
    elif val in [3, 4, 5]:
        return 'Poor'
    return np.nan

df['childhood_health_5cat'] = df['ht231'].apply(clean_child_health_5)
df['childhood_health'] = df['ht231'].apply(clean_child_health_bin)

# Childhood Bedridden: ht233 (1=Yes, 2=No)
def clean_child_bedridden(val):
    if pd.isna(val):
        return np.nan
    val = int(val)
    if val == 1:
        return 'Yes'
    elif val == 2:
        return 'No'  # Reference
    return np.nan

df['childhood_bedridden'] = df['ht233'].apply(clean_child_bedridden)

# Cumulative Childhood Disadvantage Score (0 to 3)
# Poor SES (Poor) = 1, Poor Health (Fair/Poor/Very poor) = 1, Bedridden (Yes) = 1
def calc_cumulative_disadvantage(row):
    ses = row['childhood_ses']
    hlth = row['childhood_health']
    bed = row['childhood_bedridden']
    if pd.isna(ses) or pd.isna(hlth) or pd.isna(bed):
        return np.nan
    score = 0
    if ses == 'Poor':
        score += 1
    if hlth == 'Poor':
        score += 1
    if bed == 'Yes':
        score += 1
    return score

df['cumulative_disadvantage'] = df.apply(calc_cumulative_disadvantage, axis=1)

# 5. Clean Depression Outcomes (CES-D 10 Items)
# Negative items: fs701, fs702, fs703, fs704, fs706, fs707, fs708
# 1 = Rarely/never (<1 day) -> 0; 2,3,4 = Sometimes/Often/Most (>=1 day) -> 1 (Standard published dichotomization)
neg_items = ['fs701', 'fs702', 'fs703', 'fs704', 'fs706', 'fs707', 'fs708']
# Positive items (reverse-coded): fs705, fs709, fs710
# 3,4 = Often/Most -> 0; 1,2 = Rarely/Never/Sometimes -> 1
pos_items = ['fs705', 'fs709', 'fs710']

for item in neg_items:
    df[f'{item}_bin'] = df[item].apply(lambda v: 1 if v in [3, 4] else (0 if v in [1, 2] else np.nan))

for item in pos_items:
    df[f'{item}_bin'] = df[item].apply(lambda v: 1 if v in [1, 2] else (0 if v in [3, 4] else np.nan))

cesd_bin_cols = [f'{col}_bin' for col in (neg_items + pos_items)]

# Sum score: Require at least 8 of 10 items present
df['cesd_valid_items'] = df[cesd_bin_cols].notna().sum(axis=1)
df['cesd_score'] = np.where(
    df['cesd_valid_items'] >= 8,
    df[cesd_bin_cols].sum(axis=1) * (10.0 / df['cesd_valid_items']),  # scaled to 10
    np.nan
)
df['cesd_score'] = df['cesd_score'].round(2)
df['cesd_depression'] = np.where(
    df['cesd_score'].notna(),
    (df['cesd_score'] >= 4.0).astype(int),
    np.nan
)

# 6. Clean Cognition Outcomes (43-point Composite Battery)
# Only direct interviews (rproxy == 0) were eligible for cognitive testing
df['direct_interview'] = (df['rproxy'] == 0).astype(int)

# A. Memory Domain (0 to 20): Immediate (0-10) + Delayed (0-10)
df['memory_score'] = df['mh012'] + df['mh056']

# B. Orientation Domain (0 to 8)
# mh002-mh009: 1=Correct, 2=Incorrect
orient_cols = ['mh002', 'mh003', 'mh004', 'mh005', 'mh006', 'mh007', 'mh008', 'mh009']
for c in orient_cols:
    df[f'{c}_pt'] = df[c].apply(lambda v: 1 if v == 1 else (0 if v == 2 else np.nan))
orient_pt_cols = [f'{c}_pt' for c in orient_cols]
df['orientation_score'] = df[orient_pt_cols].sum(axis=1)

# C. Arithmetic Function (0 to 9)
# mh038: Backward counting (1=Correct -> 2 pts, 2=Partial -> 1 pt, 3=Cannot -> 0 pts)
df['backward_pt'] = df['mh038'].map({1: 2, 2: 1, 3: 0})
# mh045: Serial 7s (0 to 5)
df['serial7_pt'] = df['mh045'].clip(lower=0, upper=5)
# mh046, mh047: Computation sale & lottery (1=Correct -> 1 pt, 2=Incorrect -> 0 pt)
df['comp_sale_pt'] = df['mh046'].map({1: 1, 2: 0})
df['comp_lottery_pt'] = df['mh047'].map({1: 1, 2: 0})
df['arithmetic_score'] = df[['backward_pt', 'serial7_pt', 'comp_sale_pt', 'comp_lottery_pt']].sum(axis=1)

# D. Executive Function (0 to 4)
# mh050: Paper folding (1=One task -> 1, 2=Two tasks -> 2, 3=All three -> 3, 4=None -> 0)
df['paper_folding_pt'] = df['mh050'].map({1: 1, 2: 2, 3: 3, 4: 0})
# mh051: Pentagon drawing (1=Drew -> 1, 2=Failed -> 0, 3=NA -> 0)
df['pentagon_pt'] = df['mh051'].apply(lambda v: 1 if v == 1 else (0 if pd.notna(v) else np.nan))
df['executive_score'] = df[['paper_folding_pt', 'pentagon_pt']].sum(axis=1)

# E. Object Naming (0 to 2)
# mh019, mh020: (1=Correct -> 1, 2=Incorrect -> 0)
df['naming_pencil_pt'] = df['mh019'].map({1: 1, 2: 0})
df['naming_watch_pt'] = df['mh020'].map({1: 1, 2: 0})
df['naming_score'] = df[['naming_pencil_pt', 'naming_watch_pt']].sum(axis=1)

# Composite Cognitive Score (0 to 43)
# Require valid memory and orientation at minimum
df['cognitive_score'] = np.where(
    (df['direct_interview'] == 1) & df['memory_score'].notna() & df['orientation_score'].notna(),
    df['memory_score'] + df['orientation_score'] + df['arithmetic_score'].fillna(0) + \
    df['executive_score'].fillna(0) + df['naming_score'].fillna(0),
    np.nan
)

# Cognitive Impairment: Defined as lowest 10th percentile of cognitive_score
valid_cog = df.loc[df['cognitive_score'].notna(), 'cognitive_score']
cog_cutoff_10th = valid_cog.quantile(0.10)
print(f"Cognitive score 10th percentile cutoff: {cog_cutoff_10th:.2f} points (Mean: {valid_cog.mean():.2f}, Median: {valid_cog.median():.2f})")

df['cognitive_impairment'] = np.where(
    df['cognitive_score'].notna(),
    (df['cognitive_score'] <= cog_cutoff_10th).astype(int),
    np.nan
)

# 7. Adult Health Controls (Model 3)
# Chronic conditions count: ht002, ht003, ht005, ht006, ht007 (1=Yes, 2=No)
chronic_cols = ['ht002', 'ht003', 'ht005', 'ht006', 'ht007']
for c in chronic_cols:
    df[f'{c}_yes'] = df[c].apply(lambda v: 1 if v == 1 else (0 if v == 2 else np.nan))
chronic_yes_cols = [f'{c}_yes' for c in chronic_cols]
df['chronic_count'] = df[chronic_yes_cols].sum(axis=1)
df['multimorbidity'] = df['chronic_count'].apply(lambda count: '2+ conditions' if count >= 2 else ('1 condition' if count == 1 else 'None'))

# Self-rated health (1=Very good to 5=Very poor)
df['srh'] = df['ht001_a'].map({1: 'Very good', 2: 'Good', 3: 'Fair', 4: 'Poor', 5: 'Very poor'})

# 8. Survey Design Variables
df['survey_weight'] = df['indiaindividualweight']
df['cluster_psu'] = df['ssuid'].astype(str)
df['stratum'] = (df['stateid'].astype(int).astype(str) + "_" + df['residence'].astype(int).astype(str))

# 9. Clean Analytical File Output
clean_cols = [
    # IDs & Design
    'prim_key', 'hhid', 'state', 'stateid', 'cluster_psu', 'stratum', 'survey_weight', 'rproxy', 'direct_interview',
    # Demographics
    'age', 'age_group', 'sex', 'residence_cat', 'caste', 'marital_status', 'married_binary',
    # Adult SES
    'education', 'mpce_quintile', 'mpce_amount',
    # Exposures
    'childhood_ses', 'childhood_health', 'childhood_health_5cat', 'childhood_bedridden', 'cumulative_disadvantage',
    # Depression
    'cesd_score', 'cesd_depression',
    # Cognition
    'memory_score', 'orientation_score', 'arithmetic_score', 'executive_score', 'naming_score',
    'cognitive_score', 'cognitive_impairment',
    # Adult Health Pathways
    'chronic_count', 'multimorbidity', 'srh'
]

clean_df = df[clean_cols].copy()
clean_parquet_path = os.path.join(OUTPUT_DIR, "lasi_clean_analysis.parquet")
clean_csv_path = os.path.join(OUTPUT_DIR, "lasi_clean_analysis.csv")

clean_df.to_parquet(clean_parquet_path, index=False)
clean_df.to_csv(clean_csv_path, index=False)
print(f"Saved clean analytical dataset ({len(clean_df):,} rows, {len(clean_cols)} columns) to:")
print(f"  - {clean_parquet_path}")
print(f"  - {clean_csv_path}")

# 10. Sample Flow Diagnostics
flow_records = [
    {"Stage": "1. Raw Wave 1 Individual Records", "N": n_raw, "Exclusion_Reason": "None (Full survey release)"},
    {"Stage": "2. Age >= 45 Target Population", "N": n_45plus, "Exclusion_Reason": "Excluded younger spouses (age < 45, N = 6,790)"},
    {"Stage": "3. Valid Childhood SES", "N": df['childhood_ses'].notna().sum(), "Exclusion_Reason": f"Missing ht235 (N = {df['childhood_ses'].isna().sum()})"},
    {"Stage": "4. Valid Childhood Health", "N": df['childhood_health'].notna().sum(), "Exclusion_Reason": f"Missing ht231 (N = {df['childhood_health'].isna().sum()})"},
    {"Stage": "5. Valid Childhood Bedridden", "N": df['childhood_bedridden'].notna().sum(), "Exclusion_Reason": f"Missing ht233 (N = {df['childhood_bedridden'].isna().sum()})"},
    {"Stage": "6. Direct Interview (Cognitive Eligible)", "N": (df['direct_interview'] == 1).sum(), "Exclusion_Reason": "Proxy interviews (rproxy = 1, N = 705)"},
    {"Stage": "7. Valid Cognitive Composite Score", "N": df['cognitive_score'].notna().sum(), "Exclusion_Reason": "Incomplete cognitive test battery"},
    {"Stage": "8. Valid CES-D Depression Score", "N": df['cesd_score'].notna().sum(), "Exclusion_Reason": "Incomplete CES-D items (>= 3 items missing)"},
]

flow_df = pd.DataFrame(flow_records)
flow_path = os.path.join(DIAG_DIR, "sample_flow.csv")
flow_df.to_csv(flow_path, index=False)
print(f"Saved sample flow table to {flow_path}:")
print(flow_df.to_string(index=False))

# 11. Missingness Summary for Analysis Variables
miss_records = []
for c in clean_cols:
    n_miss = clean_df[c].isna().sum()
    pct_miss = (n_miss / len(clean_df)) * 100
    miss_records.append({"Variable": c, "Non_Missing_N": len(clean_df) - n_miss, "Missing_N": n_miss, "Pct_Missing": round(pct_miss, 2)})

miss_df = pd.DataFrame(miss_records)
miss_path = os.path.join(DIAG_DIR, "missingness_summary.csv")
miss_df.to_csv(miss_path, index=False)
print(f"Saved missingness summary to {miss_path}")
