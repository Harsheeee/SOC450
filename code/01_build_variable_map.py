#!/usr/bin/env python3
"""
Step 01: Build Variable Inventory and Master Variable Specification Map
- Inventories raw variables from LASI Wave 1 Individual Dataset
- Extracts exact variable names, labels, types, and value formats
- Creates master `variable_map.csv` adhering to the pre-specified protocol
"""

import os
import csv
import pyreadstat
import pandas as pd

INDIVIDUAL_DTA = "dataset/3_LASI_W1_Individual_v4.dta"
DIAGNOSTICS_DIR = "outputs/diagnostics"
os.makedirs(DIAGNOSTICS_DIR, exist_ok=True)

print("Reading metadata from:", INDIVIDUAL_DTA)
_, meta = pyreadstat.read_dta(INDIVIDUAL_DTA, metadataonly=True)

# 1. Output full variable inventory TSV
inventory_path = os.path.join(DIAGNOSTICS_DIR, "variable_inventory.tsv")
with open(inventory_path, "w", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["column_index", "variable_name", "variable_label", "storage_type"])
    for idx, (name, label) in enumerate(zip(meta.column_names, meta.column_labels), start=1):
        lbl = label if label is not None else ""
        type_str = meta.readstat_variable_types.get(name, "")
        writer.writerow([idx, name, lbl, type_str])
print(f"Saved full inventory ({len(meta.column_names):,} variables) to {inventory_path}")

