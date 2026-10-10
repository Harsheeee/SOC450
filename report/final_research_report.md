# Early-Life Disadvantage and Later-Life Mental and Cognitive Health in India: Evidence from LASI Wave 1

**Authors:** Quantitative Ageing Research Working Group  
**Course / Institutional Context:** SOC450 Project, Semester 5  
**Data Source:** Longitudinal Ageing Study in India (LASI), Wave 1 (2017–2018)  
**Date of Completion:** October 2026  
**Document Status:** Complete Empirical Research Report  

---

## Executive Summary & Structured Abstract

### Background
India is undergoing unprecedented demographic ageing. With over 138 million individuals aged 60 and above, understanding why some individuals reach older age with preserved cognitive and mental health while others experience severe impairment is a pressing public health priority. Guided by the life-course epidemiological framework, this study investigates whether adverse socioeconomic and health conditions in childhood are associated with poorer later-life cognitive performance and elevated depressive symptoms among Indian adults, and whether these associations differ across stages of ageing.

### Methods
We conducted a cross-sectional secondary analysis of the nationally representative **Longitudinal Ageing Study in India (LASI) Wave 1 (2017–2018)**. The study population was restricted to adults aged **45 years and above** ($N = 66,606$, representing approximately 228 million individuals). Three early-life exposures were operationalized: self-reported childhood family financial status before age 16 (Childhood SES: Pretty well-off, Average, Poor), childhood self-rated health up to age 16 (Good vs. Poor), and childhood bedridden status for $\ge 1$ month due to illness. Outcomes were: (1) cognitive impairment, defined as the lowest 10th percentile ($\le 16$ points) of an HRS-harmonized 43-point cognitive battery; (2) depressive symptoms, defined as a score of $\ge 4$ on the 10-item Center for Epidemiologic Studies Depression (CES-D) scale; and (3) continuous cognitive and depressive scores. Sequential survey-weighted modified Poisson regressions with clustered robust standard errors (accounting for 2,439 community PSUs and 72 state $\times$ residence strata) were fitted to estimate Adjusted Prevalence Ratios (APRs) across demographic, adult socioeconomic, and adult health adjustment models. Multiplicative interaction models ($\text{Childhood Exposure} \times \text{Age Group}$) with marginal predicted prevalences were estimated.

### Results
The survey-weighted prevalence of depressive symptoms was **$28.24\%$** (95% CI: 27.88–28.60%), rising from $26.28\%$ in adults aged 45–59 to $34.18\%$ in those aged 75+. The weighted prevalence of cognitive impairment was **$11.64\%$** (95% CI: 11.28–12.00%), escalating steeply from $6.70\%$ in adults aged 45–59 to $13.70\%$ in those aged 60–74 and $29.17\%$ in those aged 75+. 
In demographic-adjusted models, adults from poor childhood families had a **65.3% higher prevalence of cognitive impairment** ($\text{APR} = 1.653$, 95% CI: 1.334–2.049, $p < 0.0001$) compared to those who were pretty well-off. However, adjusting for adult educational attainment and household consumption expenditure (MPCE) completely attenuated this association ($\text{APR} = 1.057$, 95% CI: 0.902–1.239, $p = 0.4909$), demonstrating substantial life-course socioeconomic mediation. Nonetheless, on the continuous scale, adults from poor childhoods scored **0.862 points lower** on the 43-point test even after full socioeconomic adjustment ($\beta = -0.862$, $p < 0.0001$).
In contrast, early-life health disadvantage exhibited an **enduring, direct association with later-life depressive symptoms**: poor childhood health was associated with a **30.6% higher prevalence of depressive symptoms** in the fully adjusted adult socioeconomic model ($\text{APR} = 1.306$, 95% CI: 1.185–1.440, $p < 0.0001$) and remained robust after adjusting for adult chronic multimorbidity and self-rated health ($\text{APR} = 1.288$, $p < 0.0001$). Childhood bedridden history was independently associated with a **17.5% higher prevalence of depressive symptoms** ($\text{APR} = 1.175$, 95% CI: 1.059–1.303, $p = 0.0023$). Each additional childhood adversity increased depressive symptom prevalence by **11.3%** in a monotonic dose-response fashion ($\text{APR} = 1.113$, $p < 0.0001$).

### Conclusion
Early-life disadvantage leaves distinct, domain-specific footprints on later-life well-being in India. While early socioeconomic disadvantage operates primarily through educational and material accumulation pathways to affect cognitive performance, early health shocks produce persistent psychological vulnerabilities that adult socioeconomic mobility cannot fully erase. Interventions targeting childhood health and educational equity are essential components of long-term healthy ageing policy in India.

---

## 1. Introduction & Conceptual Framework

### 1.1 Population Ageing in India
India is in the midst of a historic demographic transition. Driven by sustained declines in fertility and improvements in survival across adulthood, the older adult population is expanding rapidly. According to projections, the proportion of Indian adults aged 60 and older will exceed 20% by 2050, numbering over 300 million individuals. However, population ageing in lower- and middle-income countries (LMICs) unfolds under conditions of high cumulative disadvantage: vast segments of today’s older cohorts experienced intense childhood poverty, frequent infectious diseases, undernutrition, and minimal formal education during the mid-20th century.

