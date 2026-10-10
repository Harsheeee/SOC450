# Cognitive Sensitivity Analysis Plan

**Goal:** Conduct the primary cognitive sensitivity analysis as a separate, reproducible extension of the existing workflow, focusing on continuous cognitive scores across domains.

## 1. Research Question
Does the association between recalled childhood socioeconomic disadvantage and later-life measured cognitive performance differ across memory, orientation, and the combined memory-orientation score, under defensible scoring rules?

## 2. Outcomes & Scoring Rules
We will model three continuous cognitive outcomes that were administered to all direct respondents without differential skip logic based on education:
1. `memory_score` (0-20 points): Sum of immediate and delayed 10-word recall.
2. `orientation_score` (0-8 points): Sum of temporal and spatial orientation items.
3. `mem_orient` (0-28 points): Sum of the memory and orientation scores.

*Feasibility Limitation:* We will intentionally exclude the "broad cognitive battery" (`battery_pct`) from the main estimation because, as documented in previous reviews, its administration rules skipped items for uneducated adults. Creating a common cognitive score without a defensible common scoring basis is invalid.

## 3. Sample
The analysis uses the same complete-case analytical sample derived for the primary cognition models (`table_s0_common_samples.csv` logic). To ensure comparability, we will filter for respondents with non-missing data across all relevant adult SES and health confounders.

## 4. Exposures
- `childhood_ses_3cat` (Poor, Middle, Pretty well-off)
- `childhood_health_poor_original` (Poor/Very poor vs. Rest)
- `childhood_bedridden` (Yes vs. No)

## 5. Models (Linear Regressions)
We will run continuous linear regressions using survey weights:
- **Model A (Baseline):** Adjusts for age, sex, caste, religion, residence, and state fixed effects.
- **Model B (Adult-SES Adjusted):** Adds adult educational attainment and MPCE quintile.
- **Model C (Health Adjusted - Exploratory):** Adds ADL limitations, self-rated health, and morbidity.

## 6. Survey Design
We will use the custom `svy_glm` Taylor-linearization estimator with `family='gaussian'` and normalized survey weights, clustered at the PSU (`ssuid`) level and stratified by `stratum`. Effect estimates (betas) will be reported unexponentiated with 95% confidence intervals and exact p-values.

## 7. Execution Plan
1. Ensure the `extension/` directory exists.
2. Write a Python script (`extension/01_cognitive_sensitivity.py`) that loads `lasi_clean_v2.parquet`, applies the complete-case mask, and runs the models for the continuous outcomes.
3. Output the results as formatted tables in `extension/`.
4. The script will explicitly document sample sizes, scoring ranges, and missingness.
