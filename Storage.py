
import os
from datetime import datetime
import shutil

def initialize_storage():
    os.makedirs("data/telemetry", exist_ok=True)
    os.makedirs("data/tle", exist_ok=True)
    os.makedirs("data/predictions", exist_ok=True)
    os.makedirs("incoming", exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    csv_name = f"data/telemetry/{today}.csv"
    tle_name = f"data/tle/{today}.tle"

    return csv_name, tle_name


def process_incoming_files(csv_file, tle_file):
    files = os.listdir("incoming")
    for file in files:
        source = f"incoming/{file}"
        if file.endswith(".csv"):
            shutil.copy(source, csv_file)
            print("Telemetry saved")
        elif file.endswith(".tle") or file.endswith(".txt"):
            shutil.copy(source, tle_file)
            print("TLE saved")


def list_available_dates():
    #Return sorted list of dates (YYYY-MM-DD) that have BOTH telemetry and TLE files.
    csv_dates = {f.replace(".csv", "") for f in os.listdir("data/telemetry") if f.endswith(".csv")}
    tle_dates = {f.replace(".tle", "") for f in os.listdir("data/tle") if f.endswith(".tle")}

    common_dates = sorted(csv_dates & tle_dates)
    if not common_dates:
        raise FileNotFoundError("No dates with both telemetry and TLE found")

    return common_dates


def load_csv_for_date(date_str):
    path = f"data/telemetry/{date_str}.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"No telemetry for {date_str}")
    return path


def load_tle_for_date(date_str):
    path = f"data/tle/{date_str}.tle"
    if not os.path.exists(path):
        raise FileNotFoundError(f"No TLE for {date_str}")
    return path


def load_latest_csv():
    files = sorted(os.listdir("data/telemetry"))
    if not files:
        raise FileNotFoundError("No telemetry files found")
    return f"data/telemetry/{files[-1]}"


def load_latest_tle():
    files = sorted(os.listdir("data/tle"))
    if not files:
        raise FileNotFoundError("No tle files found")
    return f"data/tle/{files[-1]}"

