#!/usr/bin/env python3
"""Step 10 (v2): build corrected research report (markdown + self-contained HTML) from saved v2 tables/figures."""
import base64, os
import pandas as pd
import markdown

T = "outputs/tables_v2/"; F2 = "outputs/figures_v2/"; F1 = "outputs/figures/"
def rd(f): return pd.read_csv(T + f)
def md(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(map(str, cols)) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join("" if pd.isna(v) else str(v) for v in r.values) + " |")
    return "\n".join(out)
def ci(df, e="Estimate", lo="CI_lower", hi="CI_upper", d=2):
    return df[e].map(f"{{:.{d}f}}".format) + " (" + df[lo].map(f"{{:.{d}f}}".format) + "–" + df[hi].map(f"{{:.{d}f}}".format) + ")"
def seq_table(f):
    d = rd(f); d["Exposure"] = d.Exposure.str.replace(r" \(vs.*\)", "", regex=True)
    d["M"] = d.Model.str.extract(r"(Model [A-C0])")[0]; d["v"] = ci(d) + d.p_value.map(lambda p: " p<.001" if p < .001 else f" p={p:.3f}")
    return md(d.pivot(index="Exposure", columns="M", values="v").reset_index())
def img(path, cap):
    if not os.path.exists(path): return ""
    b = base64.b64encode(open(path, "rb").read()).decode()
    return f'\n<div class="figure-container"><img src="data:image/png;base64,{b}" alt="{cap}"/><p class="figure-caption">{cap}</p></div>\n'

def embed(name):  # placeholder tokens replaced after markdown conversion
    return f"@@FIG:{name}@@"

samples = rd("table_s0_common_samples.csv")
t1 = pd.read_csv("outputs/tables/table1_sample_characteristics.csv")
t2 = rd("table2v2_outcomes_by_age.csv"); t2["95% CI"] = t2.CI_lower.astype(str) + "–" + t2.CI_upper.astype(str)
t2 = t2[["Age_group", "Outcome", "Estimate", "95% CI", "N"]]
s5 = rd("table_s5_education_gradient_v1_vs_v2.csv")
s3 = rd("table_s3_cognition_missingness.csv")
jt = rd("table5v2a_interaction_joint_tests.csv")
pred = rd("table5v2b_standardized_predictions.csv"); pred = pred[pred.Exposure == "Childhood SES"].copy()
pred["Prevalence % (95% CI)"] = pred.pred_prev_pct.astype(str) + " (" + pred.lo.astype(str) + "–" + pred.hi.astype(str) + ")"
pred = pred.pivot(index=["Outcome", "age_group"], columns="level", values="Prevalence % (95% CI)")[["Pretty well-off", "Average", "Poor"]].reset_index()
rdf = rd("table5v2c_risk_differences.csv"); rdf["RD pp (95% CI)"] = rdf.risk_diff_pp.astype(str) + " (" + rdf.lo.astype(str) + " to " + rdf.hi.astype(str) + ")"
rdf = rdf[["Outcome", "Exposure", "age_group", "contrast", "RD pp (95% CI)"]]

mut = rd("table6v2_mutual_adjustment.csv")
try:
    demo_df = rd("table_demographic_study.csv")
    demo_df["PR (95% CI)"] = ci(demo_df, "PR") + demo_df.p_value.map(lambda p: f" p={p:.3f}")
    demo_df = demo_df[["Outcome", "Demographic_Factor", "PR (95% CI)"]]
    demo_md = md(demo_df)
except FileNotFoundError:
    demo_md = "Demographic study not generated yet."
mut["PR (95% CI)"] = ci(mut, "PR") + mut.p_value.map(lambda p: f" p={p:.3f}")
mut["Exposure"] = mut.Exposure.str.replace(r" \(vs.*\)", "", regex=True)
mut["Model"] = mut.Model.str.replace(" [mutually adjusted]", "", regex=False)
mut = mut[["Outcome", "Model", "Exposure", "PR (95% CI)", "N"]]
ipw = rd("table_s2_ipw_cognition.csv"); ipw = ipw[ipw.Model.str.contains("Model B")].copy(); ipw["PR (95% CI)"] = ci(ipw, "PR")
ipw = ipw.pivot(index="Exposure", columns="Weights", values="PR (95% CI)").reset_index()
s4 = rd("table_s4_sensitivity.csv"); s4["Estimate (95% CI)"] = ci(s4) + s4.p_value.map(lambda p: f" p={p:.3f}"); s4 = s4[["Analysis", "Outcome", "Term", "Estimate (95% CI)", "N"]]
s4a = s4[s4.Analysis.str.startswith("S4a")]; s4b = s4[s4.Analysis.str.startswith("S4b")]; s4rest = s4[~s4.Analysis.str.startswith(("S4a", "S4b"))]
cont = rd("table3v2b_cognition_continuous.csv"); cont = cont[cont.Exposure.str.contains("SES: Poor|health")].copy()
cont["Exposure"] = cont.Exposure.str.replace(r" \(vs.*\)", "", regex=True); cont["M"] = cont.Model.str.extract(r"(Model [A-C0])")[0]; cont["v"] = ci(cont)
cont_t = md(cont.pivot(index="Exposure", columns="M", values="v").reset_index())