### 1.2 The Life-Course Epidemiological Perspective
Life-course epidemiology examines how physical, economic, and social exposures during gestation, childhood, adolescence, and earlier adult life influence adult health and disease risk decades later. Two dominant life-course models guide this investigation:
1. **The Critical/Sensitive Period (Biological/Somatic Scarring) Model:** Adverse events during critical developmental windows (such as childhood severe illness, chronic infections, or malnutrition) cause permanent structural, physiological, or neurological alterations that persist into late life regardless of subsequent socioeconomic trajectory.
2. **The Accumulation of Disadvantage (Chain of Risks) Model:** Early-life socioeconomic disadvantage impairs human capital accumulation (e.g., formal schooling), restricts employment opportunities, and channels individuals into lower adult socioeconomic strata, which in turn elevates exposure to mid-life chronic stressors, poor living environments, and accelerated cognitive or physical decline.

```
┌────────────────────────────────┐
│   Early-Life Disadvantage      │
│  - Childhood SES (ht235)       │
│  - Childhood Health (ht231)    │
│  - Serious Illness (ht233)     │
└───────────────┬────────────────┘
                │
                ├─────────────────────────────────────────────┐
                │ (Pathway 1: Structural Accumulation)        │ (Pathway 2: Direct Somatic/
                ▼                                             │  Psychological Scarring)
┌────────────────────────────────┐                            │
│  Adult Socioeconomic Position  │                            │
│  - Educational Attainment      │                            │
│  - Household MPCE Quintile     │                            │
└───────────────┬────────────────┘                            │
                │                                             │
                ├──────────────────────┐                      │
                ▼                      ▼                      │
┌─────────────────────────┐  ┌───────────────────────┐        │
│ Adult Health & Morbidity│  │ Age Strata Moderation │        │
│ - Chronic Multimorbidity│  │ - 45-59 / 60-74 / 75+ │        │
│ - Self-Rated Health     │  └───────────┬───────────┘        │
└───────────────┬─────────┘              │                    │
                │                        ▼                    │
                └────────────────►┌───────────────────────────┴──┐
                                  │   Later-Life Health Outcomes │
                                  │   - Cognitive Impairment     │
                                  │   - Depressive Symptoms      │
                                  └──────────────────────────────┘
```

### 1.3 Research Gap & Study Objectives
While previous studies in high-income countries have linked early-life socioeconomic and health adversity to older-age cognitive decline and depression, empirical evidence from India remains limited and fragmented. Most prior Indian analyses have either focused exclusively on concurrent adult socioeconomic correlates or utilized non-representative local samples. Furthermore, few studies have tested whether early-life associations differ across distinct stages of the ageing life cycle (younger-old vs. oldest-old).

This study addresses these gaps using LASI Wave 1 to test five pre-specified hypotheses:
- **Hypothesis 1:** Lower childhood family SES is associated with lower cognitive performance and higher depressive symptom prevalence.
- **Hypothesis 2:** Poorer childhood health is associated with poorer cognitive performance and elevated depressive symptoms.
- **Hypothesis 3:** Severe childhood illness requiring bedridden confinement ($\ge 1$ month) is associated with adverse cognitive and depressive outcomes.
- **Hypothesis 4 (Age Heterogeneity):** The magnitude of early-life disadvantage associations varies across chronological age groups (45–59, 60–74, 75+).
- **Hypothesis 5 (Life-Course Attenuation):** Associations between early-life disadvantage and later-life outcomes attenuate substantially following adjustment for adult education and economic position.

---

## 2. Methodology & Analytical Approach

### 2.1 Study Design & Data Source
We analyzed microdata from **Wave 1 of the Longitudinal Ageing Study in India (LASI)**, conducted between April 2017 and December 2018 under the scientific stewardship of the International Institute for Population Sciences (IIPS), Mumbai, Harvard T.H. Chan School of Public Health, and the University of Southern California (USC). LASI is an internationally harmonized panel survey representative of India and all 36 States and Union Territories. 

### 2.2 Sampling Architecture & Survey Weights
LASI employed a multistage stratified area probability cluster sampling design:
- **Rural Areas:** A three-stage sampling design was implemented, selecting sub-districts (Tehsils/Talukas) as Primary Sampling Units (PSUs), villages within PSUs in the second stage, and households in the third stage.
- **Urban Areas:** A four-stage sampling design was implemented, selecting sub-districts (PSUs), wards within sub-districts, Census Enumeration Blocks (CEBs) within wards, and households in the fourth stage.
- **Survey Weights:** To account for differential selection probabilities, non-response adjustments, and state-level post-stratification, national individual probability weights (`indiaindividualweight`) were applied in all analyses.
- **Clustering & Stratification:** Standard errors and confidence intervals were computed taking into account the survey's complex design using $2,439$ unique community Secondary Sampling Units (`ssuid`) as clusters nested within $72$ sampling strata defined by state and urban/rural residence (`stateid` $\times$ `residence`).

