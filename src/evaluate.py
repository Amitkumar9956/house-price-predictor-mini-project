import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_model(model, X_test, y_test):
    """
    Evaluates a regression model using MAE, RMSE, and R2 score.
    Returns: predictions, mae, rmse, r2
    """
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    r2 = r2_score(y_test, predictions)
    return predictions, mae, rmse, r2


def compare_models(models_dict, X_test, y_test):
    """
    Evaluates a dictionary of {model_name: model_instance} on test data.
    Returns a pandas DataFrame comparing MAE, RMSE, and R2 score.
    """
    records = []
    for name, model in models_dict.items():
        preds, mae, rmse, r2 = evaluate_model(model, X_test, y_test)
        records.append({
            "Model": name,
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2 Score": round(r2, 4)
        })

    return pd.DataFrame(records)