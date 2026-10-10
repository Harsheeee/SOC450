#!/usr/bin/env python3
"""
Step 05: Sensitivity Analyses
- Linear regression models for continuous cognitive score and continuous CES-D score
- Survey-weighted logistic regression (AORs) for comparison with prevalence ratios
- Dose-response cumulative disadvantage models (0, 1, 2, 3)
- 5-level ordinal childhood health models
- Saves sensitivity table to outputs/tables/table_sensitivity.csv
"""

import os
import warnings
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf

warnings.filterwarnings('ignore', category=sm.tools.sm_exceptions.SpecificationWarning)

DATA_PATH = "data_analysis/lasi_clean_analysis.parquet"
TABLES_DIR = "outputs/tables"
os.makedirs(TABLES_DIR, exist_ok=True)

print("Loading data for sensitivity analysis...")
df = pd.read_parquet(DATA_PATH)

demo_covars = ["age", "C(sex, Treatment('Male'))", "C(residence_cat, Treatment('Rural'))", 
               "C(caste, Treatment('General/None'))", "C(married_binary, Treatment(1))"]

ses_covars = demo_covars + ["C(education, Treatment('No formal education'))", 
                            "C(mpce_quintile, Treatment(1))"]

sens_rows = []

# Helper: WLS for continuous outcomes
def fit_wls_model(formula, data, cluster_col='cluster_psu', weight_col='survey_weight'):
    sub = data.dropna(subset=['cluster_psu', weight_col]).copy()
    sub['norm_weight'] = sub[weight_col] / sub[weight_col].mean()
    model = smf.wls(formula=formula, data=sub, weights=sub['norm_weight'])
    res = model.fit(cov_type='cluster', cov_kwds={'groups': sub[cluster_col]})
    return res

# Helper: Logistic GLM for AOR
def fit_logit_model(formula, data, cluster_col='cluster_psu', weight_col='survey_weight'):
    sub = data.dropna(subset=['cluster_psu', weight_col]).copy()
    sub['norm_weight'] = sub[weight_col] / sub[weight_col].mean()
    model = smf.glm(formula=formula, data=sub, family=sm.families.Binomial(), freq_weights=sub['norm_weight'])
    res = model.fit(cov_type='cluster', cov_kwds={'groups': sub[cluster_col]})
    return res

# ==============================================================================
# 1. CONTINUOUS COGNITIVE SCORE (WLS Linear Regression)
# ==============================================================================
print("\n--- Running Continuous Cognition WLS Models ---")
cog_data = df[(df['direct_interview'] == 1) & df['cognitive_score'].notna()].copy()
cog_data = cog_data[cog_data['childhood_ses'].isin(['Pretty well-off', 'Average', 'Poor'])].copy()

# A. Childhood SES on Continuous Cognition
f_cog_wls = f"cognitive_score ~ C(childhood_ses, Treatment('Pretty well-off')) + {' + '.join(ses_covars)}"
sub_cog = cog_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile'])
res_cog_wls = fit_wls_model(f_cog_wls, sub_cog)

for term in ["C(childhood_ses, Treatment('Pretty well-off'))[T.Average]", "C(childhood_ses, Treatment('Pretty well-off'))[T.Poor]"]:
    ci = res_cog_wls.conf_int().loc[term]
    sens_rows.append({
        'Analysis': 'Continuous Cognition (WLS)',
        'Outcome': 'Cognitive Score (0-43)',
        'Exposure': term.replace("C(childhood_ses, Treatment('Pretty well-off'))", "Childhood SES"),
        'Estimand': 'Beta (Mean Diff)',
        'Estimate': round(res_cog_wls.params[term], 3),
        'CI_lower': round(ci[0], 3),
        'CI_upper': round(ci[1], 3),
        'p_value': round(res_cog_wls.pvalues[term], 4),
        'N_obs': int(res_cog_wls.nobs)
    })

