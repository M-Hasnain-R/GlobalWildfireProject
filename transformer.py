import pandas as pd


def transform_records(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, dict]:

    # Step 1: Copy original data
    clean_df = df.copy()

    original_count = len(clean_df)

    # Step 2: Required columns
    required_columns = [
        "latitude",
        "longitude",
        "bright_ti4",
        "scan",
        "track",
        "acq_date",
        "acq_time",
        "satellite",
        "instrument",
        "confidence",
        "version",
        "bright_ti5",
        "frp",
        "daynight"
    ]

    # Step 3: Count missing rows
    missing_rows = (
        clean_df[required_columns]
        .isna()
        .any(axis=1)
        .sum()
    )

    # Step 4: Remove missing values
    clean_df = clean_df.dropna(
        subset=required_columns
    ).copy()

    # Step 5: Remove duplicates
    duplicate_count = clean_df.duplicated().sum()

    clean_df = clean_df.drop_duplicates().copy()

    # Step 6: Convert date
    clean_df["acq_date"] = pd.to_datetime(
        clean_df["acq_date"]
    )

    # Step 7: Extract year, month and day
    clean_df["year"] = clean_df["acq_date"].dt.year
    clean_df["month"] = clean_df["acq_date"].dt.month
    clean_df["day"] = clean_df["acq_date"].dt.day

    # Step 8: Standardize time
    clean_df["acq_time"] = (
        clean_df["acq_time"].astype(str).str.zfill(4)
    )

    # Step 9: Confidence labels
    clean_df["confidence_label"] = (
        clean_df["confidence"].map({
            "l": "Low",
            "n": "Nominal",
            "h": "High"
        })
    )

    # Step 10: Day and night labels
    clean_df["daynight_label"] = (
        clean_df["daynight"].map({
            "D": "Day",
            "N": "Night"
        })
    )

    # Step 11: FRP intensity classification
    clean_df["intensity_level"] = "High"

    clean_df.loc[
        clean_df["frp"] < 50,
        "intensity_level"
    ] = "Medium"

    clean_df.loc[
        clean_df["frp"] < 10,
        "intensity_level"
    ] = "Low"

    # Step 12: Transformation report
    report = {
        "original_records": original_count,
        "missing_rows_removed": int(missing_rows),
        "duplicates_removed": int(duplicate_count),
        "final_records": len(clean_df)
    }

    return clean_df, report