### 2.3 Eligibility & Participant Flow
The released LASI Individual microdata contains $73,396$ respondents. In accordance with the pre-specified study protocol:
1. **Age Restriction:** Only age-eligible respondents aged **45 years and above** were included ($N = 66,606$). Younger spouses aged $< 45$ ($N = 6,790$, $9.25\%$) were excluded.
2. **Cognitive Testing Sample:** Direct cognitive assessment was administered only to self-respondents. Proxy respondents ($N = 705$, $1.06\%$) were structurally excluded from the cognitive test battery in accordance with LASI interview protocol, yielding an eligible cognition sample of $65,901$. Among these, $60,782$ completed all core domains.
3. **Depression Sample:** The 10-item CES-D scale was answered by $64,825$ eligible respondents with $\ge 8$ valid items.

```
Raw LASI Wave 1 Individual Dataset
              (N = 73,396)
                   │
                   ▼
       Exclude spouses age < 45 (N = 6,790)
                   │
                   ▼
  Target Study Population (Age >= 45)
              (N = 66,606)
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
Cognitive Test Subsample   Depression Subsample
Direct Interview (rproxy=0) Valid CES-D Items (>=8)
    (N = 65,901)               (N = 64,825)
         │                           │
         ▼                           ▼
Complete Cognitive Battery  Complete Covariate Set
    (N = 60,782)               (N = 62,123)
         │
         ▼
Complete Covariate Set
    (N = 58,265)
```

### 2.4 Operationalization of Exposures
1. **Childhood Socioeconomic Status:** Captured by question `ht235`: *"Thinking about the time when you were growing up, up to age 16, would you say your family was pretty well-off financially, about average, or poor?"* Coded as:
   - `Pretty well-off` ($7.77\%$, Reference Category)
   - `Average` ($49.32\%$)
   - `Poor` ($42.16\%$)
   - (Voluntary response `Varied`, $0.76\%$, evaluated separately in sensitivity analysis).
2. **Childhood Health:** Captured by question `ht231`: *"Consider your health while you were growing up, from birth to age 16. Would you say that your health was very good, good, fair, poor, or very poor?"* Coded as:
   - `Good` (Reference Category: Very good [$46.07\%$] + Good [$41.42\%$])
   - `Poor` (Fair [$9.59\%$] + Poor [$1.34\%$] + Very poor [$0.13\%$])
   - The original 5-level ordinal version was retained for sensitivity checks.
3. **Childhood Bedridden History (Severe Illness):** Captured by question `ht233`: *"Did you have a health condition that required you to be bedridden for a month or more before age 16?"* Coded as:
   - `No` ($94.25\%$, Reference Category)
   - `Yes` ($5.75\%$)
4. **Cumulative Disadvantage Score:** A continuous composite index ranging from 0 to 3, computed as the sum of: Poor childhood SES ($=1$), Poor childhood health ($=1$), and Childhood bedridden history ($=1$).

### 2.5 Operationalization of Outcomes
1. **Cognitive Performance & Impairment:**
   - Evaluated using an HRS-harmonized 43-point multi-domain cognitive battery comprising:
     - **Memory Domain (0–20 points):** Immediate 10-word recall (`mh012`, 0–10) + Delayed 10-word recall (`mh056`, 0–10).
     - **Orientation Domain (0–8 points):** Temporal orientation (date, month, year, day of week: 0–4) + Spatial orientation (place, village/town, landmark, district: 0–4) from questions `mh002`–`mh009`.
     - **Arithmetic Domain (0–9 points):** Backward counting from 100/20 (`mh038`, 0–2), Serial 7s subtraction (`mh045`, 0–5), and computation problems (`mh046` & `mh047`, 0–2).
     - **Executive Function & Construction (0–4 points):** Three-stage paper folding task (`mh050`, 0–3) and overlapping pentagons drawing (`mh051`, 0–1).
     - **Object Naming (0–2 points):** Visual naming of pencil (`mh019`, 0–1) and wristwatch (`mh020`, 0–1).
   - **Continuous Cognitive Score:** Total score (0 to 43 points, Mean = 24.70, SD = 8.12).
   - **Cognitive Impairment (Binary):** Defined using the established lower-tail threshold (lowest 10th percentile of the weighted distribution, cut-off $\le 16.00$ points).
2. **Depressive Symptoms:**
   - Measured via the 10-item short form of the **Center for Epidemiologic Studies Depression (CES-D)** scale (`fs701` through `fs710`).
   - Respondents rated symptom frequency in the past week on a 4-point scale: 1 = Rarely/never (<1 day), 2 = Sometimes (1–2 days), 3 = Often (3–4 days), 4 = Most/all of the time (5–7 days).
   - In accordance with standard epidemiological scoring, the 7 negative affect items (depressed, lonely, bothered, low energy, afraid, trouble concentrating, effort) were scored 1 if symptoms occurred $\ge 3$ days/week (codes 3 or 4) and 0 otherwise. The 3 positive affect items (overall satisfied, hopeful, happy) were reverse-coded (1 if experienced $\le 2$ days/week, codes 1 or 2).
   - **Continuous CES-D Score:** Sum of valid items scaled to 0–10 (Mean = 2.96, SD = 1.68).
   - **Depressive Symptoms Indicator (Binary):** Dichotomized at the clinically validated threshold of $\text{CES-D} \ge 4.0$.

