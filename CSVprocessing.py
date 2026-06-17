# Telemetry processing and frame generation
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation
from frames import LVLH_X, LVLH_Y, LVLH_Z, build_lvlh
from datetime import datetime
from sgp4.api import jday
from tleprocessing import propagate_to_timestamp
# reads csv 
def readcsv(file):
  data=pd.read_csv(file)    # loads csv into dataframe
  return data
# function take dataframe to extract timestamps and quanternions
def extract_quaternions(data):
    timestamps=[]
    quaternions = []

    for i, row in data.iterrows():
        
        timestamp = row["Timestamp"]
        timestamps.append(timestamp)
        quat = [
            row["Q1"],
            row["Q2"],
            row["Q3"],
            row["Q0"]
        ]

        quaternions.append(quat)
   
    return timestamps,quaternions
# function builds the lvlh frame, does rotation of frame and saves it
def generate_frames(timestamps, quats, convention, sat=None):
    frames = []
    for timestamp, quat in zip(timestamps, quats):
        if sat is not None:
            error, r, v = propagate_to_timestamp(sat, timestamp)
            if error != 0:
                print(f"Warning: SGP4 propagation error {error} at {timestamp}")

        rotation = Rotation.from_quat(quat)
        Xp = rotation.apply(LVLH_X)
        Yp = rotation.apply(LVLH_Y)
        Zp = rotation.apply(LVLH_Z)
        frames.append({"timestamp": timestamp, "Xp": Xp, "Yp": Yp, "Zp": Zp})
    return frames


