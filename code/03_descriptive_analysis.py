#!/usr/bin/env python3
"""
Step 03: Descriptive Analysis (Tables 1 & 2, Figures 1-3)
- Survey-weighted sample characteristics (Table 1)
- Survey-weighted outcome prevalence by age group (Table 2)
- Exposure-outcome cross-tabulations (Table 2B)
- Publication-quality visualization of sample distributions (Figures 1-3)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data_analysis/lasi_clean_analysis.parquet"
TABLES_DIR = "outputs/tables"
FIGS_DIR = "outputs/figures"
os.makedirs(TABLES_DIR, exist_ok=True)
os.makedirs(FIGS_DIR, exist_ok=True)

# Set high-quality plot aesthetics
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8
sns.set_theme(style="whitegrid", palette="deep")

print("Loading clean dataset from:", DATA_PATH)
df = pd.read_parquet(DATA_PATH)
n_total = len(df)
print(f"Total respondents (Age >= 45): {n_total:,}")

# Helper function to compute survey-weighted percentages and unweighted N
def calc_weighted_freq(data, group_col, weight_col='survey_weight'):
    valid = data.dropna(subset=[group_col, weight_col]).copy()
    unweighted_n = valid.groupby(group_col, observed=True).size()
    weighted_sum = valid.groupby(group_col, observed=True)[weight_col].sum()
    total_weight = weighted_sum.sum()
    weighted_pct = (weighted_sum / total_weight) * 100
    
    res = pd.DataFrame({
        'Unweighted_N': unweighted_n,
        'Weighted_Percent': weighted_pct.round(2)
    })
    return res

# 1. TABLE 1: Study Population Characteristics
t1_sections = [
    ("Age Group", 'age_group'),
    ("Sex", 'sex'),
    ("Place of Residence", 'residence_cat'),
    ("Social Group / Caste", 'caste'),
    ("Marital Status", 'marital_status'),
    ("Educational Attainment", 'education'),
    ("Household MPCE Quintile", 'mpce_quintile'),
    ("Childhood SES", 'childhood_ses'),
    ("Childhood Health", 'childhood_health'),
    ("Childhood Bedridden", 'childhood_bedridden'),
    ("Cumulative Disadvantage Score", 'cumulative_disadvantage')
]

t1_rows = []
for label, col in t1_sections:
    freq_df = calc_weighted_freq(df, col)
    for cat_name, row in freq_df.iterrows():
        t1_rows.append({
            'Characteristic': label,
            'Category': cat_name,
            'Unweighted_N': int(row['Unweighted_N']),
            'Weighted_Pct': row['Weighted_Percent']
        })

table1_df = pd.DataFrame(t1_rows)
table1_path = os.path.join(TABLES_DIR, "table1_sample_characteristics.csv")
table1_df.to_csv(table1_path, index=False)
print(f"Saved Table 1 to {table1_path}")

# 2. TABLE 2: Outcome Prevalence by Age Group
def calc_weighted_stats(sub_df, val_col, weight_col='survey_weight'):
    valid = sub_df.dropna(subset=[val_col, weight_col]).copy()
    if len(valid) == 0:
        return np.nan, np.nan
    w = valid[weight_col]
    val = valid[val_col]
    mean_w = np.sum(val * w) / np.sum(w)
    var_w = np.sum(w * (val - mean_w) ** 2) / np.sum(w)
    se_w = np.sqrt(var_w / len(valid))
    return mean_w, se_w

t2_rows = []
age_groups = ['Overall', '45-59', '60-74', '75+']
for ag in age_groups:
    sub = df if ag == 'Overall' else df[df['age_group'] == ag]
    
    # Depression
    dep_prev, dep_se = calc_weighted_stats(sub, 'cesd_depression')
    cesd_mean, cesd_se = calc_weighted_stats(sub, 'cesd_score')
    
    # Cognition (direct interviews only)
    cog_sub = sub[sub['direct_interview'] == 1]
    cog_prev, cog_se = calc_weighted_stats(cog_sub, 'cognitive_impairment')
    cog_mean, cog_se = calc_weighted_stats(cog_sub, 'cognitive_score')
    
    t2_rows.append({
        'Age_Group': ag,
        'N_Eligible': len(sub),
        'Depression_Prev_Weighted_Pct': round(dep_prev * 100, 2),
        'Depression_Prev_SE': round(dep_se * 100, 2),
        'CESD_Score_Mean': round(cesd_mean, 2),
        'Cognitive_Imp_Prev_Weighted_Pct': round(cog_prev * 100, 2),
        'Cognitive_Imp_SE': round(cog_se * 100, 2),
        'Cognitive_Score_Mean': round(cog_mean, 2)
    })

table2_df = pd.DataFrame(t2_rows)
table2_path = os.path.join(TABLES_DIR, "table2_outcome_prevalence_by_age.csv")
table2_df.to_csv(table2_path, index=False)
print(f"Saved Table 2 to {table2_path}")
print(table2_df.to_string(index=False))

# 3. TABLE 2B: Outcome Prevalence by Childhood Disadvantage
def calc_cross_prev(data, exp_col, out_col, weight_col='survey_weight'):
    valid = data.dropna(subset=[exp_col, out_col, weight_col]).copy()
    res = []
    for cat in valid[exp_col].unique():
        cat_sub = valid[valid[exp_col] == cat]
        prev_w, se_w = calc_weighted_stats(cat_sub, out_col, weight_col)
        res.append({
            'Exposure': exp_col,
            'Category': cat,
            'Outcome': out_col,
            'Unweighted_N': len(cat_sub),
            'Weighted_Prev_Pct': round(prev_w * 100, 2),
            'SE': round(se_w * 100, 2)
        })
    return pd.DataFrame(res)

t2b_list = []
for exp in ['childhood_ses', 'childhood_health', 'childhood_bedridden', 'cumulative_disadvantage']:
    t2b_list.append(calc_cross_prev(df, exp, 'cesd_depression'))
    t2b_list.append(calc_cross_prev(df[df['direct_interview'] == 1], exp, 'cognitive_impairment'))

table2b_df = pd.concat(t2b_list, ignore_index=True)
table2b_path = os.path.join(TABLES_DIR, "table2b_prevalence_by_exposure.csv")
table2b_df.to_csv(table2b_path, index=False)
print(f"Saved Table 2B to {table2b_path}")

# 4. FIGURE 1: Age Distribution
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
ax.hist(df['age'], bins=35, weights=df['survey_weight'] / df['survey_weight'].sum(), color='#2b5c8f', edgecolor='white', alpha=0.85)
ax.set_title(r"Figure 1: Survey-Weighted Age Distribution of LASI Respondents (Age $\geq$ 45)", fontsize=13, fontweight='bold', pad=12)
ax.set_xlabel("Age in Years", fontsize=11)
ax.set_ylabel("Weighted Population Proportion", fontsize=11)
ax.axvline(60, color='#e06666', linestyle='--', linewidth=1.5, label='Age 60 (Senior Citizen Threshold)')
ax.axvline(75, color='#cc0000', linestyle='--', linewidth=1.5, label='Age 75 (Oldest-Old Threshold)')
ax.legend(frameon=True, facecolor='white')
fig.tight_layout()
fig1_path = os.path.join(FIGS_DIR, "figure1_age_distribution.png")
fig.savefig(fig1_path)
plt.close(fig)
print(f"Saved Figure 1 to {fig1_path}")

# 5. FIGURE 2: Prevalence of Early-Life Disadvantage Exposures
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 4.5), dpi=300)

# Childhood SES
ses_freq = calc_weighted_freq(df, 'childhood_ses')
sns.barplot(x=ses_freq.index, y=ses_freq['Weighted_Percent'], ax=ax1, palette="crest", hue=ses_freq.index, legend=False)
ax1.set_title("Childhood SES", fontsize=11, fontweight='bold')
ax1.set_ylabel("Weighted Percentage (%)", fontsize=10)
ax1.set_xlabel("")
for i, v in enumerate(ses_freq['Weighted_Percent']):
    ax1.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=9, fontweight='semibold')
ax1.set_ylim(0, 65)

# Childhood Health
hlth_freq = calc_weighted_freq(df, 'childhood_health')
sns.barplot(x=hlth_freq.index, y=hlth_freq['Weighted_Percent'], ax=ax2, palette="flare", hue=hlth_freq.index, legend=False)
ax2.set_title("Childhood Health", fontsize=11, fontweight='bold')
ax2.set_ylabel("")
ax2.set_xlabel("")
for i, v in enumerate(hlth_freq['Weighted_Percent']):
    ax2.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=9, fontweight='semibold')
ax2.set_ylim(0, 100)

# Bedridden
bed_freq = calc_weighted_freq(df, 'childhood_bedridden')
sns.barplot(x=bed_freq.index, y=bed_freq['Weighted_Percent'], ax=ax3, palette="Blues_r", hue=bed_freq.index, legend=False)
ax3.set_title(r"Bedridden $\geq$ 1 Month", fontsize=11, fontweight='bold')
ax3.set_ylabel("")
ax3.set_xlabel("")
for i, v in enumerate(bed_freq['Weighted_Percent']):
    ax3.text(i, v + 1, f"{v:.1f}%", ha='center', fontsize=9, fontweight='semibold')
ax3.set_ylim(0, 110)

fig.suptitle("Figure 2: Survey-Weighted Prevalence of Early-Life Disadvantage Exposures", fontsize=13, fontweight='bold', y=1.03)
fig.tight_layout()
fig2_path = os.path.join(FIGS_DIR, "figure2_childhood_disadvantage_prevalence.png")
fig.savefig(fig2_path, bbox_inches='tight')
plt.close(fig)
print(f"Saved Figure 2 to {fig2_path}")

# 6. FIGURE 3: Outcome Prevalence across Age Groups
fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
age_prevs = table2_df[table2_df['Age_Group'] != 'Overall']
x = np.arange(len(age_prevs))
width = 0.35

rects1 = ax.bar(x - width/2, age_prevs['Cognitive_Imp_Prev_Weighted_Pct'], width, label='Cognitive Impairment', color='#c25953')
rects2 = ax.bar(x + width/2, age_prevs['Depression_Prev_Weighted_Pct'], width, label=r'Depressive Symptoms (CES-D $\geq$ 4)', color='#4a7c59')

ax.set_title("Figure 3: Survey-Weighted Prevalence of Cognitive Impairment & Depression by Age Group", fontsize=12, fontweight='bold', pad=12)
ax.set_ylabel("Prevalence (%)", fontsize=11)
ax.set_xlabel("Age Group (Years)", fontsize=11)
ax.set_xticks(x)
ax.set_xticklabels(age_prevs['Age_Group'], fontsize=10)
ax.legend(frameon=True, facecolor='white')
ax.set_ylim(0, 35)

for rect in rects1:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)
for rect in rects2:
    h = rect.get_height()
    ax.annotate(f'{h:.1f}%', xy=(rect.get_x() + rect.get_width()/2, h), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=9)

fig.tight_layout()
fig3_path = os.path.join(FIGS_DIR, "figure3_outcome_prevalence_by_age.png")
fig.savefig(fig3_path)
plt.close(fig)
print(f"Saved Figure 3 to {fig3_path}")