# B. Childhood Health on Continuous Cognition
f_cog_hlth = f"cognitive_score ~ C(childhood_health, Treatment('Good')) + {' + '.join(ses_covars)}"
sub_cog_hlth = cog_data.dropna(subset=['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile'])
res_cog_hlth = fit_wls_model(f_cog_hlth, sub_cog_hlth)
term_h = "C(childhood_health, Treatment('Good'))[T.Poor]"
ci_h = res_cog_hlth.conf_int().loc[term_h]
sens_rows.append({
    'Analysis': 'Continuous Cognition (WLS)',
    'Outcome': 'Cognitive Score (0-43)',
    'Exposure': 'Childhood Health: Poor vs Good',
    'Estimand': 'Beta (Mean Diff)',
    'Estimate': round(res_cog_hlth.params[term_h], 3),
    'CI_lower': round(ci_h[0], 3),
    'CI_upper': round(ci_h[1], 3),
    'p_value': round(res_cog_hlth.pvalues[term_h], 4),
    'N_obs': int(res_cog_hlth.nobs)
})

# ==============================================================================
# 2. CONTINUOUS CES-D SCORE (WLS Linear Regression)
# ==============================================================================
print("\n--- Running Continuous CES-D WLS Models ---")
dep_data = df[df['cesd_score'].notna()].copy()
dep_data = dep_data[dep_data['childhood_ses'].isin(['Pretty well-off', 'Average', 'Poor'])].copy()

# A. Childhood SES on Continuous CES-D
f_dep_wls = f"cesd_score ~ C(childhood_ses, Treatment('Pretty well-off')) + {' + '.join(ses_covars)}"
sub_dep = dep_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile'])
res_dep_wls = fit_wls_model(f_dep_wls, sub_dep)

for term in ["C(childhood_ses, Treatment('Pretty well-off'))[T.Average]", "C(childhood_ses, Treatment('Pretty well-off'))[T.Poor]"]:
    ci = res_dep_wls.conf_int().loc[term]
    sens_rows.append({
        'Analysis': 'Continuous Depression (WLS)',
        'Outcome': 'CES-D Score (0-10)',
        'Exposure': term.replace("C(childhood_ses, Treatment('Pretty well-off'))", "Childhood SES"),
        'Estimand': 'Beta (Mean Diff)',
        'Estimate': round(res_dep_wls.params[term], 3),
        'CI_lower': round(ci[0], 3),
        'CI_upper': round(ci[1], 3),
        'p_value': round(res_dep_wls.pvalues[term], 4),
        'N_obs': int(res_dep_wls.nobs)
    })

# B. Childhood Health on Continuous CES-D
f_dep_hlth = f"cesd_score ~ C(childhood_health, Treatment('Good')) + {' + '.join(ses_covars)}"
sub_dep_hlth = dep_data.dropna(subset=['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile'])
res_dep_hlth = fit_wls_model(f_dep_hlth, sub_dep_hlth)
ci_dh = res_dep_hlth.conf_int().loc[term_h]
sens_rows.append({
    'Analysis': 'Continuous Depression (WLS)',
    'Outcome': 'CES-D Score (0-10)',
    'Exposure': 'Childhood Health: Poor vs Good',
    'Estimand': 'Beta (Mean Diff)',
    'Estimate': round(res_dep_hlth.params[term_h], 3),
    'CI_lower': round(ci_dh[0], 3),
    'CI_upper': round(ci_dh[1], 3),
    'p_value': round(res_dep_hlth.pvalues[term_h], 4),
    'N_obs': int(res_dep_hlth.nobs)
})

# ==============================================================================
# 3. LOGISTIC REGRESSION (AORs vs APRs)
# ==============================================================================
print("\n--- Running Logistic Regression Models ---")
# Cognition Logistic Model 2
f_cog_logit = f"cognitive_impairment ~ C(childhood_ses, Treatment('Pretty well-off')) + {' + '.join(ses_covars)}"
res_cog_logit = fit_logit_model(f_cog_logit, sub_cog)
ci_cl = np.exp(res_cog_logit.conf_int())