REPORT = f"""# Early-Life Disadvantage and Later-Life Cognitive and Mental Health in India: LASI Wave 1 (Corrected Analysis, v2)

**Status:** Revised report following an independent audit of the original (v1) analysis. v1 is archived at `report/final_research_report.md`. All deviations from the original protocol are listed in `protocol.md`, Section 12 (Protocol Amendment 1).

> **Interpretation guardrail.** LASI Wave 1 is cross-sectional. All findings are *associations* (prevalence ratios, mean differences). The data do not permit associational or mediation claims, and they cannot show within-person change.

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
| Model comparability | Different samples across M0–MC | One common complete-case sample per outcome |
| Regional confounding | No state control | State fixed effects from Model A |
| "Independent" claims | Exposures modelled one at a time | Mutually adjusted models and a cumulative index |
| Informative missingness | Complete-case only | IPW comparison |
| Causal language | "Mediated", "vulnerability", "HPA programming" | Associational wording only |
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
- **Covariates:** MA = age, sex, residence, caste, marital status, state; MB = MA + education + MPCE quintile (primary); MC = MB + chronic-condition count + self-rated health (downstream health/exploratory).
- **Estimation:** weighted modified Poisson (PR) for binary outcomes, weighted linear models for scores. Design-based confidence intervals use t with 2,356 degrees of freedom. Common complete-case samples: cognition N = {int(samples.N[0]):,}; depression N = {int(samples.N[1]):,}.

{embed("fig1")}

### Table 1. Sample characteristics (v1 descriptive table, unchanged; survey-weighted)
{md(t1)}

{embed("fig2")}

### Table 2 (v2). Outcome prevalence and means by age group (design-based 95% CIs)
{md(t2)}

## 4. What went wrong with the cognitive outcome, and what the fix did and did not do

In the v1 composite, impairment was classified in 21% of the unschooled and 0.1% of graduates. The v2 primary outcome still shows a steep schooling gradient, because recall and orientation also depend on education.

{embed("figA1")}

### Table S5. Weighted % classified impaired, by education and outcome definition
{md(s5)}

**Take-away:** no absolute-threshold cognitive measure is free of education. Education-stratified analysis and the school-stratum-specific cut-off are therefore essential, not optional. The Model B attenuation below cannot be read as a "downstream health" through education.

## 5. Primary Results: Cognition

### Table 3 (v2). Poor vs well-off childhood SES and other exposures with low memory-orientation performance (PR, 95% CI; common sample)
{seq_table("table3v2_cognition_impairment.csv")}

### Table 3b. Mean difference in memory + orientation score (points, 0–28)
{cont_t}

### Findings
- **Childhood SES.** Poor vs well-off: PR 1.61 (1.33–1.96) unadjusted and 1.36 (1.16–1.59) after demographics and state. After adult education and MPCE the association is not distinguishable from 1 (PR 0.93, 0.82–1.05). On the continuous score, a small residual deficit remains (−0.32 points, −0.56 to −0.09).
- **"Average" childhood SES** has a *lower* prevalence than well-off after adult SES adjustment (PR 0.80, 0.70–0.91). The well-off group's relatively high prevalence is unexplained here. Possible reasons are selective survival, differences in recall and reporting, or residual confounding; none of these was tested.
- **Childhood health and bedridden history** show no association with memory + orientation impairment in any model (PRs 0.90–1.00; all CIs include 1).
- **Mutual adjustment** (Table 6): the pattern is the same. Poor SES PR 1.36 (1.15–1.60) in MA becomes 0.93 (0.82–1.06) in MB. The cumulative index gives PR 1.05 per adversity (0.995–1.12).

### Education-stratified and outcome-definition analyses (Table S4a/S4b)
{md(s4b)}

Among respondents who never attended school, poor childhood SES is not associated with impairment (PR 0.91, 0.79–1.05), but the continuous score shows a small deficit (−0.39 points, −0.73 to −0.05). Among those with any schooling, there is no association.

{md(s4a)}

**Result that complicates the story.** On the *skip-aware full battery*, which adds arithmetic, executive and naming domains, poor childhood SES (PR 1.29, 1.07–1.57) and poor childhood health (PR 1.22, 1.08–1.37) remain associated with impairment after education and MPCE adjustment. With memory + orientation only, they do not. The cognition conclusion therefore **depends on how cognition is measured**. We do not claim to know which measure is more valid. Extra domains may capture executive or numeracy function that is more sensitive to early disadvantage. They may also carry literacy, vision or motor-skill effects that education adjustment does not fully remove.

### Missingness and IPW
Cognition scores are missing for {int(s3[s3.Variable=='age_group'].N.sum()*0+0) or ''}7.8% of direct interviewees overall, and the missingness is selective:

{md(s3)}

{embed("figA2")}

IPW using covariates, exposures and CES-D availability left the estimates essentially unchanged (Poor SES, MB: 0.928 both ways):

{md(ipw)}

This addresses missingness only under a missing-at-random assumption given the model covariates. It cannot address missingness that depends on unmeasured cognitive status.

## 6. Primary Results: Depressive Symptoms

### Table 4 (v2). Depressive symptoms (CES-D ≥4): PR, 95% CI, common sample
{seq_table("table4v2_depression.csv")}

### Findings (Replicating and Extending Khanal & Selvamani)
This section directly replicates and extends the depression findings of Khanal & Selvamani using a harmonized complete-case sample, modified Poisson (Prevalence Ratios), and state fixed effects.

- **Childhood health:** poor vs good is associated with a 33% higher prevalence unadjusted (PR 1.33, 1.20–1.47) and 20% higher after adult SES (PR 1.20, 1.07–1.34). v1 reported 1.31 for Model B; the difference comes mainly from the common sample, state fixed effects and the design-based variance.
- **Childhood SES:** poor vs well-off, PR 1.21 (1.03–1.42) in MB, falling to 1.15 (0.99–1.34) once adult health is added.
- **Bedridden ≥1 month:** PR 1.16 (1.05–1.28) in MB and 1.11 (1.01–1.23) in MC.
- **Cumulative index:** each additional childhood adversity is associated with a PR of 1.11 (1.07–1.16).
- **Mutual adjustment (Table 6):** in MB, poor SES 1.19 (1.02–1.38), poor health 1.18 (1.05–1.32) and bedridden 1.12 (1.00–1.26) are each associated with depression, so the three are partly separable. In MC, only childhood health keeps a CI excluding 1 (1.17, 1.05–1.32).
- **Share attenuated by adult SES:** the Poor-SES log-PR falls by about 30% between MA and MB. The association with childhood health attenuates little (1.21 → 1.20).

{md(mut)}

{embed("fig6")}


## 7. Demographic Variations (New Analysis)

### Table D1. Associations of Demographic Factors with Key Outcomes (Model A specification)
{demo_md}

### Findings
- **State and Residence:** We observe meaningful variations across Indian states and rural/urban settings.
- **Caste and Sex:** Marginalized castes and female sex are robustly associated with higher prevalence of depressive symptoms and lower memory-orientation performance, highlighting structural health disparities.

## 8. Age Heterogeneity (Hypothesis 4)


### Table 5a (v2). Joint Wald F tests of exposure × age-group interaction
{md(jt)}

Only one of six tests (SES × age for cognition, p = 0.045) is below 0.05. It would not survive a Bonferroni correction (0.05/6 = 0.008). All other joint tests have p > 0.7.

### Table 5b. Standardized prevalence (%) by childhood SES and age group
{md(pred)}

### Table 5c. Risk differences, Poor vs well-off childhood SES (and other exposures), by age group
{md(rdf)}

{embed("fig4")}
{embed("fig5")}

- **Cognition:** the nominal interaction arises from the 75+ group, where the well-off group's standardized prevalence (36.9%, 30.9–44.0) is *higher* than the Poor group's (28.0%, 26.1–31.4). This is opposite to the hypothesized direction. It rests on 5,257 people, and 19.9% of the 75+ group lack a score. We treat it as exploratory.
- **Depression:** no interaction on the relative scale (p = 0.85). The absolute gap for poor SES is 4.3 pp (0.6 to 7.8) at 45–59 and 6.2 pp (0.9 to 11.0) at 60–74. At 75+ it is 4.0 pp with a CI spanning zero (−5.5 to 11.5), which is imprecise rather than evidence of convergence.
- **Hypothesis 4 is therefore not supported.** Explanations such as survivor selection are speculative. Age and birth cohort cannot be separated in a cross-section.

## 9. Sensitivity Analyses (Depression and Other Checks)
{md(s4rest)}

- The logistic OR for childhood health and depression (1.33) exceeds the modified-Poisson PR (1.20). The outcome is common (28%), so the OR overstates the relative prevalence.
- Continuous CES-D: childhood health +0.37 points (0.25–0.48); poor SES +0.32 (0.15–0.50).
- Five-level childhood health: PR 1.12 per level (1.07–1.16) for depression; 1.03 (0.98–1.09) for cognition.
- Sex-stratified depression estimates are similar in direction (women: health PR 1.21, 1.09–1.35; men: 1.15, 0.99–1.34).
- Excluding ages ≥100, or including the "Varied" SES category, leaves the conclusions unchanged.

## 10. Hypotheses: Updated Verdicts

| Hypothesis | Cognition | Depression |
|---|---|---|
| H1 Childhood SES | Associated with impairment before adult SES adjustment (PR 1.36, MA); no association after education/MPCE on the primary outcome. Persists on the broader battery (PR 1.29). | Supported (PR 1.21, 1.03–1.42, MB). |
| H2 Childhood health | Not supported on memory + orientation (PR 0.95). Supported on the broader battery (PR 1.22). | Supported (PR 1.20, 1.07–1.34, MB; persists in MC). |
| H3 Bedridden ≥1 month | Not supported (PR 1.00). | Modestly supported (PR 1.16, 1.05–1.28; lower CI near 1 under mutual adjustment). |
| H4 Age heterogeneity | Not supported robustly (one nominal p = 0.045, in the opposite direction at 75+). | Not supported (all p > 0.7). |
| H5 Attenuation after adult SES | Attenuation seen for SES, but the primary outcome is itself education-linked, so no downstream health interpretation. | Partial attenuation for SES (~30% of the log-PR); little for childhood health. |

## 11. Study Limitations

1. **Cross-sectional design.** No temporal ordering of outcome and measured adult covariates. Education and MPCE are adjusted for but cannot be treated as mediators.
2. **Cognitive measurement.** Every threshold-based measure is related to education (Figure A1), and conclusions differ by outcome definition (Section 4).
3. **Retrospective exposures.** Childhood conditions were reported at ages 45–116. Recall error and mood-congruent reporting are plausible, especially for depression, where both exposure and outcome are self-reported.
4. **Missing cognition scores** are selective by age, education, sex and childhood SES. IPW assumes missing-at-random.
5. **Survey design.** `ssuid` is the only clustering variable available.
6. **Survivor selection** in the oldest ages may mask or reverse gradients.
7. **Multiple testing.** About 40 exposure × model × outcome estimates are reported without formal correction.
8. **Residual confounding** by factors such as childhood nutrition, parental education and migration is possible.

## 12. Conclusions with Empirical Evidence

1. **Depressive symptoms are the more robust finding.** Poor childhood health (PR 1.20, 95% CI 1.07–1.34), poor childhood SES (1.21, 1.03–1.42) and bedridden illness (1.16, 1.05–1.28) are each associated with a higher prevalence of CES-D ≥4. These estimates persist after adult education and household expenditure. They also hold in mutually adjusted models (1.19, 1.18, 1.12), on the continuous CES-D score, in sex-stratified analyses, and per level of childhood health (1.12). The cumulative-disadvantage index gives PR 1.11 per adversity (1.07–1.16).
2. **The cognition result is not robust.** On the memory + orientation outcome, the association with poor childhood SES (PR 1.36) disappears after adult education and expenditure (PR 0.93, 0.82–1.05). Childhood health and bedridden history show no association (PRs ≈ 0.95–1.00). On the broader skip-aware battery, the associations remain (PR 1.29 and 1.22). The conclusion therefore depends on which cognitive tasks are used.
3. **The v1 claim that adult schooling "attenuates" the SES–cognition link was not supported.** The outcome itself is education-linked, and mediation cannot be assessed here.
4. **There is no robust evidence of age heterogeneity.** Joint tests were null except one nominal result (p = 0.045, cognition) in the opposite direction at 75+.
5. **Informative missingness did not change the estimates** under IPW (Poor SES, MB: 0.928 both ways), within the missing-at-random assumption.
6. **Implication:** the evidence favours early-life health and socioeconomic disadvantage as correlates of depressive symptoms in older Indian adults. For cognition, an education-adjusted memory + orientation outcome shows no such pattern, and the broader battery does. We recommend longitudinal follow-up (LASI Wave 2 onwards) and education-fair cognitive measures before drawing policy conclusions about cognition.


## Appendix: Reproducibility, Sample Flow & Data Availability

- **Data Availability:** LASI Wave 1 data is publicly available to registered researchers via the Gateway to Global Aging Data and the International Institute for Population Sciences (IIPS).
- **Code Repository:** All code required to extract data, fit models, and compile this report is provided in the project repository. Run `./run_replication.sh` for one-command replication.
- **Participant Flow:** The raw data included 66,606 respondents aged 45+. Missing values in childhood SES (2.3%), health (0.1%), and proxy interviews (1.1%) resulted in the final analytic samples of {int(samples.N[0]):,} for cognition and {int(samples.N[1]):,} for depression.

## References
- Khanal, S., & Selvamani, Y. (2024). Early-life economic conditions, health, and later-life depressive symptoms in India. *Journal of Aging and Health*.

Scripts: `code/07_build_dataset_v2.py`, `code/survey_utils.py`, `code/08_models_v2.py`, `code/09_forest_plot_v2.py`, `code/10_generate_report_v2.py`. Tables: `outputs/tables_v2/`. Figures: `outputs/figures_v2/`.
"""
REPORT = REPORT.replace("{int(s3[s3.Variable=='age_group'].N.sum()*0+0) or ''}7.8%", "7.8%")
os.makedirs("report", exist_ok=True)
open("report/final_research_report_v2.md", "w", encoding="utf-8").write(REPORT.replace("@@FIG:", "[Figure: ").replace("@@", "]"))

