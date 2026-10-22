from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def generate_visualizations(save_to_disk=True):
    """
    Generates exploratory data analysis plots for house prices and living area.
    Saves plots to project root and prevents blocking execution.
    """
    data_path = DATA_DIR / "train.csv"
    if not data_path.exists():
        print(f"Dataset not found at: {data_path}")
        return

    df = pd.read_csv(data_path)

    # 1. Distribution of House Prices
    plt.figure(figsize=(10, 6))
    plt.hist(df["SalePrice"], bins=30, color="#3b82f6", edgecolor="white")
    plt.title("Distribution of House Prices")
    plt.xlabel("Sale Price ($)")
    plt.ylabel("Number of Houses")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    if save_to_disk:
        plt.savefig(BASE_DIR / "price_distribution.png", dpi=300)
        print("Saved price_distribution.png")
    plt.close()

    # 2. Living Area vs Sale Price
    plt.figure(figsize=(10, 6))
    plt.scatter(df["GrLivArea"], df["SalePrice"], alpha=0.5, color="#2563eb", edgecolors="none")
    plt.xlabel("Ground Living Area (sq ft)")
    plt.ylabel("Sale Price ($)")
    plt.title("Living Area vs Sale Price")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    if save_to_disk:
        plt.savefig(BASE_DIR / "livarea_vs_price.png", dpi=300)
        print("Saved livarea_vs_price.png")
    plt.close()


if __name__ == "__main__":
    generate_visualizations()