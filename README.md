# Life-Course Disadvantage and Late-Life Cognitive and Mental Health in India

## Replication Codebase and Empirical Analysis
**Course:** SOC450 - Sociology of Ageing  
**Institution:** Indian Institute of Technology Kanpur (IIT Kanpur)  
**Primary Report:** `report.pdf` (45 pages, full research report)

---

## 1. Project Overview and Executive Summary

This repository contains the complete empirical analysis and replication pipeline for investigating the relationship between childhood disadvantage and later-life cognitive impairment and depressive symptoms among older Indian adults, using data from the Longitudinal Ageing Study in India (LASI Wave 1, 2017-2018).

### 1.1 Research Questions
1. To what extent do early-life disadvantages (perceived childhood socioeconomic status, poor childhood self-rated health, and childhood bedridden status for >= 1 month) predict late-life cognitive impairment and depressive symptoms among Indian adults aged 45 and older?
2. Does adult socioeconomic attainment (educational attainment and per-capita household consumption expenditure) mediate or attenuate these early-life associations?
3. Does the association between childhood disadvantage and late-life health outcomes vary across age cohorts (45-59, 60-74, and 75+ years), testing the competing theoretical models of Cumulative Advantage/Disadvantage (divergence) versus Age-as-Leveler (convergence)?
4. How do intergenerational educational mobility trajectories (persistently poor, downwardly mobile, upwardly mobile, persistently affluent) pattern late-life cognitive function and mental health?

### 1.2 Theoretical Framework
The study evaluates four major paradigms from the sociology of ageing and life-course epidemiology:
- **Cumulative Advantage and Disadvantage (CAD) / Life-Course Divergence:** Postulates that health differentials between socially advantaged and disadvantaged groups widen as cohorts age due to systemic accumulation of stress, economic insecurity, and insults.
- **Age-as-Leveler / Cohort Convergence:** Hypothesizes that biological senescence, universal access to age-based entitlements (such as pensions), and selective mortality attenuate socioeconomic health disparities in oldest-old age.
- **Pathway / Chains-of-Risk Model:** Suggests that childhood conditions primarily matter through their downstream impacts on educational attainment, occupational trajectories, and adult socioeconomic status.
- **Critical Period / Biological Latency:** Posits that early biological shocks or chronic poverty during sensitive developmental windows exert immutable, direct effects on neural and cognitive reserve that persist regardless of adult socioeconomic mobility.

### 1.3 Key Empirical Findings
- **High Prevalence of Childhood Disadvantage:** In the nationally representative sample of adults aged >= 45 (N = 66,606), 28.5% reported living in a poor household during childhood, 15.6% reported fair/poor childhood health, and 3.6% were bedridden for at least one month before age 16.
- **Cognitive Impairment (Memory + Orientation Composite):**
  - In demographic-adjusted models (Model A), childhood poverty was associated with a 35.6% higher prevalence of cognitive impairment (PR = 1.356, 95% CI: 1.156-1.590, p = 0.0002).
  - After controlling for adult educational attainment and household consumption expenditure (Model B), this association was completely attenuated (PR = 0.928, 95% CI: 0.818-1.052, p = 0.241). Adult education accounts for over 100% of the initial association, demonstrating that formal schooling is the primary structural pathway linking childhood origins to late-life cognitive function in India.
  - Childhood poor health (PR = 0.949, 95% CI: 0.820-1.099) and childhood bedridden status (PR = 1.005, 95% CI: 0.860-1.176) exhibited no residual direct association with late-life cognitive impairment once adult socioeconomic status was accounted for.
- **Depressive Symptoms (CES-D >= 4):**
  - Childhood disadvantage exhibits persistent, unattenuated associations with elevated depressive symptoms in late life.
  - In adult SES-adjusted models (Model B), childhood poverty remained independently associated with late-life depression (PR = 1.208, 95% CI: 1.032-1.415, p = 0.0189).
  - Poor childhood health (PR = 1.198, 95% CI: 1.070-1.341, p = 0.0017; original strict metric PR = 1.418, 95% CI: 1.212-1.659, p < 0.0001) and childhood bedridden status (PR = 1.159, 95% CI: 1.048-1.281, p = 0.0040) remained robust, direct predictors of depression, supporting latency and allostatic load mechanisms for mental health.
