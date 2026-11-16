
import os
import requests
import pandas as pd

from io import StringIO
from datetime import date
from dotenv import load_dotenv


# Load API key
load_dotenv()

MAP_KEY = os.getenv("NASA_MAP_KEY")


def fetch_daily_data(target_date: date) -> pd.DataFrame:

    if not MAP_KEY:
        raise ValueError("NASA API key not found!")

    # API configuration
    source = "VIIRS_NOAA21_NRT"
    area = "world"
    day_range = 1

    # Format date
    date_text = target_date.strftime("%Y-%m-%d")

    # Create URL
    url = (
        f"https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{MAP_KEY}/{source}/{area}/{day_range}/{date_text}"
    )

    print(f"Retrieving wildfire data for: {date_text}")

    # Send API request
    response = requests.get(url, timeout=120)
    response.raise_for_status()

    csv_data = response.text.strip()

    if not csv_data:
        return pd.DataFrame()

    # Check API response
    first_line = csv_data.splitlines()[0].lower()

    if "latitude" not in first_line:
        raise ValueError(
            "Unexpected NASA API response: " + csv_data[:200]
        )

    # Convert CSV into DataFrame
    df = pd.read_csv(
        StringIO(csv_data),
        dtype={"acq_time": str}
    )

    return df
