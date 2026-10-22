from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

# Data Files
RAW_DATA_PATH = DATA_DIR / "train.csv"
CLEANED_DATA_PATH = DATA_DIR / "cleaned_train.csv"
PROCESSED_DATA_PATH = DATA_DIR / "processed_train.csv"
TEST_DATA_PATH = DATA_DIR / "test.csv"

# Model Artifacts
MODEL_PATH = MODELS_DIR / "house_price_model.pkl"
FEATURE_COLUMNS_PATH = MODELS_DIR / "feature_columns.pkl"
BASELINE_INPUT_PATH = MODELS_DIR / "baseline_input.pkl"

# Visualizations
FEATURE_IMPORTANCE_PNG = BASE_DIR / "feature_importance.png"
MODEL_COMPARISON_PNG = BASE_DIR / "model_comparison.png"

# Supported Ames Neighborhoods
NEIGHBORHOODS = [
    "Blmngtn", "Blueste", "BrDale", "BrkSide", "ClearCr", "CollgCr", "Crawfor",
    "Edwards", "Gilbert", "IDOTRR", "MeadowV", "Mitchel", "NAmes", "NPkVill",
    "NWAmes", "NoRidge", "NridgHt", "OldTown", "SWISU", "Sawyer", "SawyerW",
    "Somerst", "StoneBr", "Timber", "Veenker"
]

# Random Forest Hyperparameters
RF_PARAMS = {
    "n_estimators": 300,
    "max_depth": 20,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "random_state": 42
}
