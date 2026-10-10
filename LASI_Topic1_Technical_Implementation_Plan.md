# LASI Wave 1 Quantitative Ageing Study
## Technical Implementation Plan

### Project title
**Early-Life Disadvantage and Later-Life Mental and Cognitive Health in India: Evidence from LASI Wave 1**

### Core research question
Among adults aged 45 years and above in India, are adverse childhood socioeconomic and health conditions associated with poorer later-life cognitive performance and depressive symptoms, and do these associations differ across stages of ageing?

> **Design warning:** LASI Wave 1 is a cross-sectional baseline for this project. The study can estimate age-group differences and age interaction/heterogeneity, but it cannot establish individual longitudinal cognitive decline or causal effects.

---

# 1. Project at a glance

## 1.1 Problem

Population ageing increases the importance of understanding why some people reach older age with better mental and cognitive health than others. A life-course perspective asks whether circumstances experienced early in life continue to be associated with health much later.

LASI Wave 1 is particularly suited to this question because it combines retrospective childhood information with current adult health, cognitive assessment, mental-health measures, socioeconomic characteristics, family/social information, and a nationally representative survey design.

The immediate empirical problem is therefore:

> **Can measurable early-life disadvantage be linked to current cognitive and depressive outcomes in a nationally representative sample of Indian adults, after accounting for present-day demographic and socioeconomic circumstances?**

## 1.2 Proposed solution

Build a respondent-level analytical dataset from LASI Wave 1, operationalize three early-life exposures, derive two outcomes, properly account for LASI's sampling design, and estimate adjusted associations.

The primary analytical structure is:

```text
Childhood socioeconomic status ─────┐
                                    │
Childhood health ───────────────────┼──> Cognitive outcome
                                    │
Childhood serious illness ─────────┤
                                    │
                                    └──> Depressive symptoms

Age group is examined as an effect modifier:

Childhood disadvantage × Age group ──> Outcome
```

## 1.3 Why this is technically interesting

The project is not just a prevalence calculation. It combines:

1. Survey data engineering.
2. Complex-survey weighting.
3. Construction of standardized health outcomes.
4. Multivariable regression.
5. Interaction/effect-modification analysis.
6. Predicted probabilities and publication-quality figures.
7. Sensitivity analysis.
8. Transparent reproducibility.

---

# 2. Scope and exclusions

## 2.1 Data files to use

### Required

- LASI Wave 1 **Individual dataset** — primary analysis file.
- LASI Wave 1 **Household dataset** — use only for household-derived variables not already present in the individual file, especially current economic-status measures.
- LASI Wave 1 **Data User Guide** and questionnaire/codebook.

### Potentially useful for validation only

- Household roster / CV member file, if household-member composition or household linkage checks are needed.

### Not used in the core analysis

- Biomarker dataset.
- Community dataset.
- Death/member dataset.
- Environmental exposure dataset.
- Spirometry dataset.
- DBS dataset.
- Metro-city dataset.
- LASI Pilot 2010.

Do not merge these into the main analytical dataset unless a later sensitivity analysis is explicitly approved.

## 2.2 Target population

Primary target:

\[
\text{LASI respondents aged }45+
\]

LASI Wave 1 contains 73,396 individual observations, with one observation per respondent in the released Individual file. The LASI User Guide also reports 31,902 adults aged 60+ and 6,880 aged 75+.

The individual survey was administered to people aged 45+ and their spouses irrespective of age; for this project restrict to age >= 45 unless the approved protocol states otherwise.

## 2.3 Unit of analysis

The primary unit of analysis is the **individual respondent**.

Household variables are merged onto the respondent using the LASI household identifier.

---

# 3. Technical terminology students must understand

## 3.1 Cross-sectional study

Data are observed at one survey wave/time point for each respondent. We compare people of different ages and characteristics at the same wave rather than repeatedly observing the same person over time.

## 3.2 Exposure

A characteristic treated as the explanatory variable of interest. Here, examples are childhood socioeconomic status and childhood health.

## 3.3 Outcome

The variable whose variation we are trying to explain statistically. Here, cognitive impairment/performance and depressive symptoms.

## 3.4 Covariate

A variable included in the statistical model to account for other factors related to the exposure and/or outcome.

## 3.5 Confounder

A variable associated with both the exposure and outcome that can distort an exposure-outcome association if ignored.

## 3.6 Effect modifier / interaction variable

A variable for which the exposure-outcome association differs between groups or levels. Here age group is a candidate effect modifier.

## 3.7 Prevalence

The proportion of the study population with an outcome at the survey time point.

## 3.8 Prevalence ratio (PR)

The ratio of prevalence between two exposure groups. A PR of 1.30 means the estimated prevalence is 30% higher in the exposed group, under the fitted model.

## 3.9 Odds ratio (OR)

The ratio of odds, not prevalence. ORs can be substantially farther from 1 than PRs when outcomes are common, so ORs should not be casually interpreted as risk ratios.

## 3.10 Survey weight

A weight adjusts for the fact that some sampled people represent more population members than others because of unequal selection probabilities, non-response adjustment, and post-stratification.

LASI provides `indiaindividualweight` for national individual-level estimates and `stateindividualweight` for state-level estimates.

## 3.11 PSU

Primary Sampling Unit. In LASI's multistage design, PSUs include sub-district-level sampling units before lower-level sampling.

## 3.12 Stratum