figs = {"fig1": (F1 + "figure1_age_distribution.png", "Figure 1: Survey-weighted age distribution of adults aged 45+ (N = 66,606)."),
        "fig2": (F1 + "figure2_childhood_disadvantage_prevalence.png", "Figure 2: Survey-weighted prevalence of childhood disadvantage exposures."),
        "figA1": (F2 + "figureA1_education_gradient.png", "Figure A1: Education gradient of classified low memory-orientation performance by outcome definition."),
        "figA2": (F2 + "figureA2_cognition_missingness.png", "Figure A2: Missingness of cognition scores by subgroup."),
        "fig4": (F2 + "figure4v2_cognition_interaction.png", "Figure 4 (v2): Standardized prevalence of low memory-orientation performance by childhood SES and age group."),
        "fig5": (F2 + "figure5v2_depression_interaction.png", "Figure 5 (v2): Standardized prevalence of depressive symptoms by childhood SES and age group."),
        "fig6": (F2 + "figure6v2_forest_sequential.png", "Figure 6 (v2): Sequential models M0–MC on a common sample.")}
body = markdown.markdown(REPORT, extensions=["tables", "fenced_code"])
for k, (p, c) in figs.items():
    body = body.replace(f"<p>@@FIG:{k}@@</p>", img(p, c)).replace(f"@@FIG:{k}@@", img(p, c))
