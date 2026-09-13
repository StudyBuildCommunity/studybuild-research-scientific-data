# Academic Stress and Student Well-being

This project examines whether study load, sleep quality, and social support are associated with students' stress levels.

## Research question

Are study load, sleep quality, and social support associated with students' stress levels?

The analysis is observational, so the results are interpreted as associations rather than causal effects.

## Data

Dataset: `StressLevelDataset.csv`

Source: Student Stress Factors dataset on Kaggle  
https://www.kaggle.com/datasets/samyakb/student-stress-factors

The analysis focuses on:

- `stress_level`
- `study_load`
- `sleep_quality`
- `social_support`

Before modeling, the notebook checks data types, missing values, duplicate rows, observed ranges, and stress-level codes.

## Methods

The main model is ordinal logistic regression because the outcome has three ordered stress categories.

Supporting analyses include:

- Chi-square tests
- Cramer's V
- Spearman correlation
- VIF for multicollinearity
- threshold-specific logistic models
- multinomial logistic regression as a sensitivity analysis

The multinomial model is used because the proportional-odds assumption appears questionable for social support.

## Main findings

Higher study load is associated with higher stress.

Higher sleep-quality scores are associated with lower stress.

Social support shows a more category-specific pattern. Its relationship is much stronger for high versus low stress than for medium versus low stress after adjustment.

These results should not be interpreted as causal effects.

## Repository structure

```text
academic-stress-research/
├── README.md
├── requirements.txt
├── data/
│   └── StressLevelDataset.csv
├── notebooks/
│   └── finalresreach_FINAL_REVIEWED.ipynb
└── figures/
```

## How to run

1. Create a Python environment.
2. Install the packages:

```bash
pip install -r requirements.txt
```

3. Place the dataset in the `data/` folder.
4. Open the notebook.
5. Restart the kernel and run all cells from top to bottom.

## Limitations

The data are observational, so causal conclusions are not supported.

Some variables are integer-coded scores and complete scale documentation is limited in the notebook.

Information about the sampling frame is limited, so the findings should not automatically be generalized to all students.

The proportional-odds assumption is not equally convincing for all predictors, especially social support.
