# Study Protocol: Pre-Specified Analysis Plan

## Project Title
**Early-Life Disadvantage and Later-Life Mental and Cognitive Health in India: Evidence from LASI Wave 1**

---

## 1. Research Questions & Hypotheses

### Primary Research Question
Among Indian adults aged 45 years and above, are adverse childhood socioeconomic and health conditions associated with poorer cognitive performance in later life, and does the magnitude of this association differ across age groups?

### Secondary Research Question
Are adverse childhood socioeconomic and health conditions associated with depressive symptoms, and do the age patterns look similar for depressive and cognitive outcomes?

### Core Pre-Specified Hypotheses
1. **Hypothesis 1 (Childhood SES):** Lower perceived childhood family socioeconomic status (Poor / Average vs. Pretty well-off) is associated with poorer later-life cognitive performance and higher prevalence of depressive symptoms.
2. **Hypothesis 2 (Childhood Health):** Poorer reported childhood health (Fair / Poor / Very poor vs. Good / Very good) is associated with poorer cognitive performance and elevated depressive symptoms.
3. **Hypothesis 3 (Childhood Bedridden / Serious Illness):** Having been bedridden for at least one month before age 16 due to health problems is associated with poorer cognitive performance and elevated depressive symptoms.
4. **Hypothesis 4 (Age Heterogeneity / Effect Modification):** The association between childhood disadvantage and cognitive/mental health outcomes differs across age groups (45–59, 60–74, 75+).
5. **Hypothesis 5 (Life-Course Attenuation):** Associations will attenuate after sequential adjustment for adult socioeconomic attainment (education and household MPCE), consistent with life-course socioeconomic accumulation pathways.

---

## 2. Non-Negotiable Methodological Guardrails
- **Cross-Sectional Baseline:** LASI Wave 1 is a cross-sectional baseline for this study. The analysis estimates cross-sectional associations and age-graded heterogeneity across cohort strata; it **cannot** estimate within-individual longitudinal decline, incidence, or causal effects over time.
- **Language Policy:** All reporting must strictly use non-causal associative phrasing (*"associated with"*, *"correlated with"*, *"prevalence ratio"*), never causal phrasing (*"caused"*, *"led to"*, *"increased risk of"*).

---

## 3. Inclusion & Exclusion Criteria

### Target Study Population
- All individuals in LASI Wave 1 residing in India aged **45 years and above** (`dm005 >= 45`).

### Exclusions
1. **Spouses aged < 45:** Excluded from the primary ageing analysis (N = 6,790).
2. **Proxy Interviews:** Direct cognitive test questions were omitted for proxy interviews per LASI protocol (`rproxy == 1`, N = 705). Excluded from direct cognitive assessment analysis.
3. **Missing Data Handling:** Transparent complete-case analysis for pre-specified primary models, with formal documentation of sample flow and item missingness.

---

## 4. Exposure Definitions

1. **Childhood Socioeconomic Status (SES):**
   - Survey Question: `ht235` (*Financial status of family during childhood up to age 16*)
   - Categories:
     - `1`: Pretty well-off financially (Reference group)
     - `2`: Average
     - `3`: Poor
     - `4`: Varied (Voluntary category, evaluated or combined with Average/Poor in sensitivity analysis)

2. **Childhood Health:**
   - Survey Question: `ht231` (*Status of childhood health up to age 16*)
   - Primary Binary Specification:
     - `Good` (Reference): Very good (1) + Good (2)
     - `Poor`: Fair (3) + Poor (4) + Very poor (5)
   - Secondary Sensitivity Specification: Ordered 5-level categorical variable (1 Very good to 5 Very poor).

3. **Childhood Serious Illness (Bedridden):**
   - Survey Question: `ht233` (*Ever bedridden for a month or more during childhood before age 16*)
   - Coding: `0 = No` (Reference), `1 = Yes`.

4. **Parental Education (Secondary / Sensitivity):**
   - Father schooling / attainment (`fs306`, `fs308`)
   - Mother schooling / attainment (`fs315`, `fs317`)

---

## 5. Outcome Definitions

1. **Cognitive Performance:**
   - **Primary Outcome:** Continuous composite cognitive score combining:
     - Immediate word recall (0–10 words, `mh012`)
     - Delayed word recall (0–10 words, `mh056`)
     - Orientation domain (Date, month, year, day, place, village, landmark, district: 0–8 points, `mh002`–`mh009`)
     - Arithmetic / Serial 7s (0–5 points, `mh045`)
     - Verbal fluency (count of animals named, `mh016_correct`)
     - Executive function / Object naming (`mh019`, `mh020`, `mh051`)
   - **Secondary Binary Outcome:** Cognitive impairment indicator defined using the lowest 10th percentile / literature-established lower-tail cut-off of the composite cognitive score.