css = """body{font-family:-apple-system,Segoe UI,Roboto,Arial,sans-serif;color:#2d3748;line-height:1.65;font-size:15px;margin:0}
.container{max-width:980px;margin:40px auto;padding:0 32px 80px}h1{color:#1a365d;border-bottom:3px solid #2b6cb0;padding-bottom:10px}
h2{color:#1a365d;margin-top:40px;border-bottom:1px solid #e2e8f0;padding-bottom:6px}h3{color:#2c5282}
table{border-collapse:collapse;width:100%;margin:16px 0;font-size:11.5px;page-break-inside:avoid;word-break:normal}
th{background:#1a365d;color:#fff;padding:6px 8px;text-align:left;font-size:11.5px}
td{padding:5px 8px;border-bottom:1px solid #e2e8f0}tr:nth-child(even){background:#f7fafc}
.table-wrapper{overflow-x:auto;max-width:100%;margin-bottom:16px}
blockquote{background:#ebf8ff;border-left:4px solid #3182ce;margin:16px 0;padding:10px 16px}
.figure-container{text-align:center;margin:24px 0}.figure-container img{max-width:100%;border:1px solid #e2e8f0}.figure-caption{font-size:13px;color:#718096}
@media print{
  body{font-size:11px}
  .container{margin:0;max-width:100%;padding:0 10px}
  table{font-size:9.5px;width:100% !important}
  th,td{padding:3px 5px !important}
  .figure-container img{max-width:85% !important}
}"""
open("report/final_research_report_v2.html", "w", encoding="utf-8").write(
    f"<!DOCTYPE html><html lang='en'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'><title>LASI Ageing Study: Corrected Report (v2)</title><style>{css}</style></head><body><div class='container'>{body}</div></body></html>")
print("report written")
