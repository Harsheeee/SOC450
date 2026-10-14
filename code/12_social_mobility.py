#!/usr/bin/env python3
"""
Step 12: Social Mobility & Intergenerational Trajectories.
Tests whether adult upward mobility erases childhood disadvantage scars on
cognitive impairment and depressive symptoms.
Outputs:
  outputs/tables_v2/table_social_mobility.csv
  outputs/figures_v2/figure7_social_mobility.png
"""
import os, sys, warnings
import numpy as np
import pandas as pd
import patsy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
sys.path.insert(0, os.path.dirname(__file__))
from survey_utils import svy_glm, term_row
warnings.filterwarnings("ignore")

T = "outputs/tables_v2"
F = "outputs/figures_v2"
F_REPORT = "report/new_report/figures"
os.makedirs(T, exist_ok=True)
os.makedirs(F, exist_ok=True)
os.makedirs(F_REPORT, exist_ok=True)

rng = np.random.default_rng(20260510)

print("Loading data...")
d = pd.read_parquet("data_analysis/lasi_clean_v2.parquet")

# Standardize variables consistent with 08_models_v2.py
d['srh'] = d['srh'].map({'Very good': 'Excellent', 'Good': 'Very good', 'Fair': 'Good', 'Poor': 'Fair', 'Very poor': 'Poor'})
d['state_fe'] = d['stateid'].astype(int)
d['ses_avg'] = np.where(d.childhood_ses.isin(['Pretty well-off', 'Average', 'Poor']), (d.childhood_ses == 'Average').astype(float), np.nan)
d['ses_poor'] = np.where(d.childhood_ses.isin(['Pretty well-off', 'Average', 'Poor']), (d.childhood_ses == 'Poor').astype(float), np.nan)
d['hlth_poor'] = np.where(d.childhood_health.notna(), (d.childhood_health == 'Poor').astype(float), np.nan)
d['hlth_poor_orig'] = np.where(d.childhood_health_poor_original.notna(), d.childhood_health_poor_original, np.nan)
d['bed_yes'] = np.where(d.childhood_bedridden.notna(), (d.childhood_bedridden == 'Yes').astype(float), np.nan)

# Define 4-category social mobility trajectories
def assign_mobility(row):
    if pd.isna(row['childhood_ses']) or pd.isna(row['mpce_quintile']):
        return np.nan
    if row['childhood_ses'] not in ['Pretty well-off', 'Average', 'Poor']:
        return np.nan
    poor_child = row['childhood_ses'] == 'Poor'
    poor_adult = row['mpce_quintile'] in [1, 2]
    if poor_child and poor_adult:
        return 'Persistently Poor'
    elif poor_child and not poor_adult:
        return 'Upwardly Mobile'
    elif not poor_child and poor_adult:
        return 'Downwardly Mobile'
    else:
        return 'Persistently Affluent'

d['mobility'] = d.apply(assign_mobility, axis=1)

CORE = ['ses_avg', 'ses_poor', 'hlth_poor', 'hlth_poor_orig', 'bed_yes', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'state_fe',
        'education', 'mpce_quintile', 'chronic_count', 'srh', 'survey_weight', 'cluster_psu', 'stratum', 'mobility']

cog_sample = d[d.direct_interview == 1].dropna(subset=CORE + ['low_memory_orientation']).copy()
dep_sample = d.dropna(subset=CORE + ['cesd_depression']).copy()

DEMO = "age + C(sex, Treatment('Male')) + C(residence_cat, Treatment('Rural')) + C(caste, Treatment('General/None')) + married_binary + C(state_fe)"
EDU = "C(education, Treatment('No formal education'))"

MODELS = {
    'Model 0: Unadjusted': '1',
    'Model A: Demographics + State': DEMO,
    'Model B: + Adult Education': f"{DEMO} + {EDU}"
}

TRAJECTORIES = ['Persistently Affluent', 'Downwardly Mobile', 'Upwardly Mobile', 'Persistently Poor']

results = []
pred_results = []

for outcome_label, s, out_col in [
    ('Cognitive Impairment', cog_sample, 'low_memory_orientation'),
    ('Depressive Symptoms', dep_sample, 'cesd_depression')
]:
    print(f"\nProcessing {outcome_label} (N = {len(s)})...")
    
    # Run Models 0, A, B
    for m_label, m_covs in MODELS.items():
        formula = f"{out_col} ~ C(mobility, Treatment('Persistently Affluent')) + {m_covs}"
        f = svy_glm(formula, s, family='poisson')
        
        # Reference row
        results.append({
            'Outcome': outcome_label,
            'Model': m_label,
            'Trajectory': 'Persistently Affluent (Reference)',
            'PR': 1.000,
            'CI_lower': 1.000,
            'CI_upper': 1.000,
            'p_value': np.nan,
            'N': f.nobs
        })
        
        for traj in ['Downwardly Mobile', 'Upwardly Mobile', 'Persistently Poor']:
            term = f"C(mobility, Treatment('Persistently Affluent'))[T.{traj}]"
            r = term_row(f, term, exp=True)
            results.append({
                'Outcome': outcome_label,
                'Model': m_label,
                'Trajectory': traj,
                'PR': round(r['est'], 3),
                'CI_lower': round(r['lo'], 3),
                'CI_upper': round(r['hi'], 3),
                'p_value': round(r['p'], 4),
                'N': f.nobs
            })

    # Standardized prevalence predictions (Model B)
    f_b = svy_glm(f"{out_col} ~ C(mobility, Treatment('Persistently Affluent')) + {MODELS['Model B: + Adult Education']}", s, family='poisson')
    di = f_b.model.data.model_spec
    w = s.survey_weight.values / s.survey_weight.sum()
    B = rng.multivariate_normal(f_b.params.values, f_b.V.values, size=300)
    
    for traj in TRAJECTORIES:
        nd = s.copy()
        nd['mobility'] = traj
        X = np.asarray(patsy.build_design_matrices([di], nd, return_type='dataframe')[0])
        pt = np.clip(np.exp(X @ f_b.params.values), 0, 1) @ w
        dr = np.clip(np.exp(X @ B.T), 0, 1).T @ w
        lo = np.percentile(dr, 2.5)
        hi = np.percentile(dr, 97.5)
        pred_results.append({
            'Outcome': outcome_label,
            'Trajectory': traj,
            'pred_prev_pct': round(pt * 100, 2),
            'lo': round(lo * 100, 2),
            'hi': round(hi * 100, 2)
        })

