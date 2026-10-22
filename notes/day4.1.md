# Day 4.1- Linear Regression Model and Evaluation

## Objective

Build the first Machine Learning model to predict house prices and evaluate its performance.

---

## Topics Covered

- Linear Regression
- Model Training
- Prediction
- Model Evaluation
- MAE
- RMSE
- R² Score

---

## New Libraries

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import numpy as np
```

---

## New Functions

### 1. LinearRegression()

Creates a Linear Regression model.

Example:

```python
model = LinearRegression()
```

---

### 2. fit()

Trains the model using training data.

Example:

```python
model.fit(X_train, y_train)
```

---

### 3. predict()

Predicts house prices for unseen data.

Example:

```python
predictions = model.predict(X_test)
```

---

### 4. mean_absolute_error()

Calculates the average prediction error.

Example:

```python
mae = mean_absolute_error(y_test, predictions)
```

---

### 5. mean_squared_error()

Calculates the average squared error.

Example:

```python
mse = mean_squared_error(y_test, predictions)
```

---

### 6. np.sqrt()

Calculates the square root of MSE to obtain RMSE.

Example:

```python
rmse = np.sqrt(mse)
```

---

### 7. r2_score()

Measures how well the model explains the variation in the target variable.

Example:

```python
r2 = r2_score(y_test, predictions)
```

---

## Workflow

1. Import the required libraries.
2. Create the Linear Regression model.
3. Train the model using the training dataset.
4. Predict house prices on the test dataset.
5. Compare predicted prices with actual prices.
6. Evaluate the model using MAE, RMSE, and R² Score.

---

## Model Evaluation Results

### Mean Absolute Error (MAE)

MAE = 20383.82

Meaning:

On average, the predicted house price differs from the actual price by about $20,384.

---

### Root Mean Squared Error (RMSE)

RMSE = 31932.44

Meaning:

RMSE gives more importance to larger prediction errors. Lower RMSE indicates a better model.

---

### R² Score

R² = 0.8671

Meaning:

The model explains approximately 86.7% of the variation in house prices.

This indicates that the Linear Regression model performs well on this dataset.

---

## Actual vs Predicted

Example:

| Actual Price | Predicted Price |
|--------------|-----------------|
| 154500 | 156441 |
| 325000 | 339187 |
| 115000 | 86611 |
| 159000 | 187116 |
| 315500 | 320804 |

The predictions are reasonably close to the actual values, although some prediction error still exists.

---

## Key Concepts Learned

### Model

A mathematical algorithm that learns patterns from data.

---

### Training

The process of teaching the model using known input-output examples.

---

### Prediction

Using the trained model to estimate outputs for unseen data.

---

### Evaluation

Measuring how accurately the model predicts the target values.

---

## Important Metrics

### MAE

Average prediction error.

Lower MAE is better.

---

### RMSE

Measures prediction error while giving higher penalties to large mistakes.

Lower RMSE is better.

---

### R² Score

Measures how well the model fits the data.

Range:

- 1.0 → Perfect model
- Above 0.90 → Excellent
- 0.80–0.90 → Very Good
- 0.70–0.80 → Good
- Below 0.70 → Needs Improvement

---

## Learning Outcome

After completing Day 4, I can:

- Build a Linear Regression model.
- Train the model using training data.
- Predict house prices.
- Compare predicted and actual values.
- Evaluate the model using MAE, RMSE, and R² Score.
- Interpret evaluation metrics to judge model performance.

---

## Conclusion

Day 4 introduced the first Machine Learning model for the House Price Prediction project.

The model achieved an R² Score of **0.8671**, indicating strong predictive performance.

This serves as the baseline model. In the next stage, more advanced algorithms such as Random Forest will be implemented and compared to improve prediction accuracy.