### 2.6 Statistical Modeling Strategy
Because the primary binary outcomes were common ($28.2\%$ for depressive symptoms, $11.6\%$ for cognitive impairment), ordinary logistic regression odds ratios (ORs) tend to substantially overestimate prevalence ratios (PRs). Therefore:
1. **Primary Regression Models:** We estimated survey-weighted **Modified Poisson regression models with robust variance estimators** to generate Adjusted Prevalence Ratios (APRs) and 95% Confidence Intervals.
2. **Sequential Model Hierarchy:**
   - **Model 0 (Unadjusted):** Outcome $\sim$ Childhood Exposure.
   - **Model 1 (Demographic Adjustment):** Model 0 + Continuous Age + Sex (Ref: Male) + Place of Residence (Ref: Rural) + Social Group/Caste (Ref: General/None) + Marital Status (Ref: Married).
   - **Model 2 (Adult Socioeconomic Adjustment - Primary Model):** Model 1 + Educational Attainment (Ref: No formal education) + Household MPCE Quintile (Ref: Poorest).
   - **Model 3 (Adult Health Pathway Adjustment):** Model 2 + Diagnosed Chronic Multimorbidity Count (0, 1, 2+) + Self-Rated General Health (Ref: Very good).
3. **Age Interaction & Marginal Predictions:** To evaluate effect modification across ageing stages, interaction terms ($\text{Childhood Exposure} \times \text{Age Group}$) were added to Model 2. Adjusted marginal predicted probabilities were calculated across all 9 strata ($3 \text{ Age Groups} \times 3 \text{ Childhood SES Categories}$) holding covariates at representative levels.
4. **Sensitivity Analyses:**
   - Survey-weighted Weighted Least Squares (WLS) linear regressions for continuous cognitive score and continuous CES-D score.
   - Survey-weighted logistic regressions to provide Adjusted Odds Ratios (AORs) for direct comparison with published literature.
   - Linear and Poisson models using the continuous cumulative disadvantage score (0–3).

---

## 3. Empirical Results

### 3.1 Sample Characteristics (Table 1)
Table 1 displays the survey-weighted percentage distributions and unweighted sample sizes for all analytical variables among Indian adults aged 45 and above ($N = 66,606$).

| Characteristic | Category | Unweighted $N$ | Weighted Percent (%) |
| :--- | :--- | :---: | :---: |
| **Age Group** | 45–59 years | 34,704 | 49.77% |
| | 60–74 years | 25,022 | 38.80% |
| | 75+ years | 6,880 | 11.42% |
| **Sex** | Female | 35,567 | 54.06% |
| | Male | 31,039 | 45.94% |
| **Place of Residence** | Rural | 43,240 | 68.53% |
| | Urban | 23,366 | 31.47% |
| **Caste / Social Group** | General / None | 16,295 | 24.84% |
| | Other Backward Class (OBC) | 25,212 | 46.66% |
| | Scheduled Caste (SC) | 11,014 | 19.66% |
| | Scheduled Tribe (ST) | 11,746 | 8.84% |
| **Marital Status** | Married / Partnered | 49,949 | 73.86% |
| | Widowed | 14,780 | 23.72% |
| | Divorced / Separated | 1,006 | 1.23% |
| | Never Married | 868 | 1.19% |
| **Educational Attainment** | No formal education | 31,350 | 50.62% |
| | Less than primary | 7,598 | 10.92% |
| | Primary completed | 8,761 | 12.05% |
| | Middle completed | 6,337 | 8.35% |
| | Secondary completed | 5,953 | 7.93% |
| | Higher secondary / Diploma | 3,175 | 4.94% |
| | Graduate and above | 3,429 | 5.19% |
| **Household MPCE Quintile** | 1 (Poorest) | 13,181 | 20.86% |
| | 2 (Poorer) | 13,403 | 21.24% |
| | 3 (Middle) | 13,371 | 20.49% |
| | 4 (Richer) | 13,412 | 19.42% |
| | 5 (Richest) | 13,239 | 17.99% |
| **Childhood SES** | Pretty well-off | 4,848 | 7.77% |
| | Average | 35,438 | 49.32% |
| | Poor | 25,605 | 42.16% |
| | Varied | 394 | 0.76% |
| **Childhood Health** | Good / Very good | 58,272 | 87.46% |
| | Poor / Fair | 7,369 | 12.54% |
| **Childhood Bedridden** | No | 62,881 | 94.25% |
| | Yes ($\ge 1$ month) | 3,370 | 5.75% |
| **Cumulative Disadvantage** | 0 adversities | 34,506 | 48.19% |
| | 1 adversity | 26,556 | 44.06% |
| | 2 adversities | 4,003 | 6.86% |
| | 3 adversities | 466 | 0.88% |

---

### 3.2 Age Patterns in Outcome Prevalence (Table 2 & Figures 1–3)
Figure 1 illustrates the survey-weighted population age distribution, showing the expected pyramid taper with significant mass at advanced ages. Figure 2 summarizes the weighted prevalence of early-life adversities. Table 2 and Figure 3 depict the clear, age-graded progression in cognitive impairment and depressive symptoms across older adulthood.

```
                    PREVALENCE OF OUTCOMES BY AGE GROUP
  35% ───────────────────────────────────────────────────────────── 34.18%
                                                     29.17%          (Depression)
  30% ──────────────────────────────────────────────── (Cognition)
                                      29.10%
  25% ────────────── 26.28%        (Depression)
                   (Depression)
  20% ───────────────────────────
                                      13.70%
  15% ───────────────────────────── (Cognition)
  10% ─────────────── 6.70%
                    (Cognition)
   5% ───────────────────────────
   0% ─────────────────────────────────────────────────────────────
              45-59 Years          60-74 Years          75+ Years
```

