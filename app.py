from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# Dashboard configuration
st.set_page_config(
    page_title="Global Wildfire Monitoring",
    page_icon="🔥",
    layout="wide"
)

CSV_PATH = Path(__file__).parent / "data" / "wildfires_cleaned.csv"


# Load dataset
@st.cache_data
def load_data():

    if not CSV_PATH.exists():
        raise FileNotFoundError("Wildfire CSV file not found!")

    df = pd.read_csv(CSV_PATH)

    required_columns = [
        "latitude",
        "longitude",
        "acq_date",
        "frp",
        "confidence_label",
        "daynight_label",
        "intensity_level"
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

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


# Load data safely
try:
    df = load_data()

except Exception as error:
    st.error(f"Unable to load data: {error}")
    st.stop()


# Dashboard heading
st.title("🔥 Global Wildfire Monitoring")
st.write(
    "Global wildfire detection analysis using NASA FIRMS satellite data."
)

st.caption(
    "Data source: NASA FIRMS | "
    "Intensity levels are defined by this project."
)

st.divider()


# Sidebar filters
st.sidebar.title("Dashboard Filters")

available_dates = sorted(
    df["acq_date"].dropna().dt.strftime("%Y-%m-%d").unique()
)

selected_date = st.sidebar.selectbox(
    "Select Date",
    ["All Dates"] + list(available_dates)
)

available_intensities = sorted(
    df["intensity_level"].dropna().unique()
)

selected_intensities = st.sidebar.multiselect(
    "Intensity Level",
    available_intensities,
    default=available_intensities
)

available_periods = ["Day", "Night"]

selected_periods = st.sidebar.multiselect(
    "Day / Night",
    available_periods,
    default=available_periods
)

available_confidence = sorted(
    df["confidence_label"].dropna().unique()
)

selected_confidence = st.sidebar.multiselect(
    "Confidence",
    available_confidence,
    default=available_confidence
)


# Apply filters
filtered_df = df.copy()

if selected_date != "All Dates":

    filtered_df = filtered_df[
        filtered_df["acq_date"].dt.strftime("%Y-%m-%d")
        == selected_date
    ]

filtered_df = filtered_df[
    filtered_df["intensity_level"].isin(
        selected_intensities
    )
]

filtered_df = filtered_df[
    filtered_df["daynight_label"].isin(
        selected_periods
    )
]

filtered_df = filtered_df[
    filtered_df["confidence_label"].isin(
        selected_confidence
    )
]


# Main statistics
st.subheader("Wildfire Statistics")

col1, col2, col3, col4 = st.columns(4)

total_records = len(filtered_df)

average_frp = (
    filtered_df["frp"].mean()
    if total_records > 0 else 0
)

high_intensity = len(
    filtered_df[
        filtered_df["intensity_level"] == "High"
    ]
)

day_records = len(
    filtered_df[
        filtered_df["daynight_label"] == "Day"
    ]
)

col1.metric(
    "Total Detections",
    f"{total_records:,}"
)

col2.metric(
    "Average FRP",
    f"{average_frp:.2f} MW"
)

col3.metric(
    "High Intensity",
    f"{high_intensity:,}"
)

col4.metric(
    "Daytime Detections",
    f"{day_records:,}"
)


st.divider()


if filtered_df.empty:

    st.warning("No records found for selected filters.")

else:

    # Intensity chart
    st.subheader("Intensity Distribution")

    intensity_counts = (
        filtered_df["intensity_level"]
        .value_counts()
        .reindex(["Low", "Medium", "High"], fill_value=0)
    )

    col1, col2 = st.columns(2)

    with col1:

        fig, ax = plt.subplots(figsize=(7, 4))

        intensity_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel("Intensity")
        ax.set_ylabel("Detections")
        ax.set_title("Wildfire Intensity")

        st.pyplot(fig)
        plt.close(fig)

    with col2:

        # Day and night chart
        period_counts = (
            filtered_df["daynight_label"]
            .value_counts()
            .reindex(["Day", "Night"], fill_value=0)
        )

        fig, ax = plt.subplots(figsize=(7, 4))

        period_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_xlabel("Period")
        ax.set_ylabel("Detections")
        ax.set_title("Day vs Night")

        st.pyplot(fig)
        plt.close(fig)


    st.divider()


    # Daily detections
    st.subheader("Daily Wildfire Trend")

    daily_counts = (
        filtered_df.groupby(
            filtered_df["acq_date"].dt.date
        ).size()
    )

    fig, ax = plt.subplots(figsize=(10, 4))

    daily_counts.plot(
        kind="line",
        marker="o",
        ax=ax
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Detections")
    ax.set_title("Daily Detection Trend")

    fig.autofmt_xdate()

    st.pyplot(fig)
    plt.close(fig)


    st.divider()


    # FRP histogram
    st.subheader("Fire Radiative Power Distribution")

    fig, ax = plt.subplots(figsize=(10, 4))

    ax.hist(
        filtered_df["frp"].dropna(),
        bins=30
    )

    ax.set_xlabel("Fire Radiative Power (MW)")
    ax.set_ylabel("Frequency")
    ax.set_title("FRP Distribution")

    st.pyplot(fig)
    plt.close(fig)


    st.divider()


    # Global hotspot map
    st.subheader("Global Wildfire Hotspots")

    map_df = filtered_df[
        ["latitude", "longitude"]
    ].dropna()

    map_df = map_df[
        map_df["latitude"].between(-90, 90)
        & map_df["longitude"].between(-180, 180)
    ]

    if len(map_df) > 5000:

        map_df = map_df.sample(
            n=5000,
            random_state=42
        )

    if not map_df.empty:

        st.map(
            map_df,
            latitude="latitude",
            longitude="longitude"
        )

        st.caption(
            f"Showing {len(map_df):,} plotted detections. "
            "The map may sample records for performance."
        )


    st.divider()


    # Records table
    st.subheader("Wildfire Detection Records")

    display_columns = [
        "acq_date",
        "latitude",
        "longitude",
        "frp",
        "confidence_label",
        "daynight_label",
        "intensity_level"
    ]

    st.dataframe(
        filtered_df[display_columns].head(500),
        use_container_width=True
    )


    # Download filtered records
    csv_download = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv_download,
        file_name="wildfire_filtered_data.csv",
        mime="text/csv"
    )


st.divider()

st.caption(
    "Global Wildfire Monitoring Project | "
    "NASA FIRMS | Programming for AI"
)