df_res = pd.DataFrame(results)
df_res.to_csv(f"{T}/table_social_mobility.csv", index=False)
print("Saved table_social_mobility.csv")

df_pred = pd.DataFrame(pred_results)
df_pred.to_csv(f"{T}/table_social_mobility_predictions.csv", index=False)
print(df_pred.to_string())

# ----------------------------------------------------------------------------
# Figure 7: Adjusted prevalence by social mobility trajectory
# ----------------------------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5), dpi=300, sharex=True)

colors = ['#2b5c8f', '#e69f00', '#009e73', '#d55e00']
traj_labels = ['Persistently\nAffluent', 'Downwardly\nMobile', 'Upwardly\nMobile', 'Persistently\nPoor']
x = np.arange(len(TRAJECTORIES))

# Panel A: Cognitive Impairment
cog_p = df_pred[df_pred.Outcome == 'Cognitive Impairment'].set_index('Trajectory').loc[TRAJECTORIES]
for i, traj in enumerate(TRAJECTORIES):
    y = cog_p.loc[traj, 'pred_prev_pct']
    y_err = [[y - cog_p.loc[traj, 'lo']], [cog_p.loc[traj, 'hi'] - y]]
    ax1.errorbar(x[i], y, yerr=y_err, fmt='o', color=colors[i], markersize=9, capsize=5, capthick=1.5, elinewidth=1.8)
    ax1.text(x[i], y + 0.35, f"{y:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=colors[i])

ax1.plot(x, cog_p.pred_prev_pct, color='#555555', linestyle='--', alpha=0.5, zorder=1)
ax1.set_title("Panel A: Cognitive Impairment\n(Lowest Decile Mem+Orient, Model B)", fontsize=11, fontweight='bold', pad=10)
ax1.set_ylabel("Standardized Prevalence (%) with 95% CI", fontsize=10)
ax1.set_xticks(x)
ax1.set_xticklabels(traj_labels, fontsize=9.5)
ax1.grid(axis='y', alpha=0.3, linestyle=':')
ax1.set_ylim(8, 17)

# Panel B: Depressive Symptoms
dep_p = df_pred[df_pred.Outcome == 'Depressive Symptoms'].set_index('Trajectory').loc[TRAJECTORIES]
for i, traj in enumerate(TRAJECTORIES):
    y = dep_p.loc[traj, 'pred_prev_pct']
    y_err = [[y - dep_p.loc[traj, 'lo']], [dep_p.loc[traj, 'hi'] - y]]
    ax2.errorbar(x[i], y, yerr=y_err, fmt='o', color=colors[i], markersize=9, capsize=5, capthick=1.5, elinewidth=1.8)
    ax2.text(x[i], y + 0.45, f"{y:.1f}%", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color=colors[i])

ax2.plot(x, dep_p.pred_prev_pct, color='#555555', linestyle='--', alpha=0.5, zorder=1)
ax2.set_title("Panel B: Depressive Symptoms\n(CES-D ≥ 4, Model B)", fontsize=11, fontweight='bold', pad=10)
ax2.set_ylabel("Standardized Prevalence (%) with 95% CI", fontsize=10)
ax2.set_xticks(x)
ax2.set_xticklabels(traj_labels, fontsize=9.5)
ax2.grid(axis='y', alpha=0.3, linestyle=':')
ax2.set_ylim(23, 34)

# Annotation for key finding
ax2.annotate("Upward mobility fails to erase\nchildhood depression scar\n(29.2% vs. 29.4% persistently poor)",
             xy=(2, dep_p.loc['Upwardly Mobile', 'pred_prev_pct']),
             xytext=(1.2, 31.8),
             arrowprops=dict(facecolor='#333333', arrowstyle='->', lw=1.2),
             fontsize=8.5, bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffdd', edgecolor='#cccccc', alpha=0.9))

plt.suptitle("Figure 7: Life-Course Social Mobility Trajectories and Late-Life Health in India (LASI Wave 1)",
             fontsize=12, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(f"{F}/figure7_social_mobility.png")
if os.path.exists(F_REPORT):
    fig.savefig(f"{F_REPORT}/figure7_social_mobility.png")
plt.close(fig)
print(f"Saved figure7_social_mobility.png to {F} and {F_REPORT}")
