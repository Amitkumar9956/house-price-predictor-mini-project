from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def clean_data(input_csv=None, output_csv=None):
    """
    Cleans the raw dataset by imputing missing values:
    - Numerical columns: imputed with median
    - Categorical columns: imputed with mode
    Saves cleaned dataset to data/cleaned_train.csv
    """
    if input_csv is None:
        input_csv = DATA_DIR / "train.csv"
    else:
        input_csv = Path(input_csv)

    if output_csv is None:
        output_csv = DATA_DIR / "cleaned_train.csv"
    else:
        output_csv = Path(output_csv)

    print(f"Loading raw dataset from: {input_csv}")
    df = pd.read_csv(input_csv)

    missing_before = df.isnull().sum()
    missing_cols = missing_before[missing_before > 0]
    print(f"Found {len(missing_cols)} columns with missing values.")

    numerical_columns = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_columns = df.select_dtypes(include=["object"]).columns

    for column in numerical_columns:
        if column != "SalePrice":
            df[column] = df[column].fillna(df[column].median())

    for column in categorical_columns:
        mode_series = df[column].mode()
        fill_val = mode_series[0] if not mode_series.empty else "None"
        df[column] = df[column].fillna(fill_val)

    remaining_missing = df.isnull().sum().sum()
    print(f"Remaining Missing Values: {remaining_missing}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"Cleaned dataset saved successfully to: {output_csv}")

    return df


if __name__ == "__main__":
    clean_data()