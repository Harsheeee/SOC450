#!/usr/bin/env python3
"""
Step 08 (v2, Protocol Amendment 1): corrected models.
 A4 common sample + state FE; A5 design-based variance; A6 mutual adjustment; A7 interaction tests + AME;
 A8 IPW; plus sensitivity analyses. Outputs in outputs/tables_v2, outputs/figures_v2.
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import patsy
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
from survey_utils import svy_glm, term_row, wald_F, wmean_ci
import statsmodels.api as sm
import statsmodels.formula.api as smf
warnings.filterwarnings("ignore")

T = "outputs/tables_v2"; F = "outputs/figures_v2"
os.makedirs(T, exist_ok=True); os.makedirs(F, exist_ok=True)
rng = np.random.default_rng(20260510)

d = pd.read_parquet("data_analysis/lasi_clean_v2.parquet")
# Correct SRH labels (v1 labels were shifted by one; ht001_a: 1 Excellent ... 5 Poor). Reference = Excellent.
d['srh'] = d['srh'].map({'Very good': 'Excellent', 'Good': 'Very good', 'Fair': 'Good', 'Poor': 'Fair', 'Very poor': 'Poor'})
d['state_fe'] = d['stateid'].astype(int)
d['ses_avg'] = np.where(d.childhood_ses.isin(['Pretty well-off', 'Average', 'Poor']), (d.childhood_ses == 'Average').astype(float), np.nan)
d['ses_poor'] = np.where(d.childhood_ses.isin(['Pretty well-off', 'Average', 'Poor']), (d.childhood_ses == 'Poor').astype(float), np.nan)
d['hlth_poor'] = np.where(d.childhood_health.notna(), (d.childhood_health == 'Poor').astype(float), np.nan)
d['bed_yes'] = np.where(d.childhood_bedridden.notna(), (d.childhood_bedridden == 'Yes').astype(float), np.nan)
d['age_c'] = d['age']

DEMO = "age + C(sex, Treatment('Male')) + C(residence_cat, Treatment('Rural')) + C(caste, Treatment('General/None')) + married_binary + C(state_fe)"
EDU = "C(education, Treatment('No formal education')) + C(mpce_quintile)"
HLTH = "chronic_count + C(srh, Treatment('Excellent'))"
FORM = {'M0': "", 'M1': DEMO, 'M2': f"{DEMO} + {EDU}", 'M3': f"{DEMO} + {EDU} + {HLTH}"}
MLAB = {'M0': 'Model 0: Unadjusted', 'M1': 'Model 1: Demographics + state', 'M2': 'Model 2: + Adult SES (Primary)', 'M3': 'Model 3: + Adult health (Pathway)'}
EXPO = {'ses_avg': 'Childhood SES: Average (vs well-off)', 'ses_poor': 'Childhood SES: Poor (vs well-off)',
        'hlth_poor': 'Childhood health: Fair/Poor/Very poor (vs Good/Very good)', 'bed_yes': 'Childhood bedridden ≥1 month (vs No)'}
CORE = ['ses_avg', 'ses_poor', 'hlth_poor', 'bed_yes', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'state_fe',
        'education', 'mpce_quintile', 'chronic_count', 'srh', 'survey_weight', 'cluster_psu', 'stratum']

def sample(outcome, extra=None, base=None):
    b = d if base is None else base
    return b.dropna(subset=CORE + [outcome] + (extra or [])).copy()

def rhs(exposures, m):
    parts = list(exposures) + ([FORM[m]] if FORM[m] else [])
    return " + ".join(parts)

def fam_of(outcome):
    return 'gaussian' if outcome in ('mem_orient', 'battery_pct') else 'poisson'

samples = {
    'Cognition (memory+orientation)': ('imp_mo', sample('imp_mo', base=d[d.direct_interview == 1])),
    'Depressive symptoms': ('cesd_depression', sample('cesd_depression')),
}
cont_cog = ('mem_orient', samples['Cognition (memory+orientation)'][1])

flow = []
for k, (o, s) in samples.items():
    flow.append(dict(Sample=k, N=len(s), Clusters=s.cluster_psu.nunique(), Strata=s.stratum.nunique()))
pd.DataFrame(flow).to_csv(f"{T}/table_s0_common_samples.csv", index=False)
print(pd.DataFrame(flow))

# ----------------------------------------------------------------------------
# TABLES 3v2/4v2: single-exposure models M0-M3 on the common sample
# ----------------------------------------------------------------------------
def run_single(label, outcome, s, family):
    exp_ = family == 'poisson'
    rows = []
    for e in EXPO:
        for m in ['M0', 'M1', 'M2', 'M3']:
            pre = ['ses_avg', 'ses_poor'] if e in ('ses_avg', 'ses_poor') else [e]  # SES always modelled jointly (ref = well-off)
            f = svy_glm(f"{outcome} ~ {rhs(pre, m)}", s, family)
            for term in ([e] if True else []):
                r = term_row(f, term, exp=exp_)
                rows.append(dict(Outcome=label, Exposure=EXPO[e], Model=MLAB[m], Estimate=round(r['est'], 3), CI_lower=round(r['lo'], 3),
                                 CI_upper=round(r['hi'], 3), p_value=round(r['p'], 4), Metric='PR' if exp_ else 'Mean diff (beta)', N=f.nobs))
    return rows

t3 = run_single('Cognitive impairment (lowest weighted decile, mem+orient)', 'imp_mo', samples['Cognition (memory+orientation)'][1], 'poisson')
pd.DataFrame(t3).to_csv(f"{T}/table3v2_cognition_impairment.csv", index=False)
t3c = run_single('Memory+orientation score (0-28)', 'mem_orient', cont_cog[1], 'gaussian')
pd.DataFrame(t3c).to_csv(f"{T}/table3v2b_cognition_continuous.csv", index=False)
t4 = run_single('Depressive symptoms (CES-D>=4)', 'cesd_depression', samples['Depressive symptoms'][1], 'poisson')
pd.DataFrame(t4).to_csv(f"{T}/table4v2_depression.csv", index=False)
print(pd.DataFrame(t3)[lambda x: x.Model.str.contains('Model 1|Model 2')].to_string())
print(pd.DataFrame(t4)[lambda x: x.Model.str.contains('Model 2')].to_string())

# Single-exposure estimates with Average SES term only partially shown; also add Poor-SES + Average joint (same model)
rows = []
for label, outcome, s in [('Cognitive impairment', 'imp_mo', samples['Cognition (memory+orientation)'][1]),
                          ('Depressive symptoms', 'cesd_depression', samples['Depressive symptoms'][1])]:
    for m in ['M0', 'M1', 'M2', 'M3']:
        f = svy_glm(f"{outcome} ~ ses_avg + ses_poor + {FORM[m] if FORM[m] else '1'}", s, 'poisson')
        for e in ['ses_avg', 'ses_poor']:
            r = term_row(f, e)
            rows.append(dict(Outcome=label, Exposure=EXPO[e], Model=MLAB[m], PR=round(r['est'], 3), CI_lower=round(r['lo'], 3), CI_upper=round(r['hi'], 3), p_value=round(r['p'], 4), N=f.nobs))
pd.DataFrame(rows).to_csv(f"{T}/table3v2c_ses_joint_categories.csv", index=False)

# ----------------------------------------------------------------------------
# TABLE 6: mutually adjusted models (A6) at M2 and M3, plus cumulative index
# ----------------------------------------------------------------------------
rows = []
for label, outcome, s in [('Cognitive impairment', 'imp_mo', samples['Cognition (memory+orientation)'][1]),
                          ('Depressive symptoms', 'cesd_depression', samples['Depressive symptoms'][1])]:
    for m in ['M1', 'M2', 'M3']:
        f = svy_glm(f"{outcome} ~ ses_avg + ses_poor + hlth_poor + bed_yes + {FORM[m]}", s, 'poisson')
        for e in EXPO:
            r = term_row(f, e)
            rows.append(dict(Outcome=label, Model=MLAB[m] + ' [mutually adjusted]', Exposure=EXPO[e], PR=round(r['est'], 3),
                             CI_lower=round(r['lo'], 3), CI_upper=round(r['hi'], 3), p_value=round(r['p'], 4), N=f.nobs))
    s2 = s.copy(); s2['cum'] = s2['ses_poor'] + s2['hlth_poor'] + s2['bed_yes']
    for m in ['M2']:
        f = svy_glm(f"{outcome} ~ cum + {FORM[m]}", s2, 'poisson')
        r = term_row(f, 'cum')
        rows.append(dict(Outcome=label, Model=MLAB[m] + ' [cumulative index 0-3]', Exposure='Per additional childhood adversity (Poor SES + poor health + bedridden)',
                         PR=round(r['est'], 3), CI_lower=round(r['lo'], 3), CI_upper=round(r['hi'], 3), p_value=round(r['p'], 4), N=f.nobs))
t6 = pd.DataFrame(rows); t6.to_csv(f"{T}/table6v2_mutual_adjustment.csv", index=False)
print(t6.to_string())

# ----------------------------------------------------------------------------
# TABLE 5v2: interaction (A7) -- joint Wald F tests + AME standardized predictions
# ----------------------------------------------------------------------------
AGE_CATS = ['45-59', '60-74', '75+']
def interaction(label, outcome, s, expo_cols, expo_name, ndraw=400):
    s = s.copy()
    f = svy_glm(f"{outcome} ~ ({' + '.join(expo_cols)}) * C(age_group, Treatment('45-59')) + {FORM['M2']}", s, 'poisson')
    ints = [n for n in f.names if ':' in n and any(c in n for c in expo_cols)]
    Fs, p = wald_F(f, ints)
    out = dict(Outcome=label, Exposure=expo_name, joint_F=round(Fs, 3), df_num=len(ints), joint_p=round(p, 4), N=f.nobs)
    # AME standardization within each age group
    di = f.model.data.model_spec
    B = rng.multivariate_normal(f.params.values, f.V.values, size=ndraw)
    preds = {}
    for ag in AGE_CATS:
        sub = s[s.age_group == ag]
        w = sub.survey_weight.values / sub.survey_weight.sum()
        for lvl_name, setting in LEVELS[expo_name].items():
            nd = sub.copy()
            for c, v in zip(expo_cols, setting):
                nd[c] = v
            X = np.asarray(patsy.build_design_matrices([di], nd, return_type='dataframe')[0])
            pt = np.clip(np.exp(X @ f.params.values), 0, 1) @ w
            dr = np.clip(np.exp(X @ B.T), 0, 1).T @ w
            preds[(ag, lvl_name)] = (pt, dr)
    rows = []
    for (ag, lv), (pt, dr) in preds.items():
        rows.append(dict(Outcome=label, Exposure=expo_name, age_group=ag, level=lv, pred_prev_pct=round(pt * 100, 2),
                         lo=round(np.percentile(dr, 2.5) * 100, 2), hi=round(np.percentile(dr, 97.5) * 100, 2)))
    rd = []
    for ag in AGE_CATS:
        lv0, lv1 = list(LEVELS[expo_name].keys())[0], list(LEVELS[expo_name].keys())[-1]
        pt = preds[(ag, lv1)][0] - preds[(ag, lv0)][0]
        dr = preds[(ag, lv1)][1] - preds[(ag, lv0)][1]
        rd.append(dict(Outcome=label, Exposure=expo_name, age_group=ag, contrast=f"{lv1} - {lv0}", risk_diff_pp=round(pt * 100, 2),
                       lo=round(np.percentile(dr, 2.5) * 100, 2), hi=round(np.percentile(dr, 97.5) * 100, 2)))
    return out, rows, rd

LEVELS = {
    'Childhood SES': {'Pretty well-off': (0, 0), 'Average': (1, 0), 'Poor': (0, 1)},
    'Childhood health': {'Good': (0,), 'Poor': (1,)},
    'Childhood bedridden': {'No': (0,), 'Yes': (1,)},
}
EXPCOLS = {'Childhood SES': ['ses_avg', 'ses_poor'], 'Childhood health': ['hlth_poor'], 'Childhood bedridden': ['bed_yes']}

jt, pred_rows, rd_rows = [], [], []
for label, outcome, s in [('Cognitive impairment', 'imp_mo', samples['Cognition (memory+orientation)'][1]),
                          ('Depressive symptoms', 'cesd_depression', samples['Depressive symptoms'][1])]:
    for en in LEVELS:
        o, pr, rd = interaction(label, outcome, s, EXPCOLS[en], en)
        jt.append(o); pred_rows += pr; rd_rows += rd
pd.DataFrame(jt).to_csv(f"{T}/table5v2a_interaction_joint_tests.csv", index=False)
pd.DataFrame(pred_rows).to_csv(f"{T}/table5v2b_standardized_predictions.csv", index=False)
pd.DataFrame(rd_rows).to_csv(f"{T}/table5v2c_risk_differences.csv", index=False)
print(pd.DataFrame(jt).to_string()); print(pd.DataFrame(rd_rows).to_string())

# Figures 4v2, 5v2
pr_df = pd.DataFrame(pred_rows)
pal = {'Pretty well-off': '#2b5c8f', 'Average': '#e69f00', 'Poor': '#d55e00'}
for label, fn, ttl in [('Cognitive impairment', 'figure4v2_cognition_interaction.png', 'Figure 4 (v2): Standardized prevalence of cognitive impairment\n(lowest weighted decile, memory + orientation) by childhood SES and age group'),
                       ('Depressive symptoms', 'figure5v2_depression_interaction.png', 'Figure 5 (v2): Standardized prevalence of depressive symptoms\n(CES-D ≥ 4) by childhood SES and age group')]:
    fig, ax = plt.subplots(figsize=(8, 5.5), dpi=200)
    sub0 = pr_df[(pr_df.Outcome == label) & (pr_df.Exposure == 'Childhood SES')]
    for k, lvl in enumerate(['Pretty well-off', 'Average', 'Poor']):
        sb = sub0[sub0.level == lvl].set_index('age_group').loc[AGE_CATS]
        x = np.arange(3) + (k - 1) * 0.12
        ax.errorbar(x, sb.pred_prev_pct, yerr=[sb.pred_prev_pct - sb.lo, sb.hi - sb.pred_prev_pct], fmt='o-', capsize=3, color=pal[lvl], label=lvl, lw=1.8)
    p_ = [j for j in jt if j['Outcome'] == label and j['Exposure'] == 'Childhood SES'][0]['joint_p']
    ax.set_xticks(range(3)); ax.set_xticklabels(AGE_CATS)
    ax.set_xlabel('Age group (years)'); ax.set_ylabel('Standardized prevalence (%) with 95% CI')
    ax.set_title(ttl + f"\nJoint test of SES × age interaction: p = {p_:.3f}", fontsize=10, fontweight='bold')
    ax.legend(title='Childhood SES', loc='upper left'); ax.grid(alpha=.25)
    fig.tight_layout(); fig.savefig(f"{F}/{fn}"); plt.close(fig)

# ----------------------------------------------------------------------------
# IPW for missing cognition (A8)
# ----------------------------------------------------------------------------
print("\n--- IPW ---")
base = d[d.direct_interview == 1].dropna(subset=CORE).copy()
pf = f"cog_observed ~ {rhs(['ses_avg', 'ses_poor', 'hlth_poor', 'bed_yes'], 'M3')} + cesd_depression_miss"
base['cesd_depression_miss'] = base['cesd_depression'].isna().astype(int)
lg = smf.glm(pf, base, family=sm.families.Binomial()).fit()
base['p_obs'] = lg.predict(base)
base['ipw'] = 1 / base['p_obs'].clip(lower=0.05)
base['ipw'] = base['ipw'].clip(upper=base['ipw'].quantile(.99))
print("response rate", base.cog_observed.mean(), "ipw range", base.ipw.min(), base.ipw.max())
resp = base[base.cog_observed == 1].copy()
resp['w_ipw'] = resp['survey_weight'] * resp['ipw']
resp['w_ipw'] = resp['w_ipw'] / resp['w_ipw'].mean() * resp['survey_weight'].mean()
# response model summary
imp_tab = pd.DataFrame({'term': lg.params.index, 'OR': np.exp(lg.params.values), 'p': lg.pvalues.values})
imp_tab = imp_tab[~imp_tab.term.str.contains('state_fe')]
imp_tab.round(4).to_csv(f"{T}/table_s1_response_model.csv", index=False)
rows = []
for e in list(EXPO) + ['joint_ses']:
    for m in ['M1', 'M2', 'M3']:
        for wcol, wl in [('survey_weight', 'Complete-case'), ('w_ipw', 'IPW-adjusted')]:
            if e == 'joint_ses':
                f = svy_glm(f"imp_mo ~ ses_avg + ses_poor + {FORM[m]}", resp, 'poisson', wcol)
                r = term_row(f, 'ses_poor'); nm = EXPO['ses_poor'] + ' [joint SES model]'
            else:
                pre = 'ses_avg + ses_poor' if e in ('ses_avg', 'ses_poor') else e
                f = svy_glm(f"imp_mo ~ {pre} + {FORM[m]}", resp, 'poisson', wcol); r = term_row(f, e); nm = EXPO[e]
            rows.append(dict(Exposure=nm, Model=MLAB[m], Weights=wl, PR=round(r['est'], 3), CI_lower=round(r['lo'], 3), CI_upper=round(r['hi'], 3), p_value=round(r['p'], 4), N=f.nobs))
pd.DataFrame(rows).to_csv(f"{T}/table_s2_ipw_cognition.csv", index=False)
print(pd.DataFrame(rows)[lambda x: x.Model.str.contains('Model 2')].to_string())

# Missingness diagnostics
dm = d[d.direct_interview == 1].copy(); dm['cog_miss'] = 1 - dm['cog_observed']
rows = []
for var in ['age_group', 'education', 'childhood_ses', 'sex']:
    for lvl, g in dm.groupby(var):
        rows.append(dict(Variable=var, Level=lvl, N=len(g), Pct_missing_cognition=round(g.cog_miss.mean() * 100, 1)))
pd.DataFrame(rows).to_csv(f"{T}/table_s3_cognition_missingness.csv", index=False)

# ----------------------------------------------------------------------------
# SENSITIVITY (Table S4)
# ----------------------------------------------------------------------------
print("\n--- Sensitivity ---")
dd = d[d.direct_interview == 1]
rows = []
def add(sens, outcome_label, f, term, exp=True, extra=''):
    r = term_row(f, term, exp=exp)
    rows.append(dict(Analysis=sens, Outcome=outcome_label, Term=term, Estimate=round(r['est'], 3), CI_lower=round(r['lo'], 3), CI_upper=round(r['hi'], 3), p_value=round(r['p'], 4), N=f.nobs, Note=extra))

# S4a: alternative cognitive outcomes (common exposure/covariate sample per outcome), SES poor, M1 & M2 (joint SES model)
alts = [('imp_mo', 'Primary: lowest weighted decile mem+orient', 'poisson'),
        ('imp_battery', 'Skip-aware full battery (% of max), lowest decile', 'poisson'),
        ('imp_mo_edustrat', 'Mem+orient, schooling-stratum-specific decile', 'poisson'),
        ('cognitive_impairment', 'Original v1 composite (skips scored 0)', 'poisson'),
        ('mem_orient', 'Mem+orient continuous (beta, points)', 'gaussian'),
        ('battery_pct', 'Skip-aware battery continuous (beta, % of max)', 'gaussian')]
for o, lab, fam in alts:
    s = sample(o, base=dd)
    for m in ['M1', 'M2']:
        f = svy_glm(f"{o} ~ ses_avg + ses_poor + {FORM[m]}", s, fam)
        add(f"S4a Alt. cognitive outcome / {MLAB[m]}", lab, f, 'ses_poor', exp=(fam == 'poisson'))
        f = svy_glm(f"{o} ~ hlth_poor + {FORM[m]}", s, fam)
        add(f"S4a Alt. cognitive outcome / {MLAB[m]}", lab, f, 'hlth_poor', exp=(fam == 'poisson'))

# S4b: stratified by schooling (primary outcome)
s = samples['Cognition (memory+orientation)'][1]
for grp, sub, form in [('Never attended school', s[s.education == 'No formal education'], f"{DEMO} + C(mpce_quintile)"),
                       ('Any schooling', s[s.education != 'No formal education'], f"{DEMO} + C(education, Treatment('Less than primary')) + C(mpce_quintile)")]:
    for o, lab in [('imp_mo', 'Cognitive impairment (primary)'), ('imp_mo_edustrat', 'Cognitive impairment (school-stratum decile)')]:
        sub2 = sub.dropna(subset=[o])
        f = svy_glm(f"{o} ~ ses_avg + ses_poor + {form}", sub2, 'poisson')
        add(f"S4b Schooling stratum: {grp}", lab, f, 'ses_poor')
        f = svy_glm(f"{o} ~ hlth_poor + {form}", sub2, 'poisson')
        add(f"S4b Schooling stratum: {grp}", lab, f, 'hlth_poor')
    f = svy_glm(f"mem_orient ~ ses_avg + ses_poor + {form}", sub, 'gaussian')
    add(f"S4b Schooling stratum: {grp}", 'Mem+orient continuous (beta)', f, 'ses_poor', exp=False)

# S4c: 'Varied' SES as separate category and combined with Poor (Depression & cognition, M2)
for label, o, base_ in [('Cognitive impairment', 'imp_mo', dd), ('Depressive symptoms', 'cesd_depression', d)]:
    b = base_.copy()
    b = b[b.childhood_ses.notna()].copy()
    b['v_avg'] = (b.childhood_ses == 'Average').astype(float); b['v_poor'] = (b.childhood_ses == 'Poor').astype(float); b['v_var'] = (b.childhood_ses == 'Varied').astype(float)
    b = b.dropna(subset=['hlth_poor', 'bed_yes', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile', o, 'survey_weight'])
    f = svy_glm(f"{o} ~ v_avg + v_poor + v_var + {FORM['M2']}", b, 'poisson')
    add('S4c SES incl. Varied category / M2', label, f, 'v_poor'); add('S4c SES incl. Varied category / M2', label, f, 'v_var')

# S4d: exclude ages >= 100
for label, o, s in [('Cognitive impairment', 'imp_mo', samples['Cognition (memory+orientation)'][1]), ('Depressive symptoms', 'cesd_depression', samples['Depressive symptoms'][1])]:
    s2 = s[s.age < 100]
    f = svy_glm(f"{o} ~ ses_avg + ses_poor + {FORM['M2']}", s2, 'poisson'); add('S4d Exclude age>=100 / M2', label, f, 'ses_poor')
    f = svy_glm(f"{o} ~ hlth_poor + {FORM['M2']}", s2, 'poisson'); add('S4d Exclude age>=100 / M2', label, f, 'hlth_poor')

# S4e: Depression -- logistic AOR vs PR, continuous CES-D, ordinal childhood health (5 level, trend)
sdep = samples['Depressive symptoms'][1]
f = svy_glm(f"cesd_depression ~ hlth_poor + {FORM['M2']}", sdep, 'poisson'); add('S4e Depression: modified Poisson PR / M2', 'CES-D>=4', f, 'hlth_poor')
f = svy_glm(f"cesd_depression ~ hlth_poor + {FORM['M2']}", sdep, 'binomial'); add('S4e Depression: logistic OR / M2', 'CES-D>=4', f, 'hlth_poor', extra='OR (binomial)')
sc = sdep.dropna(subset=['cesd_score'])
f = svy_glm(f"cesd_score ~ hlth_poor + {FORM['M2']}", sc, 'gaussian'); add('S4e Depression: continuous CES-D / M2', 'CES-D score 0-10 (beta)', f, 'hlth_poor', exp=False)
f = svy_glm(f"cesd_score ~ ses_poor + ses_avg + {FORM['M2']}", sc, 'gaussian'); add('S4e Depression: continuous CES-D / M2', 'CES-D score 0-10 (beta)', f, 'ses_poor', exp=False)
sdep5 = sdep.dropna(subset=['childhood_health_5cat']).copy()
sdep5['h5'] = sdep5['childhood_health_5cat'].map({'Very good': 0, 'Good': 1, 'Fair': 2, 'Poor': 3, 'Very poor': 4})
f = svy_glm(f"cesd_depression ~ h5 + {FORM['M2']}", sdep5, 'poisson'); add('S4e Childhood health 5-level, per-level trend / M2', 'CES-D>=4', f, 'h5')
scog5 = samples['Cognition (memory+orientation)'][1].dropna(subset=['childhood_health_5cat']).copy()
scog5['h5'] = scog5['childhood_health_5cat'].map({'Very good': 0, 'Good': 1, 'Fair': 2, 'Poor': 3, 'Very poor': 4})
f = svy_glm(f"imp_mo ~ h5 + {FORM['M2']}", scog5, 'poisson'); add('S4e Childhood health 5-level, per-level trend / M2', 'Cognitive impairment', f, 'h5')

# S4f: Sex-stratified depression and cognition (exploratory)
for sx in ['Female', 'Male']:
    for label, o, s in [('Cognitive impairment', 'imp_mo', samples['Cognition (memory+orientation)'][1]), ('Depressive symptoms', 'cesd_depression', samples['Depressive symptoms'][1])]:
        s2 = s[s.sex == sx]
        form = FORM['M2'].replace("C(sex, Treatment('Male')) + ", "")
        f = svy_glm(f"{o} ~ ses_avg + ses_poor + hlth_poor + bed_yes + {form}", s2, 'poisson')
        for e in ['ses_poor', 'hlth_poor', 'bed_yes']:
            add(f'S4f Sex-stratified (mutually adjusted, M2): {sx}', label, f, e)
pd.DataFrame(rows).to_csv(f"{T}/table_s4_sensitivity.csv", index=False)
print(pd.DataFrame(rows).to_string())

# ----------------------------------------------------------------------------
# Outcome descriptives (v2) with design-based CIs (Table 2v2) + diagnostics for the cognition-score fix
# ----------------------------------------------------------------------------
rows = []
for ag in AGE_CATS + ['All']:
    g = d if ag == 'All' else d[d.age_group == ag]
    for o, lab in [('imp_mo', 'Cognitive impairment (%)'), ('cesd_depression', 'Depressive symptoms (%)'), ('mem_orient', 'Mem+orient score (mean, 0-28)'), ('cesd_score', 'CES-D score (mean)')]:
        est, lo, hi, n = wmean_ci(g, o)
        k = 100 if o in ('imp_mo', 'cesd_depression') else 1
        rows.append(dict(Age_group=ag, Outcome=lab, Estimate=round(est * k, 2), CI_lower=round(lo * k, 2), CI_upper=round(hi * k, 2), N=n))
pd.DataFrame(rows).to_csv(f"{T}/table2v2_outcomes_by_age.csv", index=False)

# education gradient: v1 vs v2
cmp = []
for lvl, g in d[d.education.notna()].groupby('education'):
    a = g[g.cognitive_impairment.notna()]; b = g[g.imp_mo.notna()]; c = g[g.imp_battery.notna()]
    cmp.append(dict(Education=lvl, v1_composite_impaired_pct=round(np.average(a.cognitive_impairment, weights=a.survey_weight) * 100, 1),
                    v2_mem_orient_impaired_pct=round(np.average(b.imp_mo, weights=b.survey_weight) * 100, 1),
                    v2_battery_impaired_pct=round(np.average(c.imp_battery, weights=c.survey_weight) * 100, 1), n_v2=len(b)))
cmp = pd.DataFrame(cmp)
order = ['No formal education', 'Less than primary', 'Primary completed', 'Middle completed', 'Secondary completed', 'Higher secondary/Diploma', 'Graduate and above']
cmp = cmp.set_index('Education').loc[order].reset_index()
cmp.to_csv(f"{T}/table_s5_education_gradient_v1_vs_v2.csv", index=False)
fig, ax = plt.subplots(figsize=(9, 5), dpi=200)
x = np.arange(len(order)); wd = .27
ax.bar(x - wd, cmp.v1_composite_impaired_pct, wd, label='v1 composite (skips scored 0)', color='#b2182b')
ax.bar(x, cmp.v2_mem_orient_impaired_pct, wd, label='v2 memory + orientation (primary)', color='#2166ac')
ax.bar(x + wd, cmp.v2_battery_impaired_pct, wd, label='v2 skip-aware battery', color='#4daf4a')
ax.set_xticks(x); ax.set_xticklabels(['None', '<Primary', 'Primary', 'Middle', 'Secondary', 'Higher sec.', 'Graduate+'], fontsize=9)
ax.set_ylabel('Weighted % classified impaired'); ax.set_xlabel('Highest education')
ax.set_title('Figure A1: Education gradient of "cognitive impairment" by outcome definition', fontsize=10, fontweight='bold')
ax.legend(); ax.grid(axis='y', alpha=.25); fig.tight_layout(); fig.savefig(f"{F}/figureA1_education_gradient.png"); plt.close(fig)

# Missingness figure
ms = pd.DataFrame(rows := [], columns=[])
mm = pd.read_csv(f"{T}/table_s3_cognition_missingness.csv")
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=200)
lab = mm.Variable + ': ' + mm.Level.astype(str)
ax.barh(lab[::-1], mm.Pct_missing_cognition[::-1], color='#6a3d9a'); ax.set_xlabel('% of direct interviewees with missing cognition score')
ax.set_title('Figure A2: Cognition-score missingness (complete-case selection)', fontsize=10, fontweight='bold')
fig.tight_layout(); fig.savefig(f"{F}/figureA2_cognition_missingness.png"); plt.close(fig)

# Forest plot: primary models
fig, axes = plt.subplots(1, 2, figsize=(11, 5), dpi=200, sharey=True)
for ax, tt, ttl in [(axes[0], pd.DataFrame(t3), 'Cognitive impairment (mem+orient)'), (axes[1], pd.DataFrame(t4), 'Depressive symptoms (CES-D ≥ 4)')]:
    ylabels = []; y = 0
    colors = {'Model 0': '#999999', 'Model 1': '#2b8cbe', 'Model 2': '#d95f0e', 'Model 3': '#31a354'}
    for e in ['ses_poor', 'hlth_poor', 'bed_yes']:
        for m in ['M0', 'M1', 'M2', 'M3']:
            r = tt[(tt.Exposure == EXPO[e]) & (tt.Model == MLAB[m])].iloc[0]
            ax.errorbar(r.Estimate, y, xerr=[[r.Estimate - r.CI_lower], [r.CI_upper - r.Estimate]], fmt='o', color=colors[m[:1] + 'odel ' + m[1]], capsize=2)
            ylabels.append(f"{EXPO[e].split(' (')[0]} | {m}"); y += 1
        y += 1; ylabels.append('')
    ax.axvline(1, color='k', lw=.8, ls='--'); ax.set_xscale('log'); ax.xaxis.set_major_formatter(matplotlib.ticker.ScalarFormatter()); ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.set_xticks([0.8, 1, 1.25, 1.5, 2]); ax.set_title(ttl, fontsize=10, fontweight='bold'); ax.set_xlabel('Prevalence ratio (log scale), 95% CI')
    ax.set_yticks(range(len(ylabels))); ax.set_yticklabels(ylabels, fontsize=7); ax.invert_yaxis()
fig.suptitle('Figure 6 (v2): Sequential models on a common sample (M0 unadjusted → M3 + adult health)', fontsize=10, fontweight='bold')
fig.tight_layout(); fig.savefig(f"{F}/figure6v2_forest_sequential.png"); plt.close(fig)
print("DONE")