- **Age Heterogeneity and CAD Testing:**
  - Formal joint Wald tests of exposure-by-age interactions revealed no statistically significant divergence across age cohorts for depressive symptoms (p = 0.540 for SES x age, p = 0.697 for health x age, p = 0.354 for bedridden x age).
  - For cognitive impairment, the interaction between childhood SES and age was marginally significant (p = 0.045 uncorrected; p > 0.05 under Benjamini-Hochberg FDR control). Standardized marginal predicted prevalences revealed that risk differences widened in absolute terms from 4.7 percentage points at age 45-59 to 9.3 percentage points at age 75+, reflecting persistent absolute divergence consistent with Cumulative Disadvantage, despite stable relative prevalence ratios.
- **Intergenerational Educational Mobility:**
  - Upwardly mobile individuals (illiterate parents -> literate respondent) achieved late-life cognitive impairment rates (12.98%, 95% CI: 12.20-14.17%) that closely matched persistently affluent peers (10.86%, 95% CI: 10.21-11.80%), demonstrating the powerful compensatory capacity of educational acquisition in overcoming early-life structural disadvantage.

---

## 2. Directory Structure

```
soc450/
|-- README.md                         Master documentation and replication guide
|-- report.pdf                        Full 45-page final research manuscript
|-- requirements.txt                  Python dependency specifications
|-- run_replication.sh                One-click end-to-end execution script
|-- variable_map.csv                  Data dictionary and LASI variable cross-reference
|
|-- code/                             Core econometric and epidemiological scripts
|   |-- survey_utils.py               Design-based Taylor linearization and delta-method tools
|   |-- 01_build_variable_map.py      Data dictionary parser across LASI modules
|   |-- 02_extract_and_clean.py       Raw data harmonization and cleaning
|   |-- 03_descriptive_analysis.py    Descriptive statistics (Tables 1-2, Figures 1-3)
|   |-- 04_regression_models.py       Baseline modified Poisson regression models
|   |-- 05_sensitivity_analyses.py    Dose-response and continuous sensitivity models
|   |-- 07_build_dataset_v2.py        Protocol Amendment 1 dataset build and cognitive derivation
|   |-- 08_models_v2.py               Sequential models, interaction tests, IPW, and margins
|   |-- 09_forest_plot_v2.py          Sequential model forest plot visualization
|   `-- 12_social_mobility.py         Intergenerational educational mobility models
|
|-- data_analysis/                    Harmonized analysis datasets
|   |-- lasi_clean_v2.parquet         Primary analytic dataset (N = 66,606; 48 variables)
|   `-- lasi_clean_analysis.parquet   Harmonized baseline dataset
|
|-- dataset/                          Raw microdata documentation
|   `-- README.md                     Access instructions for obtaining IIPS microdata
|
|-- extension/                        Advanced sensitivity extensions
|   |-- 01_cognitive_sensitivity.py   Continuous cognitive domain sensitivity models
|   |-- continuous_cognitive_sensitivity.csv   Output regression estimates
|   `-- analysis_plan.md              Extension methodological protocol
|
`-- outputs/                          Generated tabular and visual artifacts
    |-- diagnostics/                  Attrition logs, missingness tables, sample flow
    |-- figures/                      Descriptive charts (Figures 1, 2, 3)
    |-- figures_v2/                   Primary analytical figures (Figures 4, 5, 6, 7, A1, A2)
    |-- tables/                       Descriptive tables (Tables 1, 2, 2b)
    `-- tables_v2/                    Primary regression tables (Tables 3-19, S0-S5)
```

---

## 3. Cross-Walk: Report Tables and Generating Scripts

The following table maps every table presented in `report.pdf` to its corresponding data generation script and output CSV artifact.

