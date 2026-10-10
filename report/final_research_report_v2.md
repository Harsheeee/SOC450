# Early-Life Disadvantage and Later-Life Cognitive and Mental Health in India: LASI Wave 1 (Corrected Analysis, v2)

**Status:** Revised report following an independent audit of the original (v1) analysis. v1 is archived at `report/final_research_report.md`. All deviations from the original protocol are listed in `protocol.md`, Section 12 (Protocol Amendment 1).

> **Interpretation guardrail.** LASI Wave 1 is cross-sectional. All findings are *associations* (prevalence ratios, mean differences). The data do not permit causal or mediation claims, and they cannot show within-person change.

---

## 1. Why this revision exists

An audit of v1 found problems that changed conclusions. This table lists each one and the corrective action.

| Audit finding | v1 behaviour | v2 correction |
|---|---|---|
| Cognitive score was a schooling proxy | Items skipped by unschooled respondents scored 0 (`fillna(0)`) | Primary outcome = memory + orientation (0–28); skip-aware full battery kept as sensitivity |
| Orientation partial credit | Missing orientation items counted as 0 | All 8 items required |
| Cut-off | Unweighted pooled 10th percentile | Survey-weighted 10th percentile; school-stratum-specific version as sensitivity |
| Interaction was not tested | Visual reading of one covariate profile | Joint Wald F test; standardized predictions averaged over each age group's covariates |
| Survey design | Strata ignored | Stratified-cluster linearization (72 strata, 2,428 clusters) |
| Model comparability | Different samples across M0–M3 | One common complete-case sample per outcome |
| Regional confounding | No state control | State fixed effects from Model 1 |
| "Independent" claims | Exposures modelled one at a time | Mutually adjusted models and a cumulative index |
| Informative missingness | Complete-case only | IPW comparison |
| Causal language | "Mediated", "scarring", "HPA programming" | Associational wording only |
| SES contrast bug (found during v2 coding) | not applicable | SES always modelled as a joint 3-level variable (reference = well-off) |


## 2. Primer on Ageing, Epidemiological, and Survey Methodology (Layman's Glossary)

To ensure that the empirical findings of this report are accessible to non-specialists, policymakers, and interdisciplinary readers, this section defines the essential technical terms from life-course epidemiology, gerontology, and survey methodology. Common concepts have been omitted; only complex, domain-specific terms are clarified below.

### 2.1 Life-Course Epidemiology and Ageing Paradigms
- **Biological Scarring (Sensitive / Critical Period Model):** The biological principle that severe physical shocks, malnutrition, or infectious illnesses during early childhood permanently alter the body's physiological set-points (such as chronic immune inflammation, vascular stiffness, or neuroendocrine stress regulation). These physiological alterations remain dormant or active throughout adult life, re-emerging decades later in old age as elevated risks of depression, disability, or physical frailty, even if the individual achieved upward socioeconomic mobility in adulthood.
- **Accumulation of Disadvantage (Cumulative Adversity):** A developmental trajectory whereby initial childhood disadvantage triggers a cascade of sequential hardships across the lifespan. Being born into poverty frequently constrains schooling opportunities, channeling individuals into hazardous manual labor with low wages, substandard living conditions, poorer nutrition, and delayed medical care. Over 50 to 70 years, these recurring hardships accumulate, gradually degrading physical and cognitive reserves.
- **Selective Survival (Mortality Selection / Survivor Bias):** A statistical phenomenon observed in populations with historically high mortality rates. In mid-20th-century India, infants and children born into severe poverty faced substantial risks of premature death. Consequently, impoverished individuals who successfully survived into late adulthood (past age 75) often possess exceptional biological hardiness, psychological resilience, or favorable genetic profiles. In cross-sectional surveys, this can cause the oldest-old disadvantaged survivors to appear as healthy as---or even healthier than---their wealthier peers, because the most vulnerable individuals died prior to study enrollment.
- **Cross-Sectional Baseline (Non-Causal Guardrail):** A single snapshot observation of a population at one point in time. Because LASI Wave 1 was collected cross-sectionally, we observe older adults at different ages simultaneously rather than tracking the same individual across their life. Therefore, statistical findings represent *cross-sectional associations* across cohort strata and cannot establish individual disease progression, longitudinal cognitive decline, or definitive cause-and-effect relationships.

### 2.2 Survey Sampling and Statistical Design
- **Primary Sampling Unit (PSU) and Secondary Sampling Unit (SSUID):** In massive national demographic surveys, interviewers cannot sample individuals randomly from a national registry. Instead, multi-stage cluster sampling is employed: first, geographic sub-districts (taluks or tehsils) are selected as Primary Sampling Units (PSUs); within those districts, specific rural villages or urban census enumeration blocks are selected as Secondary Sampling Units (SSUIDs). All households within sampled clusters are then enumerated.
- **Stratification (72 Strata):** The technique of dividing the total population into non-overlapping geographic subgroups (called "strata") before sampling. In LASI, 72 strata were created by crossing each of the 36 States and Union Territories with sector of residence (Rural vs. Urban). Stratification guarantees that the sample accurately represents every geographic and regional corner of India, preventing rural or remote regions from being overlooked.
- **Sampling Weights (`indiaindividualweight`):** To ensure reliable regional estimates, smaller states (such as Goa or Sikkim) were sampled at a higher rate relative to their population size than populous states (such as Uttar Pradesh). Sampling weights mathematically rescale each respondent's contribution so that one participant in an oversampled region represents fewer citizens and one in an undersampled region represents more citizens. Applying weights ensures that calculated statistics accurately reflect the national population of India.
- **Taylor Series Linearization (Cluster-Robust Standard Errors):** Households located in the same village share identical environmental risks, drinking water sources, local clinic infrastructure, and socioeconomic conditions. Because their health outcomes are mathematically correlated rather than independent, standard textbook formulas would underestimate uncertainty (yielding falsely narrow confidence intervals). Taylor series linearization calculates cluster-robust variance estimates by measuring variation between clusters centered within each stratum.
- **Survey Degrees of Freedom (df = 2,356):** In complex survey analysis, the degrees of freedom for statistical testing is determined not by the number of individual respondents (N = 66,606), but by the number of independent sampling clusters minus the number of strata (2,428 clusters - 72 strata = 2,356).
- **Proxy Interview (`rproxy`):** An interview protocol used when an older respondent was cognitively incapacitated, speech-impaired, severely ill, or deaf. An informed family member (proxy) answered basic demographic and health questions on the respondent's behalf. Because family proxies cannot complete direct cognitive performance tasks, proxy respondents (N = 705) were systematically excluded from direct cognitive assessment modules.

