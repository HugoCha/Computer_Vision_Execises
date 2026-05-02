#!/usr/bin/python3

import os

# File and Path
DATA_RAW_PATH="data/raw/camera"
DATA_PROCESSED_PATH="data/processed/camera"
DATA_IGNORED_PATH="data/ignored/camera"

# Calibration
CHESSBOARD=(8,6)
CHESSBOARD_PATH=DATA_IGNORED_PATH
CAMERA_PATH=os.path.join( DATA_IGNORED_PATH, "camera.json" )
FRAME_NB=50
FRAME_INTERVAL=1000 #ms

# Launch Parameters
LIVE_CALIBRATION=True
CAMERA_INDEX=2 # index associated with camera in /dev/video(*)
IMAGE_BASE_NAME="chessboard"
IMAGE_EXTENSION=".jpg"
SHOW_IMAGE=False