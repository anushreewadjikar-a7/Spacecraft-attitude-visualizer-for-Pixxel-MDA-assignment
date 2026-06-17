# Spacecraft Attitude Visualization and Prediction Tool

## Overview

This project was developed as part of the Pixxel Mission Design & Analysis Internship Assignment.

The objective was to create a software package capable of visualizing spacecraft attitude using telemetry quaternion data and TLE-based orbital information. In addition to displaying historical attitude data, the system can generate and visualize future attitude predictions while preserving previous prediction results for later inspection.

The software uses spacecraft telemetry quaternions to determine the orientation of the spacecraft body frame relative to the Local Vertical Local Horizontal (LVLH) reference frame. The resulting attitude is displayed through an interactive 3D visualization with animation and time-slider controls.

A secondary goal was to design the software as a modular system rather than a single script. Telemetry processing, orbital propagation, visualization, storage, and prediction are therefore separated into independent components.

---

## Features

* Visualize spacecraft attitude from telemetry quaternions
* Construct LVLH reference frames from TLE-derived position and velocity vectors
* Interactive 3D visualization using Plotly
* Time-slider navigation through telemetry history
* Future attitude prediction using quaternion propagation
* Local archival of telemetry, TLE, and prediction data
* Historical telemetry visualization
* Historical prediction visualization

---
## Installation

Requires Python 3.9+.

```bash
git clone <your-repo-url>
cd <repo-folder>
pip install -r requirements.txt
```
## Usage

1. Drop one telemetry CSV and one TLE file into the `incoming/` folder.
   The TLE file may be `.tle` or `.txt`. The CSV must have columns
   `Q0, Q1, Q2, Q3, Timestamp`.
2. Run the program:

```bash
python Main.py
```

3. Choose a mode from the menu:
   - `1` — visualize today's telemetry
   - `2` — generate and visualize an attitude prediction (you'll be asked
     for a horizon in days)
   - `3` — visualize a previous day's telemetry
   - `4` — revisit a previously generated prediction

Each run with choice `1` or `3` archives the incoming files under
`data/telemetry/` and `data/tle/` by date, so historical data accumulates
automatically. Predictions are stored under `data/predictions/`.

## How the System Works

The software combines two independent data sources:

### Telemetry Data

Telemetry CSV files provide:

* Timestamp
* Quaternion components (Q0, Q1, Q2, Q3)

These quaternions describe the spacecraft attitude at each telemetry epoch.

### Orbital Data

TLE files are propagated using the SGP4 orbital model to obtain the spacecraft position and velocity vectors at each telemetry timestamp. This propagation is currently used to validate the TLE epoch against the telemetry timestamps and is retained as a hook for future extensions (e.g. ground-track or eclipse overlays). It is not used in the attitude rotation itself -- see below.

### Attitude Visualization

The telemetry quaternion is taken to already express the spacecraft body attitude relative to the LVLH frame (a common convention for ADCS telemetry built around local pointing). The LVLH frame is therefore represented in the visualization by the fixed unit axes X, Y, Z, and the quaternion is applied directly to them to obtain the moving body axes:

For each telemetry timestamp:

1. The telemetry quaternion is converted into a rotation.
2. The fixed LVLH unit axes (X, Y, Z) are rotated by that quaternion to produce the body axes (X', Y', Z').
3. The rotated body frame is displayed alongside the fixed LVLH frame.

A zero-rotation (identity) quaternion therefore correctly shows the body frame perfectly aligned with the LVLH reference axes in the plot.
---

## Prediction Method

Future attitude prediction is implemented using a constant angular velocity assumption.

The prediction workflow is:

1. Compute the attitude change between consecutive telemetry samples.
2. Estimate the average angular velocity vector.
3. Propagate the final known attitude forward in time.
4. Generate future quaternion states.
5. Store prediction results for future inspection.

The prediction model is intentionally lightweight and was selected to demonstrate the software architecture and prediction workflow rather than provide flight-quality attitude forecasting.

---

## Design Decisions

Several design decisions were made during development:

* A modular architecture was used to separate telemetry processing, orbital propagation, visualization, storage, and prediction logic.
* Plotly was selected because it provides interactive 3D graphics and slider support without requiring a dedicated GUI framework.
* SGP4 was used for orbit propagation because TLEs are provided as an input requirement.
* LVLH frames are generated directly from propagated position and velocity vectors.
* Prediction results are stored locally so that historical forecasts can be revisited later.

The emphasis was placed on clarity, maintainability, and ease of extension rather than implementing highly sophisticated attitude dynamics models.

## Limitations

* The prediction model assumes constant angular velocity.
* External disturbance torques and spacecraft attitude control behavior are not modeled.
* Prediction accuracy decreases as the prediction horizon increases.
* The current implementation assumes a single spacecraft workflow.
* Historical predictions can be reviewed, but prediction-versus-truth comparison is not currently implemented.
* The software is intended as an engineering prototype and visualization tool rather than a flight operations system.