A sampling-design grouping used when selecting the sample. Survey software needs strata to estimate uncertainty correctly.

## 3.13 Robust standard error

A standard-error estimate designed to be less sensitive to certain forms of variance misspecification. We will use survey-design-aware estimators where possible and robust methods where appropriate.

## 3.14 Interaction term

A product of two variables in a regression model. Example:

\[
ChildSES \times AgeGroup
\]

It tests whether the estimated association between childhood SES and the outcome differs by age group.

## 3.15 Sensitivity analysis

A secondary analysis testing whether the main conclusion changes when reasonable alternative definitions or model specifications are used.

## 3.16 Missing not asked / skip code

LASI uses special missing/eligibility codes. They are not all equivalent to ordinary missing data and must be recoded according to the LASI documentation before analysis.

---

# 4. Source-data architecture

The LASI User Guide states that the released microdata include separate household roster, household, individual and biomarker files, and that `hhid` identifies a household while `prim_key` uniquely identifies an individual.

Conceptually:

```text
                 LASI Wave 1
                     |
       +-------------+--------------+
       |                            |
   Individual                    Household
  73,396 rows                   43,584 rows
       |                            |
 prim_key + hhid                  hhid
       |                            |
       +-------------+--------------+
                     |
                   MERGE
                     |
                     v
            Analytical dataset
```

The User Guide also states that all LASI datasets can be linked using `prim_key`, `hhid`, or `ssuid` as appropriate.

---

# 5. Recommended software stack

## Primary recommendation

### R for statistical inference

Use R because the `survey` package is designed for complex survey samples and handles weights, strata and PSUs directly.

### Python for data engineering

Use Python/pandas/pyreadstat for:

- reading large `.dta` files
- metadata inspection
- automated variable discovery
- data-quality checks
- export to smaller analysis files
- plots where convenient

### Alternative

If the team has Stata and is comfortable with it, Stata is also an excellent option and is consistent with several published LASI papers. The analysis logic remains the same.

For a two-week student project, avoid using three statistical languages simultaneously. A good setup is:

> **Python for inspection/ETL + R for final statistical analysis.**

---

# 6. Project directory structure

Create this structure before doing analysis:

```text
lasi_ageing_project/
|
+-- data_raw/
|   +-- individual/
|   +-- household/
|   +-- roster/
|   +-- documentation/
|
+-- data_intermediate/
|   +-- individual_selected.rds
|   +-- household_selected.rds
|   +-- merge_diagnostics.csv
|
+-- data_analysis/
|   +-- lasi_analysis.rds
|   +-- lasi_analysis.dta
|
+-- code/
|   +-- 00_environment.R
|   +-- 01_inspect_metadata.py
|   +-- 02_extract_individual.py
|   +-- 03_extract_household.py
|   +-- 04_merge.R
|   +-- 05_clean.R
|   +-- 06_construct_outcomes.R
|   +-- 07_descriptives.R
|   +-- 08_models.R
|   +-- 09_interactions.R
|   +-- 10_sensitivity.R
|   +-- 11_figures.R
|   +-- 12_tables.R
|   +-- 13_final_checks.R
|
+-- outputs/
|   +-- tables/
|   +-- figures/
|   +-- model_objects/
|   +-- diagnostics/
|
+-- report/
|   +-- paper.md
|   +-- presentation.pptx
|
+-- README.md
+-- renv.lock             # optional, if using renv
```

Never edit raw `.dta` files manually.

---

# 7. Phase 0 — freeze the protocol before touching results

Create `protocol.md` with:

- research question
- hypotheses
- inclusion/exclusion criteria
- primary exposure definitions
- primary outcome definitions
- primary covariates
- primary model
- interaction specification
- sensitivity analyses
- outcome of interest
- estimand

This reduces the risk of changing the research question after seeing significant results.

---

# 8. Phase 1 — inspect the raw files

## 8.1 Inventory files

Make a list of:

```text
filename
file size
number of observations
number of variables
modification date
```

## 8.2 Inspect metadata

For each `.dta` file extract:

- variable name
- variable label
- value labels
- storage type
- missing-value conventions

Python example:

```python
import pyreadstat

path = "data_raw/individual/LASI_W1_Individual.dta"
_, meta = pyreadstat.read_dta(path, metadataonly=True)

with open("outputs/diagnostics/individual_variables.tsv", "w", encoding="utf-8") as f:
    for name, label in zip(meta.column_names, meta.column_labels):
        f.write(f"{name}\t{label}\n")
```

## 8.3 Search by module/question wording

Do not rely only on column names.

Search:

- variable name
- variable label
- question text in questionnaire

The LASI User Guide states that variables are indexed by module and question number, with the module abbreviation used as the prefix.

---

# 9. Phase 2 — build the master variable specification

Create `variable_map.csv`.

Recommended columns:

```text
construct
role
source_file
module
lasi_variable
question_text
original_codes
clean_codes
reference_category
missing_codes
analysis_use
source
notes
```

Example:

