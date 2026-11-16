
from datetime import datetime, timedelta, timezone

from api import fetch_daily_data
from validator import validate_records
from transformer import transform_records
from db_loader import load_data


def main():

    # Get previous completed UTC date
    target_date = (
        datetime.now(timezone.utc).date()
        - timedelta(days=1)
    )

    print("\n=================================")
    print(" GLOBAL WILDFIRE MONITORING")
    print("=================================")

    print("\nTarget Date:", target_date)

    # 1. Extract data
    raw_df = fetch_daily_data(target_date)

    print("\nRetrieved Records:", len(raw_df))

    if raw_df.empty:
        print("\nNo data available.")
        return

    # 2. Validate data
    valid_df, rejected_df = validate_records(raw_df)

    print("\n========== VALIDATION REPORT ==========")

    print("Total Records:", len(raw_df))
    print("Valid Records:", len(valid_df))
    print("Rejected Records:", len(rejected_df))

    if not rejected_df.empty:

        print("\nRejected Records:")

        print(
            rejected_df[
                ["row_number", "errors"]
            ].to_string(index=False)
        )

    if valid_df.empty:
        print("\nNo valid records available.")
        return

    # 3. Transform data
    cleaned_df, report = transform_records(valid_df)

    print("\n========== TRANSFORMATION REPORT ==========")

    print("Original Records:", report["original_records"])
    print("Missing Rows Removed:", report["missing_rows_removed"])
    print("Duplicates Removed:", report["duplicates_removed"])
    print("Final Clean Records:", report["final_records"])

    if cleaned_df.empty:
        print("\nNo clean records available.")
        return

    # 4. Display cleaned data
    print("\n========== DATA PREVIEW ==========")

    preview_columns = [
        "latitude",
        "longitude",
        "acq_date",
        "frp",
        "confidence_label",
        "daynight_label",
        "intensity_level"
    ]

    print(
        cleaned_df[preview_columns]
        .head(5)
        .to_string(index=False)
    )

    # 5. Intensity analysis
    print("\n========== INTENSITY DISTRIBUTION ==========")

    print(
        cleaned_df["intensity_level"]
        .value_counts()
        .to_string()
    )

    # 6. Day and night analysis
    print("\n========== DAY / NIGHT DISTRIBUTION ==========")

    print(
        cleaned_df["daynight_label"]
        .value_counts()
        .to_string()
    )

    # 7. Load data
    load_report = load_data(cleaned_df)

    print("\n========== DATA LOADING REPORT ==========")

    print("New Records Inserted:", load_report["inserted_records"])
    print("Total Database Records:", load_report["total_records"])
    print("Database:", load_report["database_path"])
    print("CSV:", load_report["csv_path"])

    print("\n=================================")
    print(" PIPELINE COMPLETED SUCCESSFULLY")
    print("=================================")


if __name__ == "__main__":
    main()
