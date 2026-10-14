# Gap Analysis: Report vs. Code/Outputs

## What the Code + Outputs Actually Produced

### Full table inventory (`outputs/tables_v2/`)
| Table File | Content | In Report? |
|---|---|---|
| `table2v2_outcomes_by_age.csv` | Outcome prevalence by age | ✅ Section 4 (Table 2) |
| `table3v2_cognition_impairment.csv` | Cognition Models 0/A/B/C (binary) | ✅ Section 5 (Table 3) |
| `table3v2b_cognition_continuous.csv` | Cognition continuous WLS Models 0/A/B/C | ⚠️ Partially — only direction stated, **no full table in Section 5** |
| `table3v2c_ses_joint_categories.csv` | SES joint categories both outcomes | ✅ Duplicate / used in Forest plot |
| `table4v2_depression.csv` | Depression Models 0/A/B/C | ✅ Section 5 (Table 4) |
| `table5v2a_interaction_joint_tests.csv` | Joint Wald F-tests (age×exposure) | ✅ Section 6 (Table 5A) |
| `table5v2b_standardized_predictions.csv` | Predicted prevalences 3×3 age×SES grid | ⚠️ Referenced but **table not embedded** in Section 6 |
| `table5v2c_risk_differences.csv` | Marginal risk differences by age group | ✅ Section 6 (Table 5C) |
| `table6v2_mutual_adjustment.csv` | Mutually adjusted + cumulative index | ✅ Section 5 (Table 6) |
| `table_demographic_study.csv` | Demographics Model A (sex/residence/caste) | ✅ Section 4 |
| `table_s0_common_samples.csv` | Common sample N reporting | ⚠️ **Never shown in report** |
| `table_s1_response_model.csv` | IPW response model logistic | ⚠️ **Mentioned but table never embedded** |
| `table_s2_ipw_cognition.csv` | IPW-corrected estimates vs. unweighted | ⚠️ **Never embedded as table** |
| `table_s3_cognition_missingness.csv` | Missingness rates by exposure | ⚠️ **Never embedded** |
| `table_s4_sensitivity.csv` | Full sensitivity suite (S4a–S4f) | ⚠️ **Only S4e referenced; S4a/b/c/d/f all MISSING from Section 7** |
| `table_s5_education_gradient_v1_vs_v2.csv` | Education gradient old vs new outcome | ❌ **Completely absent from report** |

### Full figure inventory (`outputs/figures_v2/`)
| Figure | Content | In Report? |
|---|---|---|
| `figure1_age_distribution.png` | Age histogram | ✅ Section 3 |
| `figure2_childhood_disadvantage_prevalence.png` | Childhood exposure bars | ✅ Section 4 |
| `figure3_outcome_prevalence_by_age.png` | Outcome prevalence by age | ✅ Section 4 |
| `figure4v2_cognition_interaction.png` | Cognition × age × SES | ✅ Section 6 |
| `figure5v2_depression_interaction.png` | Depression × age × SES | ✅ Section 6 |
| `figure6v2_forest_sequential.png` | Forest plot sequential models | ✅ Section 5 |
| `figureA1_education_gradient.png` | Education gradient | ✅ Section 6 appendix |
| `figureA2_cognition_missingness.png` | Missingness pattern | ✅ Section 7 appendix |

---

## What's Missing or Under-Developed

### ❌ ENTIRELY ABSENT — No code yet, no output yet

**1. Social Mobility Model** *(User explicitly requested this)*

This is the most important gap. The research question — *does moving up the social ladder in adulthood erase childhood scars?* — is the central sociological question but has never been tested. It requires:

- Cross-tabulating **childhood SES × adult MPCE quintile** into four mobility trajectories:
  - **Persistently poor** (Poor child → Bottom 2 quintiles adult)
  - **Upwardly mobile** (Poor child → Top 3 quintiles adult)
  - **Persistently affluent** (Well-off child → Top 3 quintiles adult)
  - **Downwardly mobile** (Well-off child → Bottom 2 quintiles adult)
- Running outcome models with mobility group as the main exposure (vs. persistently affluent)
- New script needed: `code/12_social_mobility.py`

> [!IMPORTANT]
> This is the **most theoretically rich addition** possible. The finding — whether upward mobility restores mental health to affluent levels or whether the scar remains — directly tests Hypothesis 5 with a sociologically grounded framing.

---

### ⚠️ COMPUTED BUT NOT SHOWN IN REPORT

**2. Full Sensitivity Suite (Section 7 is very incomplete)**