| Construct | Role | LASI variable | Analysis version |
|---|---|---|---|
| Age | covariate/modifier | resolve from DM | continuous + 3 groups |
| Childhood SES | primary exposure | resolve from questionnaire | poor/average/well-off |
| Childhood health | primary exposure | resolve from questionnaire | good vs poor or ordinal sensitivity |
| Childhood bedridden | primary exposure | resolve from questionnaire | no vs yes |
| Cognitive score | primary outcome | resolve from HT | continuous |
| Cognitive impairment | primary outcome | derived | low-tail indicator |
| CES-D | secondary outcome | resolve from HT | score + binary |
| Education | covariate | resolve from DM | categorical/years |
| MPCE | covariate | resolve from HH | quintiles |
| Sex | covariate | resolve from DM | binary/categorical |
| Caste | covariate | resolve from DM | LASI categories |
| Residence | covariate | resolve from DM | rural/urban |
| Marital status | covariate | resolve from DM | married/not |
| Survey weight | survey design | `indiaindividualweight` | national analysis |
| PSU | survey design | exact design variable | survey PSU |
| Stratum | survey design | exact design variable | survey strata |
| HH ID | merge key | `hhid` | household link |
| Person ID | identifier | `prim_key` | respondent key |

**Important:** Exact names for the cognitive/depression/childhood-question variables must be resolved from the actual codebook. Do not invent variable names.

---

# 10. Phase 3 — define the outcomes precisely

## 10.1 Cognitive outcome

LASI cognition includes multiple domains under an HRS-harmonized cognitive module. Published LASI work uses a composite cognitive score and identifies poor cognition using a lower-tail threshold.

Primary analysis:

```text
cognitive_impairment = 1 if score is below the approved LASI cutoff
cognitive_impairment = 0 otherwise
```

Use the exact published/codebook-supported cutoff for the chosen definition.

Secondary outcome:

```text
cognitive_score = continuous composite score
```

This allows sensitivity analysis to determine whether conclusions depend on dichotomizing cognition.

### Do not

Create a new arbitrary cognitive cutoff merely because it produces a convenient prevalence.

## 10.2 Depressive symptoms

Use the LASI 10-item CES-D construction documented in the literature/codebook.

The established Wave 1 analysis uses:

\[
CESD \ge 4 \Rightarrow depressive\ symptoms
\]

and scores range from 0 to 10.

Construct both:

```text
cesd_score
cesd_depression
```

If LASI provides an official derived variable and the corresponding item-level variables, validate that the derived score matches the item reconstruction for a sample/all eligible observations before relying on it.

---

# 11. Phase 4 — define the exposures

## 11.1 Childhood SES

Original LASI response categories:

- Poor
- Average
- Pretty well-off

Primary model:

```text
reference = Pretty well-off
comparison = Average
comparison = Poor
```

Keep the original ordinal version available for sensitivity analysis.

## 11.2 Childhood health

Original responses:

- Very good
- Good
- Fair
- Poor
- Very poor

Primary published-compatible definition:

```text
Good = very good + good + fair
Poor = poor + very poor
```

Sensitivity analysis:

Retain all five ordered categories if sample sizes permit.

## 11.3 Childhood serious illness

Binary indicator:

```text
No = 0
Yes = 1
```

for the LASI question about being bedridden for one month or more before age 16 because of a health problem.

---

# 12. Phase 5 — define age

Maintain exact age if available.

Create:

```text
45-59
60-74
75+
```

Also retain continuous age.

Why both?

- Categories are easy to explain and visualize.
- Continuous age improves information retention.
- Interaction models can use age groups for interpretable presentation.

---

# 13. Phase 6 — choose covariates using a causal framework

Avoid blindly adding every available variable.

## Core demographic adjustment

- age
- sex
- rural/urban residence
- caste
- marital status

## Current socioeconomic adjustment

- education
- MPCE/household economic position

## Health variables

Use primarily as secondary/sensitivity adjustments:

- multimorbidity
- self-rated health
- ADL
- IADL

Reason:

A plausible life-course pathway is:

```text
Childhood disadvantage
        |
        v
Adult educational attainment / socioeconomic position
        |
        v
Adult health
        |
        v
Cognition / depression
```

Some adult health variables may therefore be mediators or downstream variables, not pure confounders. The primary model should not automatically control for all downstream health variables.

---

# 14. Phase 7 — merge the datasets correctly

## 14.1 Start with Individual data

The Individual file is the backbone.

Select only the variables needed for the project.

## 14.2 Prepare Household data

Select:

- `hhid`
- MPCE/consumption measure
- household size if needed to construct an economic measure
- any other pre-approved household covariates

The LASI User Guide states that MPCE is calculated from household consumption divided by household size and that household-level files contain the consumption module.

## 14.3 Validate household key

In the household file:

```text
hhid should be unique
```

In the individual file:

```text
hhid can repeat because several respondents may belong to one household
```

## 14.4 Merge

Conceptually:

```text
individual LEFT JOIN household USING hhid
```

Use a left join so no respondent disappears simply because household data are unavailable.

## 14.5 Report merge diagnostics

After merging, calculate:

```text
N individual before merge
N matched to household
N unmatched individual respondents
N household records with no respondent
```

The IIPS User Guide warns that household-individual merge mismatches occur and reports a national example of unmatched records. Do not assume a perfect 1:1 merge.

---

# 15. Phase 8 — cleaning rules

## 15.1 Never alter raw data

Use immutable raw files and create derived variables.

## 15.2 Convert LASI special missing values correctly

LASI documentation identifies special missing codes for:

- Don't know
- Refused
- Missing
- not asked / ineligible / skip-related statuses

Map them to appropriate analytical missing values only after understanding the original codebook.