| Report Table | Description | Generating Script | Output Artifact |
| :--- | :--- | :--- | :--- |
| Table 1 | Survey-weighted sample sociodemographic characteristics | `code/03_descriptive_analysis.py` | `outputs/tables/table1_sample_characteristics.csv` |
| Table 2 | Outcome prevalence across age groups (45-59, 60-74, 75+) | `code/03_descriptive_analysis.py` | `outputs/tables/table2_outcome_prevalence_by_age.csv` |
| Table 3 | Sequential modified Poisson models for cognitive impairment | `code/08_models_v2.py` | `outputs/tables_v2/table3v2_cognition_impairment.csv` |
| Table 4 | Sequential modified Poisson models for depressive symptoms | `code/08_models_v2.py` | `outputs/tables_v2/table4v2_depression.csv` |
| Table 5 | Joint Wald F-tests for exposure-by-age interactions | `code/08_models_v2.py` | `outputs/tables_v2/table5v2a_interaction_joint_tests.csv` |
| Table 6 | Standardized marginal predicted prevalences by age and SES | `code/08_models_v2.py` | `outputs/tables_v2/table5v2b_standardized_predictions.csv` |
| Table 7 | Age-specific marginal risk differences for childhood exposures | `code/08_models_v2.py` | `outputs/tables_v2/table5v2c_risk_differences.csv` |
| Table 8 | Mutually adjusted models with simultaneous exposures | `code/08_models_v2.py` | `outputs/tables_v2/table6v2_mutual_adjustment.csv` |
| Table 9 | Demographic comparison: reference study vs full sample | `code/08_models_v2.py` | `outputs/tables_v2/table_demographic_study.csv` |
| Table 10 | Comparison of common analytic samples across model steps | `code/08_models_v2.py` | `outputs/tables_v2/table_s0_common_samples.csv` |
| Table 11 | Survey-weighted logistic response model for cognitive testing | `code/08_models_v2.py` | `outputs/tables_v2/table_s1_response_model.csv` |
| Table 12 | IPW attrition-adjusted models for cognitive impairment | `code/08_models_v2.py` | `outputs/tables_v2/table_s2_ipw_cognition.csv` |
| Table 13 | Covariate missingness and interview completion summary | `code/08_models_v2.py` | `outputs/tables_v2/table_s3_cognition_missingness.csv` |
| Table 14 | Sensitivity analyses: alternate cutoffs and full battery | `code/08_models_v2.py` | `outputs/tables_v2/table_s4_sensitivity.csv` |
| Table 15 | Education gradient robustness: linear vs categorical models | `code/08_models_v2.py` | `outputs/tables_v2/table_s5_education_gradient_v1_vs_v2.csv` |
| Table 16 | Linear survey-weighted regression on continuous cognition | `code/08_models_v2.py` | `outputs/tables_v2/table3v2b_cognition_continuous.csv` |
| Table 17 | Joint childhood SES categories (Poor, Average, Varied) | `code/08_models_v2.py` | `outputs/tables_v2/table3v2c_ses_joint_categories.csv` |
| Table 18 | Continuous cognitive domain sensitivity models | `extension/01_cognitive_sensitivity.py` | `extension/continuous_cognitive_sensitivity.csv` |
| Table 19 | Intergenerational educational mobility trajectory models | `code/12_social_mobility.py` | `outputs/tables_v2/table_social_mobility.csv` |

---

## 4. Cross-Walk: Report Figures and Generating Scripts

The following table maps every visual figure in `report.pdf` to its generating script and high-resolution output file.

