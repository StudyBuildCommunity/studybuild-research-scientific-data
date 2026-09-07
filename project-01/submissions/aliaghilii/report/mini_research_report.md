# Mini Research Report: Academic Stress & Student Burnout

## 1. Research Question

Are self-esteem, sleep quality, perceived safety, academic performance, and 
social support — representing the psychological, physiological, environmental, 
academic, and social dimensions of the Biopsychosocial Model (Engel, 1977) — 
associated with student stress level?

**Motivation:** Student stress is rarely driven by a single factor. The 
Biopsychosocial framework provides a theoretically grounded way to sample 
across distinct domains of student well-being rather than selecting predictors 
ad hoc. Understanding which dimensions show the strongest association with 
stress can help institutions prioritize interventions (e.g., academic support 
vs. sleep hygiene programs vs. social support services).

**Type of claim:** This is an observational, cross-sectional dataset. Findings 
are reported strictly in terms of *association*, not causation.

## 2. Data

**Source:** Student Stress Factors: A Comprehensive Analysis (Kaggle, author: 
rxnach), file `StressLevelDataset.csv`.

**Sample:** 1,100 students, survey-based, drawn from various educational 
institutions. Demographic details (age, country, field of study) and the 
sampling method are not documented by the source.

**Outcome variable:** `stress_level` — ordinal, 3 levels (0=Low, 1=Medium, 
2=High). Direction confirmed by cross-tabulating with sleep_quality, 
self_esteem, and anxiety_level group means.

**Explanatory variables (one representative per Biopsychosocial dimension):**

| Variable | Dimension | Scale | Range |
|---|---|---|---|
| self_esteem | Psychological | Quasi-continuous (Rosenberg-type summed scale) | 0-30 |
| sleep_quality | Physiological | Ordinal | 0-5 |
| safety | Environmental | Ordinal | 0-5 |
| academic_performance | Academic | Ordinal, self-rated | 0-5 |
| social_support | Social | Ordinal | 0-3 |

All five variables are negatively coded relative to stress: higher scores 
represent more favorable conditions.

**Data quality:** No missing values, no duplicate records. Values flagged as 
statistical outliers in boxplots were retained, as they fall within each 
variable's valid documented range and represent legitimate responses rather 
than data errors.

**Note on dataset selection:** An initial 150,000-row synthetic dataset was 
evaluated first. A full correlation matrix showed no meaningful relationship 
between any pair of variables (all |r| < 0.01), indicating no embedded 
structure. This dataset was replaced with the current, empirically validated 
one before any research question was finalized.

## 3. Methods

**Variable selection:** Within each Biopsychosocial dimension, the variable 
with the strongest raw correlation to stress_level was selected, with two 
exceptions chosen for conceptual alignment with the research theme over raw 
correlation strength (academic_performance over future_career_concerns; 
social_support over bullying).

**Primary method:** Kruskal-Wallis H test, run separately for each of the 
five predictors across the three stress_level groups, paired with Spearman 
rank correlation (with 95% CI via Fisher z-transformation) to summarize 
direction and strength in a single coefficient.

**Why Kruskal-Wallis over ANOVA:** The outcome has three groups, ruling out 
a t-test. Shapiro-Wilk tests confirmed non-normal distributions for all five 
predictors in all three groups (p < 0.000001 throughout), ruling out one-way 
ANOVA's normality assumption. Kruskal-Wallis compares distributions via ranks 
and is appropriate for ordinal/discrete Likert-type data.

**Alternatives considered and rejected:** Independent t-test (only handles 2 
groups); one-way ANOVA (normality violated); Chi-square test of independence 
(discards ordinal information — retained as a conceptual alternative, not used 
as primary).

**Multiple comparisons:** Benjamini-Hochberg FDR correction applied across 
the five Kruskal-Wallis tests.

