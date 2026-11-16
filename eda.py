from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Project folders
BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "data" / "wildfires_cleaned.csv"

CHART_FOLDER = BASE_DIR / "eda_charts"


def load_data():

    # Check CSV file
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {CSV_PATH}"
        )

    # Read dataset
    df = pd.read_csv(CSV_PATH)

    # Required columns
    required_columns = [
        "latitude",
        "longitude",
        "acq_date",
        "frp",
        "intensity_level",
        "daynight_label"
    ]

    # Check columns
    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    # Convert data types
    df["acq_date"] = pd.to_datetime(
        df["acq_date"],
        errors="coerce"
    )

    df["frp"] = pd.to_numeric(
        df["frp"],
        errors="coerce"
    )

    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    return df


def generate_charts(df):

    # Create charts folder
    CHART_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    # ==================================
    # 1. DAILY WILDFIRE TREND
    # ==================================

    date_data = df.dropna(
        subset=["acq_date"]
    )

    daily_counts = date_data.groupby(
        date_data["acq_date"].dt.strftime("%Y-%m-%d")
    ).size()

    fig, ax = plt.subplots(figsize=(9, 5))

    daily_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Daily Wildfire Detections")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Detections")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(CHART_FOLDER / "daily_trend.png")
    plt.close(fig)


    # ==================================
    # 2. INTENSITY DISTRIBUTION
    # ==================================

    intensity_counts = (
        df["intensity_level"]
        .value_counts()
        .reindex(
            ["Low", "Medium", "High"],
            fill_value=0
        )
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    intensity_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Wildfire Intensity Distribution")
    ax.set_xlabel("Intensity Level")
    ax.set_ylabel("Number of Detections")

    plt.tight_layout()

    plt.savefig(CHART_FOLDER / "intensity.png")
    plt.close(fig)


    # ==================================
    # 3. DAY AND NIGHT DISTRIBUTION
    # ==================================

    daynight_counts = (
        df["daynight_label"]
        .value_counts()
        .reindex(
            ["Day", "Night"],
            fill_value=0
        )
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    daynight_counts.plot(
        kind="bar",
        ax=ax
    )

    ax.set_title("Day vs Night Wildfire Detections")
    ax.set_xlabel("Time Period")
    ax.set_ylabel("Number of Detections")

    plt.tight_layout()

    plt.savefig(CHART_FOLDER / "day_night.png")
    plt.close(fig)


    # ==================================
    # 4. FRP DISTRIBUTION
    # ==================================

    frp_data = df["frp"].dropna()

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.hist(
        frp_data,
        bins=30
    )

    ax.set_title("Fire Radiative Power Distribution")
    ax.set_xlabel("FRP (MW)")
    ax.set_ylabel("Frequency")

    plt.tight_layout()

    plt.savefig(CHART_FOLDER / "frp_distribution.png")
    plt.close(fig)


    # ==================================
    # 5. GLOBAL HOTSPOT DISTRIBUTION
    # ==================================

    map_data = df[
        ["latitude", "longitude"]
    ].dropna()

    # Keep valid coordinates
    map_data = map_data[
        map_data["latitude"].between(-90, 90)
        & map_data["longitude"].between(-180, 180)
    ]

    # Sample records for better performance
    if len(map_data) > 10000:

        map_data = map_data.sample(
            n=10000,
            random_state=42
        )

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.scatter(
        map_data["longitude"],
        map_data["latitude"],
        s=3,
        alpha=0.4
    )

    ax.set_title("Global Wildfire Hotspot Distribution")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)

    plt.tight_layout()

    plt.savefig(CHART_FOLDER / "global_hotspots.png")
    plt.close(fig)


    print("\nAll EDA charts generated successfully!")

    print("Total charts: 5")

    print("Charts folder:", CHART_FOLDER)


def main():

    print("\nStarting Wildfire EDA...")

    # Load cleaned dataset
    df = load_data()

    print("Total Records:", len(df))

    print("Available Dates:")

    print(
        df["acq_date"]
        .dropna()
        .dt.date
        .nunique()
    )

    # Generate charts
    generate_charts(df)


if __name__ == "__main__":
    main()