| Report Figure | Caption and Content | Generating Script | Output Artifact |
| :--- | :--- | :--- | :--- |
| Figure 1 | Population age distribution of LASI Wave 1 sample | `code/03_descriptive_analysis.py` | `outputs/figures/figure1_age_distribution.png` |
| Figure 2 | Weighted prevalence of childhood disadvantages by sex | `code/03_descriptive_analysis.py` | `outputs/figures/figure2_childhood_disadvantage_prevalence.png` |
| Figure 3 | Unadjusted outcome prevalence across age cohorts | `code/03_descriptive_analysis.py` | `outputs/figures/figure3_outcome_prevalence_by_age.png` |
| Figure 4 | Standardized predicted prevalence of cognitive impairment | `code/08_models_v2.py` | `outputs/figures_v2/figure4v2_cognition_interaction.png` |
| Figure 5 | Standardized predicted prevalence of depressive symptoms | `code/08_models_v2.py` | `outputs/figures_v2/figure5v2_depression_interaction.png` |
| Figure 6 | Sequential model forest plots (Models 0, A, B, C) | `code/09_forest_plot_v2.py` | `outputs/figures_v2/figure6v2_forest_sequential.png` |
| Figure 7 | Intergenerational educational mobility trajectories | `code/12_social_mobility.py` | `outputs/figures_v2/figure7_social_mobility.png` |
| Figure A1 | Education gradient comparison (linear vs categorical) | `code/08_models_v2.py` | `outputs/figures_v2/figureA1_education_gradient.png` |
| Figure A2 | Cognitive assessment missingness across demographic strata | `code/08_models_v2.py` | `outputs/figures_v2/figureA2_cognition_missingness.png` |

---

## 5. Software Environment and Installation

### 5.1 Prerequisites
- Linux, macOS, or Windows (WSL recommended for Windows).
- Python 3.10, 3.11, or 3.12.
- At least 4 GB of available RAM.

### 5.2 Environment Setup
Set up an isolated virtual environment and install the required dependencies:

