# Camera Calibration

In order to run camera calibration use

```bash
python -m src.common.camera_calibration
    [--camera CAMERA]
    [--chessboard-path CHESSBOARD_PATH]
    [--chessboard WIDTH HEIGHT]
    [--output-path OUTPUT_PATH]
```

Command menu:

```bash
-h, --help                          show this help message and exit
--camera CAMERA                     Camera index. (default: -1)
--chessboard-path CHESSBOARD_PATH   Folder path to chessboard files (default: None)
--chessboard WIDTH HEIGHT           Optional chessboard dimensions as (WIDTH, HEIGHT) (default: (8, 8))
--output-path OUTPUT_PATH           Folder path to save the camera calibration file. (default: current directory)
```

For example, run live camera calibration:
```bash
python -m src.common.camera_calibration --camera 0 --chessboard 8 8 --chessboard-path "data/chessboard" --output-path "data/camera"
```

Otherwise, run camera calibration from saved images
```bash
python -m src.common.camera_calibration --chessboard-path "data/chessboard" --chessboard 8 8 --output-path "data/camera"
```