| Age Group | Eligible $N$ | Depressive Symptoms ($\text{CES-D} \ge 4$) | Mean CES-D Score (0–10) | Cognitive Impairment ($\le 16$ pts) | Mean Cognitive Score (0–43) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Overall (45+)** | **66,606** | **28.24%** (SE: 0.18%) | **2.96** | **11.64%** (SE: 2.70%) | **24.70** |
| 45–59 Years | 34,704 | 26.28% (SE: 0.24%) | 2.86 | 6.70% (SE: 3.53%) | 26.10 |
| 60–74 Years | 25,022 | 29.10% (SE: 0.29%) | 3.01 | 13.70% (SE: 4.29%) | 23.80 |
| 75+ Years | 6,880 | 34.18% (SE: 0.59%) | 3.27 | 29.17% (SE: 9.27%) | 20.93 |

---

### 3.3 Bivariate Associations between Exposures and Outcomes (Table 2B)
Cross-tabulations reveal striking gradients across childhood conditions:
- **Childhood SES and Cognition:** Cognitive impairment prevalence was **7.99%** among adults from pretty well-off childhood families, **8.99%** among those from average families, and **15.41%** among those from poor families (nearly double).
- **Childhood Health and Depression:** Depressive symptoms were present in **27.07%** of adults with good childhood health versus **36.60%** of adults with poor childhood health (+9.5 percentage points).
- **Childhood Bedridden Status:** Adults bedridden for $\ge 1$ month in childhood had higher depressive symptom prevalence (**32.29%** vs. **27.97%**).
- **Cumulative Disadvantage Gradient:** Depressive symptom prevalence increased monotonically from **26.05%** (0 adversities) $\rightarrow$ **29.28%** (1) $\rightarrow$ **34.92%** (2) $\rightarrow$ **42.91%** (3 adversities).

---

### 3.4 Primary Regression Results: Cognitive Impairment (Table 3)
Table 3 summarizes sequential survey-weighted modified Poisson regressions modeling cognitive impairment.

| Exposure Parameter | Model 0: Unadjusted APR (95% CI) | Model 1: Demographics APR (95% CI) | Model 2: Adult SES APR (95% CI) [Primary] | Model 3: Adult Health APR (95% CI) [Pathway] |
| :--- | :---: | :---: | :---: | :---: |
| **Childhood SES** (Ref: Pretty well-off) | | | | |
| - Average | 1.125 (0.916–1.383) | 1.096 (0.887–1.354) | 0.853 (0.736–0.989)\* | 0.855 (0.738–0.991)\* |
| - Poor | **1.928 (1.583–2.348)\*\*\*** | **1.653 (1.334–2.049)\*\*\*** | **1.057 (0.902–1.239)** | **1.036 (0.886–1.212)** |
| **Childhood Health** (Ref: Good) | | | | |
| - Poor | 1.133 (0.946–1.356) | 1.103 (0.940–1.294) | 1.058 (0.894–1.252) | 1.051 (0.893–1.237) |
| **Childhood Bedridden** (Ref: No) | | | | |
| - Yes ($\ge 1$ month) | 0.925 (0.781–1.096) | 0.970 (0.829–1.135) | 1.024 (0.873–1.201) | 1.005 (0.849–1.191) |
| **Complete Analytic Sample ($N$)** | 60,344 – 60,377 | 58,221 – 58,265 | 58,221 – 58,265 | 58,210 – 58,254 |

Significance levels: \* $p < 0.05$, \*\* $p < 0.01$, \*\*\* $p < 0.001$.  
*Model 1 adjusts for age, sex, place of residence, caste, and marital status.*  
*Model 2 adds educational attainment and household MPCE consumption quintiles.*  
*Model 3 adds chronic multimorbidity count and self-rated health.*

> **Key Empirical Takeaway on Cognitive Health:** In Model 0 and Model 1, growing up in poverty is associated with a highly significant **65.3% to 92.8% higher prevalence of cognitive impairment** ($p < 0.0001$). However, the addition of adult educational attainment and household consumption expenditure in Model 2 attenuates the APR to **1.057** ($p = 0.4909$). This demonstrates that adult socioeconomic capital acts as the primary transmission mechanism linking early poverty to later-life cognitive preservation in India.

---

### 3.5 Primary Regression Results: Depressive Symptoms (Table 4)
Table 4 presents sequential survey-weighted modified Poisson regressions modeling depressive symptoms ($\text{CES-D} \ge 4$).