```bash
# Navigate to the soc450 directory
cd soc450

# Create virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade package installer
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 5.3 Core Package Dependencies
- `pandas` (>= 2.0.0): Vectorized data manipulation.
- `numpy` (>= 1.24.0): Matrix computation and numerical linear algebra.
- `scipy` (>= 1.10.0): Scientific distributions and hypothesis testing.
- `statsmodels` (>= 0.14.0): Generalized linear modeling (GLM) and sandwich variance estimators.
- `pyarrow` (>= 12.0.0): Columnar Parquet read/write routines.
- `pyreadstat` (>= 1.2.0): Stata (`.dta`) file decompression and dictionary parsing.
- `matplotlib` (>= 3.7.0): Publication graphics and figure generation.
- `seaborn` (>= 0.12.0): Statistical plot styling.

---

## 6. Replication Instructions

### 6.1 Automated One-Click Replication
To execute the complete analysis pipeline and regenerate all 19 tables and 9 figures, run:

```bash
bash run_replication.sh
```

The script will automatically detect the Python environment, verify the cleaned dataset, execute the sequential models, estimate interaction effects, generate forest plots and mobility models, and compile the cognitive sensitivity extension. Total execution time is approximately 2 minutes on standard hardware.

### 6.2 Modular Step-by-Step Execution
Individual stages can also be executed independently from within the `soc450` root directory:

1. **Step 1: Dataset Verification and Cognitive Score Derivation**
   ```bash
   python code/07_build_dataset_v2.py
   ```
   *Reads `data_analysis/lasi_clean_analysis.parquet` and derives skip-pattern-aware cognitive impairment cutoffs, outputting `data_analysis/lasi_clean_v2.parquet`.*

2. **Step 2: Descriptive Statistics and Baseline Figures**
   ```bash
   python code/03_descriptive_analysis.py
   ```
   *Generates Tables 1, 2, 2B and Figures 1, 2, 3 into `outputs/tables/` and `outputs/figures/`.*

3. **Step 3: Core Econometric Regressions, Interactions, and IPW**
   ```bash
   python code/08_models_v2.py
   ```
   *Fits survey-weighted modified Poisson models (Models 0, A, B, C), joint Wald interaction tests, standardized margins, risk differences, IPW attrition corrections, and sensitivity models (Tables 3-17 and Figures 4, 5, A1, A2).*

4. **Step 4: Forest Plot Generation**
   ```bash
   python code/09_forest_plot_v2.py
   ```
   *Generates the sequential model forest plot (Figure 6) in `outputs/figures_v2/`.*

5. **Step 5: Intergenerational Educational Mobility Trajectory Analysis**
   ```bash
   python code/12_social_mobility.py
   ```
   *Constructs the parental-offspring education transition matrix and fits trajectory models (Table 19 and Figure 7).*

6. **Step 6: Continuous Cognitive Domain Sensitivity Extension**
   ```bash
   python extension/01_cognitive_sensitivity.py
   ```
   *Fits survey-weighted Gaussian GLMs on continuous episodic memory, orientation, and composite scores, saving results to `extension/continuous_cognitive_sensitivity.csv`.*

---

## 7. Statistical Methodology

### 7.1 Complex Survey Design Adjustments
LASI Wave 1 employs a multistage stratified cluster sampling design:
- **Sampling Units:** 2,428 Primary Sampling Units (PSUs / Sub-Centre villages and urban Census Enumeration Blocks).
- **Stratification:** 72 explicit strata cross-classifying states and urban/rural domains.
- **Sampling Weights:** Individual sampling weights normalized to sample size:
  $$\tilde{w}_i = w_i \times \frac{N}{\sum_{j=1}^N w_j}$$
- **Variance Estimation:** Design-based Taylor series linearization (`code/survey_utils.py`):
  $$V(\hat{\beta}) = (X^T W X)^{-1} \left[ \sum_{h=1}^H \frac{n_h}{n_h - 1} \sum_{i=1}^{n_h} (u_{hi} - \bar{u}_h)(u_{hi} - \bar{u}_h)^T \right] (X^T W X)^{-1}$$
  Degrees of freedom are defined as the number of PSUs minus strata ($df = 2,428 - 72 = 2,356$).

### 7.2 Modified Poisson Regression for Binary Outcomes
Because cognitive impairment (11.6%) and depressive symptoms (28.2%) are common outcomes (>10%), standard logistic regression odds ratios (ORs) substantially overestimate relative risk. Following Zou (2004), we estimate modified Poisson models with robust sandwich standard errors:
$$\log(\mu_i) = \alpha + \beta_1 \text{Disadvantage}_i + \mathbf{X}_i^T \boldsymbol{\gamma}$$
Exponentiated coefficients provide direct, interpretable Prevalence Ratios (PR):
$$\text{PR} = \exp(\beta_1)$$

### 7.3 Standardized Predictions and Marginal Risk Differences
To evaluate Cumulative Disadvantage on the additive scale without model dependence, we compute average marginal predictions across counterfactual exposure assignments:
$$\hat{P}(Y=1 \mid \text{Disadvantage}=d, \text{Age}=a) = \frac{1}{\sum w_i} \sum_{i \in \text{Age}=a} w_i \cdot g^{-1}(\hat{\alpha} + \hat{\beta}_1 d + \mathbf{X}_i^T \hat{\boldsymbol{\gamma}})$$
Risk differences (RD) and 95% confidence intervals are computed via the multivariable delta method.

### 7.4 Non-Response and Inverse Probability Weighting (IPW)
Of 62,835 age-eligible respondents who completed direct interviews, 5,590 (8.9%) were unable or refused to complete direct cognitive testing. We estimate a survey-weighted multivariable logistic response model predicting cognitive completion from baseline covariates, compute stabilized inverse probability weights:
$$\text{IPW}_i = \frac{P(R=1)}{\hat{P}(R=1 \mid \mathbf{Z}_i)}$$
and re-estimate all cognitive models under survey-weight-by-IPW multiplication ($w_i^* = w_i \times \text{IPW}_i$).

---

## 8. Data Access and Attribution

The raw microdata analyzed in this study are from the **Longitudinal Ageing Study in India (LASI) Wave 1 (2017-2018)**, conducted by the International Institute for Population Sciences (IIPS), Mumbai, in collaboration with the Harvard T.H. Chan School of Public Health and the University of Southern California.

Under the terms of the LASI Data Use Agreement, raw microdata files cannot be redistributed publicly. Researchers can access the dataset free of charge:
- **IIPS Mumbai Portal:** [https://www.iipsindia.ac.in/lasi/](https://www.iipsindia.ac.in/lasi/)
- **Gateway to Global Aging Data:** [https://g2aging.org/](https://g2aging.org/)

The pre-processed, harmonized analytical datasets (`lasi_clean_v2.parquet` and `lasi_clean_analysis.parquet`) included in `data_analysis/` contain only the derived research variables necessary for replication, ensuring full reproducibility while maintaining compliance with academic data agreements.
