import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from sklearn.model_selection import train_test_split, cross_val_score
from src.preprocessing import clean_data
from src.train import (
    train_linear_regression,
    train_decision_tree,
    train_random_forest
)
from src.evaluate import evaluate_model, compare_models
from src.predict import (
    save_model,
    load_model,
    save_feature_columns,
    save_baseline_input,
    predict
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"


def main():
    print("=" * 60)
    print("HOUSE PRICE PREDICTION: MACHINE LEARNING PIPELINE")
    print("=" * 60)

    # ==========================================================
    # STEP 1: Load and Clean Dataset
    # ==========================================================
    cleaned_csv = DATA_DIR / "cleaned_train.csv"
    if not cleaned_csv.exists():
        print("\nCleaned dataset not found. Running data cleaning step...")
        df = clean_data()
    else:
        print(f"\nLoading cleaned dataset from: {cleaned_csv}")
        df = pd.read_csv(cleaned_csv)

    print(f"Dataset shape: {df.shape}")
    print("\nFirst 5 rows (sample columns):")
    sample_cols = ["Id", "OverallQual", "GrLivArea", "GarageCars", "YearBuilt", "Neighborhood", "SalePrice"]
    available_sample_cols = [c for c in sample_cols if c in df.columns]
    print(df[available_sample_cols].head())

    # ==========================================================
    # STEP 2: One-Hot Encoding
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 2: One-Hot Encoding")
    print("=" * 60)

    # Remove Id column if present
    if "Id" in df.columns:
        df = df.drop("Id", axis=1)

    df_encoded = pd.get_dummies(df, drop_first=True)
    print("Shape after One-Hot Encoding:", df_encoded.shape)

    # ==========================================================
    # STEP 3: Features and Target Definition
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 3: Features and Target Definition")
    print("=" * 60)

    X = df_encoded.drop("SalePrice", axis=1)
    y = df_encoded["SalePrice"]

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # Save feature column names
    save_feature_columns(X.columns.tolist())
    print(f"Saved {len(X.columns)} feature columns to models/feature_columns.pkl")

    # Compute and save baseline feature medians for web app inference
    baseline_median = X.median(numeric_only=True).to_dict()
    save_baseline_input(baseline_median)
    print("Saved baseline feature median profile to models/baseline_input.pkl")

    # ==========================================================
    # STEP 4: Train-Test Split (Prevent Data Leakage)
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 4: Train-Test Split (80% Train, 20% Test)")
    print("=" * 60)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    print(f"Training set: X={X_train.shape}, y={y_train.shape}")
    print(f"Testing set : X={X_test.shape}, y={y_test.shape}")

    # Save processed training dataset for reference
    processed_df = pd.concat([X, y], axis=1)
    processed_df.to_csv(DATA_DIR / "processed_train.csv", index=False)
    print("Saved processed dataset to data/processed_train.csv")

    # ==========================================================
    # STEP 5: Train Candidate Regression Models
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 5: Training Candidate Models")
    print("=" * 60)

    # 1. Linear Regression
    print("Training Linear Regression baseline...")
    lr_model = train_linear_regression(X_train, y_train)

    # 2. Decision Tree Regressor
    print("Training Decision Tree Regressor...")
    dt_model = train_decision_tree(X_train, y_train, max_depth=10, random_state=42)

    # 3. Tuned Random Forest Regressor
    print("Training Tuned Random Forest Regressor...")
    rf_model = train_random_forest(
        X_train,
        y_train,
        n_estimators=300,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )

    # ==========================================================
    # STEP 6: Model Evaluation & Comparison
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 6: Model Performance Comparison on Test Set")
    print("=" * 60)

    models_dict = {
        "Linear Regression": lr_model,
        "Decision Tree": dt_model,
        "Tuned Random Forest": rf_model
    }

    comparison_df = compare_models(models_dict, X_test, y_test)
    print("\nPerformance Comparison Table:")
    print(comparison_df.to_string(index=False))

    # Evaluate individual metrics for reporting
    rf_preds, rf_mae, rf_rmse, rf_r2 = evaluate_model(rf_model, X_test, y_test)

    # ==========================================================
    # STEP 7: Cross-Validation
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 7: 5-Fold Cross-Validation (Random Forest)")
    print("=" * 60)

    cv_scores = cross_val_score(rf_model, X, y, cv=5, scoring="r2")
    print("Fold R2 Scores:", [round(s, 4) for s in cv_scores])
    print(f"Average CV R2 Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    # ==========================================================
    # STEP 8: Feature Importance Analysis & Charts
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 8: Feature Importance Analysis")
    print("=" * 60)

    importance_df = pd.DataFrame({
        "Feature": X.columns,
        "Importance": rf_model.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    print("\nTop 10 Most Important Features:")
    print(importance_df.head(10).to_string(index=False))

    # Save feature importance chart without blocking execution
    top10 = importance_df.head(10)
    plt.figure(figsize=(10, 6))
    plt.bar(top10["Feature"], top10["Importance"], color="#3b82f6")
    plt.title("Top 10 Important Features in Random Forest Model")
    plt.xlabel("Features")
    plt.ylabel("Importance")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    chart_path = BASE_DIR / "feature_importance.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"Feature importance chart saved to: {chart_path}")

    # Save model comparison bar chart
    plt.figure(figsize=(8, 5))
    colors = ["#94a3b8", "#fbbf24", "#22c55e"]
    plt.bar(comparison_df["Model"], comparison_df["R2 Score"], color=colors)
    plt.title("Model Performance Comparison (R² Score)")
    plt.xlabel("Model")
    plt.ylabel("R² Score")
    plt.ylim(0, 1.0)
    for i, v in enumerate(comparison_df["R2 Score"]):
        plt.text(i, v + 0.02, f"{v:.4f}", ha="center", fontweight="bold")
    plt.tight_layout()
    comp_path = BASE_DIR / "model_comparison.png"
    plt.savefig(comp_path, dpi=300)
    plt.close()
    print(f"Model comparison chart saved to: {comp_path}")

    # ==========================================================
    # STEP 9: Save Best Model
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 9: Save Best Model (Tuned Random Forest)")
    print("=" * 60)

    save_model(rf_model)
    print("Tuned Random Forest model saved to: models/house_price_model.pkl")

    # ==========================================================
    # STEP 10: Model Loading and Prediction Verification
    # ==========================================================
    print("\n" + "=" * 60)
    print("STEP 10: Verification Test")
    print("=" * 60)

    loaded_model = load_model()
    loaded_preds = predict(loaded_model, X_test)
    test_sample = pd.DataFrame({
        "Actual Price ($)": y_test.values[:5],
        "Predicted Price ($)": [round(p, 2) for p in loaded_preds[:5]]
    })
    print("\nFirst 5 Test Predictions:")
    print(test_sample.to_string(index=False))
    print("\nPipeline execution completed successfully!")


if __name__ == "__main__":
    main()