### 2.3 Cognitive Assessment and Mental Health Metrics
- **CES-D-10 Scale (Center for Epidemiologic Studies Depression):** A standardized 10-item psychiatric screening tool evaluating depressive symptom frequency during the past week (e.g., feelings of sadness, loneliness, fatigue, disrupted sleep, and hopelessness). Responses are aggregated into a score from 0 to 10; scores of &ge; 4.0 are clinically validated as indicating significant depressive symptoms.
- **Cognitive Battery and Item-Skip Bias:** A multi-domain assessment testing memory, temporal/spatial orientation, numeracy, executive function, and object naming. In developing nations with high illiteracy, respondents who never attended school are protocol-skipped on formal arithmetic tasks (e.g., serial 7 subtractions or backward counting). If skipped tasks are improperly coded as "zero points" (failure), the test inadvertently measures lack of formal schooling rather than neurological impairment.
- **Orientation vs. Word Recall Domains:** Orientation tests fundamental cognitive awareness of time and place (identifying the day, month, year, state, district, and local landmarks). Word recall tests episodic memory by reading a list of 10 common nouns to the respondent and recording immediate recall and delayed recall (after a short interference task).

### 2.4 Analytical Models and Epidemiological Estimands
- **Modified Poisson Regression vs. Odds Ratios (OR):** In medical studies, logistic regression is commonly used to produce Odds Ratios. However, when an outcome is common (such as depressive symptoms, which affect 28.2% of older Indians), Odds Ratios severely exaggerate relative risk (transforming a true 20% increase into a misleading 50% increase). Modified Poisson regression with robust standard errors estimates the **Prevalence Ratio (PR)**, which directly conveys the true relative percentage difference between groups.
- **Average Marginal Effects / Standardized Predictions (AME):** Instead of calculating predicted probabilities for a hypothetical "average person" (who does not realistically exist), AME takes every real individual in the survey sample, computes their predicted health probability under contrasting childhood conditions while preserving their actual age, sex, and comorbidities, and averages the results across the full population.
- **Inverse-Probability Weighting (IPW):** A statistical method designed to correct for potential selection bias caused by missing cognitive tests. Because frail, very old (75+), and unschooled respondents were more likely to have missing cognitive assessments, IPW statistically upweights the complete tests of similar respondents, mathematically restoring sample balance under the Missing at Random (MAR) assumption.
- **Monthly Per Capita Consumption Expenditure (MPCE):** The gold standard measure of economic status in Indian household surveys. In developing, largely rural economies, asking about formal annual income or wealth is notoriously unreliable due to informal labor and agricultural seasonality. MPCE measures total household spending on food, fuel, health, and consumer goods divided by household size.

## 3. Data and Empirical Methodology

- **Source:** LASI Wave 1 (2017–18), individual file; adults aged ≥45 (N = 66,606).
- **Design variables:** national individual weight, 2,439 `ssuid` clusters, 72 strata (state × residence). `ssuid` is a secondary sampling unit, and no PSU identifier exists in the release, so variances may be somewhat understated.
- **Exposures (retrospective, up to age 16):** childhood SES (`ht235`; "Varied" excluded from the main analysis), childhood health (`ht231`; Fair/Poor/Very poor vs Good/Very good), bedridden ≥1 month (`ht233`).
- **Outcomes:** (i) memory (immediate + delayed recall, 0–20) plus orientation (8 items), 0–28, with a binary indicator for the lowest weighted decile (≤11 points; 12.8% weighted prevalence); (ii) CES-D-10 ≥4 (28.2% weighted).
- **Covariates:** M1 = age, sex, residence, caste, marital status, state; M2 = M1 + education + MPCE quintile (primary); M3 = M2 + chronic-condition count + self-rated health (pathway/exploratory).
- **Estimation:** weighted modified Poisson (PR) for binary outcomes, weighted linear models for scores. Design-based confidence intervals use t with 2,356 degrees of freedom. Common complete-case samples: cognition N = 57,245; depression N = 62,047.

[Figure: fig1]

### Table 1. Sample characteristics (v1 descriptive table, unchanged; survey-weighted)
| Characteristic | Category | Unweighted_N | Weighted_Pct |
|---|---|---|---|
| Age Group | 45-59 | 34704 | 49.77 |
| Age Group | 60-74 | 25022 | 38.8 |
| Age Group | 75+ | 6880 | 11.42 |
| Sex | Female | 35567 | 54.06 |
| Sex | Male | 31039 | 45.94 |
| Place of Residence | Rural | 43240 | 68.53 |
| Place of Residence | Urban | 23366 | 31.47 |
| Social Group / Caste | General/None | 16295 | 24.84 |
| Social Group / Caste | OBC | 25212 | 46.66 |
| Social Group / Caste | SC | 11014 | 19.66 |
| Social Group / Caste | ST | 11746 | 8.84 |
| Marital Status | Divorced/Separated | 1006 | 1.23 |
| Marital Status | Married/Partnered | 49949 | 73.86 |
| Marital Status | Never Married | 868 | 1.19 |
| Marital Status | Widowed | 14780 | 23.72 |
| Educational Attainment | Graduate and above | 3429 | 5.19 |
| Educational Attainment | Higher secondary/Diploma | 3175 | 4.94 |
| Educational Attainment | Less than primary | 7598 | 10.92 |
| Educational Attainment | Middle completed | 6337 | 8.35 |
| Educational Attainment | No formal education | 31350 | 50.62 |
| Educational Attainment | Primary completed | 8761 | 12.05 |
| Educational Attainment | Secondary completed | 5953 | 7.93 |
| Household MPCE Quintile | 1 | 13181 | 20.86 |
| Household MPCE Quintile | 2 | 13403 | 21.24 |
| Household MPCE Quintile | 3 | 13371 | 20.49 |
| Household MPCE Quintile | 4 | 13412 | 19.42 |
| Household MPCE Quintile | 5 | 13239 | 17.99 |
| Childhood SES | Average | 35438 | 49.32 |
| Childhood SES | Poor | 25605 | 42.16 |
| Childhood SES | Pretty well-off | 4848 | 7.77 |
| Childhood SES | Varied | 394 | 0.76 |
| Childhood Health | Good | 58272 | 87.46 |
| Childhood Health | Poor | 7369 | 12.54 |
| Childhood Bedridden | No | 62881 | 94.25 |
| Childhood Bedridden | Yes | 3370 | 5.75 |
| Cumulative Disadvantage Score | 0.0 | 34506 | 48.19 |
| Cumulative Disadvantage Score | 1.0 | 26556 | 44.06 |
| Cumulative Disadvantage Score | 2.0 | 4003 | 6.86 |
| Cumulative Disadvantage Score | 3.0 | 466 | 0.88 |

