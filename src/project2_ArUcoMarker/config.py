#!/usr/bin/python3
import cv2

CAMERA_INDEX=2
MARKER_DICTIONARY=cv2.aruco.DICT_6X6_50
MARKER_IDS=[1,3,10,25, 33]
MARKER_SIZE_MM=100
DATA_RAW_PATH="data/raw/project2"
DATA_PROCESSED_PATH="data/processed/project2"
DATA_IGNORED_PATH="data/ignored"
CAMERA_PATH="data/ignored/camera/camera.json"