2. **Depressive Symptoms:**
   - **Scale:** 10-item Center for Epidemiologic Studies Depression (CES-D) short scale (`fs701`–`fs710`).
   - Items:
     - Negative affect (7 items): Trouble concentrating (`fs701`), Depressed (`fs702`), Low energy/tired (`fs703`), Afraid (`fs704`), Alone/lonely (`fs706`), Bothered (`fs707`), Everything an effort (`fs708`).
     - Positive affect (3 items, reverse-coded): Overall satisfied (`fs705`), Hopeful about future (`fs709`), Happy (`fs710`).
   - Scoring: Items scored 0/1 based on symptom frequency, yielding a total score from 0 to 10.
   - **Secondary Primary Outcome:** Binary depressive symptom indicator ($\text{CES-D} \ge 4$).
   - **Sensitivity Outcome:** Continuous CES-D score (0–10).

---

## 6. Covariates

### Core Demographic Adjustments (Model 1)
- **Age:** Continuous age (`dm005`) and age strata (45–59, 60–74, 75+).
- **Sex:** Male vs. Female (`dm003`).
- **Place of Residence:** Rural vs. Urban (`residence`).
- **Social Group / Caste:** Scheduled Caste (SC), Scheduled Tribe (ST), Other Backward Class (OBC), None/General (`dm013`).
- **Marital Status:** Currently Married vs. Not Currently Married (Widowed, Divorced/Separated, Never Married) (`dm021`).

### Adult Socioeconomic Attainment (Model 2)
- **Educational Attainment:** Derived from `dm006` (Ever attended school) and `dm008` (Highest educational level completed):
  - 0: No formal education
  - 1: Less than primary (Standards 1–4)
  - 2: Primary completed (Standards 5–7)
  - 3: Middle completed (Standards 8–9)
  - 4: Secondary / Matriculation (Standard 10)
  - 5: Higher secondary / Diploma
  - 6: Graduate degree & above
- **Household Economic Status:** Monthly Per Capita Consumption Expenditure (MPCE) quintile (`mpce_quintile`: 1 Poorest to 5 Richest).

### Adult Health Status (Model 3 - Exploratory / Downstream Pathway)
- **Multimorbidity Count / Chronic Conditions:** Diagnosed hypertension (`ht002`), diabetes (`ht003`), chronic lung disease (`ht005`), chronic heart disease (`ht006`), stroke (`ht007`).
- **Self-Rated Health (SRH):** General health rating (`ht001_a`).

---

## 7. Statistical Models & Estimands

### Survey Design Specification
All point estimates, standard errors, and confidence intervals will account for the multistage stratified cluster sampling design:
- **Sampling Weight:** National individual sampling weight (`indiaindividualweight`).
- **Clustering / PSU:** Secondary Sampling Unit (`ssuid`, 2,439 clusters).
- **Strata:** State $\times$ Residence (`stateid` $\times$ `residence`, 72 strata).

### Modeling Strategy
1. **Model 0 (Unadjusted):** Outcome $\sim$ Childhood Exposure.
2. **Model 1 (Demographic Adjustment):** Outcome $\sim$ Childhood Exposure + Age + Sex + Residence + Caste + Marital Status.
3. **Model 2 (Adult SES Adjustment - Primary Model):** Model 1 + Educational Attainment + Household MPCE Quintile.
4. **Model 3 (Adult Health Adjustment - Pathway Model):** Model 2 + Chronic Conditions + Self-Rated Health.

### Model Families & Estimands
- **Continuous Cognitive Score:** Survey-weighted Linear Ordinary Least Squares (OLS) regression with design-consistent robust standard errors. Estimand: Mean difference ($\beta$).
- **Binary Outcomes (Depression $\ge 4$, Cognitive Impairment):** Survey-weighted modified Poisson regression with robust variance estimators to compute adjusted **Prevalence Ratios (PR)** and 95% Confidence Intervals.
- **Sensitivity:** Survey-weighted Logistic Regression to estimate Adjusted Odds Ratios (AOR) for comparison with earlier literature.

---

## 8. Interaction / Effect-Modification Plan

To test whether the association between childhood disadvantage and later-life health varies across ageing stages, an interaction term between each childhood exposure and the three age groups will be fitted:
$$\text{Outcome} \sim \text{Childhood Exposure} \times \text{Age Group} + \text{Covariates}$$