[Figure: fig2]

### Table 2 (v2). Outcome prevalence and means by age group (design-based 95% CIs)
| Age_group | Outcome | Estimate | 95% CI | N |
|---|---|---|---|---|
| 45-59 | Cognitive impairment (%) | 7.61 | 7.0–8.22 | 32301 |
| 45-59 | Depressive symptoms (%) | 26.28 | 24.99–27.58 | 34009 |
| 45-59 | Mem+orient score (mean, 0-28) | 17.01 | 16.85–17.17 | 32301 |
| 45-59 | CES-D score (mean) | 2.86 | 2.81–2.91 | 34009 |
| 60-74 | Cognitive impairment (%) | 15.61 | 14.58–16.65 | 22223 |
| 60-74 | Depressive symptoms (%) | 29.1 | 27.8–30.41 | 24370 |
| 60-74 | Mem+orient score (mean, 0-28) | 15.51 | 15.38–15.65 | 22223 |
| 60-74 | CES-D score (mean) | 3.01 | 2.95–3.06 | 24370 |
| 75+ | Cognitive impairment (%) | 28.85 | 26.2–31.5 | 5257 |
| 75+ | Depressive symptoms (%) | 34.18 | 31.02–37.33 | 6446 |
| 75+ | Mem+orient score (mean, 0-28) | 13.88 | 13.65–14.11 | 5257 |
| 75+ | CES-D score (mean) | 3.27 | 3.15–3.39 | 6446 |
| All | Cognitive impairment (%) | 12.79 | 12.03–13.54 | 59781 |
| All | Depressive symptoms (%) | 28.24 | 27.19–29.28 | 64825 |
| All | Mem+orient score (mean, 0-28) | 16.13 | 16.0–16.25 | 59781 |
| All | CES-D score (mean) | 2.96 | 2.92–3.0 | 64825 |

## 4. What went wrong with the cognitive outcome, and what the fix did and did not do

In the v1 composite, impairment was classified in 21% of the unschooled and 0.1% of graduates. The v2 primary outcome still shows a steep schooling gradient, because recall and orientation also depend on education.

[Figure: figA1]

### Table S5. Weighted % classified impaired, by education and outcome definition
| Education | v1_composite_impaired_pct | v2_mem_orient_impaired_pct | v2_battery_impaired_pct | n_v2 |
|---|---|---|---|---|
| No formal education | 21.2 | 21.8 | 18.5 | 26760 |
| Less than primary | 7.3 | 10.5 | 5.9 | 6829 |
| Primary completed | 2.2 | 5.1 | 2.9 | 8147 |
| Middle completed | 0.9 | 2.2 | 1.1 | 5993 |
| Secondary completed | 0.3 | 1.4 | 0.6 | 5681 |
| Higher secondary/Diploma | 0.2 | 0.9 | 0.6 | 3056 |
| Graduate and above | 0.1 | 0.6 | 0.4 | 3314 |

**Take-away:** no absolute-threshold cognitive measure is free of education. Education-stratified analysis and the school-stratum-specific cut-off are therefore essential, not optional. The Model 2 attenuation below cannot be read as a "pathway" through education.

## 5. Primary Results: Cognition

### Table 3 (v2). Poor vs well-off childhood SES and other exposures with cognitive impairment (PR, 95% CI; common sample)
| Exposure | Model 0 | Model 1 | Model 2 | Model 3 |
|---|---|---|---|---|
| Childhood SES: Average | 0.97 (0.82–1.15) p=0.711 | 0.98 (0.84–1.14) p=0.777 | 0.80 (0.70–0.91) p<.001 | 0.80 (0.71–0.91) p<.001 |
| Childhood SES: Poor | 1.61 (1.33–1.96) p<.001 | 1.36 (1.16–1.59) p<.001 | 0.93 (0.82–1.05) p=0.241 | 0.91 (0.81–1.03) p=0.148 |
| Childhood bedridden ≥1 month | 0.90 (0.77–1.06) p=0.222 | 0.94 (0.81–1.09) p=0.404 | 1.00 (0.86–1.18) p=0.947 | 0.99 (0.84–1.16) p=0.868 |
| Childhood health: Fair/Poor/Very poor | 0.97 (0.81–1.17) p=0.773 | 0.97 (0.85–1.12) p=0.719 | 0.95 (0.82–1.10) p=0.487 | 0.95 (0.82–1.09) p=0.458 |

### Table 3b. Mean difference in memory + orientation score (points, 0–28)
| Exposure | Model 0 | Model 1 | Model 2 | Model 3 |
|---|---|---|---|---|
| Childhood SES: Poor | -1.65 (-1.95–-1.34) | -1.28 (-1.54–-1.01) | -0.32 (-0.56–-0.09) | -0.24 (-0.48–-0.01) |
| Childhood health: Fair/Poor/Very poor | -0.02 (-0.43–0.39) | -0.05 (-0.29–0.18) | 0.01 (-0.23–0.26) | 0.04 (-0.19–0.27) |