`table_s4_sensitivity.csv` contains 6 sub-analyses; only S4e (Poisson vs. logistic) is mentioned in the report. The following are computed and saved but never presented:

| Sub-analysis | Key finding hidden | Where it should go |
|---|---|---|
| **S4a — Battery comparison** | Skip-aware full battery SES PR = 1.29 even after adult SES adjustment — meaning some residual effect exists on the harder battery | Section 7 Table |
| **S4b — Schooling strata** | Among never-schooled adults, poor childhood SES β = −0.386 (p=0.026) — memory scarring persists even without the education channel | Section 7 |
| **S4c — SES "It Varied"** | Varied childhood SES → 1.18× depression (ns) — documents the middle-ground category | Section 7 |
| **S4d — Excluding centenarians** | Results unchanged — confirms no outlier distortion | Section 7 |
| **S4f — Sex-stratified** | Women: SES→depression APR 1.23, p=0.037; Men: APR 1.14, p=0.15 — **women uniquely vulnerable** | Section 5 or 6 |

**3. Table 5v2b (Standardized Prediction Grid)** — The 3×3 matrix of predicted prevalences across Age (45–59, 60–74, 75+) × SES (Well-off, Average, Poor) is never shown as a table, only as figures 4v2 and 5v2. The table provides precise numbers that are much easier to cite.

**4. IPW Response Model Table (S1)** — The logistic model showing that tribal (ST) adults are 28% *less* likely to complete the cognitive battery (OR=0.718, p<0.001), and higher education is 4× more likely to complete it, is never shown. This motivates the entire IPW analysis and its absence weakens the methods section.

**5. Continuous WLS Cognition Table (3v2b)** — The β = −1.28 (Model A) → −0.32 (Model B) attenuation for the continuous score is stated in prose but never shown as a structured table with all four exposures × four models.

---

### ⚠️ IN REPORT BUT NOT TIED TO LITERATURE OR UNDERDEVELOPED

**6. Social Mobility framing** — The current Discussion (Section 8) mentions that adult education attenuates the cognition penalty but doesn't frame this as *social mobility*. Missing citations:
- Blau & Duncan (1967) — status attainment model
- Sorokin (1927) — "social circulation"
- Hout (2015) — education as the mobility engine in modern India
- DiPrete & Eirich (2006) — cumulative advantage theory

**7. Sex-stratified heterogeneity** — S4f shows women drive the childhood poverty→depression link; men do not reach significance. This maps directly to:
- Kessler (2003) — "Epidemiology of women and depression"
- Patel et al. (2006) — gendered depression burden in South Asia
- Mishra et al. (2020) — gendered ageing and mental health in India

**8. Selective Survival / Mortality Selection at 75+** — The SES×age Wald test is p=0.045 for cognition, driven by *reversal* at 75+. This is the classic "mortality selection" finding: the poorest with worst cognition die before 75, leaving a survivor pool. Missing citations:
- Crimmins et al. (2005) — mortality selection in cognitive ageing studies
- Lynch & Smith (2005) — life course perspectives on health inequalities

**9. Policy chapter lacks quantified burden** — Section 8 describes interventions but never frames the scale:
- 28.24% depression prevalence × ~180 million adults aged 45+ in India = **~50.8 million people** with clinically significant symptoms
- Of those, childhood adversity accounts for ~11–21% excess risk → **potentially 5–10 million attributable cases**
- Cognitive impairment: 12.79% × 180M = **~23 million people**

---

## Priority-Ranked Action Plan

| Priority | Action | Effort | Impact |
|---|---|---|---|
| 🔴 HIGH | Write `code/12_social_mobility.py`, generate results + figure | High | Very High |
| 🔴 HIGH | Add social mobility LaTeX subsection to Section 5 or 6 | Medium | Very High |
| 🔴 HIGH | Expand Section 8 with mobility/gendered/mortality-selection literature | Low | High |
| 🟡 MEDIUM | Add sex-stratified finding paragraph to Section 5 | Low | High |
| 🟡 MEDIUM | Embed full S4 sensitivity table in Section 7 | Low | Medium |
| 🟡 MEDIUM | Add policy burden numbers (50M framing) to Section 8 | Low | Medium |
| 🟡 MEDIUM | Embed Table 5v2b (predictions grid) in Section 6 | Low | Medium |
| 🟠 LOW | Embed IPW response model table in Section 7 | Low | Low |
| 🟠 LOW | Embed continuous WLS table (3v2b) in Section 5 | Low | Low |