### Interpretation & Reporting of Interactions:
- Do not rely solely on interaction $p$-values.
- Compute and plot **adjusted marginal predicted values / prevalences** with 95% confidence intervals across all combinations:
  - 45–59 $\times$ Well-off, Average, Poor
  - 60–74 $\times$ Well-off, Average, Poor
  - 75+ $\times$ Well-off, Average, Poor

---

## 9. Pre-Specified Sensitivity Analyses
1. **Exposure Coding:** Retain full 5-level ordered childhood health response instead of binary collapse.
2. **Outcome Metric:** Compare binary cognitive impairment against continuous cognitive composite score.
3. **Cumulative Childhood Disadvantage Score:** Exploratory 0–3 sum index (Poor SES = 1, Poor Health = 1, Bedridden = 1) to test dose-response relationships.
4. **Adult Health Pathways:** Evaluate attenuation when adult multimorbidity and SRH are introduced into Model 3.
5. **Logistic vs. Poisson:** Compare Adjusted Prevalence Ratios (PR) with Adjusted Odds Ratios (AOR) from logistic regression.

---

## 10. Sample Flow Architecture
- **Sample A (Full Eligible Sample):** All respondents aged $\ge 45$ (`dm005 >= 45`, N = 66,606). Used for population description.
- **Sample B (Depression Sample):** Age $\ge 45$ + valid childhood exposures + complete 10-item CES-D + complete covariates.
- **Sample C (Cognition Sample):** Age $\ge 45$ + direct interview (`rproxy == 0`) + valid childhood exposures + complete cognitive assessment + complete covariates.

---

## 11. Documentation, Checkpoints & Progress Tracking Protocol
To ensure rigorous research continuity, transparency, and reproducibility across pair programming sessions:
- **Mandatory Living Document:** A dedicated file named `checkpoints.md` must be maintained at the workspace root.
- **Update Frequency:** `checkpoints.md` must be updated immediately after every significant analytical or engineering milestone (e.g., dataset extraction, descriptive output, model fitting, sensitivity checks, manuscript drafting).
- **Required Checkpoint Elements:**
  1. **Current Active Checkpoint:** Clear indication of current project state.
  2. **Completed Milestones Log:** Date, phase, exact operations performed, and validation results.
  3. **Key Scientific Achievements:** Effect sizes, prevalence estimates, and key substantive takeaways.
  4. **File & Artifact Registry:** Precise relative/absolute paths to all code scripts, data files, outputs, figures, and tables.
  5. **Next Starting Point:** Actionable step-by-step guidance on exactly where the next analytical session should begin.


---

## 12. Protocol Amendment 1 (dated 2026-10-05) — Post-Audit Corrections

The original protocol (Sections 1–11) is retained unchanged. A post-hoc audit found flaws; the following are **transparent deviations**, not original pre-specifications. All original ("v1") results remain on file and are reported as "original specification".

| # | Change | Reason |
|---|---|---|
| A1 | Primary cognitive outcome becomes **memory (immediate + delayed recall) + orientation, 0–28**; binary = lowest weighted decile. Full 43-pt battery (skip-aware: skipped items missing, not 0) and the original v1 composite move to sensitivity. | v1 composite scored literacy-dependent skipped items as 0, making it a schooling proxy. |
| A2 | Impairment cut-off = **survey-weighted** 10th percentile in the analytic sample; sensitivity with schooling-stratum-specific cut-offs. | v1 cut-off was unweighted and pooled. |
| A3 | Orientation requires all 8 items (no partial-credit sums); `mh045` values >5 set to missing; caste "Other" retained as a category. | Data-cleaning errors. |
| A4 | Models M0–M3 fitted on **one common complete-case sample** per outcome/exposure; **state fixed effects** added from Model 1. | Comparability of attenuation; regional confounding. |
| A5 | Survey variance uses stratified cluster linearization (72 strata, 2,439 `ssuid` clusters). | v1 ignored strata. |
| A6 | Mutually adjusted model of all childhood exposures added. | v1 claims of "independent" association. |
| A7 | Interaction: continuous age retained; **joint Wald test** and average-marginal-standardized predictions replace single-profile predictions. | v1 Table 5 profile was unrepresentative; no test performed. |
| A8 | Inverse-probability weighting for missing cognition scores (complete-case kept as comparison). | Informative missingness. |
| A9 | Reporting: associational language only; mechanisms labelled speculative; Hypothesis 4 judged by joint test. | Guardrail §2 breach in v1 report. |