### Findings
- **Childhood SES.** Poor vs well-off: PR 1.61 (1.33–1.96) unadjusted and 1.36 (1.16–1.59) after demographics and state. After adult education and MPCE the association is not distinguishable from 1 (PR 0.93, 0.82–1.05). On the continuous score, a small residual deficit remains (−0.32 points, −0.56 to −0.09).
- **"Average" childhood SES** has a *lower* prevalence than well-off after adult SES adjustment (PR 0.80, 0.70–0.91). The well-off group's relatively high prevalence is unexplained here. Possible reasons are selective survival, differences in recall and reporting, or residual confounding; none of these was tested.
- **Childhood health and bedridden history** show no association with memory + orientation impairment in any model (PRs 0.90–1.00; all CIs include 1).
- **Mutual adjustment** (Table 6): the pattern is the same. Poor SES PR 1.36 (1.15–1.60) in M1 becomes 0.93 (0.82–1.06) in M2. The cumulative index gives PR 1.05 per adversity (0.995–1.12).

### Education-stratified and outcome-definition analyses (Table S4a/S4b)
| Analysis | Outcome | Term | Estimate (95% CI) | N |
|---|---|---|---|---|
| S4b Schooling stratum: Never attended school | Cognitive impairment (primary) | ses_poor | 0.91 (0.79–1.05) p=0.188 | 25684 |
| S4b Schooling stratum: Never attended school | Cognitive impairment (primary) | hlth_poor | 0.97 (0.83–1.15) p=0.745 | 25684 |
| S4b Schooling stratum: Never attended school | Cognitive impairment (school-stratum decile) | ses_poor | 0.92 (0.73–1.15) p=0.448 | 25684 |
| S4b Schooling stratum: Never attended school | Cognitive impairment (school-stratum decile) | hlth_poor | 1.01 (0.83–1.23) p=0.916 | 25684 |
| S4b Schooling stratum: Never attended school | Mem+orient continuous (beta) | ses_poor | -0.39 (-0.72–-0.05) p=0.025 | 25684 |
| S4b Schooling stratum: Any schooling | Cognitive impairment (primary) | ses_poor | 0.99 (0.76–1.29) p=0.950 | 31561 |
| S4b Schooling stratum: Any schooling | Cognitive impairment (primary) | hlth_poor | 0.81 (0.59–1.12) p=0.209 | 31561 |
| S4b Schooling stratum: Any schooling | Cognitive impairment (school-stratum decile) | ses_poor | 1.01 (0.82–1.23) p=0.940 | 31561 |
| S4b Schooling stratum: Any schooling | Cognitive impairment (school-stratum decile) | hlth_poor | 0.94 (0.78–1.14) p=0.525 | 31561 |
| S4b Schooling stratum: Any schooling | Mem+orient continuous (beta) | ses_poor | -0.18 (-0.47–0.10) p=0.208 | 31561 |

Among respondents who never attended school, poor childhood SES is not associated with impairment (PR 0.91, 0.79–1.05), but the continuous score shows a small deficit (−0.39 points, −0.73 to −0.05). Among those with any schooling, there is no association.

| Analysis | Outcome | Term | Estimate (95% CI) | N |
|---|---|---|---|---|
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Primary: lowest weighted decile mem+orient | ses_poor | 1.36 (1.16–1.59) p=0.000 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Primary: lowest weighted decile mem+orient | hlth_poor | 0.97 (0.85–1.12) p=0.719 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Primary: lowest weighted decile mem+orient | ses_poor | 0.93 (0.82–1.05) p=0.241 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Primary: lowest weighted decile mem+orient | hlth_poor | 0.95 (0.82–1.10) p=0.487 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Skip-aware full battery (% of max), lowest decile | ses_poor | 1.97 (1.60–2.42) p=0.000 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Skip-aware full battery (% of max), lowest decile | hlth_poor | 1.25 (1.11–1.41) p=0.000 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Skip-aware full battery (% of max), lowest decile | ses_poor | 1.29 (1.07–1.57) p=0.009 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Skip-aware full battery (% of max), lowest decile | hlth_poor | 1.22 (1.08–1.37) p=0.001 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Mem+orient, schooling-stratum-specific decile | ses_poor | 0.90 (0.78–1.04) p=0.171 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Mem+orient, schooling-stratum-specific decile | hlth_poor | 0.98 (0.85–1.14) p=0.794 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Mem+orient, schooling-stratum-specific decile | ses_poor | 1.00 (0.86–1.17) p=0.991 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Mem+orient, schooling-stratum-specific decile | hlth_poor | 0.98 (0.85–1.13) p=0.812 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Original v1 composite (skips scored 0) | ses_poor | 1.65 (1.34–2.04) p=0.000 | 58202 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Original v1 composite (skips scored 0) | hlth_poor | 1.13 (0.97–1.31) p=0.126 | 58202 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Original v1 composite (skips scored 0) | ses_poor | 1.04 (0.89–1.22) p=0.595 | 58202 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Original v1 composite (skips scored 0) | hlth_poor | 1.09 (0.92–1.29) p=0.310 | 58202 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Mem+orient continuous (beta, points) | ses_poor | -1.28 (-1.54–-1.01) p=0.000 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Mem+orient continuous (beta, points) | hlth_poor | -0.05 (-0.29–0.18) p=0.656 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Mem+orient continuous (beta, points) | ses_poor | -0.32 (-0.56–-0.09) p=0.007 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Mem+orient continuous (beta, points) | hlth_poor | 0.01 (-0.23–0.26) p=0.933 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Skip-aware battery continuous (beta, % of max) | ses_poor | -5.33 (-6.40–-4.25) p=0.000 | 57245 |
| S4a Alt. cognitive outcome / Model 1: Demographics + state | Skip-aware battery continuous (beta, % of max) | hlth_poor | -1.55 (-2.32–-0.77) p=0.000 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Skip-aware battery continuous (beta, % of max) | ses_poor | -1.75 (-2.49–-1.01) p=0.000 | 57245 |
| S4a Alt. cognitive outcome / Model 2: + Adult SES (Primary) | Skip-aware battery continuous (beta, % of max) | hlth_poor | -1.29 (-2.09–-0.49) p=0.002 | 57245 |