for term in ["C(childhood_ses, Treatment('Pretty well-off'))[T.Average]", "C(childhood_ses, Treatment('Pretty well-off'))[T.Poor]"]:
    sens_rows.append({
        'Analysis': 'Logistic Regression (Sensitivity)',
        'Outcome': 'Cognitive Impairment',
        'Exposure': term.replace("C(childhood_ses, Treatment('Pretty well-off'))", "Childhood SES"),
        'Estimand': 'Adjusted Odds Ratio (AOR)',
        'Estimate': round(np.exp(res_cog_logit.params[term]), 3),
        'CI_lower': round(ci_cl.loc[term, 0], 3),
        'CI_upper': round(ci_cl.loc[term, 1], 3),
        'p_value': round(res_cog_logit.pvalues[term], 4),
        'N_obs': int(res_cog_logit.nobs)
    })

# Depression Logistic Model 2
f_dep_logit = f"cesd_depression ~ C(childhood_health, Treatment('Good')) + {' + '.join(ses_covars)}"
res_dep_logit = fit_logit_model(f_dep_logit, sub_dep_hlth)
ci_dl = np.exp(res_dep_logit.conf_int())
sens_rows.append({
    'Analysis': 'Logistic Regression (Sensitivity)',
    'Outcome': 'Depressive Symptoms (CES-D >= 4)',
    'Exposure': 'Childhood Health: Poor vs Good',
    'Estimand': 'Adjusted Odds Ratio (AOR)',
    'Estimate': round(np.exp(res_dep_logit.params[term_h]), 3),
    'CI_lower': round(ci_dl.loc[term_h, 0], 3),
    'CI_upper': round(ci_dl.loc[term_h, 1], 3),
    'p_value': round(res_dep_logit.pvalues[term_h], 4),
    'N_obs': int(res_dep_logit.nobs)
})

# ==============================================================================
# 4. CUMULATIVE CHILDHOOD DISADVANTAGE SCORE (Dose-Response)
# ==============================================================================
print("\n--- Running Cumulative Disadvantage Models ---")
sub_cum_dep = dep_data.dropna(subset=['cumulative_disadvantage', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile'])
f_cum_dep = f"cesd_depression ~ cumulative_disadvantage + {' + '.join(ses_covars)}"
model_cum = smf.glm(formula=f_cum_dep, data=sub_cum_dep, family=sm.families.Poisson(), freq_weights=sub_cum_dep['survey_weight'] / sub_cum_dep['survey_weight'].mean())
res_cum_dep = model_cum.fit(cov_type='cluster', cov_kwds={'groups': sub_cum_dep['cluster_psu']})
ci_cum = np.exp(res_cum_dep.conf_int())

sens_rows.append({
    'Analysis': 'Dose-Response (Cumulative Score)',
    'Outcome': 'Depressive Symptoms (CES-D >= 4)',
    'Exposure': 'Per 1-unit increase in Childhood Disadvantage (0 to 3)',
    'Estimand': 'Adjusted Prevalence Ratio (APR)',
    'Estimate': round(np.exp(res_cum_dep.params['cumulative_disadvantage']), 3),
    'CI_lower': round(ci_cum.loc['cumulative_disadvantage', 0], 3),
    'CI_upper': round(ci_cum.loc['cumulative_disadvantage', 1], 3),
    'p_value': round(res_cum_dep.pvalues['cumulative_disadvantage'], 4),
    'N_obs': int(res_cum_dep.nobs)
})

sens_df = pd.DataFrame(sens_rows)
sens_path = os.path.join(TABLES_DIR, "table_sensitivity_analyses.csv")
sens_df.to_csv(sens_path, index=False)
print(f"\nSaved Sensitivity Analyses to {sens_path}")
print(sens_df.to_string(index=False))
