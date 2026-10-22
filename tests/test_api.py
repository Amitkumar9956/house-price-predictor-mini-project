import unittest
import json
from flask_app import app


class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_health_endpoint(self):
        """GET /health should return status 200 with model_ready: True."""
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("model_ready"))
        self.assertEqual(data.get("status"), "healthy")

    def test_index_page(self):
        """GET / should render Homepage containing brand and hero section."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b"HousePrice" in response.data or b"Property Valuation" in response.data)

    def test_predict_page_get(self):
        """GET /predict should render the dedicated input form."""
        response = self.client.get("/predict")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"valuationForm", response.data)
        self.assertIn(b"CollgCr", response.data)

    def test_calculate_and_result_flow(self):
        """POST /calculate should validate, predict, and redirect to dedicated Result Page (/result)."""
        payload = {
            "Neighborhood": "CollgCr",
            "OverallQual": 6,
            "OverallCond": 5,
            "GrLivArea": 1600,
            "LotArea": 8500,
            "TotalBsmtSF": 900,
            "BedroomAbvGr": 3,
            "TotRmsAbvGrd": 6,
            "FullBath": 2,
            "HalfBath": 1,
            "YearBuilt": 1995,
            "YearRemodAdd": 2005,
            "GarageCars": 2,
            "GarageArea": 480
        }
        # Follow redirect from /calculate to /result
        response = self.client.post("/calculate", data=payload, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Valuation Report Generated", response.data)
        self.assertIn(b"ESTIMATED MARKET VALUATION", response.data)
        self.assertIn(b"$", response.data)

    def test_predict_endpoint_valid_json(self):
        """POST /api/predict with valid payload should return 200 and formatted price."""
        payload = {
            "Neighborhood": "CollgCr",
            "OverallQual": 6,
            "OverallCond": 5,
            "GrLivArea": 1600,
            "LotArea": 8500,
            "TotalBsmtSF": 900,
            "BedroomAbvGr": 3,
            "TotRmsAbvGrd": 6,
            "FullBath": 2,
            "HalfBath": 1,
            "YearBuilt": 1995,
            "YearRemodAdd": 2005,
            "GarageCars": 2,
            "GarageArea": 480
        }
        response = self.client.post(
            "/api/predict",
            data=json.dumps(payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("$", data.get("formatted_price"))
        self.assertGreater(data.get("prediction"), 0)

    def test_predict_endpoint_invalid(self):
        """POST /api/predict with invalid data should return 400 with descriptive error."""
        invalid_payload = {
            "Neighborhood": "CollgCr",
            "OverallQual": 6,
            "GrLivArea": -500  # invalid negative area
        }
        response = self.client.post(
            "/api/predict",
            data=json.dumps(invalid_payload),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertFalse(data.get("success"))
        self.assertIn("error", data)


if __name__ == "__main__":
    unittest.main()
