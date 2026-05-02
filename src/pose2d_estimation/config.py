#!/usr/bin/python3

import os

from src.common.launcher import LaunchOption

# File and Path
DATA_RAW_PATH="data/raw/pose2d_estimation"
DATA_PROCESSED_PATH="data/processed/pose2d_estimation"
DATA_IGNORED_PATH="data/ignored"

# Launch Parameters
LAUNCH_OPTION=LaunchOption.LOAD_IMAGE
IMAGE_LOAD_PATH=os.path.join( DATA_RAW_PATH, "img0.jpg" ) # None : load all images in DATA_RAW_PATH
IMAGE_BASE_NAME="img"
IMAGE_EXTENSION=".jpg"
CAN_OVERRIDE=True
SHOW_IMAGE=True