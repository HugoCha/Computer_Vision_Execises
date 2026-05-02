# Camera

Get camera index with the command ( /dev/video{CAMERA_INDEX} ) :
```bash
v4l2-ctl --list-devices
```

# Camera Calibration

In order to run camera calibration use, if no argument are used default argument are in config.py

## Command

```bash
python -m src.camera.camera_calibration
    [--camera CAMERA]
    [--live LIVE_CALIBRATION]
    [--chessboard-path CHESSBOARD_PATH]
    [--chessboard WIDTH HEIGHT]
    [--output-path OUTPUT_PATH]
```

For example, run live camera calibration:
```bash
python -m src.camera.camera_calibration --camera 0 --live True --chessboard 8 8 --chessboard-path "data/chessboard" --output-path "data/camera"
```

Otherwise, run camera calibration from saved images
```bash
python -m src.camera.camera_calibration --chessboard-path --live False "data/chessboard" --chessboard 8 8 --output-path "data/camera"
```

## Command Options

```bash
-h, --help                          show this help message and exit
--camera CAMERA                     Camera index. (default: CAMERA_INDEX in config.py)
--live                              run calibration in live (default: LIVE_CALIBRATION in config.py)
--chessboard-path CHESSBOARD_PATH   Folder path to chessboard files (default: CHESSBOARD_PATH in config.py)
--chessboard WIDTH HEIGHT           Optional chessboard dimensions as (WIDTH, HEIGHT) (default: CHESSBOARD in config.py)
--output-path OUTPUT_PATH           Folder path to save the camera calibration file. (default: CAMERA_PATH in config.py)
```

## Command Configuration

config.py contains the configuration, such as:
```python
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
```

## Live Calibration

 <div style="display: flex; justify-content: space-around">
  <img src="/data/processed/camera/chessboard0.jpg" alt="Processed Image" />
</div>

