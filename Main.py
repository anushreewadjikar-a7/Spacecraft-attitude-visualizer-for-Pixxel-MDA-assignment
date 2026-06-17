# importing all the required functions
from Storage import (
    initialize_storage,
    process_incoming_files,
    list_available_dates,
    load_csv_for_date,
    load_tle_for_date,
    load_latest_csv,
    load_latest_tle)
from CSVprocessing import readcsv, extract_quaternions, generate_frames
from tleprocessing import load_satellites_from_file
from plot import visualize_with_cube
from prediction import (
    angular_velocity, 
    predict_quaternions_continuous,
     save_prediction, 
     load_prediction, list_predictions_for_date)

#initizizing and processing csv and tle files
csv_file, tle_file = initialize_storage()
process_incoming_files(csv_file, tle_file)

# Printing choices for functions
print("1. Telemetry (this date)")
print("2. Prediction (generated from this date)")
print("3. Historical Data")
print("4:Historical Prediction Mode ")
choice = input("Choice: ")
#-------user input ----------
if choice == "1":
    data = readcsv(load_latest_csv())
    timestamps, quats = extract_quaternions(data)

    satellites = load_satellites_from_file(load_latest_tle())
    sat = satellites[0]

    frames = generate_frames(timestamps,quats,"lvlh_from_body",sat)
    visualize_with_cube({"Telemetry": frames})

elif choice == "2":
    data = readcsv(load_latest_csv())
    timestamps, quats = extract_quaternions(data)

    satellites = load_satellites_from_file(load_latest_tle())
    sat = satellites[0]

    days = int(input("Prediction horizon (days): "))

    omega, omega_mag = angular_velocity(timestamps,quats)
    all_times, all_quats, day_chunks = (predict_quaternions_continuous
    (timestamps,quats,omega,days))
    generated_from_date = timestamps[0][:10]
    save_prediction(generated_from_date,all_times,all_quats,days,omega_mag)
    day_datasets = {}

    for d, (chunk_times, chunk_quats) in day_chunks.items():

   
        chunk_times = chunk_times[::100]
        chunk_quats = chunk_quats[::100]

        day_datasets[f"Day {d}"] = generate_frames(
        chunk_times,chunk_quats,"lvlh_from_body",sat)

    visualize_with_cube(day_datasets,omega_magnitude=omega_mag)
elif(choice=="3"):
    dates = list_available_dates()
    print("Available dates:")
    for i, d in enumerate(dates):
        print(f"  {i}: {d}")

    idx = int(input("Select a date (index): "))
    selected_date = dates[idx]

    data = readcsv(load_csv_for_date(selected_date))
    timestamps, quats = extract_quaternions(data)

    satellites = load_satellites_from_file(
    load_tle_for_date(selected_date))
    sat = satellites[0]
    frames = generate_frames(
        timestamps,quats,"lvlh_from_body",sat)

    visualize_with_cube({f"Historical {selected_date}": frames})
elif choice == "4":

    dates = list_available_dates()

    print("Available dates:")
    for i, d in enumerate(dates):
        print(f"{i}: {d}")

    idx = int(input("Select date: "))
    selected_date = dates[idx]
    prediction_files = list_predictions_for_date(selected_date)

    if len(prediction_files) == 0:
        print("No predictions found.")
        exit()

    print("\nAvailable predictions:")

    for i, p in enumerate(prediction_files):
        print(f"{i}: {p}")

    pidx = int(input("Select prediction: "))

    filename = prediction_files[pidx]
    days = int(
        filename.split("_horizon_")[1]
        .replace("d.json", "")
    )
    prediction = load_prediction(
    selected_date,
    days
)
    timestamps = prediction["timestamps"]
    quats = prediction["quaternions"]
    timestamps = prediction["timestamps"]
    quats = prediction["quaternions"]
    satellites = load_satellites_from_file(
    load_tle_for_date(selected_date)
)

    sat = satellites[0]
    frames = generate_frames(
    timestamps,
    quats,
    "lvlh_from_body",
    sat
)
    visualize_with_cube(
    {f"Prediction from {selected_date}": frames}
)
else:
    print("Error! Please choose between 1,2,3 and 4")

#----end------------