# Day 7 - Random Forest Regression

## Objective
Build a Random Forest model and compare it with Linear Regression.

## Topics Covered
- Random Forest Regressor
- Ensemble Learning
- Model Comparison

## New Library
from sklearn.ensemble import RandomForestRegressor

## New Functions
- RandomForestRegressor()
- fit()
- predict()

## Parameters
- n_estimators = 100
- random_state = 42

## Learning
Random Forest builds multiple Decision Trees and averages their predictions.

Advantages:
- Handles non-linear relationships
- Higher accuracy
- Reduces overfitting
- More robust than a single Decision Tree

## Comparison
Compare:
- MAE
- RMSE
- R² Score

The model with lower MAE/RMSE and higher R² performs better.

# Feature Importance

## Objective

Understand which features have the greatest impact on house price prediction.

---

## Topics Covered

- Feature Importance
- Random Forest Analysis
- Data Visualization

---

## New Attribute

```python
feature_importances_
```

Returns the importance score of each feature used by the Random Forest model.

---

## Workflow

1. Train Random Forest.
2. Extract feature importance.
3. Create a DataFrame.
4. Sort features.
5. Display Top 10 features.
6. Plot a bar chart.

---

## Learning

- Feature Importance helps explain model behavior.
- Higher importance means the feature contributes more to predictions.
- Random Forest provides built-in feature importance scores.

---

## Common Important Features

- OverallQual
- GrLivArea
- GarageCars
- TotalBsmtSF
- GarageArea
- YearBuilt
- LotArea

---

## Learning Outcome

After completing Day 5, I can:

- Extract feature importance.
- Identify the most influential features.
- Visualize feature importance using a bar chart.
- Interpret why some features matter more than others.