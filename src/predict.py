from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "data"

MODEL_FILE = MODEL_DIR / "house_price_model.pkl"
COLUMNS_FILE = MODEL_DIR / "feature_columns.pkl"
BASELINE_FILE = MODEL_DIR / "baseline_input.pkl"


def save_model(model, filepath=None):
    target = Path(filepath) if filepath else MODEL_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, target)


def load_model(filepath=None):
    target = Path(filepath) if filepath else MODEL_FILE
    if not target.exists():
        raise FileNotFoundError(f"Model file not found at: {target}")
    return joblib.load(target)


def save_feature_columns(columns, filepath=None):
    target = Path(filepath) if filepath else COLUMNS_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(list(columns), target)


def load_feature_columns(filepath=None):
    target = Path(filepath) if filepath else COLUMNS_FILE
    if not target.exists():
        raise FileNotFoundError(f"Feature columns file not found at: {target}")
    return joblib.load(target)


def save_baseline_input(baseline_dict, filepath=None):
    target = Path(filepath) if filepath else BASELINE_FILE
    target.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(baseline_dict, target)


def load_baseline_input(filepath=None):
    target = Path(filepath) if filepath else BASELINE_FILE
    if target.exists():
        return joblib.load(target)

    # Fallback to computing median from data/processed_train.csv if exists
    processed_path = DATA_DIR / "processed_train.csv"
    if processed_path.exists():
        df_proc = pd.read_csv(processed_path)
        if "SalePrice" in df_proc.columns:
            df_proc = df_proc.drop("SalePrice", axis=1)
        baseline = df_proc.median(numeric_only=True).to_dict()
        save_baseline_input(baseline)
        return baseline

    return {}


def validate_user_inputs(inputs: dict):
    """
    Validates range and logic of user inputs.
    Raises ValueError with descriptive message if invalid.
    """
    if "OverallQual" in inputs:
        val = int(inputs["OverallQual"])
        if not (1 <= val <= 10):
            raise ValueError("Overall Quality must be an integer between 1 and 10.")

    if "OverallCond" in inputs:
        val = int(inputs["OverallCond"])
        if not (1 <= val <= 10):
            raise ValueError("Overall Condition must be an integer between 1 and 10.")

    if "GrLivArea" in inputs:
        val = float(inputs["GrLivArea"])
        if val <= 0 or val > 15000:
            raise ValueError("Ground Living Area must be a positive number up to 15,000 sq ft.")

    if "LotArea" in inputs:
        val = float(inputs["LotArea"])
        if val <= 0 or val > 300000:
            raise ValueError("Lot Area must be a positive number up to 300,000 sq ft.")

    if "YearBuilt" in inputs:
        val = int(inputs["YearBuilt"])
        if not (1800 <= val <= 2030):
            raise ValueError("Year Built must be between 1800 and 2030.")

    if "YearRemodAdd" in inputs:
        val = int(inputs["YearRemodAdd"])
        if not (1800 <= val <= 2030):
            raise ValueError("Year Remodeled must be between 1800 and 2030.")
        if "YearBuilt" in inputs and val < int(inputs["YearBuilt"]):
            raise ValueError("Year Remodeled cannot be earlier than Year Built.")

    if "TotalBsmtSF" in inputs:
        val = float(inputs["TotalBsmtSF"])
        if val < 0 or val > 10000:
            raise ValueError("Basement Area cannot be negative or exceed 10,000 sq ft.")

    if "BedroomAbvGr" in inputs:
        val = int(inputs["BedroomAbvGr"])
        if val < 0 or val > 15:
            raise ValueError("Bedrooms count cannot be negative or exceed 15.")

    if "FullBath" in inputs:
        val = int(inputs["FullBath"])
        if val < 0 or val > 10:
            raise ValueError("Full Bathrooms cannot be negative or exceed 10.")

    if "GarageCars" in inputs:
        val = int(inputs["GarageCars"])
        if val < 0 or val > 10:
            raise ValueError("Garage Cars capacity cannot be negative or exceed 10.")


def prepare_input_features(user_inputs: dict, feature_columns=None, baseline_dict=None):
    """
    Prepares a 1-row DataFrame aligned with feature_columns:
    - Validates inputs
    - Populates baseline median values for unprovided features
    - Injects provided user features
    - Properly sets one-hot encoded categorical features (e.g. Neighborhood)
    """
    validate_user_inputs(user_inputs)

    if feature_columns is None:
        feature_columns = load_feature_columns()

    if baseline_dict is None:
        baseline_dict = load_baseline_input()

    # Create baseline single-row dictionary
    row_data = {}
    for col in feature_columns:
        row_data[col] = baseline_dict.get(col, 0.0)

    # Neighborhood one-hot encoding handling
    selected_neighborhood = user_inputs.get("Neighborhood")
    if selected_neighborhood:
        # Reset all neighborhood dummy columns to 0
        for col in feature_columns:
            if col.startswith("Neighborhood_"):
                row_data[col] = 0.0

        target_col = f"Neighborhood_{selected_neighborhood}"
        if target_col in row_data:
            row_data[target_col] = 1.0

    # Map direct numerical features
    numeric_feature_keys = [
        "OverallQual", "OverallCond", "YearBuilt", "YearRemodAdd",
        "GrLivArea", "LotArea", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF",
        "FullBath", "HalfBath", "BedroomAbvGr", "TotRmsAbvGrd",
        "Fireplaces", "GarageCars", "GarageArea"
    ]

    for key in numeric_feature_keys:
        if key in user_inputs and key in row_data:
            try:
                row_data[key] = float(user_inputs[key])
            except (ValueError, TypeError):
                pass

    # Build DataFrame in exact column order
    df_input = pd.DataFrame([row_data])[feature_columns]
    return df_input


def predict(model, X):
    """
    Direct model prediction for a DataFrame or array.
    """
    return model.predict(X)


def predict_price(user_inputs: dict):
    """
    End-to-end prediction function:
    Validates inputs, formats features, runs model, and returns estimated price.
    """
    model = load_model()
    feature_cols = load_feature_columns()
    baseline = load_baseline_input()

    input_df = prepare_input_features(user_inputs, feature_cols, baseline)
    pred = predict(model, input_df)
    return float(pred[0])