# Prediction of attitudes

from scipy.spatial.transform import Rotation as R
import numpy as np
from datetime import datetime, timedelta
import json
import os

# function to estimate how fast the spacecraft is rotating
def angular_velocity(timestamps, quaternions):
    omega_list = []
    for i in range(1, len(quaternions)):
        rot1 = R.from_quat(quaternions[i-1])
        rot2 = R.from_quat(quaternions[i])
        rot_change = rot2 * rot1.inv()

        t1 = datetime.strptime(timestamps[i-1], "%Y-%m-%dT%H:%M:%SZ")
        t2 = datetime.strptime(timestamps[i], "%Y-%m-%dT%H:%M:%SZ")
        dt = (t2 - t1).total_seconds()

        omega_list.append(rot_change.as_rotvec() / dt)

    mean_omega = np.mean(omega_list, axis=0)
    magnitude = np.linalg.norm(mean_omega)  #computes |omega|- the overall spin rate
    return mean_omega, magnitude

# function to find average telemetry spacing
def get_average_dt(timestamps):
    dts = []
    for i in range(1, len(timestamps)):
        t1 = datetime.strptime(timestamps[i-1], "%Y-%m-%dT%H:%M:%SZ")
        t2 = datetime.strptime(timestamps[i], "%Y-%m-%dT%H:%M:%SZ")
        dts.append((t2 - t1).total_seconds())
    return np.mean(dts)

# predicts future attitude
def predict_quaternions(timestamps, quats, omega, days):
    current_rotation = R.from_quat(quats[-1])
    current_time = datetime.strptime(timestamps[-1], "%Y-%m-%dT%H:%M:%SZ")

    dt = get_average_dt(timestamps)
    steps = int((days * 24 * 3600) / dt)

    future_times = []
    future_quats = []

    for _ in range(steps):
        delta_rotation = R.from_rotvec(omega * dt)
        current_rotation = delta_rotation * current_rotation
        current_time += timedelta(seconds=dt)

        future_times.append(current_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        future_quats.append(current_rotation.as_quat())

    return future_times, future_quats

# save prediction to the prediction file
def save_prediction(generated_from_date, timestamps, quaternions, days, omega_magnitude):
    
    os.makedirs("data/predictions", exist_ok=True)
    filename = f"data/predictions/from_{generated_from_date}_horizon_{days}d.json"

    output = {
        "generated_from": generated_from_date,
        "horizon_days": days,
        "timestamps": timestamps,
        "quaternions": [q.tolist() for q in quaternions],
        "omega_magnitude_deg_s": np.degrees(omega_magnitude)
    }

    with open(filename, "w") as f:
        json.dump(output, f, indent=4)

    print(f"Saved {filename}")


def load_prediction(generated_from_date, days):
    filename = f"data/predictions/from_{generated_from_date}_horizon_{days}d.json"
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No saved prediction from {generated_from_date} for {days}d horizon")

    with open(filename, "r") as f:
        return json.load(f)

# to list the historical predictions
def list_predictions_for_date(generated_from_date):
    
    if not os.path.exists("data/predictions"):
        return []
    prefix = f"from_{generated_from_date}_horizon_"
    return [f for f in os.listdir("data/predictions") if f.startswith(prefix)]

# predicts all days continuously
def predict_quaternions_continuous(timestamps, quats, omega, total_days):
    
    current_rotation = R.from_quat(quats[-1])
    current_time = datetime.strptime(timestamps[-1], "%Y-%m-%dT%H:%M:%SZ")

    dt = get_average_dt(timestamps)
    steps_per_day = int((24 * 3600) / dt)
    total_steps = steps_per_day * total_days

    all_times = []
    all_quats = []

    for _ in range(total_steps):
        delta_rotation = R.from_rotvec(omega * dt)
        current_rotation = delta_rotation * current_rotation
        current_time += timedelta(seconds=dt)

        all_times.append(current_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        all_quats.append(current_rotation.as_quat())

    # Slice into day chunks, each starting where the previous ended
    day_chunks = {}
    for d in range(1, total_days + 1):
        end_idx = steps_per_day * d
        start_idx = 0 if d == 1 else steps_per_day * (d - 1) - 1  # overlap by 1 frame
        day_chunks[d] = (all_times[start_idx:end_idx], all_quats[start_idx:end_idx])

    return all_times, all_quats, day_chunks