**Result that complicates the story.** On the *skip-aware full battery*, which adds arithmetic, executive and naming domains, poor childhood SES (PR 1.29, 1.07–1.57) and poor childhood health (PR 1.22, 1.08–1.37) remain associated with impairment after education and MPCE adjustment. With memory + orientation only, they do not. The cognition conclusion therefore **depends on how cognition is measured**. We do not claim to know which measure is more valid. Extra domains may capture executive or numeracy function that is more sensitive to early disadvantage. They may also carry literacy, vision or motor-skill effects that education adjustment does not fully remove.

### Missingness and IPW
Cognition scores are missing for 7.8% of direct interviewees overall, and the missingness is selective:

| Variable | Level | N | Pct_missing_cognition |
|---|---|---|---|
| age_group | 45-59 | 34566 | 6.6 |
| age_group | 60-74 | 24772 | 10.3 |
| age_group | 75+ | 6563 | 19.9 |
| education | Graduate and above | 3414 | 2.9 |
| education | Higher secondary/Diploma | 3159 | 3.3 |
| education | Less than primary | 7526 | 9.3 |
| education | Middle completed | 6301 | 4.9 |
| education | No formal education | 30873 | 13.3 |
| education | Primary completed | 8710 | 6.5 |
| education | Secondary completed | 5916 | 4.0 |
| childhood_ses | Average | 35098 | 7.3 |
| childhood_ses | Poor | 25309 | 11.2 |
| childhood_ses | Pretty well-off | 4808 | 8.7 |
| childhood_ses | Varied | 389 | 10.3 |
| sex | Female | 35191 | 10.7 |
| sex | Male | 30710 | 7.7 |

[Figure: figA2]

IPW using covariates, exposures and CES-D availability left the estimates essentially unchanged (Poor SES, M2: 0.928 both ways):

| Exposure | Complete-case | IPW-adjusted |
|---|---|---|
| Childhood SES: Average (vs well-off) | 0.80 (0.70–0.91) | 0.80 (0.71–0.90) |
| Childhood SES: Poor (vs well-off) | 0.93 (0.82–1.05) | 0.93 (0.82–1.05) |
| Childhood SES: Poor (vs well-off) [joint SES model] | 0.93 (0.82–1.05) | 0.93 (0.82–1.05) |
| Childhood bedridden ≥1 month (vs No) | 1.00 (0.86–1.18) | 1.00 (0.86–1.17) |
| Childhood health: Fair/Poor/Very poor (vs Good/Very good) | 0.95 (0.82–1.10) | 0.94 (0.81–1.09) |

This addresses missingness only under a missing-at-random assumption given the model covariates. It cannot address missingness that depends on unmeasured cognitive status.

## 6. Primary Results: Depressive Symptoms

### Table 4 (v2). Depressive symptoms (CES-D ≥4): PR, 95% CI, common sample
| Exposure | Model 0 | Model 1 | Model 2 | Model 3 |
|---|---|---|---|---|
| Childhood SES: Average | 1.10 (0.94–1.30) p=0.233 | 1.20 (1.01–1.44) p=0.039 | 1.15 (0.99–1.33) p=0.072 | 1.14 (0.99–1.32) p=0.071 |
| Childhood SES: Poor | 1.17 (1.00–1.37) p=0.044 | 1.31 (1.09–1.58) p=0.004 | 1.21 (1.03–1.42) p=0.019 | 1.15 (0.99–1.34) p=0.068 |
| Childhood bedridden ≥1 month | 1.14 (1.01–1.29) p=0.037 | 1.14 (1.01–1.27) p=0.034 | 1.16 (1.05–1.28) p=0.004 | 1.11 (1.01–1.23) p=0.029 |
| Childhood health: Fair/Poor/Very poor | 1.33 (1.20–1.47) p<.001 | 1.21 (1.08–1.36) p=0.002 | 1.20 (1.07–1.34) p=0.002 | 1.19 (1.06–1.33) p=0.002 |

### Findings
- **Childhood health:** poor vs good is associated with a 33% higher prevalence unadjusted (PR 1.33, 1.20–1.47) and 20% higher after adult SES (PR 1.20, 1.07–1.34). v1 reported 1.31 for Model 2; the difference comes mainly from the common sample, state fixed effects and the design-based variance.
- **Childhood SES:** poor vs well-off, PR 1.21 (1.03–1.42) in M2, falling to 1.15 (0.99–1.34) once adult health is added.
- **Bedridden ≥1 month:** PR 1.16 (1.05–1.28) in M2 and 1.11 (1.01–1.23) in M3.
- **Cumulative index:** each additional childhood adversity is associated with a PR of 1.11 (1.07–1.16).
- **Mutual adjustment (Table 6):** in M2, poor SES 1.19 (1.02–1.38), poor health 1.18 (1.05–1.32) and bedridden 1.12 (1.00–1.26) are each associated with depression, so the three are partly separable. In M3, only childhood health keeps a CI excluding 1 (1.17, 1.05–1.32).
- **Share attenuated by adult SES:** the Poor-SES log-PR falls by about 30% between M1 and M2. The association with childhood health attenuates little (1.21 → 1.20).