# 2. Master Variable Map definitions
# Each entry captures the exact construct, operational role, source variable, clean coding, and reference category
var_specs = [
    # Identifier & Survey Design
    {
        "construct": "Respondent Identifier",
        "role": "identifier",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ID",
        "lasi_variable": "prim_key",
        "question_text": "Unique individual respondent ID (15-digit)",
        "original_codes": "15-digit number",
        "clean_codes": "String / int64",
        "reference_category": "None",
        "missing_codes": "None",
        "analysis_use": "Primary key",
        "source": "IIPS User Guide",
        "notes": "Unique for all 73,396 respondents"
    },
    {
        "construct": "Household Identifier",
        "role": "merge_key",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ID",
        "lasi_variable": "hhid",
        "question_text": "Unique household ID (15-digit)",
        "original_codes": "15-digit number",
        "clean_codes": "String / int64",
        "reference_category": "None",
        "missing_codes": "None",
        "analysis_use": "Household link",
        "source": "IIPS User Guide",
        "notes": "Links to household-level files"
    },
    {
        "construct": "Survey Weight (National)",
        "role": "survey_design",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "Weight",
        "lasi_variable": "indiaindividualweight",
        "question_text": "India level individual sample weight",
        "original_codes": "Continuous positive float",
        "clean_codes": "Continuous numeric weight",
        "reference_category": "None",
        "missing_codes": "None",
        "analysis_use": "Survey probability weighting",
        "source": "IIPS User Guide Section 5.4",
        "notes": "Accounts for selection probability, non-response, and post-stratification"
    },
    {
        "construct": "Survey Weight (State)",
        "role": "survey_design",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "Weight",
        "lasi_variable": "stateindividualweight",
        "question_text": "State level individual sample weight",
        "original_codes": "Continuous positive float",
        "clean_codes": "Continuous numeric weight",
        "reference_category": "None",
        "missing_codes": "None",
        "analysis_use": "State-level estimates",
        "source": "IIPS User Guide Section 5.4",
        "notes": "Use for state-specific sensitivity checks"
    },
    {
        "construct": "Cluster / PSU",
        "role": "survey_design",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "Design",
        "lasi_variable": "ssuid",
        "question_text": "Secondary Sampling Unit / village or urban ward/block cluster",
        "original_codes": "2,439 unique cluster IDs",
        "clean_codes": "Categorical / Cluster ID",
        "reference_category": "None",
        "missing_codes": "None",
        "analysis_use": "Cluster-robust variance estimation",
        "source": "IIPS User Guide Section 5.3a",
        "notes": "Primary sampling cluster in released public microdata"
    },
    {
        "construct": "Sampling Stratum",
        "role": "survey_design",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "Design",
        "lasi_variable": "stateid, residence",
        "question_text": "State ID and Place of Residence (Rural / Urban)",
        "original_codes": "36 states x 2 residence types = 72 strata",
        "clean_codes": "Categorical stratum (1 to 72)",
        "reference_category": "None",
        "missing_codes": "None",
        "analysis_use": "Survey stratification",
        "source": "IIPS Sampling Design Chapter 2",
        "notes": "Explicit design strata in LASI multistage sampling"
    },
    {
        "construct": "Proxy Interview Identifier",
        "role": "sample_filter",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "Survey Admin",
        "lasi_variable": "rproxy",
        "question_text": "Proxy interview identifier",
        "original_codes": "0=Not proxy, 1=Proxy interview",
        "clean_codes": "0=Direct, 1=Proxy",
        "reference_category": "0",
        "missing_codes": "None",
        "analysis_use": "Exclude proxy respondents from direct cognitive test sample",
        "source": "IIPS User Guide Section 5.3",
        "notes": "Cognitive tests were not administered in proxy interviews (N=705 in 45+)"
    },

    # Primary Exposures
    {
        "construct": "Childhood SES",
        "role": "primary_exposure",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ht",
        "lasi_variable": "ht235",
        "question_text": "Financial status of family during childhood up to age 16",
        "original_codes": "1=Pretty well off, 2=Average, 3=Poor, 4=Varied [voluntary]",
        "clean_codes": "1=Pretty well-off, 2=Average, 3=Poor",
        "reference_category": "1 (Pretty well-off)",
        "missing_codes": ".d, .r, .m, 4 (Varied kept as separate/sensitivity)",
        "analysis_use": "Primary exposure (Categorical)",
        "source": "Health module ht235",
        "notes": "321 missing values (0.48%) in 45+ sample"
    },
    {
        "construct": "Childhood Health",
        "role": "primary_exposure",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ht",
        "lasi_variable": "ht231",
        "question_text": "Status of childhood health up to age 16",
        "original_codes": "1=Very good, 2=Good, 3=Fair, 4=Poor, 5=Very poor",
        "clean_codes": "Primary: 0=Good (1,2), 1=Poor (3,4,5); Sensitivity: 5-level",
        "reference_category": "0 (Good / Very good)",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Primary exposure (Binary and 5-level ordinal)",
        "source": "Health module ht231",
        "notes": "965 missing values (1.45%) in 45+ sample"
    },
    {
        "construct": "Childhood Bedridden / Serious Illness",
        "role": "primary_exposure",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ht",
        "lasi_variable": "ht233",
        "question_text": "Ever bedridden for a month or more during childhood before age 16",
        "original_codes": "1=Yes, 2=No",
        "clean_codes": "0=No (2), 1=Yes (1)",
        "reference_category": "0 (No)",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Primary exposure (Binary)",
        "source": "Health module ht233",
        "notes": "Prevalence is 5.06% in 45+ sample (3,370 yes)"
    },
    {
        "construct": "Childhood School Absence",
        "role": "secondary_exposure",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ht",
        "lasi_variable": "ht234",
        "question_text": "Missed school for a month or more due to health problem during childhood",
        "original_codes": "1=Yes, 2=No",
        "clean_codes": "0=No, 1=Yes",
        "reference_category": "0 (No)",
        "missing_codes": "Skipped if never attended school (dm006==2)",
        "analysis_use": "Sensitivity exposure among schooling sub-sample",
        "source": "Health module ht234",
        "notes": "1,381 yes (2.1% of 45+)"
    },

    # Secondary Exposures: Parental Education
    {
        "construct": "Father Education",
        "role": "secondary_exposure",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "fs",
        "lasi_variable": "fs306, fs308",
        "question_text": "Father attended school, highest education completed by father",
        "original_codes": "fs306 (1=Yes, 2=No), fs308 (1 to 9 levels)",
        "clean_codes": "0=No school, 1=Primary or less, 2=Middle/secondary, 3=Higher sec/college",
        "reference_category": "0 (No formal schooling)",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Early-life parental background proxy",
        "source": "Family Social module fs306/fs308",
        "notes": "Used in sensitivity analysis"
    },
    {
        "construct": "Mother Education",
        "role": "secondary_exposure",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "fs",
        "lasi_variable": "fs315, fs317",
        "question_text": "Mother attended school, highest education completed by mother",
        "original_codes": "fs315 (1=Yes, 2=No), fs317 (1 to 9 levels)",
        "clean_codes": "0=No school, 1=Primary or less, 2=Middle/secondary, 3=Higher sec/college",
        "reference_category": "0 (No formal schooling)",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Early-life parental background proxy",
        "source": "Family Social module fs315/fs317",
        "notes": "Used in sensitivity analysis"
    },

    # Outcomes: Depressive Symptoms (CES-D 10 items)
    {
        "construct": "CES-D 10 Items",
        "role": "outcome_components",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "fs",
        "lasi_variable": "fs701 - fs710",
        "question_text": "In the past week: trouble concentrating, depressed, tired/low energy, afraid, satisfied, alone, bothered, effort, hopeful, happy",
        "original_codes": "1=Rarely/never (<1 day), 2=Sometimes (1-2 days), 3=Often (3-4 days), 4=Most/all (5-7 days)",
        "clean_codes": "Dichotomized 0/1 per item (Negative: 2-4 -> 1; Positive fs705,fs709,fs710 reverse: 1-2 -> 1, 3-4 -> 0)",
        "reference_category": "0 (No symptom)",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Sum score (0 to 10)",
        "source": "Psychosocial section fs701-fs710",
        "notes": "64,822 respondents (97.3%) have all 10 items complete"
    },
    {
        "construct": "Depressive Symptoms (Binary)",
        "role": "primary_outcome",
        "source_file": "Derived from fs701-fs710",
        "module": "Derived",
        "lasi_variable": "cesd_depression",
        "question_text": "Elevated depressive symptoms indicator (CES-D sum >= 4)",
        "original_codes": "Derived from 0-10 sum",
        "clean_codes": "0 = No (<4), 1 = Yes (>=4)",
        "reference_category": "0 (No depressive symptoms)",
        "missing_codes": "Missing if >= 2 items missing",
        "analysis_use": "Primary outcome for depression models (Modified Poisson PR)",
        "source": "Established LASI/HRS literature threshold",
        "notes": "Clinical validation cutoff in international ageing studies"
    },
    {
        "construct": "CES-D Score (Continuous)",
        "role": "secondary_outcome",
        "source_file": "Derived from fs701-fs710",
        "module": "Derived",
        "lasi_variable": "cesd_score",
        "question_text": "Composite CES-D depression score (range 0 to 10)",
        "original_codes": "Integer sum 0 to 10",
        "clean_codes": "Continuous/count score 0 to 10",
        "reference_category": "None",
        "missing_codes": "Missing if >= 2 items missing",
        "analysis_use": "Sensitivity outcome",
        "source": "Established LASI/HRS scoring",
        "notes": "Used for score distribution and secondary linear models"
    },

    # Outcomes: Cognition
    {
        "construct": "Orientation Score",
        "role": "cognition_domain",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "mh",
        "lasi_variable": "mh002 - mh009",
        "question_text": "Orientation to date, month, year, day of week, place, village/town, landmark, district",
        "original_codes": "1=Correct, 2=Incorrect",
        "clean_codes": "Sum of correct answers (0 to 8 points)",
        "reference_category": "None",
        "missing_codes": ".d, .r, .m coded as 0 (incorrect) if test attempted",
        "analysis_use": "Domain component of cognitive composite score",
        "source": "Mental Health module mh002-mh009",
        "notes": ">97.5% completion on all items"
    },
    {
        "construct": "Immediate Word Recall",
        "role": "cognition_domain",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "mh",
        "lasi_variable": "mh012",
        "question_text": "Number of words recalled correctly immediately from 10-word list",
        "original_codes": "0 to 10 words",
        "clean_codes": "Integer 0 to 10",
        "reference_category": "None",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Memory domain component (0 to 10)",
        "source": "Mental Health module mh012",
        "notes": "Mean ~4.5 words, 97.5% complete"
    },
    {
        "construct": "Delayed Word Recall",
        "role": "cognition_domain",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "mh",
        "lasi_variable": "mh056",
        "question_text": "Number of words recalled correctly after delay from 10-word list",
        "original_codes": "0 to 10 words",
        "clean_codes": "Integer 0 to 10",
        "reference_category": "None",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Memory domain component (0 to 10)",
        "source": "Mental Health module mh056",
        "notes": "Mean ~3.8 words, 91.4% complete"
    },
    {
        "construct": "Verbal Fluency",
        "role": "cognition_domain",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "mh",
        "lasi_variable": "mh016_correct",
        "question_text": "Number of animals/birds named correctly in 1 minute",
        "original_codes": "Count (0 to 45)",
        "clean_codes": "Integer count",
        "reference_category": "None",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Executive/retrieval domain component",
        "source": "Mental Health module mh016_correct",
        "notes": "Mean ~10.8 animals, 98.0% complete"
    },
    {
        "construct": "Arithmetic / Serial 7s",
        "role": "cognition_domain",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "mh",
        "lasi_variable": "mh045",
        "question_text": "Serial 7s respondent score (subtraction of 7 from 100 up to 5 times)",
        "original_codes": "Score 0 to 5",
        "clean_codes": "Integer 0 to 5",
        "reference_category": "None",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Working memory/attention domain component",
        "source": "Mental Health module mh045",
        "notes": "Completed by 60.3% of respondents (others skipped due to numeracy limits)"
    },
    {
        "construct": "Executive Function / Drawing",
        "role": "cognition_domain",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "mh",
        "lasi_variable": "mh019, mh020, mh051",
        "question_text": "Object naming (pencil, watch), Drawing intersecting pentagons",
        "original_codes": "mh019/mh020 (1=Correct, 2=Incorrect), mh051 (1=Drew, 2=Failed)",
        "clean_codes": "Points (0/1 for each test)",
        "reference_category": "None",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Executive function & visual construction component",
        "source": "Mental Health module",
        "notes": "Combined into composite score"
    },
    {
        "construct": "Cognitive Composite Score",
        "role": "primary_outcome",
        "source_file": "Derived from mh module",
        "module": "Derived",
        "lasi_variable": "cognitive_score",
        "question_text": "Harmonized HRS/LASI composite cognitive performance score",
        "original_codes": "Continuous composite score",
        "clean_codes": "Continuous standardized or raw score",
        "reference_category": "None",
        "missing_codes": "Missing if primary domains unattempted",
        "analysis_use": "Primary cognitive outcome for Linear Regression",
        "source": "HRS-harmonized cognitive battery",
        "notes": "Higher score indicates better cognitive function"
    },
    {
        "construct": "Cognitive Impairment (Binary)",
        "role": "secondary_outcome",
        "source_file": "Derived from cognitive_score",
        "module": "Derived",
        "lasi_variable": "cognitive_impairment",
        "question_text": "Cognitive impairment indicator (lowest decile / < -1.5 SD)",
        "original_codes": "Binary 0/1",
        "clean_codes": "0 = Normal cognition, 1 = Impaired",
        "reference_category": "0 (Normal cognition)",
        "missing_codes": "Missing if score missing",
        "analysis_use": "Secondary outcome for Modified Poisson / Logistic regression",
        "source": "Published LASI cognitive literature threshold",
        "notes": "Identifies bottom tail of cognitive performance"
    },

    # Covariates: Demographics
    {
        "construct": "Age (Continuous)",
        "role": "covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "dm",
        "lasi_variable": "dm005",
        "question_text": "Age at last birthday",
        "original_codes": "18 to 116 years",
        "clean_codes": "Continuous integer (restricted to >=45)",
        "reference_category": "None",
        "missing_codes": "None (100% complete)",
        "analysis_use": "Continuous adjustment in Model 1-3",
        "source": "Demographics module dm005",
        "notes": "Mean 57.9 across survey; 63.1 among 45+"
    },
    {
        "construct": "Age Group (Categorical)",
        "role": "effect_modifier",
        "source_file": "Derived from dm005",
        "module": "Derived",
        "lasi_variable": "age_group",
        "question_text": "Categorical age groups for older adults",
        "original_codes": "45-59, 60-74, 75+",
        "clean_codes": "1=45-59, 2=60-74, 3=75+",
        "reference_category": "1 (45-59)",
        "missing_codes": "None",
        "analysis_use": "Primary effect modifier for interaction models",
        "source": "Pre-specified in Project Plan",
        "notes": "34,704 in 45-59; 25,022 in 60-74; 6,880 in 75+"
    },
    {
        "construct": "Sex",
        "role": "covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "dm",
        "lasi_variable": "dm003",
        "question_text": "Sex of Respondent",
        "original_codes": "1=Male, 2=Female",
        "clean_codes": "1=Male, 2=Female",
        "reference_category": "1 (Male)",
        "missing_codes": "None (100% complete)",
        "analysis_use": "Demographic adjustment",
        "source": "Demographics module dm003",
        "notes": "46.8% Male, 53.2% Female in 45+"
    },
    {
        "construct": "Place of Residence",
        "role": "covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "Design/dm",
        "lasi_variable": "residence",
        "question_text": "Place of residence (Rural / Urban)",
        "original_codes": "1=Rural, 2=Urban",
        "clean_codes": "1=Rural, 2=Urban",
        "reference_category": "1 (Rural)",
        "missing_codes": "None (100% complete)",
        "analysis_use": "Demographic adjustment and stratification",
        "source": "Survey design identifier",
        "notes": "68.1% Rural, 31.9% Urban"
    },
    {
        "construct": "Caste / Social Group",
        "role": "covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "dm",
        "lasi_variable": "dm013",
        "question_text": "Caste category",
        "original_codes": "1=Scheduled Caste (SC), 2=Scheduled Tribe (ST), 3=Other Backward Class (OBC), 4=None of them/General",
        "clean_codes": "1=SC, 2=ST, 3=OBC, 4=General/None",
        "reference_category": "4 (General/None)",
        "missing_codes": "2,378 missing (3.6%)",
        "analysis_use": "Demographic adjustment",
        "source": "Demographics module dm013",
        "notes": "Includes missing category or complete case"
    },
    {
        "construct": "Marital Status",
        "role": "covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "dm",
        "lasi_variable": "dm021",
        "question_text": "Current marital status",
        "original_codes": "1=Currently married, 2=Widowed, 3=Divorced, 4=Separated, 5=Deserted, 6=Live-in, 7=Never married",
        "clean_codes": "1=Currently married, 2=Widowed, 3=Divorced/Separated/Deserted, 4=Never married",
        "reference_category": "1 (Currently married)",
        "missing_codes": "4 missing (0.01%)",
        "analysis_use": "Demographic adjustment",
        "source": "Demographics module dm021",
        "notes": "77.0% married, 21.0% widowed"
    },

    # Covariates: Adult Socioeconomic Status
    {
        "construct": "Educational Attainment",
        "role": "covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "dm",
        "lasi_variable": "dm006, dm008",
        "question_text": "Ever attended school and highest educational level completed",
        "original_codes": "dm006 (1=Yes, 2=No), dm008 (1 to 9 levels)",
        "clean_codes": "0=No formal education, 1=Less than primary, 2=Primary completed, 3=Middle completed, 4=Secondary completed, 5=Higher secondary/diploma, 6=Graduate & above",
        "reference_category": "0 (No formal education)",
        "missing_codes": "Only 4 cases missing on dm006",
        "analysis_use": "Adult SES adjustment (Model 2)",
        "source": "Demographics module dm006/dm008",
        "notes": "46.0% have no formal education; skip pattern validated"
    },
    {
        "construct": "Household Economic Status (MPCE)",
        "role": "covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "Household/Derived",
        "lasi_variable": "mpce_quintile",
        "question_text": "Monthly Per Capita Consumption Expenditure Quintile",
        "original_codes": "1=Poorest, 2=Poorer, 3=Middle, 4=Richer, 5=Richest",
        "clean_codes": "1 to 5 (Quintiles)",
        "reference_category": "1 (Poorest)",
        "missing_codes": "None (100% complete in Individual file)",
        "analysis_use": "Adult SES adjustment (Model 2)",
        "source": "Pre-computed LASI consumption quintile",
        "notes": "Equally distributed (~20% per quintile)"
    },

    # Covariates: Adult Health (Pathway Controls)
    {
        "construct": "Adult Chronic Morbidity",
        "role": "pathway_covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ht",
        "lasi_variable": "ht002, ht003, ht005, ht006, ht007",
        "question_text": "Diagnosed hypertension, diabetes, chronic lung disease, heart disease, stroke",
        "original_codes": "1=Yes, 2=No per disease",
        "clean_codes": "Sum count of chronic conditions (0, 1, 2+)",
        "reference_category": "0 (No chronic condition)",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Model 3 (Adult health pathway adjustment)",
        "source": "Health module ht002-ht007",
        "notes": "Multimorbidity indicator"
    },
    {
        "construct": "Adult Self-Rated Health",
        "role": "pathway_covariate",
        "source_file": "3_LASI_W1_Individual_v4.dta",
        "module": "ht",
        "lasi_variable": "ht001_a",
        "question_text": "Self-rated general health",
        "original_codes": "1=Very good, 2=Good, 3=Fair, 4=Poor, 5=Very poor",
        "clean_codes": "1=Very good, 2=Good, 3=Fair, 4=Poor, 5=Very poor",
        "reference_category": "1 (Very good)",
        "missing_codes": ".d, .r, .m",
        "analysis_use": "Model 3 (Adult health pathway adjustment)",
        "source": "Health module ht001_a",
        "notes": "Subjective health marker"
    }
]

# Write variable_map.csv
var_map_df = pd.DataFrame(var_specs)
var_map_path = "variable_map.csv"
var_map_df.to_csv(var_map_path, index=False)
print(f"Saved master variable map ({len(var_map_df)} constructs) to {var_map_path}")