## 15.3 Do not recode genuine zero values as missing

Example:

```text
0 diseases
0 income
0 social participation
```

may be valid observations.

## 15.4 Check impossible values

Examples:

```text
age < 45
age > plausible upper range
negative cognitive score
CES-D outside 0-10
invalid education values
invalid exposure codes
weights <= 0
```

Do not delete an observation merely because it is unusual. First compare it to the LASI codebook.

---

# 16. Phase 9 — define analysis samples

Create and save a sample-flow table.

## Sample A: Full eligible sample

```text
Age >= 45
```

Used for demographic descriptions.

## Sample B: Depression analysis

```text
Age >= 45
+ valid childhood exposure(s)
+ valid CES-D outcome
+ valid required covariates
```

## Sample C: Cognition analysis

```text
Age >= 45
+ valid childhood exposure(s)
+ valid cognitive assessment
+ no disqualifying assistance/proxy status according to approved definition
+ valid required covariates
```

Report all N's.

---

# 17. Phase 10 — descriptive analysis

Before regression, understand the dataset.

## Table 1 — Study population

Report weighted percentage and unweighted N for:

- age group
- sex
- residence
- caste
- marital status
- education
- MPCE
- childhood SES
- childhood health
- childhood bedridden status

## Table 2 — Outcome prevalence

For each age group:

- cognitive impairment prevalence
- mean cognitive score
- depressive symptom prevalence
- mean CES-D score

## Cross-tabulations

Examples:

\[
P(Cognition=1|ChildhoodSES)
\]

\[
P(Depression=1|ChildhoodHealth)
\]

Repeat by age group.

---

# 18. Survey-weighted analysis setup

Use national individual weights for national estimates.

In R, conceptual setup:

```r
library(survey)

options(survey.lonely.psu = "adjust")

lasi_design <- svydesign(
  ids = ~psu,
  strata = ~stratum,
  weights = ~indiaindividualweight,
  data = analysis_df,
  nest = TRUE
)
```

**Replace `psu` and `stratum` with the exact LASI design variables identified from the codebook.**

Do not invent them from arbitrary administrative IDs.

---

# 19. Primary regression model

## 19.1 Why not ordinary logistic regression as the main model?

Depressive symptoms may be common enough that odds ratios can overstate the magnitude compared with prevalence ratios. For an easily interpreted cross-sectional study, a modified Poisson model with robust variance is suitable for estimating adjusted prevalence ratios.

## 19.2 Primary model: modified Poisson / prevalence ratio

For binary outcome \(Y\):

\[
\log(E[Y_i]) = \beta_0 + \beta_1 X_i + \beta_2 A_i + \beta_3 C_i + \cdots
\]

Then:

\[
PR = e^{\beta}
\]

with survey-aware variance estimation.

Potential implementation in R should use a survey-compatible generalized linear model and a carefully specified family/link. Validate convergence and the resulting estimand.

## 19.3 Primary model specification

### Model 0

Unadjusted:

```text
Outcome ~ childhood SES
```

### Model 1

Demographic adjustment:

```text
Outcome ~ childhood SES
        + age
        + sex
        + residence
        + caste
        + marital status
```

### Model 2

Add current socioeconomic position:

```text
Outcome ~ childhood SES
        + age
        + sex
        + residence
        + caste
        + marital status
        + education
        + MPCE
```

### Model 3

Secondary health-adjusted model:

```text
Outcome ~ childhood SES
        + demographics
        + current SES
        + multimorbidity
        + SRH
```

Do not call Model 3 a causal model.

Repeat the same structure for childhood health and bedridden history.

---

# 20. Interaction analysis — the project's differentiating analysis

## Objective

Test whether the association between childhood disadvantage and current outcome differs by age group.

Model:

\[
Y \sim ChildhoodSES + AgeGroup + ChildhoodSES\times AgeGroup + Covariates
\]

The key coefficients are the interaction terms.

## Interpretation

Do not interpret an interaction by looking only at a single p-value.

Generate **marginal/predicted prevalences** for every combination:

```text
45-59 × well-off
45-59 × average
45-59 × poor
60-74 × well-off
60-74 × average
60-74 × poor
75+   × well-off
75+   × average
75+   × poor
```

Plot these with 95% confidence intervals.

## Presentation sentence template

> "The adjusted association between childhood socioeconomic status and [outcome] differed across age groups, with the largest/smallest predicted prevalence difference observed in [group]."

Only fill in the direction after seeing the estimates.

---

# 21. Continuous cognition sensitivity model

Binary cognitive impairment discards information.

Therefore run:

\[
CognitiveScore \sim ChildhoodSES + Age + Covariates
\]

using a survey-aware linear regression if assumptions are acceptable.

Inspect:

- residual distribution
- influential observations
- heteroskedasticity
- whether the relationship looks approximately linear

If a bounded/ceiling/floor issue is severe, report this as a limitation rather than building an unnecessarily complex model during the two-week project.

---

# 22. Depression secondary model

Use the CES-D binary outcome for the primary prevalence-ratio analysis.

Optionally also model the score:

\[
CESDScore \sim ChildhoodSES + Age + Covariates
\]

This provides an outcome-definition sensitivity check.

---

# 23. Cumulative childhood disadvantage score — optional secondary analysis

Construct:

```text
Poor childhood SES       = 1
Poor childhood health    = 1
Childhood bedridden      = 1
```

