
import subprocess
import sys
import time
import webbrowser

from pathlib import Path


# Project folder
PROJECT_DIR = Path(__file__).resolve().parent


def run_script(filename):

    print(f"\nRunning {filename}...")

    result = subprocess.run(
        [sys.executable, str(PROJECT_DIR / filename)],
        cwd=PROJECT_DIR
    )

    if result.returncode != 0:

        raise SystemExit(
            f"\nERROR: {filename} failed!"
        )


def main():

    print("\n================================")
    print(" GLOBAL WILDFIRE PROJECT")
    print("================================")

    # Step 1: Run ETL pipeline
    run_script("main.py")

    # Step 2: Generate EDA charts
    run_script("eda.py")

    # Step 3: Start Streamlit dashboard
    print("\nStarting dashboard...")

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(PROJECT_DIR / "app.py"),
            "--server.port",
            "8503"
        ],
        cwd=PROJECT_DIR
    )

    time.sleep(3)

    webbrowser.open("http://localhost:8503")

    print("\nProject started successfully!")
    print("Dashboard: http://localhost:8503")


if __name__ == "__main__":
    main()
