# Academic Stress & Student Well-being

An independent statistical analysis of the relationship between study load, sleep quality, social support, and student stress level.

## Research question

**Are study load, sleep quality, and social support associated with students' stress levels?**

The dataset is observational, so the analysis is about association rather than causation.

## Data

The project uses `StressLevelDataset.csv`, with 1,100 observations and 21 variables.

Dataset page: [Student Stress Factors: A Comprehensive Analysis](https://www.kaggle.com/datasets/rxnach/student-stress-factors-a-comprehensive-analysis/data)

The four variables used in the main analysis are:

| Variable | Role | Coding / observed range |
|---|---|---|
| `stress_level` | Outcome | 0 = Low, 1 = Medium, 2 = High |
| `study_load` | Predictor | 0-5 |
| `sleep_quality` | Predictor | 0-5 |
| `social_support` | Predictor | 0-3 |

Data-quality checks found no missing values and no exact duplicate rows. The original CSV is kept unchanged in `data/`.

## Analysis

The main model is **ordinal logistic regression** because `stress_level` has three ordered categories.

The analysis also includes:

- focused cross-tabulations and percentage plots;
- chi-square tests with Cramer's V for unadjusted categorical associations;
- Spearman correlations for monotonic associations;
- VIF to check multicollinearity;
- threshold-specific binary logistic models as an exploratory proportional-odds diagnostic;
- multinomial logistic regression as a sensitivity analysis when the proportional-odds assumption looked questionable.

## Main results

The adjusted ordinal-logistic estimates were:

| Predictor | Odds ratio | 95% CI | p-value |
|---|---:|---:|---:|
| Study load | 2.16 | 1.85-2.51 | < 0.001 |
| Sleep quality | 0.31 | 0.27-0.36 | < 0.001 |
| Social support | 0.45 | 0.38-0.53 | < 0.001 |

Higher study load was associated with higher stress, while higher sleep-quality and social-support scores were associated with lower odds of being in a higher stress category.

The threshold check suggested that the proportional-odds assumption was less convincing for social support. In the multinomial sensitivity analysis, social support did not clearly distinguish medium from low stress after adjustment (OR = 0.98, 95% CI 0.78-1.22, p = 0.836), but it was strongly associated with high versus low stress (OR = 0.17, 95% CI 0.12-0.24, p < 0.001). Because of this, the social-support result is interpreted more cautiously.

## Limitations

- The analysis is observational and cannot establish causal effects.
- The full wording and scale anchors for some integer-coded predictors are not available in the dataset file.
- Information about the sampling frame is limited, so the results should not automatically be generalized to all students.
- Other psychological, academic, and environmental factors may confound the observed relationships.
- Some relationships in the dataset are unusually strong, which is relevant when considering generalizability.
- The proportional-odds assumption is not equally convincing for all predictors.

## Repository structure

```text
academic-stress-research-final/
├── README.md
├── requirements.txt
├── data/
│   ├── README.md
│   └── StressLevelDataset.csv
├── notebooks/
│   └── analysis.ipynb
├── report/
│   └── mini_research_report.pdf
└── figures/
    ├── stress_by_study_load.png
    ├── stress_by_sleep_quality.png
    ├── stress_by_social_support.png
    ├── predicted_stress_by_study_load.png
    ├── predicted_stress_by_sleep_quality.png
    └── predicted_stress_by_social_support.png
```

## How to run

1. Create or activate a Python environment.
2. Install the packages:

```bash
pip install -r requirements.txt
```

3. Keep `StressLevelDataset.csv` inside the `data/` folder.
4. Open `notebooks/analysis.ipynb`.
5. Restart the kernel and run all cells from top to bottom.

The notebook saves the final figures automatically to `figures/`.
