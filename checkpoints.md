# Project Progress & Checkpoint Log

**Project Title:** Early-Life Disadvantage and Later-Life Mental and Cognitive Health in India: Evidence from LASI Wave 1  
**Working Directory:** `/home/harshit/Documents/Sem5/SOC450 Project`  
**Last Updated:** 2026-10-05 16:32:00 IST  

---

## 1. Current Active Checkpoint
- **Status:** **Milestone 7 (Comprehensive Research Report & Self-Contained Deliverables) Complete**
- **Readiness:** Complete academic research report generated in both Markdown ([`report/final_research_report.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.md)) and portable standalone HTML with base64 embedded figures ([`report/final_research_report.html`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.html)).
- **Immediate Next Step:** **Presentation Slide Deck Assembly** (`report/presentation_slides.md`) mapping the 14-slide presentation flow.

---

## 2. Chronological Milestones Log

### Milestone 0: Environment Setup & Tooling Configuration
- **Date:** 2026-10-05
- **Actions:**
  - Created isolated virtual environment `.venv` with `pip`.
  - Installed and verified analytical libraries: `pandas`, `pyreadstat`, `numpy`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`, `pyarrow`.
  - Established project directory structure:
    `code/`, `data_analysis/`, `data_intermediate/`, `outputs/tables/`, `outputs/figures/`, `outputs/diagnostics/`, `outputs/model_objects/`, `report/`.

### Milestone 1: Phase 0 — Pre-Specified Protocol Freezing
- **Date:** 2026-10-05
- **Artifact:** [`protocol.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/protocol.md)
- **Key Decisions:**
  - Formulated 5 core hypotheses covering early-life SES, childhood health, bedridden history, age heterogeneity, and socioeconomic attenuation.
  - Established non-negotiable cross-sectional baseline guardrails: strictly associative phrasing, no causal language, no claims of individual longitudinal decline.
  - Specified modified Poisson regression (APRs) for binary outcomes and weighted linear regression (WLS) for continuous scores.

### Milestone 2: Phase 1 & 2 — Metadata Inventory & Master Variable Mapping
- **Date:** 2026-10-05
- **Script:** [`code/01_build_variable_map.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/01_build_variable_map.py)
- **Outputs:**
  - Full variable inventory (2,623 variables): [`outputs/diagnostics/variable_inventory.tsv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/diagnostics/variable_inventory.tsv)
  - Master variable specification map (34 constructs): [`variable_map.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/variable_map.csv)
- **Key Discovery:**
  - `mpce_quintile` and `mpce_amount` are already merged and complete in `3_LASI_W1_Individual_v4.dta`, eliminating any merge loss from the 612 MB household file.

### Milestone 3: Phase 3–8 — Extraction, Feature Engineering & Cleaning
- **Date:** 2026-10-05
- **Script:** [`code/02_extract_and_clean.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/02_extract_and_clean.py)
- **Outputs:**
  - Clean analysis dataset: [`data_analysis/lasi_clean_analysis.parquet`](file:///home/harshit/Documents/Sem5/SOC450%20Project/data_analysis/lasi_clean_analysis.parquet) (66,606 rows $\times$ 36 columns)
  - CSV export: [`data_analysis/lasi_clean_analysis.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/data_analysis/lasi_clean_analysis.csv)
  - Sample flow table: [`outputs/diagnostics/sample_flow.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/diagnostics/sample_flow.csv)
  - Missingness summary: [`outputs/diagnostics/missingness_summary.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/diagnostics/missingness_summary.csv)
- **Key Constructs Engineered:**
  - Target population: $N = 66,606$ ($\ge 45$ years, excluding 6,790 younger spouses).
  - Childhood SES (`ht235`: Pretty well-off, Average, Poor).
  - Childhood Health (`ht231`: Good vs. Poor binary; 5-level ordinal).
  - Childhood Bedridden (`ht233`: No vs. Yes).
  - Cumulative Disadvantage Score (0 to 3 sum index).
  - 10-Item CES-D Scale (`fs701`–`fs710`): scored 0–10; Depressive symptoms ($\ge 4$).
  - 43-Point Harmonized Cognitive Battery: Memory (0–20), Orientation (0–8), Arithmetic (0–9), Executive (0–4), Object Naming (0–2).
  - Cognitive Impairment: lowest 10th percentile ($\le 16.00$ points).
  - Clustered survey design: `cluster_psu` (2,439 clusters), `stratum` (72 strata), `survey_weight` (`indiaindividualweight`).

### Milestone 4: Phase 10 — Survey-Weighted Descriptive Analysis
- **Date:** 2026-10-05
- **Script:** [`code/03_descriptive_analysis.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/03_descriptive_analysis.py)
- **Outputs:**
  - Table 1 (Sample Characteristics): [`outputs/tables/table1_sample_characteristics.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table1_sample_characteristics.csv)
  - Table 2 (Outcome Prevalence by Age Group): [`outputs/tables/table2_outcome_prevalence_by_age.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table2_outcome_prevalence_by_age.csv)
  - Table 2B (Prevalence across Exposures): [`outputs/tables/table2b_prevalence_by_exposure.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table2b_prevalence_by_exposure.csv)
  - Figures:
    - [`figure1_age_distribution.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure1_age_distribution.png)
    - [`figure2_childhood_disadvantage_prevalence.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure2_childhood_disadvantage_prevalence.png)
    - [`figure3_outcome_prevalence_by_age.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure3_outcome_prevalence_by_age.png)

### Milestone 5: Phase 11 & 12 — Primary Regression & Age-Interaction Analysis
- **Date:** 2026-10-05
- **Script:** [`code/04_regression_models.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/04_regression_models.py)
- **Outputs:**
  - Table 3 (Cognitive Impairment Models): [`outputs/tables/table3_cognition_regression.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table3_cognition_regression.csv)
  - Table 4 (Depressive Symptoms Models): [`outputs/tables/table4_depression_regression.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table4_depression_regression.csv)
  - Table 5 (Age Interaction Predictions): [`outputs/tables/table5_interaction_predictions.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table5_interaction_predictions.csv)
  - Figures:
    - [`figure4_cognitive_interaction.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure4_cognitive_interaction.png)
    - [`figure5_depression_interaction.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure5_depression_interaction.png)

### Milestone 6: Phase 13 — Sensitivity Analyses
- **Date:** 2026-10-05
- **Script:** [`code/05_sensitivity_analyses.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/05_sensitivity_analyses.py)
- **Outputs:**
  - Table S (Sensitivity Models): [`outputs/tables/table_sensitivity_analyses.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table_sensitivity_analyses.csv)
  - Methods compared: Linear WLS (continuous scores), Logistic Regression (AORs), Dose-Response (Cumulative Disadvantage).

### Milestone 7: Phase 14 — Comprehensive Research Report & Self-Contained Publication Artifacts
- **Date:** 2026-10-05
- **Scripts:** [`code/06_generate_html_report.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/06_generate_html_report.py)
- **Deliverables:**
  - **Full Academic Manuscript (Markdown):** [`report/final_research_report.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.md)
  - **Self-Contained Publication HTML Report:** [`report/final_research_report.html`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.html) (1.3 MB, fully portable with base64 embedded Figures 1–5, print CSS, styled tables, and formatted equations).
- **Substantive Scope Included:**
  - Detailed background, life-course conceptual models, sampling design, variable derivations, survey weighting equations.
  - Full Tables 1, 2, 2B, 3, 4, 5, and Table S embedded.
  - Embedded publication figures (Figures 1–5).
  - Mechanistic discussion comparing cognitive socioeconomic attenuation vs. persistent mental health somatic scarring.
  - Evidence-based conclusion and step-by-step reproducibility instructions.

---

## 3. Key Findings & Empirical Summary

1. **Life-Course Socioeconomic Attenuation for Cognition:**
   - Unadjusted: Poor childhood SES is associated with nearly double the prevalence of cognitive impairment ($\text{PR} = 1.928, p < 0.0001$).
   - Demographic adjustment: $\text{PR} = 1.653$ ($95\%\text{ CI: } 1.334–2.049, p < 0.0001$).
   - Adult SES adjustment (education + MPCE): $\text{PR} = 1.057$ ($p = 0.49$).
   - **Conclusion:** Adult schooling and accumulated material resources mediate almost the entire early-life socioeconomic disparity in cognitive impairment (Hypothesis 5 confirmed).
   - On the continuous scale, adults from poor childhoods still score $0.86$ points lower on the 43-point test battery ($\beta = -0.862, p < 0.0001$).

2. **Enduring Direct Association for Early Health Vulnerability on Depression:**
   - Poor childhood health remains a significant predictor of depressive symptoms ($\text{CES-D} \ge 4$) across all models:
     - Model 0: $\text{PR} = 1.340$ ($p < 0.0001$)
     - Model 1: $\text{PR} = 1.322$ ($p < 0.0001$)
     - Model 2 (Primary): $\text{PR} = 1.306$ ($95\%\text{ CI: } 1.185–1.440, p < 0.0001$)
     - Model 3 (Health): $\text{PR} = 1.288$ ($p < 0.0001$)
   - Childhood bedridden history ($\ge 1$ month) is associated with elevated depressive symptoms in Model 2 ($\text{PR} = 1.175, p = 0.0023$).
   - **Conclusion:** Unlike SES, early-life somatic vulnerability displays an enduring psychological imprint that adult socioeconomic success does not erase (Hypotheses 2 and 3 confirmed).

3. **Cumulative Disadvantage Dose-Response:**
   - Each additional childhood disadvantage is associated with an **11.3% increase in depressive symptom prevalence** ($\text{APR} = 1.113, p < 0.0001$).

4. **Age Heterogeneity:**
   - Cognitive impairment prevalence rises steeply with age ($6.7\%$ in 45–59 $\rightarrow$ $13.7\%$ in 60–74 $\rightarrow$ $29.2\%$ in 75+).
   - Childhood SES disparities in cognitive impairment are widest in middle and young-old ages, narrowing in the oldest-old ($75+$) where selective survival and biological ageing dominate.

---

## 4. File & Artifact Registry

### A. Scripts & Code
| File Path | Description |
| :--- | :--- |
| [`code/01_build_variable_map.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/01_build_variable_map.py) | Generates full variable inventory TSV and master variable map CSV. |
| [`code/02_extract_and_clean.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/02_extract_and_clean.py) | Reads raw DTA, filters 45+, cleans exposures/outcomes/covariates, outputs clean datasets. |
| [`code/03_descriptive_analysis.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/03_descriptive_analysis.py) | Calculates survey-weighted Tables 1, 2, 2B and generates Figures 1, 2, 3. |
| [`code/04_regression_models.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/04_regression_models.py) | Fits survey-weighted modified Poisson regressions, interaction models, and Figures 4 & 5. |
| [`code/05_sensitivity_analyses.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/05_sensitivity_analyses.py) | Fits continuous WLS models, logistic regressions (AORs), and cumulative disadvantage score models. |
| [`code/06_generate_html_report.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/06_generate_html_report.py) | Converts manuscript markdown into portable, self-contained HTML with embedded figures. |

### B. Analytical Datasets
| File Path | Description | Dimensions |
| :--- | :--- | :---: |
| [`data_analysis/lasi_clean_analysis.parquet`](file:///home/harshit/Documents/Sem5/SOC450%20Project/data_analysis/lasi_clean_analysis.parquet) | Primary clean analysis file (fast binary format) | 66,606 rows $\times$ 36 cols |
| [`data_analysis/lasi_clean_analysis.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/data_analysis/lasi_clean_analysis.csv) | Primary clean analysis file (plain CSV format) | 66,606 rows $\times$ 36 cols |

### C. Output Tables
| File Path | Contents |
| :--- | :--- |
| [`outputs/tables/table1_sample_characteristics.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table1_sample_characteristics.csv) | Table 1: Weighted percentage and unweighted N for all demographic, adult SES, and childhood exposure variables. |
| [`outputs/tables/table2_outcome_prevalence_by_age.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table2_outcome_prevalence_by_age.csv) | Table 2: Survey-weighted prevalence and means of cognitive impairment and depression by age group. |
| [`outputs/tables/table2b_prevalence_by_exposure.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table2b_prevalence_by_exposure.csv) | Table 2B: Outcome prevalence broken down by childhood conditions. |
| [`outputs/tables/table3_cognition_regression.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table3_cognition_regression.csv) | Table 3: Modified Poisson regression models for Cognitive Impairment (Models 0–3). |
| [`outputs/tables/table4_depression_regression.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table4_depression_regression.csv) | Table 4: Modified Poisson regression models for Depressive Symptoms (Models 0–3). |
| [`outputs/tables/table5_interaction_predictions.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table5_interaction_predictions.csv) | Table 5: Adjusted marginal predicted prevalences across the 9 age $\times$ childhood SES strata. |
| [`outputs/tables/table_sensitivity_analyses.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/table_sensitivity_analyses.csv) | Table S: WLS linear regression, logistic AORs, and cumulative dose-response models. |

### D. Figures
| File Path | Description |
| :--- | :--- |
| [`outputs/figures/figure1_age_distribution.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure1_age_distribution.png) | Survey-weighted histogram and density of respondent age ($\ge 45$). |
| [`outputs/figures/figure2_childhood_disadvantage_prevalence.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure2_childhood_disadvantage_prevalence.png) | Prevalence of childhood SES, childhood health, and bedridden history. |
| [`outputs/figures/figure3_outcome_prevalence_by_age.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure3_outcome_prevalence_by_age.png) | Cognitive impairment and depressive symptom prevalence across age groups. |
| [`outputs/figures/figure4_cognitive_interaction.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure4_cognitive_interaction.png) | Adjusted predicted cognitive impairment by childhood SES across age groups. |
| [`outputs/figures/figure5_depression_interaction.png`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/figure5_depression_interaction.png) | Adjusted predicted depressive symptoms by childhood SES across age groups. |

### E. Reports & Deliverables
| File Path | Description |
| :--- | :--- |
| [`report/final_research_report.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.md) | Full academic research paper and empirical manuscript in Markdown. |
| [`report/final_research_report.html`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.html) | Self-contained, portable publication report with embedded base64 figures and print CSS. |
| [`protocol.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/protocol.md) | Pre-specified analysis protocol, hypotheses, estimands, and checkpoint rules. |
| [`checkpoints.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/checkpoints.md) | Living checkpoint progress log and registry. |
| [`variable_map.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/variable_map.csv) | Master variable codebook mapping. |
| [`outputs/diagnostics/sample_flow.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/diagnostics/sample_flow.csv) | Step-by-step sample flow counts and exclusion accounting. |
| [`outputs/diagnostics/missingness_summary.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/diagnostics/missingness_summary.csv) | Missing value summary across all analytical variables. |
| [`outputs/diagnostics/variable_inventory.tsv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/diagnostics/variable_inventory.tsv) | Full 2,623-variable inventory of the raw Individual DTA file. |

---

## 5. Where to Start From Next

When beginning the next session, start directly at **Presentation Slide Deck Assembly**:
1. Navigate to [`report/`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report).
2. Create `report/presentation_slides.md` (or `.pptx` outline) mapping the 14-slide presentation flow specified in Section 43 of the Implementation Plan:
   - Slide 1: Ageing in India & The Research Problem
   - Slide 2: Research Gap & Life-Course Perspective
   - Slide 3: Exact Research Questions & Hypotheses
   - Slide 4: Data Source & Sampling Design (LASI Wave 1)
   - Slide 5: Conceptual Framework Diagram
   - Slide 6: Master Variable Definitions & Harmonization
   - Slide 7: Methodology & Survey-Weighted Modified Poisson Modeling
   - Slide 8: Participant Sample Flow ($N=66,606$)
   - Slide 9: Descriptive Results (Table 1 & Figures 1–2)
   - Slide 10: Outcome Prevalence across Age Groups (Table 2 & Figure 3)
   - Slide 11: Main Regression Results — Attenuation vs. Persistence (Tables 3 & 4)
   - Slide 12: Age Heterogeneity & Interaction Predictions (Table 5 & Figures 4–5)
   - Slide 13: Sensitivity Analyses & Robustness Checks (Table S)
   - Slide 14: Methodological Limitations, Public Health Implications & Conclusion


---

## Milestone 8 — Post-Audit Correction (v2) — 2026-10-05

**Current active checkpoint:** v2 analysis complete; corrected report produced. v1 outputs are retained and archived, not deleted.

**What was done**
1. Independent audit found problems in v1 (see `audit_report.md` in the artifacts folder): the cognitive composite was a schooling proxy (skips scored 0); the age interaction was never tested; strata were ignored; model samples differed; no state control; exposures were never mutually adjusted; informative missingness was not handled; causal/mediation language breached protocol §2.
2. **Protocol Amendment 1** appended to `protocol.md` (Section 12). Original Sections 1–11 are unchanged.
3. Rebuilt the dataset: `code/07_build_dataset_v2.py` → `data_analysis/lasi_clean_v2.parquet`. Primary cognition = memory + orientation (0–28); skip-aware battery; weighted p10 cut-offs; strict orientation; `mh045` outliers set to missing; caste "Other" retained.
4. `code/survey_utils.py`: stratified-cluster Taylor variance (72 strata, 2,428 clusters). Validated against the earlier statsmodels cluster SE (0.0297 vs 0.0299).
5. `code/08_models_v2.py`: common-sample M0–M3 with state FE, mutual adjustment, interaction joint tests + standardized predictions, IPW, sensitivity analyses. `code/09_forest_plot_v2.py` regenerates Figure 6. `code/10_generate_report_v2.py` writes the report.
6. Bug found and fixed during v2: single-exposure SES rows compared Poor with everyone else. SES is now always a joint 3-level variable.

**Key v2 results**
- Depression (N = 62,047): childhood health PR 1.20 (1.07–1.34), poor SES 1.21 (1.03–1.42), bedridden 1.16 (1.05–1.28), all M2; cumulative index 1.11 per adversity (1.07–1.16). Robust to mutual adjustment, continuous CES-D and sex stratification.
- Cognition (N = 57,245, memory + orientation): Poor SES PR 1.36 (M1) → 0.93 (0.82–1.05, M2). Childhood health and bedridden ≈ null. On the skip-aware battery, associations persist (SES 1.29, health 1.22). The conclusion therefore depends on the outcome definition.
- The new primary outcome still has a steep education gradient (Figure A1). Education-stratified results: never-schooled PR 0.91 (0.79–1.05); any schooling 0.99 (0.76–1.29).
- Age heterogeneity (H4) not supported: joint p for SES×age on cognition = 0.045 (opposite direction at 75+), all others > 0.7.
- IPW did not change estimates (Poor SES M2 0.928 both ways).

**File registry (new)**
- Report: [`report/final_research_report_v2.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report_v2.md), [`report/final_research_report_v2.html`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report_v2.html) (self-contained, figures embedded), [`report/final_research_report_v2.pdf`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report_v2.pdf) (18 pages vector PDF)
- LaTeX Master: [`report/final_research_report.tex`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.tex), [`report/overleaf_package.zip`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/overleaf_package.zip) (Self-contained Overleaf bundle)
- Tables: `outputs/tables_v2/` (table3v2*, table4v2*, table5v2a/b/c, table6v2, table2v2, table_s0–s5)
- Figures: `outputs/figures_v2/` (figure4v2, figure5v2, figure6v2, figureA1, figureA2)
- Run log: `outputs/diagnostics/run_08_log.txt`
- v1 (archived): `report/final_research_report.*`, `outputs/tables/`, `outputs/figures/`

---

## Milestone 9 — Layman's Technical Glossary & Table Overflow Resolution — 2026-10-05

**Current active checkpoint:** Technical glossary embedded; LaTeX and HTML table overflow issues fully resolved; Overleaf package and 18-page publication PDF verified.

**What was done**
1. **Technical Terms Glossary Added (Section 2):** Created a dedicated, accessible primer in both LaTeX (`report/final_research_report.tex`), HTML (`report/final_research_report_v2.html`), and Markdown (`report/final_research_report_v2.md`). Skipped common terms and focused specifically on complex, domain-specific concepts:
   - *Life-Course Paradigms:* Biological Scarring, Accumulation of Disadvantage, Selective Survival (Survivor Bias / Mortality Selection), Cross-Sectional Baseline Guardrails.
   - *Survey Architecture:* PSU and SSUID (`ssuid`), Stratification (72 Strata), Sampling Weights (`indiaindividualweight`), Taylor Series Linearization (Cluster-Robust SEs), Survey Degrees of Freedom ($df = 2,356$), Proxy Interviews (`rproxy`).
   - *Clinical & Cognitive Metrics:* CES-D-10 Scale ($\ge 4.0$ cutoff), Cognitive Battery & Item-Skip Bias, Orientation vs. Word Recall Domains.
   - *Analytical Estimands:* Modified Poisson Regression vs. Odds Ratios (PR vs. OR), Average Marginal Effects / Standardized Predictions (AME), Inverse-Probability Weighting (IPW), Monthly Per Capita Consumption Expenditure (MPCE).
2. **Table Overflow Resolution (Section 4 Onwards):**
   - In [`code/11_generate_latex_report.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/11_generate_latex_report.py), wrapped all wide tables (Tables 3, 3b, 4, 5a, 5c, 6, and S2) in `\resizebox{\textwidth}{!}{...}` to guarantee strict adherence to page margins.
   - Split Table 6 (Mutually Adjusted) and Table 5c (Marginal Risk Differences across Age Groups) into multi-row stacked panels (Panel A: Cognitive Impairment, Panel B: Depressive Symptoms), cutting column widths in half and ensuring professional typography.
   - Fixed a duplicate row in Table S2 for joint SES models and cleaned math delimiters.
   - Updated print CSS in [`code/10_generate_report_v2.py`](file:///home/harshit/Documents/Sem5/SOC450%20Project/code/10_generate_report_v2.py) with `overflow-x: auto;` and compact cell padding.
3. **Compilation & Deliverable Verification:**
   - Rebuilt [`report/overleaf_package.zip`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/overleaf_package.zip) containing `main.tex`, `final_research_report.tex`, and 7 figures in `figures/`. Configured with `\graphicspath{{figures/}{report/figures/}{./}}` for 100% plug-and-play Overleaf compilation.
   - Re-exported [`report/final_research_report_v2.pdf`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report_v2.pdf) (18 pages, 1.4 MB) with zero horizontal table clipping verified via `pdftoppm` rendering.

**Next starting point**
1. Milestone 10 completed below.

---

## Milestone 10 — GitHub Repository Preparation — 2026-10-10

**Current active checkpoint:** Repository prepared and configured for GitHub deployment.

**What was done**
1. **Repository Sanitization:**
   - Initialized Git repository on `main` branch.
   - Removed `LICENSE`, Overleaf `.zip` packages (`overleaf_package.zip`, `report/overleaf_package.zip`), and HTML reports (`report/*.html`) per user request.
   - Configured `.gitignore` to strictly exclude raw Stata microdata files (`dataset/*.dta`), virtual environments (`.venv/`), compiler/LaTeX auxiliary files (`*.aux`, `*.log`, `*.toc`), editor caches, `.zip` archives, and HTML reports.
2. **Replication Infrastructure:**
   - Created `requirements.txt` specifying minimal, pinned dependencies (`pandas`, `numpy`, `scipy`, `statsmodels`, `pyarrow`, `pyreadstat`, `matplotlib`, `seaborn`, `Markdown`).
   - Created `run_replication.sh` master bash script for one-command end-to-end execution of data extraction, model fitting, forest plotting, and report generation.
   - Created `dataset/README.md` guiding users on how to acquire official LASI Wave 1 microdata from IIPS and Gateway to Global Aging.
3. **Comprehensive Documentation:**
   - Created publication-grade [`README.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/README.md) focusing fully on instructions to run the application (prerequisites, setup, one-command master run, step-by-step commands, dataset options, and local LaTeX compilation). All Overleaf and HTML references were removed.
4. **Active Assets:**
   - Cleaned analytic dataset: [`data_analysis/lasi_clean_v2.parquet`](file:///home/harshit/Documents/Sem5/SOC450%20Project/data_analysis/lasi_clean_v2.parquet) ($N = 66,606$).
   - Publication PDF: [`report/final_research_report_v2.pdf`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report_v2.pdf) (18 pages).
   - LaTeX Master: [`report/final_research_report.tex`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report.tex).
   - Markdown Report: [`report/final_research_report_v2.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/report/final_research_report_v2.md).

**Next starting point**
1. Push to remote GitHub repository using:
   ```bash
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

---

## Milestone 11 — Second Critical Review Fixes & Demographic Expansion — 2026-10-10

**Current active checkpoint:** Data rebuilt with updated parameters; next step is updating the models script.

**What was done**
1. Analyzed the second critical review and drafted an implementation plan (`implementation_plan_fixes.md`).
2. Appended Protocol Amendment 2 (Section 13) to `protocol.md` to capture new definitions (e.g. `low_memory_orientation`), restructuring of models (A, B, C), and the new demographic analysis requirement.
3. Updated `code/07_build_dataset_v2.py`:
   - Added `childhood_health_poor_original` calculation matching the published paper's logic (Poor/Very poor vs. the rest).
   - Renamed `imp_mo` to `low_memory_orientation` to strictly avoid diagnostic terminology.
   - Re-ran the dataset builder to regenerate `data_analysis/lasi_clean_v2.parquet` successfully.

**Next starting point**
1. Open and refactor `code/08_models_v2.py` to:
   - Run the sensitivity test comparing `childhood_health` and `childhood_health_poor_original`.
   - Separate models cleanly into Model A, Model B, and Model C.
   - Add the new Demographic Variations section (analyzing state, caste, residence, sex).


---

## Milestone 12 — Final Consolidation & Continuous Cognitive Sensitivity Extension — 2026-10-10

**Current active checkpoint:** Final project consolidation complete. All files packaged for Overleaf.

**What was done**
1. Executed a reproducible Continuous Cognitive Sensitivity Analysis as an extension, testing the differences between memory and orientation domains across adult-SES adjustment.
2. Verified that the small continuous penalty is driven entirely by memory, while orientation deficits are attenuated by adult schooling.
3. Updated the core Python report generators (`code/10_generate_report_v2.py` and `code/11_generate_latex_report.py`) to inject the Extension findings directly into the main, consolidated reports.
4. Corrected the remaining audit errors within the LaTeX report (removed final instances of causal terminology and clarified causal mediation limitations).
5. Cleaned temporary files from the workspace, leaving a finalized directory state.
6. Regenerated the master manuscript and finalized the complete `final_overleaf_package.zip`.

**Next starting point**
Project complete. The user may upload `final_overleaf_package.zip` to Overleaf for submission.
