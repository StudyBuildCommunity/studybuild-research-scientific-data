# Academic Stress & Student Burnout — A Biopsychosocial Analysis

Statistical analysis of student stress using a research-driven, hypothesis-tested
methodology grounded in the Biopsychosocial Model (Engel, 1977).

## Overview

This project investigates whether five indicators — spanning the psychological,
physiological, environmental, academic, and social dimensions of student
well-being — are associated with self-reported student stress level.

**Research Question:** Are self-esteem, sleep quality, perceived safety, academic
performance, and social support — representing the psychological, physiological,
environmental, academic, and social dimensions of the Biopsychosocial Model —
associated with student stress level?

This is an observational, cross-sectional study. All findings are reported in
terms of *association*, not causation.

## Repository Structure

```
academic-stress-burnout-analysis/
│
├── notebook/
│   └── academic_stress_burnout_analysis.ipynb
│
├── data/
│   └── StressLevelDataset.csv
│
├── figures/
│   ├── stress_level_distribution.png
│   ├── predictors_by_stress_boxplots.png
│   └── self_esteem_distribution.png
│
├── report/
│   └── mini_research_report.md
│
└── README.md
```

## Dataset

- **Source:** [Student Stress Factors: A Comprehensive Analysis](https://www.kaggle.com/datasets/rxnach/student-stress-factors-a-comprehensive-analysis) (Kaggle, author: rxnach)
- **File used:** `StressLevelDataset.csv`
- **Sample size:** 1,100 students, survey-based (not synthetic)
- **Scope:** 21 variables spanning psychological, physiological, environmental,
  academic, and social factors related to student stress

### Note on Dataset Selection

An initial candidate dataset (a 150,000-row synthetic dataset on Kaggle) was
tested first. A full correlation matrix revealed no meaningful relationship
between *any* pair of variables (all |r| < 0.01), including between the outcome
variable and every predictor — indicating the dataset had no embedded structure.
This was documented as a finding rather than discarded silently, and the project
was rebuilt on the current, empirically validated dataset instead. This decision
is elaborated in the Mini Research Report's Limitations section and reflects a
deliberate data-quality check performed *before* committing to a research
question — full correlation screening is recommended as a first step whenever
working with a large or synthetic dataset.

### Data Dictionary (Variables Used in This Study)

| Variable | Role | Biopsychosocial Dimension | Scale | Range | Direction |
|---|---|---|---|---|---|
| `stress_level` | Outcome | — | Ordinal (3 levels) | 0–2 | 0=Low, 1=Medium, 2=High |
| `self_esteem` | Predictor | Psychological | Quasi-continuous (summed scale, Rosenberg-type) | 0–30 | Higher = higher self-esteem |
| `sleep_quality` | Predictor | Physiological | Ordinal (6-point) | 0–5 | Higher = better sleep quality |
| `safety` | Predictor | Environmental | Ordinal (6-point) | 0–5 | Higher = greater perceived safety |
| `academic_performance` | Predictor | Academic | Ordinal (6-point, self-rated) | 0–5 | Higher = better self-rated performance |
| `social_support` | Predictor | Social | Ordinal (4-point) | 0–3 | Higher = more perceived support |

The dataset contains 15 additional variables not used in this study (e.g.
`anxiety_level`, `depression`, `bullying`, `blood_pressure`). These were
reviewed during variable selection but excluded to keep the analysis focused
and theoretically grounded — see the method-selection note below.

**Documented ambiguities:**
- `safety`: the dataset does not specify whether this refers to home, campus,
  or neighborhood safety.
- `academic_performance`: this is self-perceived performance, not an objective
  measure such as GPA.
- No official codebook with exact item wording is publicly available; variable
  interpretation relies on column names and prior published analyses of this
  dataset.

**Data quality:** No missing values, no duplicate records. Values flagged as
statistical outliers in boxplots were retained — they fall within each
variable's valid, documented scale range and represent legitimate individual
responses rather than data errors. The chosen statistical methods
(Kruskal-Wallis, Spearman) are rank-based and inherently robust to extreme
values.

## Method-Selection Note

**Chosen approach:** Kruskal-Wallis H test (per predictor) + Spearman rank
correlation, followed by a Jonckheere-Terpstra trend test and a multivariable
ordinal logistic regression as robustness checks.

**Why:** The outcome (`stress_level`) has three ordinal categories, ruling out
a two-sample t-test. Visual inspection (boxplots, histograms) and formal
Shapiro-Wilk tests confirmed non-normal distributions across all five
predictors in all three groups, ruling out one-way ANOVA. Kruskal-Wallis and
Spearman make no normality assumption and are appropriate for ordinal/discrete
Likert-type data.

**Alternatives considered and rejected as primary methods:**
- *Independent t-test* — mathematically inapplicable (3 groups, not 2).
- *One-way ANOVA* — normality assumption violated.
- *Chi-square test of independence* — discards ordinal information by treating
  categories as nominal.

**Assumptions and limitations:** The five predictors show moderate-to-high
pairwise correlation (r = 0.56–0.68) and substantial multicollinearity in the
combined model (VIF = 8.8–12.3). This does not invalidate the univariate
Kruskal-Wallis/Spearman results, but individual coefficients from the combined
regression model should be interpreted with caution.

Full method justification is in Q4–Q5 of the notebook and the Mini Research
Report.

## Key Findings (Summary)

- All five predictors show a statistically significant, moderate-to-large
  negative association with stress level (epsilon-squared = 0.45–0.61),
  confirmed convergently across four independent statistical methods.
- Self-esteem and sleep quality show the strongest association; social support
  the weakest (though still significant).
- Findings represent *association*, not causation — the data are
  cross-sectional and self-reported, so reverse causality and common method
  bias cannot be ruled out.

Full results, effect sizes, confidence intervals, and discussion are in
[`report/mini_research_report.md`](report/mini_research_report.md).

## How to Reproduce

```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn
jupyter notebook notebook/academic_stress_burnout_analysis.ipynb
```

Run all cells in order. The notebook is self-contained and reads
`data/StressLevelDataset.csv` directly.

## Tools & Libraries

Python, pandas, numpy, scipy.stats, statsmodels (OrderedModel, VIF), matplotlib,
seaborn.

## Author

Ali Aghili ([@aliaghilii](https://github.com/aliaghilii)) — StudyBuild
Data Analytics Community
