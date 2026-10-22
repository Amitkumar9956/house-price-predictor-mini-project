import os
from pathlib import Path
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from src.predict import (
    load_model,
    load_feature_columns,
    load_baseline_input,
    predict_price,
    validate_user_inputs
)
from src.config import NEIGHBORHOODS

BASE_DIR = Path(__file__).resolve().parent

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)
app.secret_key = os.environ.get("SECRET_KEY", "house-price-prediction-secret-key-2026")


@app.route("/")
def home():
    """Homepage: Beautiful hero section, project overview, model stats, and CTA."""
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict_page():
    """
    Input Page:
    - GET: renders the dedicated input form.
    - POST: handles legacy JSON requests for testing/API compatibility.
    """
    if request.method == "POST" and request.is_json:
        return handle_api_prediction(request.get_json())

    return render_template("predict.html", neighborhoods=sorted(NEIGHBORHOODS))


@app.route("/calculate", methods=["POST"])
def calculate():
    """
    Form submission handler:
    Validates user input, calls the ML model, saves the valuation to session,
    and navigates the user to the dedicated Result Page (/result).
    """
    try:
        data = request.form.to_dict()
        if not data:
            flash("Please enter property details before submitting.", "error")
            return redirect(url_for("predict_page"))

        # 1. Validate inputs
        validate_user_inputs(data)

        # 2. Predict actual price using the trained Random Forest model
        price = predict_price(data)

        # 3. Calculate derived metrics
        liv_area = float(data.get("GrLivArea", 1500))
        lot_area = float(data.get("LotArea", 8500))
        bsmt_area = float(data.get("TotalBsmtSF", 900))
        price_per_sqft = price / max(liv_area, 1.0)

        # Ames dataset median sale price benchmark
        ames_median = 163000.0
        diff_from_median = price - ames_median

        # Typical confidence bounds based on test MAE (~$17,676)
        mae_margin = 17676.0
        lower_bound = max(price - mae_margin, 25000.0)
        upper_bound = price + mae_margin

        # Package data for the dedicated result page
        result_payload = {
            "prediction": round(price, 2),
            "formatted_price": f"${price:,.2f}",
            "lower_bound": f"${lower_bound:,.2f}",
            "upper_bound": f"${upper_bound:,.2f}",
            "price_per_sqft": f"${price_per_sqft:,.2f}",
            "diff_from_median": f"{'+' if diff_from_median >= 0 else '-'}${abs(diff_from_median):,.2f}",
            "is_above_median": diff_from_median >= 0,
            "inputs": {
                "neighborhood": data.get("Neighborhood", "CollgCr"),
                "overall_qual": int(data.get("OverallQual", 6)),
                "overall_cond": int(data.get("OverallCond", 5)),
                "gr_liv_area": int(liv_area),
                "lot_area": int(lot_area),
                "total_bsmt_sf": int(bsmt_area),
                "bedrooms": int(data.get("BedroomAbvGr", 3)),
                "full_baths": int(data.get("FullBath", 2)),
                "half_baths": int(data.get("HalfBath", 1)),
                "total_rooms": int(data.get("TotRmsAbvGrd", 6)),
                "year_built": int(data.get("YearBuilt", 1995)),
                "year_remod": int(data.get("YearRemodAdd", 2005)),
                "garage_cars": int(data.get("GarageCars", 2)),
                "garage_area": int(float(data.get("GarageArea", 480))),
                "property_age": 2026 - int(data.get("YearBuilt", 1995))
            }
        }

        session["valuation_result"] = result_payload
        return redirect(url_for("result_page"))

    except ValueError as ve:
        flash(f"Validation Error: {str(ve)}", "error")
        return redirect(url_for("predict_page"))

    except Exception as e:
        flash(f"Prediction Error: {str(e)}", "error")
        return redirect(url_for("predict_page"))


@app.route("/result")
def result_page():
    """
    Dedicated Result Page:
    Displays the actual valuation, price per sq ft, market comparison,
    specifications breakdown, and model performance metrics.
    """
    result = session.get("valuation_result")
    if not result:
        result = {
            "prediction": 218500.0,
            "formatted_price": "$218,500.00",
            "lower_bound": "$200,823.60",
            "upper_bound": "$236,176.40",
            "price_per_sqft": "$136.56",
            "diff_from_median": "+$55,500.00",
            "is_above_median": True,
            "inputs": {
                "neighborhood": "CollgCr",
                "overall_qual": 7,
                "overall_cond": 5,
                "gr_liv_area": 1600,
                "lot_area": 8500,
                "total_bsmt_sf": 900,
                "bedrooms": 3,
                "full_baths": 2,
                "half_baths": 1,
                "total_rooms": 6,
                "year_built": 2002,
                "year_remod": 2005,
                "garage_cars": 2,
                "garage_area": 480,
                "property_age": 24
            }
        }

    return render_template("result.html", result=result)


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """API endpoint returning JSON for programmatic/AJAX requests."""
    return handle_api_prediction(request.get_json() if request.is_json else request.form.to_dict())


def handle_api_prediction(data):
    try:
        if not data:
            return jsonify({"success": False, "error": "No input property data provided."}), 400

        validate_user_inputs(data)
        price = predict_price(data)
        liv_area = float(data.get("GrLivArea", 1500))
        price_per_sqft = price / max(liv_area, 1.0)

        return jsonify({
            "success": True,
            "prediction": round(price, 2),
            "formatted_price": f"${price:,.2f}",
            "price_per_sqft": f"${price_per_sqft:,.2f}",
            "summary": {
                "living_area": int(liv_area),
                "bedrooms": int(data.get("BedroomAbvGr", 3)),
                "bathrooms": float(data.get("FullBath", 2)) + 0.5 * float(data.get("HalfBath", 0)),
                "neighborhood": data.get("Neighborhood", "CollgCr"),
                "year_built": int(data.get("YearBuilt", 2000))
            }
        })
    except ValueError as ve:
        return jsonify({"success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/health")
def health():
    try:
        load_model()
        load_feature_columns()
        load_baseline_input()
        return jsonify({"status": "healthy", "model_ready": True})
    except Exception as e:
        return jsonify({"status": "degraded", "model_ready": False, "error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Flask House Price Prediction Server on http://127.0.0.1:{port}")
    app.run(host="127.0.0.1", port=port, debug=False)