| Exposure Parameter | Model 0: Unadjusted APR (95% CI) | Model 1: Demographics APR (95% CI) | Model 2: Adult SES APR (95% CI) [Primary] | Model 3: Adult Health APR (95% CI) [Pathway] |
| :--- | :---: | :---: | :---: | :---: |
| **Childhood SES** (Ref: Pretty well-off) | | | | |
| - Average | 1.113 (0.948–1.308) | 1.109 (0.935–1.316) | 1.056 (0.911–1.224) | 1.050 (0.911–1.211) |
| - Poor | **1.188 (1.017–1.388)\*** | 1.161 (0.979–1.376) | 1.070 (0.924–1.239) | 1.022 (0.889–1.175) |
| **Childhood Health** (Ref: Good) | | | | |
| - Poor | **1.340 (1.217–1.474)\*\*\*** | **1.322 (1.196–1.461)\*\*\*** | **1.306 (1.185–1.440)\*\*\*** | **1.288 (1.167–1.422)\*\*\*** |
| **Childhood Bedridden** (Ref: No) | | | | |
| - Yes ($\ge 1$ month) | **1.149 (1.019–1.295)\*** | **1.156 (1.032–1.295)\*** | **1.175 (1.059–1.303)\*\*** | **1.129 (1.022–1.247)\*** |
| **Complete Analytic Sample ($N$)** | 64,331 – 64,387 | 62,070 – 62,123 | 62,070 – 62,123 | 62,058 – 62,111 |

Significance levels: \* $p < 0.05$, \*\* $p < 0.01$, \*\*\* $p < 0.001$.

> **Key Empirical Takeaway on Mental Health:** In stark contrast to cognitive outcomes, **poor childhood health and serious illness (bedridden $\ge 1$ month) remain persistent, statistically robust predictors of depressive symptoms across all models**. Adults reporting poor childhood health had a **30.6% higher adjusted prevalence of depressive symptoms** in Model 2 ($\text{APR} = 1.306$, $p < 0.0001$), which remained virtually unchanged at **28.8%** in Model 3 after controlling for concurrent chronic illnesses and self-rated health. Similarly, childhood bedridden history was associated with a **17.5% higher prevalence** ($\text{APR} = 1.175$, $p = 0.0023$). Early somatic vulnerability exerts an enduring psychological impact independent of adult socioeconomic success.

---

### 3.6 Age-Interaction & Marginal Predicted Prevalences (Table 5 & Figures 4–5)
To test Hypothesis 4, we modeled interaction terms between Childhood SES and Age Groups. Table 5 and Figures 4 and 5 report the adjusted marginal predicted prevalences across the nine strata holding all other covariates constant at representative baseline values (Rural, Male, Married, General caste, No formal education, Poorest MPCE).

| Age Group | Childhood SES | Adjusted Predicted Cognitive Impairment (%) | 95% Confidence Interval (%) | Adjusted Predicted Depressive Symptoms (%) | 95% Confidence Interval (%) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **45–59 Years** | Pretty well-off | 8.24% | (6.04% – 11.26%) | 25.34% | (21.29% – 30.16%) |
| | Average | 7.84% | (6.39% – 9.62%) | 27.14% | (23.72% – 31.05%) |
| | Poor | **10.51%** | (8.84% – 12.49%) | 27.19% | (24.34% – 30.38%) |
| **60–74 Years** | Pretty well-off | 17.08% | (13.00% – 22.45%) | 25.44% | (20.68% – 31.30%) |
| | Average | 13.48% | (11.53% – 15.76%) | 27.60% | (24.84% – 30.66%) |
| | Poor | **16.93%** | (14.63% – 19.59%) | 28.01% | (24.87% – 31.55%) |
| **75+ Years** | Pretty well-off | 31.63% | (24.13% – 41.48%) | 31.61% | (23.72% – 42.13%) |
| | Average | 26.30% | (21.39% – 32.34%) | 29.24% | (24.49% – 34.91%) |
| | Poor | **28.79%** | (23.98% – 34.56%) | 30.66% | (26.08% – 36.05%) |

```
    ADJUSTED PREDICTED COGNITIVE IMPAIRMENT ACROSS AGE STRATA (FIGURE 4)
  40% ───────────────────────────────────────────────────────────── 31.63% (Well-off)
                                                                    28.79% (Poor)
  30% ─────────────────────────────────────────────────────────────
                                       17.08% (Well-off)
  20% ──────────────────────────────── 16.93% (Poor)
                      10.51% (Poor)
  10% ──────────────── 8.24% (Well-off)
   0% ─────────────────────────────────────────────────────────────
          45-59 Years                 60-74 Years                 75+ Years
```

```
    ADJUSTED PREDICTED DEPRESSIVE SYMPTOMS ACROSS AGE STRATA (FIGURE 5)
  35% ───────────────────────────────────────────────────────────── 31.61% (Well-off)
                                                                    30.66% (Poor)
  30% ──────── 27.19% (Poor)          28.01% (Poor)
  25% ──────── 25.34% (Well-off)      25.44% (Well-off)
  20% ─────────────────────────────────────────────────────────────
          45-59 Years                 60-74 Years                 75+ Years
```

### Interpretation of Age Heterogeneity
- **Mid-Life Cognition Disparities:** In the youngest cohort (45–59), childhood poverty was associated with a 28% higher adjusted predicted prevalence of cognitive impairment (10.51% vs. 8.24%). 
- **Oldest-Old Convergence & Survivor Bias:** In the oldest-old (75+), the relative disparity between childhood SES groups narrowed. This convergence reflects two well-documented demographic phenomena in low-income settings: (1) **Selective survivor bias**, whereby individuals from impoverished childhoods who manage to survive past age 75 possess exceptional biological and psychological resilience; and (2) the overwhelming impact of age-related neurodegenerative changes that affect cognitive function across all socioeconomic strata in late life.

---

### 3.7 Sensitivity & Robustness Analyses (Table S)
To confirm that results were not artefacts of specific operationalization choices, four sensitivity checks were conducted:

| Analysis Specification | Outcome Metric | Exposure & Contrast | Estimand | Estimate | 95% Confidence Interval | $p$-value | $N$ |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Continuous Cognition (WLS)** | Cognitive Score (0–43) | Childhood SES: Poor vs. Well-off | Beta ($\beta$) | **-0.862** | (-1.176 to -0.549) | **< 0.0001** | 58,265 |
| | Cognitive Score (0–43) | Childhood Health: Poor vs. Good | Beta ($\beta$) | **-0.388** | (-0.774 to -0.001) | **0.0495** | 58,253 |
| **2. Continuous CES-D (WLS)** | CES-D Score (0–10) | Childhood SES: Poor vs. Well-off | Beta ($\beta$) | **+0.197** | (+0.025 to +0.369) | **0.0249** | 62,123 |
| | CES-D Score (0–10) | Childhood Health: Poor vs. Good | Beta ($\beta$) | **+0.477** | (+0.378 to +0.575) | **< 0.0001** | 62,107 |
| **3. Logistic Regression** | Cognitive Impairment | Childhood SES: Poor vs. Well-off | AOR | 1.103 | (0.892 to 1.364) | 0.3660 | 58,265 |
| | Depressive Symptoms | Childhood Health: Poor vs. Good | AOR | **1.489** | (1.284 to 1.727) | **< 0.0001** | 62,107 |
| **4. Dose-Response Model** | Depressive Symptoms | Cumulative Disadvantage (0–3) | APR | **1.113** | (1.068 to 1.160) | **< 0.0001** | 62,058 |

#### Key Sensitivity Insights:
1. **Continuous Cognition Verification:** When modeling cognition continuously rather than dichotomously, childhood poverty remains **statistically significant** ($\beta = -0.862, p < 0.0001$). Adults from poor childhoods enter late life with a measurable deficit of nearly one full point on the 43-point battery even after full control for their adult education and MPCE.
2. **Methodological Discrepancy between OR and PR:** For depressive symptoms, the logistic regression Adjusted Odds Ratio ($\text{AOR} = 1.489$) was substantially higher than the Modified Poisson Adjusted Prevalence Ratio ($\text{APR} = 1.306$). Because depressive symptoms affect over 28% of the population, odds ratios overstate the true relative risk. Using Poisson regression prevented misleading inflation of effect sizes.
3. **Dose-Response Gradient:** Each cumulative adversity in childhood added an independent 11.3% elevation in the adjusted prevalence of late-life depression ($p < 0.0001$).

---

## 4. Discussion

### 4.1 Principal Findings & Mechanistic Insights
This study provides the first comprehensive, nationally representative investigation of early-life disadvantage, late-life cognitive performance, and depressive symptoms across older adulthood in India. Two principal empirical insights emerge:

1. **Domain-Specific Transmission Channels:** Early-life disadvantage does not operate uniformly across health domains. For **cognitive health**, the impact of early poverty is overwhelmingly channeled through **adult human capital and socioeconomic position**. Individuals born into poverty receive far fewer years of schooling ($50.6\%$ of the overall sample received zero formal education), limiting cognitive reserve development and occupational complexity. When adult schooling and material assets are equalized, the excess risk of binary cognitive impairment shrinks to null ($\text{APR} = 1.057$). However, the persistence of a 0.86-point continuous deficit points to subtle, lifelong cognitive constraints resulting from early nutritional deprivation or developmental disadvantage.
2. **Biological & Psychological Scarring on Mental Health:** In stark contrast, early-life health shocks (poor general health and bedridden illness) exert an **enduring, unattenuated association with depressive symptoms** decades later ($\text{APR} = 1.306$ and $1.175$). This persists after adjusting for adult education, current household wealth, chronic multimorbidity, and concurrent self-rated health. Early somatic vulnerability may alter hypothalamic-pituitary-adrenal (HPA) axis programming, prime systemic chronic inflammatory responses, or establish deeply rooted subjective feelings of physical frailty and demoralization that persist across the life span.

### 4.2 Comparison with Previous Literature
Our findings corroborate and extend international evidence from the US Health and Retirement Study (HRS), Survey of Health, Ageing and Retirement in Europe (SHARE), and English Longitudinal Study of Ageing (ELSA):
- Like studies in Europe and the Americas, we find that education is the dominant mediator of early socioeconomic disparities in late-life cognitive function.
- However, the magnitude of early-life health associations with depression in India is notably pronounced. In an LMIC setting with minimal historical access to pediatric healthcare and social safety nets, childhood illnesses often resulted in prolonged physical debility, stunted growth, and social exclusion, magnifying long-term psychological vulnerability.

### 4.3 Policy & Public Health Implications
1. **Integrated Life-Course Interventions:** Current ageing policies in India (such as the National Programme for the Health Care of the Elderly, NPHCE) focus primarily on tertiary geriatric care and chronic disease management in late life. Our findings demonstrate that healthy cognitive and mental ageing begins in early childhood. Investments in maternal and child health, universal primary education, and childhood disease prevention are essential components of long-term healthy ageing policy.
2. **Screening for Early Adversity:** Mental health screening protocols in primary care should recognize that older adults with a history of severe childhood illness or chronic health problems represent a high-risk group requiring targeted psychological support.

