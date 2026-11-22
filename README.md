# 🌍 Global Wildfire Monitoring & Analysis

An automated ETL and Exploratory Data Analysis (EDA) project that collects global wildfire detection data using the NASA FIRMS API, validates and transforms the data, stores it in SQLite, and presents insights through an interactive Streamlit dashboard.

## 📌 Project Overview

Wildfires and thermal anomalies can cause significant environmental damage. This project aims to make satellite-based wildfire detection data easier to collect, process, analyze, and visualize.

The system retrieves daily global wildfire detection records from NASA FIRMS and processes them through an automated ETL pipeline.

## 🎯 Project Objectives

- Retrieve global wildfire detection data from NASA FIRMS.
- Validate incoming records using Pydantic.
- Clean and transform data using Pandas.
- Categorize detections according to Fire Radiative Power (FRP).
- Store processed records in SQLite and CSV.
- Perform Exploratory Data Analysis.
- Visualize global wildfire hotspots through an interactive dashboard.
- Automate daily data collection using Windows Task Scheduler.

## 🛰️ Data Source

**NASA FIRMS — Fire Information for Resource Management System**

Dataset: VIIRS NOAA-21 Near Real-Time (NRT)

Official website: https://firms.modaps.eosdis.nasa.gov/

The dataset includes:
- Latitude and longitude
- Acquisition date and time
- Brightness temperature
- Fire Radiative Power (FRP)
- Detection confidence
- Satellite and instrument information
- Day/night indicator

## ⚙️ ETL Pipeline

### 1. Extract
- Connect to NASA FIRMS using its API.
- Retrieve data for the previous completed UTC day.
- Convert the API CSV response into a Pandas DataFrame.

### 2. Transform
- Validate records using Pydantic.
- Reject invalid records.
- Remove missing values and exact duplicates.
- Standardize date and time.
- Extract year, month, and day.
- Convert confidence and day/night values into readable labels.
- Categorize FRP into project-defined intensity levels.

### 3. Load
- Store records in a local SQLite database.
- Prevent duplicate records.
- Export the accumulated dataset into a cleaned CSV file.

## 📊 Exploratory Data Analysis

The project generates five visualizations:

1. Daily Wildfire Detection Trend
2. Wildfire Intensity Distribution
3. Day vs Night Distribution
4. Fire Radiative Power Distribution
5. Global Wildfire Hotspot Distribution

## 🖥️ Interactive Dashboard

The Streamlit dashboard provides:

- Total wildfire detection statistics
- Average Fire Radiative Power
- Intensity distribution
- Day/night comparison
- Daily detection trends
- Global hotspot map
- Date, intensity, confidence, and time-period filters
- Wildfire records table
- Filtered data download

## 🛠️ Technologies Used

- Python
- Requests
- Pandas
- NumPy
- Pydantic
- SQLite
- Matplotlib
- Streamlit
- NASA FIRMS API

## 📁 Project Structure

```text
GlobalWildfireProject/
│
├── main.py
├── api.py
├── models.py
├── validator.py
├── transformer.py
├── db_loader.py
├── eda.py
├── app.py
├── run_project.py
│
├── data/
│   └── wildfires_cleaned.csv
│
├── database/
│   └── wildfires.db
│
├── eda_charts/
│
├── .env.example
├── .gitignore
└── requirements.txt
```

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/M-Hasnain-R/GlobalWildfireProject.git
```

### 2. Open the project folder

```bash
cd GlobalWildfireProject
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure NASA API key

Create a `.env` file in the project root and add your own NASA MAP_KEY:

```env
NASA_MAP_KEY=YOUR_ACTUAL_API_KEY
```

Obtain a free API key from:

https://firms.modaps.eosdis.nasa.gov/api/map_key/

Never upload your actual `.env` file or API key to GitHub.

## ▶️ Running the Project

Run the complete ETL pipeline:

```bash
python main.py
```

Generate EDA charts:

```bash
python eda.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

You can also use `run_project.py` to start the complete application from Python.

## ⏰ Daily Automation

Windows Task Scheduler is used to execute the ETL pipeline daily at the configured time.

The system retrieves the previous completed UTC day's data and stores new records in the existing database.

If the laptop is turned off at the scheduled time, the missed date is not automatically recovered.

## 📈 Intensity Classification

The project uses its own FRP-based categories:

| FRP | Category |
|---|---|
| Below 10 MW | Low |
| 10 to below 50 MW | Medium |
| 50 MW or above | High |

These are project-defined analytical categories, not official NASA fire-severity classifications.

## ⚠️ Limitations

- NASA satellite records represent thermal detections, not necessarily unique independent wildfires.
- NRT data can be updated as satellite observations are processed.
- The system does not automatically recover missed collection dates.
- Intensity categories are defined for this project.

## 🔮 Future Scope

- Extended historical data collection.
- Additional satellite datasets.
- Advanced geographical analysis.
- More analytical and visualization features.

## 👥 Team Members

**Group Project — Programming for AI, 3rd Semester**

- Member 1: [Muhammad Hasnain Raza (2025-AI-417)]
- Member 2: [Urooj Iftikhar (2025-AI-386)]
- Member 3: [Amrat Zaib (2025-AI-378)]
- Member 4: [Muhammad Arslan Razzaq (2025-AI-389)]

## 📚 Acknowledgements

NASA FIRMS for providing publicly accessible satellite-based fire detection data.

---

**Project:** Global Wildfire Monitoring & Analysis  
**Course:** Programming for AI  
**Institution:** University of Engineering and Technology, Lahore
