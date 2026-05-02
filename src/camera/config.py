#!/usr/bin/python3

import os

from src.common.launcher import LaunchOption

# File and Path
DATA_RAW_PATH="data/raw/camera"
DATA_PROCESSED_PATH="data/processed/camera"
DATA_IGNORED_PATH="data/ignored/camera"

# Calibration
CHESSBOARD=(8,6)
CHESSBOARD_PATH=DATA_IGNORED_PATH
CAMERA_PATH=os.path.join( DATA_IGNORED_PATH, "camera.json" )

# Launch Parameters
LIVE_CALIBRATION=True
CAMERA_INDEX=2 # index associated with camera in /dev/video(*)
IMAGE_BASE_NAME="chessboard"
IMAGE_EXTENSION=".jpg"
SHOW_IMAGE=False