| Outcome | Model | Exposure | PR (95% CI) | N |
|---|---|---|---|---|
| Cognitive impairment | Model 1: Demographics + state | Childhood SES: Average | 0.98 (0.84–1.14) p=0.792 | 57245 |
| Cognitive impairment | Model 1: Demographics + state | Childhood SES: Poor | 1.36 (1.15–1.60) p=0.000 | 57245 |
| Cognitive impairment | Model 1: Demographics + state | Childhood health: Fair/Poor/Very poor | 0.97 (0.84–1.12) p=0.681 | 57245 |
| Cognitive impairment | Model 1: Demographics + state | Childhood bedridden ≥1 month | 0.94 (0.81–1.10) p=0.430 | 57245 |
| Cognitive impairment | Model 2: + Adult SES (Primary) | Childhood SES: Average | 0.80 (0.70–0.91) p=0.001 | 57245 |
| Cognitive impairment | Model 2: + Adult SES (Primary) | Childhood SES: Poor | 0.93 (0.82–1.06) p=0.277 | 57245 |
| Cognitive impairment | Model 2: + Adult SES (Primary) | Childhood health: Fair/Poor/Very poor | 0.95 (0.82–1.10) p=0.533 | 57245 |
| Cognitive impairment | Model 2: + Adult SES (Primary) | Childhood bedridden ≥1 month | 1.01 (0.86–1.18) p=0.941 | 57245 |
| Cognitive impairment | Model 3: + Adult health (Pathway) | Childhood SES: Average | 0.81 (0.71–0.92) p=0.001 | 57245 |
| Cognitive impairment | Model 3: + Adult health (Pathway) | Childhood SES: Poor | 0.91 (0.81–1.04) p=0.171 | 57245 |
| Cognitive impairment | Model 3: + Adult health (Pathway) | Childhood health: Fair/Poor/Very poor | 0.95 (0.83–1.10) p=0.514 | 57245 |
| Cognitive impairment | Model 3: + Adult health (Pathway) | Childhood bedridden ≥1 month | 0.99 (0.84–1.17) p=0.892 | 57245 |
| Cognitive impairment | Model 2: + Adult SES (Primary) [cumulative index 0-3] | Per additional childhood adversity (Poor SES + poor health + bedridden) | 1.05 (0.99–1.12) p=0.071 | 57245 |
| Depressive symptoms | Model 1: Demographics + state | Childhood SES: Average | 1.18 (1.00–1.39) p=0.044 | 62047 |
| Depressive symptoms | Model 1: Demographics + state | Childhood SES: Poor | 1.29 (1.08–1.54) p=0.005 | 62047 |
| Depressive symptoms | Model 1: Demographics + state | Childhood health: Fair/Poor/Very poor | 1.19 (1.05–1.34) p=0.005 | 62047 |
| Depressive symptoms | Model 1: Demographics + state | Childhood bedridden ≥1 month | 1.10 (0.97–1.25) p=0.147 | 62047 |
| Depressive symptoms | Model 2: + Adult SES (Primary) | Childhood SES: Average | 1.13 (0.98–1.29) p=0.090 | 62047 |
| Depressive symptoms | Model 2: + Adult SES (Primary) | Childhood SES: Poor | 1.19 (1.02–1.38) p=0.026 | 62047 |
| Depressive symptoms | Model 2: + Adult SES (Primary) | Childhood health: Fair/Poor/Very poor | 1.18 (1.05–1.32) p=0.006 | 62047 |
| Depressive symptoms | Model 2: + Adult SES (Primary) | Childhood bedridden ≥1 month | 1.12 (1.00–1.26) p=0.044 | 62047 |
| Depressive symptoms | Model 3: + Adult health (Pathway) | Childhood SES: Average | 1.12 (0.98–1.29) p=0.087 | 62047 |
| Depressive symptoms | Model 3: + Adult health (Pathway) | Childhood SES: Poor | 1.13 (0.98–1.31) p=0.089 | 62047 |
| Depressive symptoms | Model 3: + Adult health (Pathway) | Childhood health: Fair/Poor/Very poor | 1.17 (1.05–1.31) p=0.006 | 62047 |
| Depressive symptoms | Model 3: + Adult health (Pathway) | Childhood bedridden ≥1 month | 1.08 (0.97–1.21) p=0.157 | 62047 |
| Depressive symptoms | Model 2: + Adult SES (Primary) [cumulative index 0-3] | Per additional childhood adversity (Poor SES + poor health + bedridden) | 1.11 (1.07–1.16) p=0.000 | 62047 |

[Figure: fig6]

## 7. Age Heterogeneity (Hypothesis 4)

### Table 5a (v2). Joint Wald F tests of exposure × age-group interaction
| Outcome | Exposure | joint_F | df_num | joint_p | N |
|---|---|---|---|---|---|
| Cognitive impairment | Childhood SES | 2.439 | 4 | 0.0451 | 57245 |
| Cognitive impairment | Childhood health | 0.322 | 2 | 0.7249 | 57245 |
| Cognitive impairment | Childhood bedridden | 0.271 | 2 | 0.7628 | 57245 |
| Depressive symptoms | Childhood SES | 0.34 | 4 | 0.8513 | 62047 |
| Depressive symptoms | Childhood health | 0.306 | 2 | 0.7361 | 62047 |
| Depressive symptoms | Childhood bedridden | 0.021 | 2 | 0.9795 | 62047 |

Only one of six tests (SES × age for cognition, p = 0.045) is below 0.05. It would not survive a Bonferroni correction (0.05/6 = 0.008). All other joint tests have p > 0.7.

### Table 5b. Standardized prevalence (%) by childhood SES and age group
| Outcome | age_group | Pretty well-off | Average | Poor |
|---|---|---|---|---|
| Cognitive impairment | 45-59 | 8.16 (6.7–10.13) | 6.38 (5.79–7.19) | 8.45 (7.75–9.35) |
| Cognitive impairment | 60-74 | 16.86 (14.52–20.2) | 14.2 (13.26–15.56) | 16.16 (15.2–17.29) |
| Cognitive impairment | 75+ | 36.87 (30.9–43.95) | 27.48 (24.99–31.02) | 28.04 (26.12–31.36) |
| Depressive symptoms | 45-59 | 22.69 (20.01–25.66) | 26.08 (24.68–27.66) | 27.01 (25.38–29.04) |
| Depressive symptoms | 60-74 | 24.13 (19.66–29.45) | 28.42 (27.14–30.34) | 30.33 (28.83–32.23) |
| Depressive symptoms | 75+ | 31.58 (23.9–42.81) | 33.0 (29.66–36.8) | 35.56 (32.19–39.99) |

