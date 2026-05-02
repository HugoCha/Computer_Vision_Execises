# Camera

Get camera index with the command ( /dev/video{CAMERA_INDEX} ) :
```bash
v4l2-ctl --list-devices
```

# Camera Calibration

In order to run camera calibration use, if no argument are used default argument are in config.py

```bash
python -m src.camera.camera_calibration
    [--camera CAMERA]
    [--chessboard-path CHESSBOARD_PATH]
    [--chessboard WIDTH HEIGHT]
    [--output-path OUTPUT_PATH]
```

config.py contains the configuration, such as:
```bash
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
IMAGE_BASE_NAME="chessboard"
IMAGE_EXTENSION=".jpg"
```

Command menu:

```bash
-h, --help                          show this help message and exit
--camera CAMERA                     Camera index. (default: CAMERA_INDEX in config.py)
--chessboard-path CHESSBOARD_PATH   Folder path to chessboard files (default: CHESSBOARD_PATH in config.py)
--chessboard WIDTH HEIGHT           Optional chessboard dimensions as (WIDTH, HEIGHT) (default: CHESSBOARD in config.py)
--output-path OUTPUT_PATH           Folder path to save the camera calibration file. (default: CAMERA_PATH in config.py)
```

For example, run live camera calibration:
```bash
python -m src.camera.camera_calibration --camera 0 --chessboard 8 8 --chessboard-path "data/chessboard" --output-path "data/camera"
```

Otherwise, run camera calibration from saved images
```bash
python -m src.camera.camera_calibration --chessboard-path "data/chessboard" --chessboard 8 8 --output-path "data/camera"
```
