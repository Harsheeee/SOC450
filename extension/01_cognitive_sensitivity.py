import os
import pandas as pd
import numpy as np
import sys

sys.path.append(os.path.abspath('code'))
import survey_utils

DATA_FILE = "data_analysis/lasi_clean_v2.parquet"
OUT_DIR = "extension"

if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

print(f"Loading {DATA_FILE}...")
df = pd.read_parquet(DATA_FILE)

# Construct same variables as 08_models_v2.py
df['srh'] = df['srh'].map({'Very good': 'Excellent', 'Good': 'Very good', 'Fair': 'Good', 'Poor': 'Fair', 'Very poor': 'Poor'})
df['state_fe'] = df['stateid'].astype(int)
df['ses_avg'] = np.where(df.childhood_ses.isin(['Pretty well-off', 'Average', 'Poor']), (df.childhood_ses == 'Average').astype(float), np.nan)
df['ses_poor'] = np.where(df.childhood_ses.isin(['Pretty well-off', 'Average', 'Poor']), (df.childhood_ses == 'Poor').astype(float), np.nan)
df['hlth_poor'] = np.where(df.childhood_health.notna(), (df.childhood_health == 'Poor').astype(float), np.nan)
df['hlth_poor_orig'] = np.where(df.childhood_health_poor_original.notna(), df.childhood_health_poor_original, np.nan)
df['bed_yes'] = np.where(df.childhood_bedridden.notna(), (df.childhood_bedridden == 'Yes').astype(float), np.nan)

outcomes = ['memory_score', 'orientation_score', 'mem_orient']

DEMO = "age + C(sex, Treatment('Male')) + C(residence_cat, Treatment('Rural')) + C(caste, Treatment('General/None')) + married_binary + C(state_fe)"
EDU = "C(education, Treatment('No formal education')) + C(mpce_quintile)"
HLTH = "chronic_count + C(srh, Treatment('Excellent'))"

models = {
    'Model A (Baseline)': DEMO,
    'Model B (Adult SES)': f"{DEMO} + {EDU}",
    'Model C (Exploratory Health)': f"{DEMO} + {EDU} + {HLTH}"
}

# The sample mask from 08_models_v2.py
CORE = ['ses_avg', 'ses_poor', 'hlth_poor_orig', 'bed_yes', 'age', 'sex', 'residence_cat', 'caste', 'married_binary', 'state_fe',
        'education', 'mpce_quintile', 'chronic_count', 'srh', 'survey_weight', 'cluster_psu', 'stratum']

# Complete case for direct respondents across all vars
mask = df[CORE + outcomes].notna().all(axis=1) & (df['direct_interview'] == 1)
df_ana = df[mask].copy()

print(f"Analytical sample size (complete cases): {len(df_ana)}")
for c in outcomes:
    m = df.loc[df['direct_interview'] == 1, c].isna().sum()
    print(f"  {c}: {m} missing among direct interviews")

def fmt(r):
    return f"{r['est']:.3f} ({r['lo']:.3f}, {r['hi']:.3f})"

results = []

for out in outcomes:
    print(f"\nAnalyzing outcome: {out} (Range: {df_ana[out].min()} - {df_ana[out].max()})")
    for m_name, f_str in models.items():
        # Joint SES modeling, plus Health (Original) and Bedridden
        full_formula = f"{out} ~ ses_avg + ses_poor + hlth_poor_orig + bed_yes + {f_str}"
        print(f"  Fitting {m_name}...")
        
        try:
            fit = survey_utils.svy_glm(full_formula, df_ana, family='gaussian')
            
            row = {'Outcome': out, 'Model': m_name, 'N': fit.nobs}
            
            # SES: Poor (ref: Well-off)
            r_ses_poor = survey_utils.term_row(fit, "ses_poor", exp=False)
            row['SES: Poor'] = fmt(r_ses_poor)
            row['SES: Poor p-value'] = f"{r_ses_poor['p']:.3f}"
            
            # SES: Average (ref: Well-off)
            r_ses_avg = survey_utils.term_row(fit, "ses_avg", exp=False)
            row['SES: Average'] = fmt(r_ses_avg)
            row['SES: Average p-value'] = f"{r_ses_avg['p']:.3f}"
            
            # Health: Poor Original
            r_hlth = survey_utils.term_row(fit, "hlth_poor_orig", exp=False)
            row['Health: Poor/Very Poor'] = fmt(r_hlth)
            row['Health p-value'] = f"{r_hlth['p']:.3f}"
            
            # Bedridden
            r_bed = survey_utils.term_row(fit, "bed_yes", exp=False)
            row['Bedridden'] = fmt(r_bed)
            row['Bedridden p-value'] = f"{r_bed['p']:.3f}"
            
            results.append(row)
        except Exception as e:
            print(f"    Failed: {e}")

res_df = pd.DataFrame(results)
out_csv = os.path.join(OUT_DIR, "continuous_cognitive_sensitivity.csv")
res_df.to_csv(out_csv, index=False)
print(f"\nResults saved to {out_csv}")