### Table 5c. Risk differences, Poor vs well-off childhood SES (and other exposures), by age group
| Outcome | Exposure | age_group | contrast | RD pp (95% CI) |
|---|---|---|---|---|
| Cognitive impairment | Childhood SES | 45-59 | Poor - Pretty well-off | 0.29 (-1.91 to 1.95) |
| Cognitive impairment | Childhood SES | 60-74 | Poor - Pretty well-off | -0.71 (-3.94 to 2.07) |
| Cognitive impairment | Childhood SES | 75+ | Poor - Pretty well-off | -8.83 (-16.21 to -1.38) |
| Cognitive impairment | Childhood health | 45-59 | Poor - Good | -0.72 (-2.39 to 1.02) |
| Cognitive impairment | Childhood health | 60-74 | Poor - Good | -0.12 (-2.54 to 2.64) |
| Cognitive impairment | Childhood health | 75+ | Poor - Good | -2.42 (-8.63 to 4.82) |
| Cognitive impairment | Childhood bedridden | 45-59 | Yes - No | 0.56 (-0.9 to 2.26) |
| Cognitive impairment | Childhood bedridden | 60-74 | Yes - No | -0.62 (-3.65 to 2.95) |
| Cognitive impairment | Childhood bedridden | 75+ | Yes - No | -0.04 (-10.44 to 16.22) |
| Depressive symptoms | Childhood SES | 45-59 | Poor - Pretty well-off | 4.32 (0.57 to 7.77) |
| Depressive symptoms | Childhood SES | 60-74 | Poor - Pretty well-off | 6.2 (0.92 to 10.95) |
| Depressive symptoms | Childhood SES | 75+ | Poor - Pretty well-off | 3.98 (-5.54 to 11.52) |
| Depressive symptoms | Childhood health | 45-59 | Poor - Good | 5.0 (0.9 to 10.16) |
| Depressive symptoms | Childhood health | 60-74 | Poor - Good | 6.82 (2.42 to 11.87) |
| Depressive symptoms | Childhood health | 75+ | Poor - Good | 2.25 (-6.71 to 12.89) |
| Depressive symptoms | Childhood bedridden | 45-59 | Yes - No | 3.91 (-1.01 to 8.94) |
| Depressive symptoms | Childhood bedridden | 60-74 | Yes - No | 4.28 (0.19 to 8.1) |
| Depressive symptoms | Childhood bedridden | 75+ | Yes - No | 6.73 (-6.68 to 27.94) |

[Figure: fig4]
[Figure: fig5]

- **Cognition:** the nominal interaction arises from the 75+ group, where the well-off group's standardized prevalence (36.9%, 30.9–44.0) is *higher* than the Poor group's (28.0%, 26.1–31.4). This is opposite to the hypothesized direction. It rests on 5,257 people, and 19.9% of the 75+ group lack a score. We treat it as exploratory.
- **Depression:** no interaction on the relative scale (p = 0.85). The absolute gap for poor SES is 4.3 pp (0.6 to 7.8) at 45–59 and 6.2 pp (0.9 to 11.0) at 60–74. At 75+ it is 4.0 pp with a CI spanning zero (−5.5 to 11.5), which is imprecise rather than evidence of convergence.
- **Hypothesis 4 is therefore not supported.** Explanations such as survivor selection are speculative. Age and birth cohort cannot be separated in a cross-section.

## 8. Sensitivity Analyses (Depression and Other Checks)
| Analysis | Outcome | Term | Estimate (95% CI) | N |
|---|---|---|---|---|
| S4c SES incl. Varied category / M2 | Cognitive impairment | v_poor | 0.93 (0.82–1.06) p=0.279 | 57597 |
| S4c SES incl. Varied category / M2 | Cognitive impairment | v_var | 1.39 (0.93–2.08) p=0.105 | 57597 |
| S4c SES incl. Varied category / M2 | Depressive symptoms | v_poor | 1.20 (1.03–1.41) p=0.021 | 62429 |
| S4c SES incl. Varied category / M2 | Depressive symptoms | v_var | 1.18 (0.89–1.57) p=0.253 | 62429 |
| S4d Exclude age>=100 / M2 | Cognitive impairment | ses_poor | 0.93 (0.82–1.05) p=0.242 | 57226 |
| S4d Exclude age>=100 / M2 | Cognitive impairment | hlth_poor | 0.95 (0.82–1.10) p=0.492 | 57226 |
| S4d Exclude age>=100 / M2 | Depressive symptoms | ses_poor | 1.21 (1.03–1.41) p=0.019 | 62011 |
| S4d Exclude age>=100 / M2 | Depressive symptoms | hlth_poor | 1.20 (1.07–1.34) p=0.002 | 62011 |
| S4e Depression: modified Poisson PR / M2 | CES-D>=4 | hlth_poor | 1.20 (1.07–1.34) p=0.002 | 62047 |
| S4e Depression: logistic OR / M2 | CES-D>=4 | hlth_poor | 1.33 (1.11–1.58) p=0.002 | 62047 |
| S4e Depression: continuous CES-D / M2 | CES-D score 0-10 (beta) | hlth_poor | 0.36 (0.25–0.48) p=0.000 | 62047 |
| S4e Depression: continuous CES-D / M2 | CES-D score 0-10 (beta) | ses_poor | 0.32 (0.15–0.50) p=0.000 | 62047 |
| S4e Childhood health 5-level, per-level trend / M2 | CES-D>=4 | h5 | 1.12 (1.07–1.16) p=0.000 | 62047 |
| S4e Childhood health 5-level, per-level trend / M2 | Cognitive impairment | h5 | 1.03 (0.98–1.09) p=0.260 | 57245 |
| S4f Sex-stratified (mutually adjusted, M2): Female | Cognitive impairment | ses_poor | 0.97 (0.84–1.13) p=0.712 | 30115 |
| S4f Sex-stratified (mutually adjusted, M2): Female | Cognitive impairment | hlth_poor | 0.98 (0.84–1.15) p=0.842 | 30115 |
| S4f Sex-stratified (mutually adjusted, M2): Female | Cognitive impairment | bed_yes | 1.09 (0.87–1.38) p=0.443 | 30115 |
| S4f Sex-stratified (mutually adjusted, M2): Female | Depressive symptoms | ses_poor | 1.23 (1.01–1.49) p=0.037 | 33226 |
| S4f Sex-stratified (mutually adjusted, M2): Female | Depressive symptoms | hlth_poor | 1.21 (1.09–1.35) p=0.001 | 33226 |
| S4f Sex-stratified (mutually adjusted, M2): Female | Depressive symptoms | bed_yes | 1.10 (0.99–1.23) p=0.069 | 33226 |
| S4f Sex-stratified (mutually adjusted, M2): Male | Cognitive impairment | ses_poor | 0.83 (0.65–1.07) p=0.147 | 27130 |
| S4f Sex-stratified (mutually adjusted, M2): Male | Cognitive impairment | hlth_poor | 0.89 (0.72–1.09) p=0.248 | 27130 |
| S4f Sex-stratified (mutually adjusted, M2): Male | Cognitive impairment | bed_yes | 0.86 (0.67–1.10) p=0.237 | 27130 |
| S4f Sex-stratified (mutually adjusted, M2): Male | Depressive symptoms | ses_poor | 1.14 (0.96–1.35) p=0.146 | 28821 |
| S4f Sex-stratified (mutually adjusted, M2): Male | Depressive symptoms | hlth_poor | 1.15 (0.99–1.34) p=0.075 | 28821 |
| S4f Sex-stratified (mutually adjusted, M2): Male | Depressive symptoms | bed_yes | 1.13 (0.94–1.35) p=0.198 | 28821 |