**Robustness checks (Q7):** (1) Jonckheere-Terpstra test, which exploits the 
natural ordering of stress groups (Low < Medium < High) for greater 
statistical power; (2) a multivariable ordinal logistic regression (all five 
predictors simultaneously), with Variance Inflation Factors (VIF) checked 
beforehand due to moderate-to-high inter-predictor correlation (r = 0.56-0.68).

## 4. Results

All five predictors showed a statistically significant association with 
stress level, surviving FDR correction (all p_adjusted ≈ 0):

| Variable | Kruskal-Wallis H | Epsilon-squared | Spearman rho | 95% CI |
|---|---|---|---|---|
| self_esteem | 668.58 | 0.608 | -0.779 | [-0.801, -0.755] |
| sleep_quality | 636.39 | 0.579 | -0.761 | [-0.785, -0.735] |
| academic_performance | 590.85 | 0.538 | -0.728 | [-0.755, -0.699] |
| safety | 573.12 | 0.522 | -0.714 | [-0.742, -0.684] |
| social_support | 498.52 | 0.454 | -0.644 | [-0.677, -0.608] |

Effect sizes (epsilon-squared: 0.45-0.61) are large by conventional 
benchmarks (Tomczak & Tomczak, 2014), and none of the 95% confidence 
intervals include zero.

**Robustness:** The Jonckheere-Terpstra test confirmed a significant 
monotonic trend for all five variables (z = 21.1 to 28.4, p ≈ 0), with the 
same relative ranking as Kruskal-Wallis. The multivariable ordinal logistic 
regression showed all five predictors remained significant (p < 0.05) after 
mutual adjustment, though VIF values (8.8-12.3) indicate substantial 
multicollinearity, so individual coefficient magnitudes should be interpreted 
cautiously. After rescaling coefficients to each variable's full range to 
allow fair comparison, the resulting ranking matched the univariate results: 
self-esteem and sleep quality strongest, social support weakest.

Four independent methods therefore converge on the same conclusion and the 
same relative ranking of predictors.

## 5. Discussion

Self-esteem, sleep quality, perceived safety, academic performance, and 
social support each show a robust, convergent, and directionally consistent 
negative association with self-reported student stress in this sample. 
Effect sizes are large enough to carry practical as well as statistical 
significance — this is not a case of a trivial effect made "significant" by 
a large sample. The consistency of findings across rank-based tests, a 
trend-sensitive test, and a multivariable model strengthens confidence that 
the pattern is real rather than a methodological artifact.

The convergence across all four methods also suggests the finding is not 
sensitive to the choice of statistical technique, which was one of the 
project's explicit goals for the robustness/sensitivity analysis (Q7).

## 6. Limitations

- **No causal inference:** The data are cross-sectional; all five predictors 
  and the outcome were measured at a single point in time. Reverse causality 
  (e.g., stress reducing perceived sleep quality) is equally plausible.
- **Common method bias:** All variables were collected via self-report in a 
  single survey administration. A general tendency toward negative 
  self-appraisal could inflate the observed associations independent of any 
  true underlying relationship. This may partly explain why effect sizes are 
  unusually large and uniform across all predictors compared to typical 
  psychological survey research.
- **Measurement limitations:** Most variables lack a documented, validated 
  item set (self_esteem, resembling the Rosenberg Self-Esteem Scale, is a 
  partial exception). `academic_performance` is self-perceived, not an 
  objective measure such as GPA. `safety` is ambiguous as to context (home, 
  campus, or neighborhood).
- **Selection bias:** Sampling method, demographics, and institutional 
  context of the 1,100 students are undocumented, limiting generalizability.
- **Multicollinearity:** VIF values of 8.8-12.3 in the combined model limit 
  precise attribution of independent effect size, though each predictor's 
  association survives mutual adjustment.

## 7. Conclusion

Within the constraints above, this analysis provides strong, methodologically 
convergent evidence that all five Biopsychosocial dimensions — psychological, 
physiological, environmental, academic, and social — are associated with 
student stress level, consistent with theoretical expectations. Self-esteem 
and sleep quality show the strongest associations; social support the 
weakest, though still substantial. These findings do not support causal 
claims about any single factor "driving" student stress, and should be 
interpreted as evidence for association only.

