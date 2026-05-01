# Project 1 — Object Pose Estimation for Pick-and-Place

## Statement

A robot must pick flat mechanical parts placed randomly on a table.

The objective is to detect for each part:

 - center position (x, y)
 - orientation angle θ
 - grasp point
 - invalid or overlapping detections

The output should be directly usable by a robotic arm for pick-and-place operations.

## Deliverable

For each detected object:

```bash
Object 1
Center: (320, 180)
Angle: 42°
Axis: (10, 0)
```

Visual output should include:

 - contour
 - center point
 - orientation axis
 - rotated bounding box

## Usage

Fill config.py with the configuration, such as:
```bash
CAMERA_INDEX=0
IMAGE_INDEX=0   # index to save image with img{IMAGE_INDEX}.jpg
DATA_RAW_PATH="data/raw/project1"
DATA_PROCESSED_PATH="data/processed/project1"
DATA_IGNORED_PATH="data/ignored"
```

Get camera index with the command ( /dev/video{CAMERA_INDEX} ) :
```bash
v4l2-ctl --list-devices
```

Run main, press q to quit application
```bash
python -m src.project1_pose_estimation.main
```

## Result

<div style="display: flex; justify-content: space-around">
  <img src="/data/raw/project1/img0.jpg" alt="Raw Image" width="45%" />
  <img src="/data/processed/project1/img0.jpg" alt="Processed Image" width="45%" />
</div>
