#!/usr/bin/python3

import os

from src.common.launcher import LaunchOption

# File and Path
DATA_RAW_PATH="data/raw/project1"
DATA_PROCESSED_PATH="data/processed/project1"
DATA_IGNORED_PATH="data/ignored"
IMAGE_INDEX=0

# Launch Parameters
LAUNCH_OPTION=LaunchOption.LOAD_IMAGE
CAMERA_INDEX=2 # index associated with camera in /dev/video(*)
IMAGE_EXTENSION=".jpg"
IMAGE_PATH=DATA_RAW_PATH#os.path.join( DATA_RAW_PATH, "img" + str( IMAGE_INDEX ) + IMAGE_EXTENSION )
IMAGE_PROCESS_PATH=None#os.path.join( DATA_PROCESSED_PATH, "img" + str( IMAGE_INDEX ) + IMAGE_EXTENSION )