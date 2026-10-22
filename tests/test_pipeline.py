import unittest
from pathlib import Path
from src.predict import (
    load_model,
    load_feature_columns,
    load_baseline_input,
    prepare_input_features,
    predict,
    predict_price,
    validate_user_inputs
)
from src.config import MODEL_PATH, FEATURE_COLUMNS_PATH, RAW_DATA_PATH


class TestMLPipeline(unittest.TestCase):

    def test_artifacts_exist(self):
        """Verify that essential model and data files exist."""
        self.assertTrue(MODEL_PATH.exists(), f"Model missing at: {MODEL_PATH}")
        self.assertTrue(FEATURE_COLUMNS_PATH.exists(), f"Feature columns missing at: {FEATURE_COLUMNS_PATH}")
        self.assertTrue(RAW_DATA_PATH.exists(), f"Raw dataset missing at: {RAW_DATA_PATH}")

    def test_model_loading(self):
        """Verify that the trained model loads and has predict method."""
        model = load_model()
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, "predict"))

    def test_feature_columns(self):
        """Verify feature column list is non-empty and contains expected features."""
        cols = load_feature_columns()
        self.assertIsInstance(cols, list)
        self.assertGreater(len(cols), 50)
        self.assertIn("OverallQual", cols)
        self.assertIn("GrLivArea", cols)

    def test_prediction_output(self):
        """Verify that prediction returns a plausible positive price."""
        test_house = {
            "Neighborhood": "CollgCr",
            "OverallQual": 7,
            "OverallCond": 5,
            "GrLivArea": 1800,
            "LotArea": 9000,
            "TotalBsmtSF": 1000,
            "BedroomAbvGr": 3,
            "FullBath": 2,
            "HalfBath": 1,
            "TotRmsAbvGrd": 7,
            "YearBuilt": 2005,
            "YearRemodAdd": 2006,
            "GarageCars": 2,
            "GarageArea": 500
        }
        price = predict_price(test_house)
        self.assertIsInstance(price, float)
        self.assertGreater(price, 50000.0)
        self.assertLess(price, 1000000.0)

    def test_validation_errors(self):
        """Verify that invalid inputs raise descriptive ValueError."""
        # Quality > 10
        with self.assertRaises(ValueError):
            validate_user_inputs({"OverallQual": 12})

        # Negative area
        with self.assertRaises(ValueError):
            validate_user_inputs({"GrLivArea": -100})

        # Year remodeled earlier than built
        with self.assertRaises(ValueError):
            validate_user_inputs({"YearBuilt": 2010, "YearRemodAdd": 1990})


if __name__ == "__main__":
    unittest.main()