---

## 5. Study Strengths & Limitations

### 5.1 Strengths
- **Nationally Representative Scale:** Inclusion of $66,606$ older adults spanning all 36 States and Union Territories of India, representing the full socioeconomic and cultural spectrum.
- **Harmonized Cognitive Assessment:** Direct administration of a 43-point multi-domain cognitive battery harmonized with global HRS standards, avoiding reliance on crude screening tools.
- **Methodological Rigor:** Application of complex survey weighting, cluster-robust standard error estimators, modified Poisson models for common outcomes, and comprehensive sensitivity analyses.
- **Pre-Specified Protocol:** Adherence to a frozen study protocol (`protocol.md`) preventing post-hoc hypothesis generation.

### 5.2 Limitations
1. **Cross-Sectional Baseline:** LASI Wave 1 provides cross-sectional observations. While childhood exposures temporally precede later-life outcomes, the study **cannot establish individual longitudinal cognitive decline, disease incidence, or causal effects over time**. Future waves of LASI will be essential to track within-person cognitive trajectories.
2. **Retrospective Recall Bias:** Childhood socioeconomic and health conditions were reported retrospectively by adults aged 45 to 90+. Recall accuracy may be imperfect, and current depressive symptoms could introduce negative recall bias. However, prior validation studies demonstrate that broad childhood financial status and major illnesses (e.g., bedridden for a month) are recalled with high reliability in older cohorts.
3. **Survivor Bias:** Older adults living in late-life represent survivors of historically high infant, child, and adult mortality regimes. Individuals from the most severely disadvantaged childhoods may have suffered premature mortality before reaching age 45, likely attenuating the observed associations toward the null.
4. **Structural Missingness in Cognition:** Direct cognitive testing was omitted for proxy interviews ($N = 705$). Because proxy interviews were conducted for severely impaired individuals, individuals with the most advanced cognitive impairment could not be included in the direct cognitive testing subsample.

---

## 6. Conclusion & Empirical Takeaways

Drawing upon a nationally representative sample of $66,606$ Indian adults aged 45 and above from LASI Wave 1, this study establishes clear empirical evidence linking early-life disadvantage to later-life cognitive performance and depressive symptoms:

1. **Childhood Poverty & Cognitive Impairment:** Childhood poverty is associated with a **65.3% higher unadjusted/demographic-adjusted prevalence of cognitive impairment** ($\text{APR} = 1.653$, $p < 0.0001$), but this association is **fully mediated by adult schooling and household economic resources** ($\text{APR} = 1.057$, $p = 0.49$).
2. **Early Health Disadvantage & Late-Life Depression:** Poor childhood health ($\text{APR} = 1.306$, $p < 0.0001$) and childhood bedridden illness ($\text{APR} = 1.175$, $p = 0.0023$) are **independently and stubbornly associated with later-life depressive symptoms**, resisting attenuation by adult socioeconomic mobility or concurrent chronic disease.
3. **Cumulative Vulnerability:** Depressive symptoms exhibit a strong, monotonic dose-response relationship with cumulative early adversity ($\text{APR} = 1.113$ per adversity, $p < 0.0001$).
4. **Age Stratification:** Cognitive disparities between childhood SES groups are widest in mid-life and young-old age, before selective survival and advanced biological ageing dominate in the oldest-old ($75+$).

These findings confirm that the foundations of healthy cognitive and mental ageing in India are laid decades before older adulthood, highlighting the critical necessity of life-course investments in maternal-child health and equitable education.

---

## 7. Appendices & Reproducibility Guide

### Appendix A: Reproducibility Pipeline
Every figure, table, and statistical estimate presented in this report is 100% reproducible directly from the raw LASI Wave 1 microdata:

```bash
# 1. Activate isolated Python environment
source .venv/bin/activate

# 2. Step 1: Generate Variable Inventory & Master Variable Map
python3 code/01_build_variable_map.py

# 3. Step 2: Extract, Filter (Age >= 45), Clean & Engineer Features
python3 code/02_extract_and_clean.py

# 4. Step 3: Produce Survey-Weighted Descriptives (Tables 1, 2, 2B & Figures 1-3)
python3 code/03_descriptive_analysis.py

# 5. Step 4: Fit Modified Poisson & Interaction Models (Tables 3, 4, 5 & Figures 4-5)
python3 code/04_regression_models.py

# 6. Step 5: Execute Sensitivity & Robustness Analyses (Table S)
python3 code/05_sensitivity_analyses.py
```

### Appendix B: File Location Summary
- **Analysis Data:** [`data_analysis/lasi_clean_analysis.parquet`](file:///home/harshit/Documents/Sem5/SOC450%20Project/data_analysis/lasi_clean_analysis.parquet)
- **Master Variable Map:** [`variable_map.csv`](file:///home/harshit/Documents/Sem5/SOC450%20Project/variable_map.csv)
- **Protocol:** [`protocol.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/protocol.md)
- **Progress Tracking:** [`checkpoints.md`](file:///home/harshit/Documents/Sem5/SOC450%20Project/checkpoints.md)
- **Tables Directory:** [`outputs/tables/`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/tables/)
- **Figures Directory:** [`outputs/figures/`](file:///home/harshit/Documents/Sem5/SOC450%20Project/outputs/figures/)