## Appendix: Full Statistical Output

### A1. Kruskal-Wallis + Spearman — Full Results (Q6)

| Variable | H statistic | df | p (raw) | p (FDR-adjusted) | Significant | Epsilon² |
|---|---|---|---|---|---|---|
| self_esteem | 668.582 | 2 | <0.0001 | <0.0001 | Yes | 0.608 |
| sleep_quality | 636.386 | 2 | <0.0001 | <0.0001 | Yes | 0.579 |
| academic_performance | 590.850 | 2 | <0.0001 | <0.0001 | Yes | 0.538 |
| safety | 573.124 | 2 | <0.0001 | <0.0001 | Yes | 0.522 |
| social_support | 498.525 | 2 | <0.0001 | <0.0001 | Yes | 0.454 |

*Note: raw p-values were already below floating-point display precision 
(reported as 0.0000 at 4 decimal places) before correction was applied. 
Benjamini-Hochberg FDR correction was still applied as planned methodology, 
but in this case it did not change any conclusion, since evidence against 
the null was already overwhelming at the raw stage.*

### A2. Jonckheere-Terpstra Test — Full Results (Q7, Robustness Check 1)

Groups ordered High → Medium → Low to test for a monotonic increasing trend 
(normal approximation, no tie correction).

| Variable | J statistic | z | p-value |
|---|---|---|---|
| self_esteem | 364,414.0 | 28.382 | <0.0001 |
| sleep_quality | 358,253.0 | 27.307 | <0.0001 |
| academic_performance | 348,084.0 | 25.534 | <0.0001 |
| safety | 344,557.5 | 24.919 | <0.0001 |
| social_support | 322,489.5 | 21.072 | <0.0001 |

### A3. Variance Inflation Factors (Q7, Robustness Check 2)

| Variable | VIF |
|---|---|
| self_esteem | 12.329 |
| safety | 10.736 |
| academic_performance | 10.443 |
| sleep_quality | 9.408 |
| social_support | 8.769 |

All VIF values exceed the conventional caution threshold of 5, and three 
exceed 10, indicating substantial multicollinearity among the five 
predictors. This affects the precision of individual coefficient estimates 
in the combined model below but does not affect the univariate results in 
A1/A2.

### A4. Multivariable Ordinal Logistic Regression — Full Model (Q7, Robustness Check 2)

Proportional odds model, N = 1,100, df model = 5, Log-Likelihood = -522.43, 
AIC = 1059, BIC = 1094.

| Variable | Coefficient | SE | z | p | 95% CI |
|---|---|---|---|---|---|
| self_esteem | -0.134 | 0.015 | -8.809 | <0.0001 | [-0.164, -0.104] |
| sleep_quality | -0.732 | 0.079 | -9.210 | <0.0001 | [-0.888, -0.576] |
| academic_performance | -0.666 | 0.089 | -7.476 | <0.0001 | [-0.841, -0.492] |
| safety | -0.576 | 0.089 | -6.495 | <0.0001 | [-0.749, -0.402] |
| social_support | -0.226 | 0.096 | -2.360 | 0.018 | [-0.414, -0.038] |
| Threshold 0/1 | -9.892 | 0.407 | -24.299 | <0.0001 | [-10.690, -9.094] |
| Threshold 1/2 | 1.309 | 0.049 | 26.577 | <0.0001 | [1.212, 1.406] |

**Full-range rescaled effect** (coefficient × variable's scale range, to allow 
fair comparison across variables measured on different scales):

| Variable | Scale range | Full-range log-odds effect |
|---|---|---|
| self_esteem | 30 | -4.01 |
| sleep_quality | 5 | -3.66 |
| academic_performance | 5 | -3.33 |
| safety | 5 | -2.88 |
| social_support | 3 | -0.68 |

This rescaled ranking matches the univariate ranking in A1, providing an 
additional layer of convergence despite the multicollinearity noted in A3.