# Project 2 — ArUco Marker Detection and Pose Estimation

## Statement

A robot must localize a workpiece precisely before assembly.

The objective is to detect fiducial markers and estimate:

 - marker ID
 - marker position
 - marker orientation
 - camera-to-object pose

This project simulates industrial calibration and robot alignment tasks.

## Deliverable

Visual output should include:

 - detected marker corners
 - marker ID
 - 3D pose axes (X, Y, Z)
 - translation vector
 - rotation vector


Data output should include:

 - camera coordinates into robot coordinates using hand-eye calibration.

## Usage

Fill config.py with the configuration, such as:
```bash
# File and path
DATA_RAW_PATH="data/raw/ArUcoMarker"
DATA_PROCESSED_PATH="data/processed/ArUcoMarker"
DATA_IGNORED_PATH="data/ignored"

# Markers
MARKER_DICTIONARY=cv2.aruco.DICT_6X6_50
MARKER_IDS=[1,3,10,25,33]
MARKER_SIZE_MM=100

# Launch Parameters
LAUNCH_OPTION=LaunchOption.CAPTURE_VIDEO
IMAGE_BASE_NAME="marker"
IMAGE_EXTENSION=".jpg"
```

Run main, press q to quit application
```bash
python -m src.ArUcoMarker.main
```

 ## Result

 <div style="display: flex; justify-content: space-around">
  <img src="/data/processed/project2/img.jpg" alt="Processed Image" />
</div>
