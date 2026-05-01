#!/usr/bin/python3

import cv2
import os

from src.common.launcher import LaunchOption

# File and path
DATA_RAW_PATH="data/raw/project2"
DATA_PROCESSED_PATH="data/processed/project2"
DATA_IGNORED_PATH="data/ignored"
CAMERA_PATH="data/ignored/camera/camera.json"

# Markers
MARKER_DICTIONARY=cv2.aruco.DICT_6X6_50
MARKER_IDS=[1,3,10,25, 33]
MARKER_SIZE_MM=100

# Launch Parameters
LAUNCH_OPTION=LaunchOption.CAPTURE_VIDEO
CAMERA_INDEX=2
IMAGE_EXTENSION=".jpg"
IMAGE_PATH=os.path.join( DATA_RAW_PATH, f"img{IMAGE_EXTENSION}" )
IMAGE_PROCESS_PATH=os.path.join( DATA_PROCESSED_PATH, f"img{IMAGE_EXTENSION}" )