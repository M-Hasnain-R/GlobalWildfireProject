
import sqlite3
from pathlib import Path

import pandas as pd


# Storage locations
DATABASE_FOLDER = Path("database")
DATA_FOLDER = Path("data")

DATABASE_PATH = DATABASE_FOLDER / "wildfires.db"
CSV_PATH = DATA_FOLDER / "wildfires_cleaned.csv"


# Columns used to identify repeated NASA records
UNIQUE_COLUMNS = [
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


def load_data(df: pd.DataFrame) -> dict:

    if df.empty:
        raise ValueError("Cannot load an empty DataFrame.")

    # Check required columns
    missing_columns = [
        column for column in UNIQUE_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Required columns are missing: {missing_columns}"
        )

    # Create folders
    DATABASE_FOLDER.mkdir(parents=True, exist_ok=True)
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    # Connect to database
    connection = sqlite3.connect(DATABASE_PATH)

    try:

        # Check whether table exists
        table_exists = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='wildfire_detections'
            """
        ).fetchone()

        # Create table on first run
        if table_exists is None:

            df.head(0).to_sql(
                "wildfire_detections",
                connection,
                index=False
            )

        # Create unique index
        unique_columns_sql = ", ".join(
            f'"{column}"' for column in UNIQUE_COLUMNS
        )

        connection.execute(
            f"""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_wildfire_record
            ON wildfire_detections ({unique_columns_sql})
            """
        )

        # Create temporary staging table
        df.to_sql(
            "incoming_detections",
            connection,
            if_exists="replace",
            index=False
        )

        # Prepare column names
        columns_sql = ", ".join(
            f'"{column}"' for column in df.columns
        )

        # Count inserted records
        before_changes = connection.total_changes

        connection.execute(
            f"""
            INSERT OR IGNORE INTO wildfire_detections ({columns_sql})
            SELECT {columns_sql}
            FROM incoming_detections
            """
        )

        inserted_records = (
            connection.total_changes - before_changes
        )

        # Remove temporary table
        connection.execute(
            "DROP TABLE incoming_detections"
        )

        # Count total database records
        total_records = connection.execute(
            "SELECT COUNT(*) FROM wildfire_detections"
        ).fetchone()[0]

        connection.commit()

        # Export complete database to CSV
        with open(
            CSV_PATH,
            "w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            header_written = False

            for chunk in pd.read_sql_query(
                "SELECT * FROM wildfire_detections",
                connection,
                chunksize=50000
            ):

                chunk.to_csv(
                    csv_file,
                    index=False,
                    header=not header_written
                )

                header_written = True

        return {
            "inserted_records": inserted_records,
            "total_records": total_records,
            "database_path": str(DATABASE_PATH),
            "csv_path": str(CSV_PATH)
        }

    finally:
        connection.close()