Total:

\[
0,1,2,3
\]

Primary use:

- descriptive dose-response visualization
- trend model

Do not present this as a validated clinical index. It is an **exploratory composite** created for this project.

---

# 24. Sensitivity analyses

Keep the set small and purposeful.

## Sensitivity 1 — Exposure coding

Compare binary childhood health coding with the original ordered five categories.

## Sensitivity 2 — Outcome coding

Compare binary cognitive impairment with continuous cognitive score.

## Sensitivity 3 — Adult health adjustment

Add multimorbidity and SRH to determine whether the childhood association is attenuated.

## Sensitivity 4 — Complete-case vs simpler covariate set

Check whether the main estimate changes mainly because of sample loss from missing covariates.

## Sensitivity 5 — Logistic regression

Run survey-weighted logistic regression as a secondary analysis to provide AORs for comparability with prior studies. Do not mix OR and PR interpretation.

---

# 25. Missing-data strategy

The first choice for a two-week project is **transparent complete-case analysis for the pre-specified primary model**, provided missingness is not extreme.

But first quantify missingness.

Create:

```text
variable
N missing
percent missing
reason/status if available
```

For the primary exposure/outcome/covariates, report missingness explicitly.

If a key variable has substantial missingness, stop and decide whether:

1. complete-case analysis is acceptable;
2. a published LASI-derived variable can reduce missingness;
3. a missing category is scientifically defensible;
4. multiple imputation is feasible.

Do not implement multiple imputation merely to make the sample larger within a two-week window unless the team already knows the method well.

---

# 26. Data-quality checks before any results are trusted

Create an automated checklist.

### IDs

```text
prim_key unique in individual data
hhid unique in household data
no duplicated respondent rows
```

### Age

```text
all analysis observations age >= 45
```

### Outcomes

```text
CES-D within expected range
cognitive score within documented range
binary indicators are 0/1
```

### Exposure

```text
all categories documented
no accidental conversion of special missing values to real categories
```

### Weights

```text
weight present
weight > 0 for analysis observations
```

### Survey design

```text
PSU nonmissing
stratum nonmissing
```

### Merge

```text
merge does not duplicate respondents
merge loss is documented
```

---

# 27. Descriptive plots that make the project presentable

## Figure 1 — Age distribution

Histogram or weighted age-group distribution.

## Figure 2 — Childhood disadvantage distribution

Weighted prevalence of:

- poor childhood SES
- poor childhood health
- childhood bedridden history

## Figure 3 — Outcome prevalence by age

Two panels or separate figures:

- cognitive impairment by age group
- depressive symptoms by age group

## Figure 4 — Primary interaction figure

Predicted probability/prevalence of cognitive impairment by childhood SES across age groups.

## Figure 5 — Secondary interaction figure

Predicted prevalence of depressive symptoms by childhood SES across age groups.

Use confidence intervals and clear reference labels.

---

# 28. Presentation-quality regression tables

Do not dump raw statistical software output into the report.

Create tables with:

```text
Exposure
Reference category
Adjusted PR / OR
95% CI
p-value
N
```

For example:

| Exposure | Adjusted PR | 95% CI | p-value |
|---|---:|---:|---:|
| Childhood SES: Average vs well-off | ... | ... | ... |
| Childhood SES: Poor vs well-off | ... | ... | ... |
| Childhood health: Poor vs good | ... | ... | ... |
| Bedridden: Yes vs no | ... | ... | ... |

Never manufacture placeholder numerical estimates in the final report.

---

# 29. Recommended final results structure

## Table 1
Weighted characteristics of the analytical sample.

## Table 2
Weighted prevalence of cognitive impairment and depressive symptoms across childhood conditions.

## Table 3
Adjusted association of childhood conditions with cognitive impairment.

## Table 4
Adjusted association of childhood conditions with depressive symptoms.

## Table 5
Age-interaction models / marginal predictions.

## Figure 1
Distribution of childhood disadvantage.

## Figure 2
Outcome prevalence across age groups.

## Figure 3
Adjusted predicted cognitive impairment by age and childhood SES.

## Figure 4
Adjusted predicted depressive symptoms by age and childhood SES.

---

# 30. Statistical interpretation rules

## PR interpretation

If:

\[
PR=1.25
\]

say:

> The estimated prevalence was 25% higher in the comparison group, conditional on the variables in the model.

Do not say:

> "The exposure increases the risk by 25%."

unless the study design and estimand support such language.

## Confidence interval

A 95% confidence interval gives a range of estimates compatible with the model/data under the stated assumptions.

Example:

\[
PR=1.25\;(95\%\ CI:1.10-1.42)
\]

## P-value

Use it as supporting evidence, not as the sole criterion for scientific importance.

Report effect size and uncertainty first.

---

# 31. Causal language policy

The correct verbs for this project are:

- associated with
- correlated with
- related to
- differed by
- showed higher/lower prevalence
- was statistically compatible with

Avoid:

- caused
- led to
- resulted in
- increased the risk
- reduced the risk
- prevented

unless a separate causal design justifies the statement.

The study is cross-sectional at Wave 1 even though LASI is designed as a longitudinal study.

---

# 32. Potential biases to acknowledge

## 32.1 Recall bias

Childhood variables are retrospective self-reports from adults who may be 45–90+ years old. Memories may be incomplete or influenced by current circumstances.

## 32.2 Reverse interpretation problem

