#!/usr/bin/env python3
"""
Step 04: Primary Regression & Interaction Analysis
- Fits survey-weighted modified Poisson models for binary outcomes (PR, 95% CI)
- Sequential models: Model 0 (Unadjusted), Model 1 (Demographics), Model 2 (Adult SES - Primary), Model 3 (Adult Health - Pathway)
- Fits Age-Interaction models (Exposure x Age Group)
- Computes marginal predicted prevalences across age x exposure strata
- Generates Table 3 (Cognition), Table 4 (Depression), Table 5 (Interactions), and Figures 4 & 5
"""

import os
import warnings
import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore', category=sm.tools.sm_exceptions.SpecificationWarning)

DATA_PATH = "data_analysis/lasi_clean_analysis.parquet"
TABLES_DIR = "outputs/tables"
FIGS_DIR = "outputs/figures"
MODELS_DIR = "outputs/model_objects"
os.makedirs(TABLES_DIR, exist_ok=True)
os.makedirs(FIGS_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

print("Loading clean analytical dataset...")
df = pd.read_parquet(DATA_PATH)

# Common complete-case filters for primary models
demo_covars = ["age", "C(sex, Treatment('Male'))", "C(residence_cat, Treatment('Rural'))", 
               "C(caste, Treatment('General/None'))", "C(married_binary, Treatment(1))"]

ses_covars = demo_covars + ["C(education, Treatment('No formal education'))", 
                            "C(mpce_quintile, Treatment(1))"]

health_covars = ses_covars + ["chronic_count", "C(srh, Treatment('Very good'))"]

# Helper function to fit survey-weighted Poisson regression and extract PR & 95% CI
def fit_poisson_model(formula, data, cluster_col='cluster_psu', weight_col='survey_weight'):
    sub = data.dropna(subset=['cluster_psu', weight_col]).copy()
    sub['norm_weight'] = sub[weight_col] / sub[weight_col].mean()
    model = smf.glm(formula=formula, data=sub, family=sm.families.Poisson(), freq_weights=sub['norm_weight'])
    res = model.fit(cov_type='cluster', cov_kwds={'groups': sub[cluster_col]})
    return res

def extract_estimates(res, exposure_terms, model_name, outcome_name):
    rows = []
    ci = np.exp(res.conf_int())
    ci.columns = ['CI_lower', 'CI_upper']
    pr = np.exp(res.params)
    pvals = res.pvalues
    
    for term in exposure_terms:
        if term in pr:
            rows.append({
                'Outcome': outcome_name,
                'Model': model_name,
                'Parameter': term,
                'PR': round(pr[term], 3),
                'CI_lower': round(ci.loc[term, 'CI_lower'], 3),
                'CI_upper': round(ci.loc[term, 'CI_upper'], 3),
                'p_value': round(pvals[term], 4),
                'N_obs': int(res.nobs)
            })
    return rows

# ==============================================================================
# 1. TABLE 3: COGNITIVE IMPAIRMENT MODELS
# ==============================================================================
print("\n--- Fitting Cognitive Impairment Models ---")
cog_data = df[(df['direct_interview'] == 1) & df['cognitive_impairment'].notna()].copy()
cog_data = cog_data[cog_data['childhood_ses'].isin(['Pretty well-off', 'Average', 'Poor'])].copy()

# A. Childhood SES
t3_rows = []
exp_ses = "C(childhood_ses, Treatment('Pretty well-off'))"
ses_terms = [f"{exp_ses}[T.Average]", f"{exp_ses}[T.Poor]"]

# Model 0: Unadjusted
f0 = f"cognitive_impairment ~ {exp_ses}"
res0 = fit_poisson_model(f0, cog_data.dropna(subset=['childhood_ses']))
t3_rows.extend(extract_estimates(res0, ses_terms, "Model 0: Unadjusted", "Cognitive Impairment"))

# Model 1: Demographics
f1 = f"cognitive_impairment ~ {exp_ses} + {' + '.join(demo_covars)}"
res1 = fit_poisson_model(f1, cog_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary']))
t3_rows.extend(extract_estimates(res1, ses_terms, "Model 1: Demographics", "Cognitive Impairment"))

# Model 2: Adult SES (Primary Model)
f2 = f"cognitive_impairment ~ {exp_ses} + {' + '.join(ses_covars)}"
res2 = fit_poisson_model(f2, cog_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']))
t3_rows.extend(extract_estimates(res2, ses_terms, "Model 2: Adult SES (Primary)", "Cognitive Impairment"))

# Model 3: Adult Health (Pathway Model)
f3 = f"cognitive_impairment ~ {exp_ses} + {' + '.join(health_covars)}"
res3 = fit_poisson_model(f3, cog_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile', 'chronic_count', 'srh']))
t3_rows.extend(extract_estimates(res3, ses_terms, "Model 3: Adult Health", "Cognitive Impairment"))

# B. Childhood Health (Good vs Poor)
exp_hlth = "C(childhood_health, Treatment('Good'))"
hlth_term = [f"{exp_hlth}[T.Poor]"]
for m_label, f_str, vars_needed in [
    ("Model 0: Unadjusted", f"cognitive_impairment ~ {exp_hlth}", ['childhood_health']),
    ("Model 1: Demographics", f"cognitive_impairment ~ {exp_hlth} + {' + '.join(demo_covars)}", ['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary']),
    ("Model 2: Adult SES (Primary)", f"cognitive_impairment ~ {exp_hlth} + {' + '.join(ses_covars)}", ['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']),
    ("Model 3: Adult Health", f"cognitive_impairment ~ {exp_hlth} + {' + '.join(health_covars)}", ['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile', 'chronic_count', 'srh'])
]:
    res = fit_poisson_model(f_str, cog_data.dropna(subset=vars_needed))
    t3_rows.extend(extract_estimates(res, hlth_term, m_label, "Cognitive Impairment"))

# C. Childhood Bedridden (No vs Yes)
exp_bed = "C(childhood_bedridden, Treatment('No'))"
bed_term = [f"{exp_bed}[T.Yes]"]
for m_label, f_str, vars_needed in [
    ("Model 0: Unadjusted", f"cognitive_impairment ~ {exp_bed}", ['childhood_bedridden']),
    ("Model 1: Demographics", f"cognitive_impairment ~ {exp_bed} + {' + '.join(demo_covars)}", ['childhood_bedridden', 'age', 'sex', 'residence_cat', 'caste', 'married_binary']),
    ("Model 2: Adult SES (Primary)", f"cognitive_impairment ~ {exp_bed} + {' + '.join(ses_covars)}", ['childhood_bedridden', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']),
    ("Model 3: Adult Health", f"cognitive_impairment ~ {exp_bed} + {' + '.join(health_covars)}", ['childhood_bedridden', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile', 'chronic_count', 'srh'])
]:
    res = fit_poisson_model(f_str, cog_data.dropna(subset=vars_needed))
    t3_rows.extend(extract_estimates(res, bed_term, m_label, "Cognitive Impairment"))

table3_df = pd.DataFrame(t3_rows)
table3_path = os.path.join(TABLES_DIR, "table3_cognition_regression.csv")
table3_df.to_csv(table3_path, index=False)
print(f"Saved Table 3 to {table3_path}")
print(table3_df.to_string(index=False))

# ==============================================================================
# 2. TABLE 4: DEPRESSIVE SYMPTOMS MODELS
# ==============================================================================
print("\n--- Fitting Depressive Symptoms Models ---")
dep_data = df[df['cesd_depression'].notna()].copy()
dep_data = dep_data[dep_data['childhood_ses'].isin(['Pretty well-off', 'Average', 'Poor'])].copy()

t4_rows = []

# A. Childhood SES
f0_dep = f"cesd_depression ~ {exp_ses}"
res0_dep = fit_poisson_model(f0_dep, dep_data.dropna(subset=['childhood_ses']))
t4_rows.extend(extract_estimates(res0_dep, ses_terms, "Model 0: Unadjusted", "Depressive Symptoms"))

f1_dep = f"cesd_depression ~ {exp_ses} + {' + '.join(demo_covars)}"
res1_dep = fit_poisson_model(f1_dep, dep_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary']))
t4_rows.extend(extract_estimates(res1_dep, ses_terms, "Model 1: Demographics", "Depressive Symptoms"))

f2_dep = f"cesd_depression ~ {exp_ses} + {' + '.join(ses_covars)}"
res2_dep = fit_poisson_model(f2_dep, dep_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']))
t4_rows.extend(extract_estimates(res2_dep, ses_terms, "Model 2: Adult SES (Primary)", "Depressive Symptoms"))

f3_dep = f"cesd_depression ~ {exp_ses} + {' + '.join(health_covars)}"
res3_dep = fit_poisson_model(f3_dep, dep_data.dropna(subset=['childhood_ses', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile', 'chronic_count', 'srh']))
t4_rows.extend(extract_estimates(res3_dep, ses_terms, "Model 3: Adult Health", "Depressive Symptoms"))

# B. Childhood Health
for m_label, f_str, vars_needed in [
    ("Model 0: Unadjusted", f"cesd_depression ~ {exp_hlth}", ['childhood_health']),
    ("Model 1: Demographics", f"cesd_depression ~ {exp_hlth} + {' + '.join(demo_covars)}", ['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary']),
    ("Model 2: Adult SES (Primary)", f"cesd_depression ~ {exp_hlth} + {' + '.join(ses_covars)}", ['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']),
    ("Model 3: Adult Health", f"cesd_depression ~ {exp_hlth} + {' + '.join(health_covars)}", ['childhood_health', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile', 'chronic_count', 'srh'])
]:
    res = fit_poisson_model(f_str, dep_data.dropna(subset=vars_needed))
    t4_rows.extend(extract_estimates(res, hlth_term, m_label, "Depressive Symptoms"))

# C. Childhood Bedridden
for m_label, f_str, vars_needed in [
    ("Model 0: Unadjusted", f"cesd_depression ~ {exp_bed}", ['childhood_bedridden']),
    ("Model 1: Demographics", f"cesd_depression ~ {exp_bed} + {' + '.join(demo_covars)}", ['childhood_bedridden', 'age', 'sex', 'residence_cat', 'caste', 'married_binary']),
    ("Model 2: Adult SES (Primary)", f"cesd_depression ~ {exp_bed} + {' + '.join(ses_covars)}", ['childhood_bedridden', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']),
    ("Model 3: Adult Health", f"cesd_depression ~ {exp_bed} + {' + '.join(health_covars)}", ['childhood_bedridden', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile', 'chronic_count', 'srh'])
]:
    res = fit_poisson_model(f_str, dep_data.dropna(subset=vars_needed))
    t4_rows.extend(extract_estimates(res, bed_term, m_label, "Depressive Symptoms"))

table4_df = pd.DataFrame(t4_rows)
table4_path = os.path.join(TABLES_DIR, "table4_depression_regression.csv")
table4_df.to_csv(table4_path, index=False)
print(f"Saved Table 4 to {table4_path}")
print(table4_df.to_string(index=False))

# ==============================================================================
# 3. TABLE 5 & FIGURES 4-5: AGE INTERACTION ANALYSIS
# ==============================================================================
print("\n--- Fitting Age Interaction Models ---")
# Interaction Model: Outcome ~ ChildhoodSES * AgeGroup + Sex + Residence + Caste + Marital + Education + MPCE
inter_covars = ["C(sex, Treatment('Male'))", "C(residence_cat, Treatment('Rural'))", 
                "C(caste, Treatment('General/None'))", "C(married_binary, Treatment(1))",
                "C(education, Treatment('No formal education'))", "C(mpce_quintile, Treatment(1))"]

# Cognition Interaction
f_inter_cog = f"cognitive_impairment ~ {exp_ses} * C(age_group, Treatment('45-59')) + {' + '.join(inter_covars)}"
complete_cog_inter = cog_data.dropna(subset=['childhood_ses', 'age_group', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']).copy()
res_inter_cog = fit_poisson_model(f_inter_cog, complete_cog_inter)

# Depression Interaction
f_inter_dep = f"cesd_depression ~ {exp_ses} * C(age_group, Treatment('45-59')) + {' + '.join(inter_covars)}"
complete_dep_inter = dep_data.dropna(subset=['childhood_ses', 'age_group', 'sex', 'residence_cat', 'caste', 'married_binary', 'education', 'mpce_quintile']).copy()
res_inter_dep = fit_poisson_model(f_inter_dep, complete_dep_inter)

# Generate Adjusted Predicted Prevalences across Age x Childhood SES
def compute_marginal_predictions(model_res, data, outcome_name):
    # Predict across grid of age_group x childhood_ses holding other covariates at reference/representative values
    age_cats = ['45-59', '60-74', '75+']
    ses_cats = ['Pretty well-off', 'Average', 'Poor']
    
    grid = []
    for ag in age_cats:
        for ses in ses_cats:
            grid.append({
                'childhood_ses': ses,
                'age_group': ag,
                'sex': 'Male',
                'residence_cat': 'Rural',
                'caste': 'General/None',
                'married_binary': 1,
                'education': 'No formal education',
                'mpce_quintile': 1
            })
    grid_df = pd.DataFrame(grid)
    preds = model_res.get_prediction(grid_df).summary_frame()
    grid_df['pred_prev_pct'] = (preds['mean'] * 100).round(2)
    grid_df['ci_lower_pct'] = (preds['mean_ci_lower'] * 100).round(2)
    grid_df['ci_upper_pct'] = (preds['mean_ci_upper'] * 100).round(2)
    grid_df['Outcome'] = outcome_name
    return grid_df

pred_cog_df = compute_marginal_predictions(res_inter_cog, complete_cog_inter, "Cognitive Impairment")
pred_dep_df = compute_marginal_predictions(res_inter_dep, complete_dep_inter, "Depressive Symptoms")

table5_df = pd.concat([pred_cog_df, pred_dep_df], ignore_index=True)
table5_path = os.path.join(TABLES_DIR, "table5_interaction_predictions.csv")
table5_df.to_csv(table5_path, index=False)
print(f"Saved Table 5 to {table5_path}")
print(table5_df.to_string(index=False))

# Plot Figure 4: Cognitive Impairment Interaction
fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
palette = {'Pretty well-off': '#2b5c8f', 'Average': '#e69f00', 'Poor': '#d55e00'}

for ses in ['Pretty well-off', 'Average', 'Poor']:
    sub = pred_cog_df[pred_cog_df['childhood_ses'] == ses]
    ax.plot(sub['age_group'], sub['pred_prev_pct'], marker='o', linewidth=2.2, label=ses, color=palette[ses])
    ax.fill_between(sub['age_group'], sub['ci_lower_pct'], sub['ci_upper_pct'], color=palette[ses], alpha=0.15)

ax.set_title("Figure 4: Adjusted Predicted Prevalence of Cognitive Impairment\nby Childhood SES across Age Groups", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Age Group (Years)", fontsize=11)
ax.set_ylabel("Adjusted Predicted Prevalence (%)", fontsize=11)
ax.legend(title="Childhood SES", frameon=True, facecolor='white', loc='upper left')
ax.set_ylim(0, 45)
fig.tight_layout()
fig4_path = os.path.join(FIGS_DIR, "figure4_cognitive_interaction.png")
fig.savefig(fig4_path)
plt.close(fig)
print(f"Saved Figure 4 to {fig4_path}")

# Plot Figure 5: Depressive Symptoms Interaction
fig, ax = plt.subplots(figsize=(8, 5.5), dpi=300)
for ses in ['Pretty well-off', 'Average', 'Poor']:
    sub = pred_dep_df[pred_dep_df['childhood_ses'] == ses]
    ax.plot(sub['age_group'], sub['pred_prev_pct'], marker='s', linewidth=2.2, label=ses, color=palette[ses])
    ax.fill_between(sub['age_group'], sub['ci_lower_pct'], sub['ci_upper_pct'], color=palette[ses], alpha=0.15)

ax.set_title("Figure 5: Adjusted Predicted Prevalence of Depressive Symptoms\nby Childhood SES across Age Groups", fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel("Age Group (Years)", fontsize=11)
ax.set_ylabel("Adjusted Predicted Prevalence (%)", fontsize=11)
ax.legend(title="Childhood SES", frameon=True, facecolor='white', loc='upper left')
ax.set_ylim(0, 45)
fig.tight_layout()
fig5_path = os.path.join(FIGS_DIR, "figure5_depression_interaction.png")
fig.savefig(fig5_path)
plt.close(fig)
print(f"Saved Figure 5 to {fig5_path}")
