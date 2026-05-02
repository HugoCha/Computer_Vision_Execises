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
