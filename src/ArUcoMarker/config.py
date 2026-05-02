#!/usr/bin/python3

import cv2
import os

from src.common.launcher import LaunchOption

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
IMAGE_LOAD_PATH=os.path.join( DATA_RAW_PATH, "img0.jpg" ) # None : load all images in DATA_RAW_PATH
IMAGE_BASE_NAME="img"
IMAGE_EXTENSION=".jpg"
CAN_OVERRIDE=True
SHOW_IMAGE=True