Current health is measured at the same time as the outcomes, so direction cannot be established from Wave 1 alone.

## 32.3 Cohort effects

Older and younger respondents were born in different periods. An age-group difference may reflect historical cohort differences rather than biological ageing alone.

## 32.4 Survivor bias

People who survive to older ages may differ systematically from those who died earlier.

## 32.5 Proxy interviews and missing cognition

LASI notes that proxy interviews do not contain cognitive tests, psychosocial questions or experimental modules. This creates structurally missing cognition data for some respondents.

## 32.6 Residual confounding

Not every determinant of later-life cognitive/mental health is measured or perfectly controlled.

---

# 33. Why the analysis remains an ageing study despite cross-sectional data

We are not claiming individual trajectories.

Instead, we study the distribution of outcomes across **stages of later life** and whether the association with early-life conditions differs across those stages.

The wording should therefore be:

> "age-patterned" or "age-graded"

rather than:

> "longitudinal decline"

unless a later wave is added.

---

# 34. Reproducibility pipeline

Every result in the report should be generated from code.

The workflow should be:

```text
RAW DATA
   |
   v
METADATA INSPECTION
   |
   v
VARIABLE MAP
   |
   v
SELECT VARIABLES
   |
   v
MERGE
   |
   v
CLEAN
   |
   v
CONSTRUCT VARIABLES
   |
   v
DEFINE ANALYSIS SAMPLES
   |
   v
SURVEY DESIGN
   |
   v
DESCRIPTIVES
   |
   v
REGRESSION
   |
   v
INTERACTIONS
   |
   v
SENSITIVITY
   |
   v
TABLES + FIGURES
   |
   v
REPORT
```

No result should be manually copied from the console into the report.

---

# 35. Suggested R package setup

```r
install.packages(c(
  "haven",
  "dplyr",
  "tidyr",
  "survey",
  "broom",
  "ggplot2",
  "marginaleffects",
  "tableone",
  "gt",
  "readr"
))
```

Useful roles:

- `haven` — read/write Stata files.
- `dplyr` — data manipulation.
- `tidyr` — reshaping.
- `survey` — complex survey design and inference.
- `ggplot2` — figures.
- `marginaleffects` — predicted values/contrasts; verify compatibility with the fitted survey model before using it for final estimates.
- `gt` — presentation tables.

---

# 36. Example R cleaning skeleton

```r
library(haven)
library(dplyr)

ind <- read_dta("data_raw/individual/LASI_W1_Individual.dta")
hh  <- read_dta("data_raw/household/LASI_W1_HH.dta")

# Keep only approved variables after exact names are confirmed.
ind_small <- ind %>%
  select(
    prim_key,
    hhid,
    # age, sex, childhood variables, cognition, CES-D, etc.
    indiaindividualweight,
    psu,
    stratum
  )

hh_small <- hh %>%
  select(
    hhid,
    # MPCE / other approved household variables
  )

analysis <- ind_small %>%
  left_join(hh_small, by = "hhid")
```

The placeholders above are intentional. Replace them only after confirming the actual LASI variable names.

---

# 37. Constructing the depression score

If using item-level CES-D variables rather than an official derived score:

1. Identify the ten questions from the questionnaire.
2. Confirm the response coding.
3. Convert response categories to the published 0/1 scheme.
4. Reverse-code the appropriate positive-affect items.
5. Sum the ten items.
6. Verify the range is 0–10.
7. Compare your reconstruction with any LASI-provided derived CES-D variable on respondents where both are available.
8. Save a validation table.

Example validation:

```text
N compared
% exact match
mean difference
max absolute difference
```

Only after validation should the derived score be used.

---

# 38. Constructing cognition

Preferred order:

1. Identify the LASI cognitive composite score if officially provided.
2. Verify how the published LASI literature defines cognitive impairment.
3. Check whether the data include respondent-assistance/proxy indicators.
4. Apply the published/codebook-supported eligibility rule.
5. Create `cognitive_score`.
6. Create `cognitive_impairment`.
7. Report the number excluded because cognition was not administered/valid.

Do not infer that missing cognition equals poor cognition.

---

# 39. Interaction result presentation

An interaction coefficient can be difficult for beginners to interpret.

Therefore report both:

### Regression interaction

```text
Childhood SES × Age group
```

and:

### Marginal predictions

For each age × childhood SES combination:

```text
estimated prevalence
95% CI
```

The marginal predictions are the primary communication tool for the presentation.

---

# 40. Minimum acceptable final analysis

If time becomes tight, the minimum scientifically complete analysis is:

1. Clean national Individual dataset.
2. Merge household MPCE if necessary.
3. Create childhood SES.
4. Create childhood health.
5. Create childhood bedridden indicator.
6. Create cognitive impairment.
7. Create CES-D depression indicator.
8. Create age groups.
9. Set survey design.
10. Produce weighted descriptive Table 1.
11. Produce weighted outcome prevalence.
12. Fit adjusted cognitive PR models.
13. Fit adjusted depression PR models.
14. Fit one age-interaction model for cognition.
15. Fit one age-interaction model for depression.
16. Produce two predicted-probability figures.
17. Run two or three targeted sensitivity analyses.
18. Write limitations and reproducibility documentation.

Do not sacrifice correct survey inference to add more exotic analyses.

---

# 41. 14-day execution schedule

## Day 1 — Project setup

