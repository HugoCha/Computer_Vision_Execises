#!/usr/bin/python3

from src.common.launcher import LaunchOption

# File and Path
DATA_RAW_PATH="data/raw/camera"
DATA_PROCESSED_PATH="data/processed/camera"
DATA_IGNORED_PATH="data/ignored"

# Calibration
CHESSBOARD=(8,6)
CHESSBOARD_PATH=DATA_RAW_PATH
CAMERA_PATH=DATA_RAW_PATH

# Launch Parameters
LAUNCH_OPTION=LaunchOption.LOAD_IMAGE
CAMERA_INDEX=2 # index associated with camera in /dev/video(*)
IMAGE_BASE_NAME="img"
IMAGE_EXTENSION=".jpg"