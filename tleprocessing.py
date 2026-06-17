# tle processing module
from sgp4.api import Satrec, jday
from datetime import datetime
# function that reads tle file
def read_tle(file):
    with open(file, "r") as f:
        lines = f.readlines()
    return lines

# function takes the raw lines and extracts tle pairs
def parse_tle(lines):
    satellites = []
    for i in range(len(lines)):
        if lines[i].startswith("1 "):
            satellite = {
                "line1": lines[i].strip(),
                "line2": lines[i + 1].strip()
            }
            satellites.append(satellite)
    return satellites

# function converts tle texts into SGP4 satellite objects
def load_satellites_from_file(tle_path):
   
    lines = read_tle(tle_path)
    tle_data = parse_tle(lines)
    satrec_objects = []
    for satellite in tle_data:
        sat = Satrec.twoline2rv(satellite["line1"], satellite["line2"])
        satrec_objects.append(sat)
    return satrec_objects

# orbit propagation
def propagate_to_timestamp(sat, timestamp):
    dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
    error, r, v = sat.sgp4(jd, fr)
    return error, r, v