**Morning**

- Freeze question and hypotheses.
- Create project directory.
- Save documentation.
- Install R/Python packages.

**Afternoon**

- Inventory every `.dta` file.
- Extract variable metadata.
- Identify Individual and Household files.

**Deliverable:** `variable_inventory.tsv`

---

## Day 2 — Variable mapping

**Morning**

- Read questionnaire sections.
- Identify childhood questions.
- Identify cognition variables.
- Identify CES-D variables.

**Afternoon**

- Identify age, sex, education, MPCE, caste, residence, marital status.
- Identify individual weight, PSU and strata.

**Deliverable:** `variable_map.csv` version 1.

---

## Day 3 — Data extraction

- Read only required variables.
- Save intermediate individual file.
- Save intermediate household file.
- Check row counts.
- Check key uniqueness.

**Deliverable:** `individual_selected.rds`, `household_selected.rds`.

---

## Day 4 — Merge and cleaning

- Merge on `hhid`.
- Produce merge diagnostics.
- Recode special missing values.
- Check all major variables.

**Deliverable:** `lasi_merged_clean.rds`.

---

## Day 5 — Outcomes and exposures

- Construct childhood SES.
- Construct childhood health.
- Construct bedridden indicator.
- Construct CES-D score.
- Construct depression.
- Construct cognition.
- Construct cognitive impairment.

**Deliverable:** validated outcome/exposure variables.

---

## Day 6 — Sample construction

- Define full 45+ sample.
- Define depression analysis sample.
- Define cognition analysis sample.
- Document exclusions.
- Produce missingness table.

**Deliverable:** sample-flow table.

---

## Day 7 — Survey design + descriptives

- Configure weights, PSU, strata.
- Verify weighted estimates behave sensibly.
- Produce Table 1.
- Produce outcome prevalence table.

**Checkpoint:** No regression until this checkpoint passes.

---

## Day 8 — Primary regression

Run:

- childhood SES → cognition
- childhood health → cognition
- bedridden → cognition
- childhood SES → depression
- childhood health → depression
- bedridden → depression

Save model objects.

---

## Day 9 — Adjusted models

- Model 1 demographic adjustment.
- Model 2 adult SES adjustment.
- Compare effect estimates across models.

Interpret attenuation carefully.

---

## Day 10 — Interaction models

- Childhood SES × age group.
- Childhood health × age group.
- Select the prespecified primary interaction.
- Compute adjusted predictions.

---

## Day 11 — Sensitivity analyses

Run:

- continuous cognition
- ordered childhood-health categories
- adult-health-adjusted model
- secondary logistic model

Stop adding analyses after the prespecified set is complete.

---

## Day 12 — Figures and tables

Produce publication-style versions of:

- Table 1
- regression tables
- outcome prevalence figure
- main interaction figure
- secondary interaction figure

---

## Day 13 — Writing

Write:

- Introduction
- Methods
- Results
- Discussion
- Limitations
- Conclusion

Do not write causal language.

---

## Day 14 — Quality assurance

### Re-run everything from raw data

The entire pipeline should run from scripts without manual edits.

Check:

- N's
- weights
- merge diagnostics
- estimates
- confidence intervals
- table numbers
- figure labels
- references
- terminology
- cross-sectional limitation

Prepare the final report and presentation.

---

# 42. Final report structure

## Title page

Title, team, course/project, date.

## Abstract

Use:

```text
Background
Methods
Results
Conclusion
```

## 1. Introduction

- ageing in India
- life-course perspective
- early-life disadvantage
- why cognition/depression matter
- research gap
- objectives

## 2. Methods

- study design
- data source
- sampling
- study population
- variables
- survey weighting
- statistical models
- interaction analysis
- sensitivity analyses

## 3. Results

- sample characteristics
- exposure distributions
- outcome prevalence
- regression estimates
- interactions
- sensitivity analyses

## 4. Discussion

- main findings
- possible mechanisms
- comparison with previous studies
- interpretation of age heterogeneity
- implications

## 5. Limitations

- cross-sectional design
- recall bias
- cohort effects
- survivor bias
- residual confounding
- missing cognition/proxy interviews

## 6. Conclusion

One short evidence-based paragraph.

## Appendix

- variable map
- sample flow
- additional model output
- codebook-derived coding details
- reproducibility instructions

---

# 43. Suggested presentation flow

## Slide 1 — Problem

India is ageing; later-life mental and cognitive health is unequally distributed.

## Slide 2 — Research gap

Early-life circumstances may persist into later life, but Wave 1 allows us to investigate age-patterned associations.

## Slide 3 — Research question

State the exact question.

## Slide 4 — Data

LASI Wave 1, national sample, 45+.

## Slide 5 — Conceptual framework

```text
Childhood disadvantage
        ↓
Life-course accumulation
        ↓
Current cognitive / mental health
        ↑
Age group as effect modifier
```

## Slide 6 — Variables

Exposures, outcomes, covariates, survey design variables.

## Slide 7 — Methods

Weighted prevalence + modified Poisson + interaction.

## Slide 8 — Sample flow

Show the actual N after each exclusion.

## Slide 9 — Descriptive results

Key prevalence differences.

## Slide 10 — Main regression results

Forest plot or compact table.

## Slide 11 — Interaction

Main predicted-prevalence graph.

## Slide 12 — Sensitivity analysis

Show whether conclusions are stable.

