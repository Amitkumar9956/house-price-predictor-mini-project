# Day 6 - Saving and Loading the Machine Learning Model

## Objective

Save the trained Random Forest model and load it later for predictions.

---

## Topics Covered

- Joblib
- Model Persistence
- Saving Models
- Loading Models

---

## New Library

```python
import joblib
```

---

## New Functions

### Save Model

```python
joblib.dump(rf_model, "house_price_model.pkl")
```

Saves the trained model to disk.

---

### Load Model

```python
loaded_model = joblib.load("house_price_model.pkl")
```

Loads the saved model into memory.

---

### Predict

```python
loaded_predictions = loaded_model.predict(X_test)
```

Uses the loaded model to predict new data.

---

## Learning

- Training a model can take a long time.
- Save the model once and reuse it later.
- `.pkl` files store trained machine learning models.
- Joblib is commonly used for saving scikit-learn models.

---

## Learning Outcome

After completing Day 6, I can:

- Save a trained machine learning model.
- Load the saved model.
- Predict without retraining.
- Understand model persistence.