- The logistic OR for childhood health and depression (1.33) exceeds the modified-Poisson PR (1.20). The outcome is common (28%), so the OR overstates the relative prevalence.
- Continuous CES-D: childhood health +0.37 points (0.25–0.48); poor SES +0.32 (0.15–0.50).
- Five-level childhood health: PR 1.12 per level (1.07–1.16) for depression; 1.03 (0.98–1.09) for cognition.
- Sex-stratified depression estimates are similar in direction (women: health PR 1.21, 1.09–1.35; men: 1.15, 0.99–1.34).
- Excluding ages ≥100, or including the "Varied" SES category, leaves the conclusions unchanged.

## 9. Hypotheses: Updated Verdicts

| Hypothesis | Cognition | Depression |
|---|---|---|
| H1 Childhood SES | Associated with impairment before adult SES adjustment (PR 1.36, M1); no association after education/MPCE on the primary outcome. Persists on the broader battery (PR 1.29). | Supported (PR 1.21, 1.03–1.42, M2). |
| H2 Childhood health | Not supported on memory + orientation (PR 0.95). Supported on the broader battery (PR 1.22). | Supported (PR 1.20, 1.07–1.34, M2; persists in M3). |
| H3 Bedridden ≥1 month | Not supported (PR 1.00). | Modestly supported (PR 1.16, 1.05–1.28; lower CI near 1 under mutual adjustment). |
| H4 Age heterogeneity | Not supported robustly (one nominal p = 0.045, in the opposite direction at 75+). | Not supported (all p > 0.7). |
| H5 Attenuation after adult SES | Attenuation seen for SES, but the primary outcome is itself education-linked, so no pathway interpretation. | Partial attenuation for SES (~30% of the log-PR); little for childhood health. |

## 10. Study Limitations

1. **Cross-sectional design.** No temporal ordering of outcome and measured adult covariates. Education and MPCE are adjusted for but cannot be treated as mediators.
2. **Cognitive measurement.** Every threshold-based measure is related to education (Figure A1), and conclusions differ by outcome definition (Section 4).
3. **Retrospective exposures.** Childhood conditions were reported at ages 45–116. Recall error and mood-congruent reporting are plausible, especially for depression, where both exposure and outcome are self-reported.
4. **Missing cognition scores** are selective by age, education, sex and childhood SES. IPW assumes missing-at-random.
5. **Survey design.** `ssuid` is the only clustering variable available.
6. **Survivor selection** in the oldest ages may mask or reverse gradients.
7. **Multiple testing.** About 40 exposure × model × outcome estimates are reported without formal correction.
8. **Residual confounding** by factors such as childhood nutrition, parental education and migration is possible.

## 11. Conclusions with Empirical Evidence

1. **Depressive symptoms are the more robust finding.** Poor childhood health (PR 1.20, 95% CI 1.07–1.34), poor childhood SES (1.21, 1.03–1.42) and bedridden illness (1.16, 1.05–1.28) are each associated with a higher prevalence of CES-D ≥4. These estimates persist after adult education and household expenditure. They also hold in mutually adjusted models (1.19, 1.18, 1.12), on the continuous CES-D score, in sex-stratified analyses, and per level of childhood health (1.12). The cumulative-disadvantage index gives PR 1.11 per adversity (1.07–1.16).
2. **The cognition result is not robust.** On the memory + orientation outcome, the association with poor childhood SES (PR 1.36) disappears after adult education and expenditure (PR 0.93, 0.82–1.05). Childhood health and bedridden history show no association (PRs ≈ 0.95–1.00). On the broader skip-aware battery, the associations remain (PR 1.29 and 1.22). The conclusion therefore depends on which cognitive tasks are used.
3. **The v1 claim that adult schooling "fully mediates" the SES–cognition link was not supported.** The outcome itself is education-linked, and mediation cannot be assessed here.
4. **There is no robust evidence of age heterogeneity.** Joint tests were null except one nominal result (p = 0.045, cognition) in the opposite direction at 75+.
5. **Informative missingness did not change the estimates** under IPW (Poor SES, M2: 0.928 both ways), within the missing-at-random assumption.
6. **Implication:** the evidence favours early-life health and socioeconomic disadvantage as correlates of depressive symptoms in older Indian adults. For cognition, an education-adjusted memory + orientation outcome shows no such pattern, and the broader battery does. We recommend longitudinal follow-up (LASI Wave 2 onwards) and education-fair cognitive measures before drawing policy conclusions about cognition.

## Appendix: reproducibility
Scripts: `code/07_build_dataset_v2.py`, `code/survey_utils.py`, `code/08_models_v2.py`, `code/09_forest_plot_v2.py`, `code/10_generate_report_v2.py`. Tables: `outputs/tables_v2/`. Figures: `outputs/figures_v2/`.