## Slide 13 — Limitations

Be explicit about cross-sectional design.

## Slide 14 — Conclusion

Three key findings + one public-health implication.

---

# 44. What counts as a strong result

A strong project does **not** require every hypothesis to be significant.

A strong result has:

- clearly defined variables;
- correct survey weighting;
- appropriate uncertainty estimates;
- effect sizes with confidence intervals;
- a meaningful age interaction or clear evidence that it is not present;
- sensitivity checks;
- transparent limitations;
- conclusions that match the design.

A null result can be scientifically useful if the analysis is correctly specified.

---

# 45. Decision tree for common problems

## Problem: cognitive sample unexpectedly small

Check:

1. proxy status;
2. cognitive-module eligibility;
3. external assistance indicator;
4. missing codes;
5. accidental use of a household rather than individual file.

## Problem: household merge loses many respondents

Check:

1. `hhid` format/type;
2. whitespace/string vs numeric conversion;
3. duplicate household IDs;
4. whether both files are from the same LASI release;
5. unmatched respondent households.

## Problem: weighted prevalence is strange

Check:

1. correct individual weight;
2. correct survey unit;
3. weight missingness;
4. PSU/stratum variables;
5. whether household weights were mistakenly applied to individuals.

## Problem: regression will not converge

Check:

1. sparse categories;
2. empty age × exposure combinations;
3. perfect separation;
4. invalid missing-value recoding;
5. extreme weights;
6. over-specified model.

Do not immediately switch methods because a result is inconvenient.

---

# 46. Final checklist before submission

### Dataset

- [ ] Individual file verified.
- [ ] Household file verified.
- [ ] Same LASI Wave 1 release.
- [ ] IDs checked.

### Variables

- [ ] Childhood SES verified.
- [ ] Childhood health verified.
- [ ] Bedridden variable verified.
- [ ] Cognition verified.
- [ ] CES-D verified.
- [ ] Age verified.
- [ ] Covariates verified.
- [ ] Survey variables verified.

### Statistics

- [ ] National individual weight used.
- [ ] PSU used.
- [ ] Strata used.
- [ ] Survey-aware SEs used.
- [ ] Primary model prespecified.
- [ ] Interaction modeled correctly.
- [ ] Marginal predictions generated.

### Quality

- [ ] Missing codes handled.
- [ ] No duplicates.
- [ ] Merge diagnostics saved.
- [ ] Sample-flow N's consistent.
- [ ] Results reproducible.

### Interpretation

- [ ] No causal claims from Wave 1.
- [ ] Cohort effects discussed.
- [ ] Recall bias discussed.
- [ ] Proxy/cognitive missingness discussed.
- [ ] OR and PR not conflated.

### Presentation

- [ ] Main research question appears early.
- [ ] One clear conceptual figure.
- [ ] One clear main-results figure.
- [ ] Tables contain effect sizes + 95% CIs.
- [ ] Conclusion matches evidence.

---

# 47. Recommended immediate next step

Before writing a single regression command, obtain the **exact Individual-file variable names and labels** for:

```text
Age
Childhood SES
Childhood health
Childhood bedridden history
Cognitive assessment / composite score
Cognitive eligibility / assistance / proxy status
CES-D items or derived score
Sex
Education
Caste
Marital status
Rural/urban
Household ID
Individual ID
Individual weight
PSU
Stratum
```

Then obtain the household variables needed for current economic status and confirm the merge key.

Once those names are frozen, create `variable_map.csv` and only then begin the cleaning and analysis scripts.

---

# 48. Key source notes from the LASI User Guide

The IIPS Wave 1 User Guide states that LASI is a multidisciplinary panel study of 73,396 adults aged 45+ and their spouses, representative of India and its states/UTs. It describes the study as covering demographics, household economic status, chronic and symptom-based conditions, functional health, cognition/depression, biomarkers, insurance/healthcare, family/social networks, social welfare, work/employment, retirement and life expectations.

It documents a multistage stratified area-probability sampling design and notes that individuals aged 65+ were oversampled. It also provides the individual and household sample weights.

The guide states that `hhid` uniquely identifies a household and `prim_key` uniquely identifies an individual, and that datasets can be merged using `prim_key`, `hhid`, or `ssuid` as appropriate.

The guide explicitly notes that proxy interviews do not include cognitive tests, psychosocial questions, biomarkers or experimental modules. This must be reflected in the cognitive analytical sample definition.

The guide also states that LASI uses special missing-value codes and that national individual estimates should use `indiaindividualweight`.

These facts should be cited to the IIPS User Guide in the final report.

---

# 49. Final analytical philosophy

Keep the project narrow enough to finish correctly.

The ideal final product is **not** the one containing the largest number of models. It is the one where every stage is defensible:

```text
Well-defined question
        ↓
Correct LASI files
        ↓
Verified variable coding
        ↓
Transparent cleaning
        ↓
Correct survey design
        ↓
Simple primary model
        ↓
Meaningful interaction
        ↓
Targeted sensitivity checks
        ↓
Clear figures
        ↓
Careful interpretation
```

The strongest presentation message should be:

> **Early-life disadvantage is measurable in LASI, later-life cognitive and mental-health outcomes are measurable in LASI, and Wave 1 allows us to test whether these associations vary across stages of later life—while explicitly recognizing that the evidence is cross-sectional rather than longitudinal change.**

