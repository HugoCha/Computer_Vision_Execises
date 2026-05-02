#!/usr/bin/python3

import argparse
import threading
import time

from cv2.typing import MatLike
from typing import Optional

from src.camera.camera import Camera
from src.common.image_loader import ImageLoader, ImageLoaderParameters
from src.common.image_saver import ImageSaver, ImageSaverParameters
from src.common.launcher import Launcher, LauncherParameters, LaunchOption
from src.common.processors import ImageProcessor, KeyProcessor, KeysProcessor

from .camera_calibration import CameraCalibrationParameters, CameraCalibration
from .config import *

class AutomaticCalibrationParameters:
    def __init__( self, 
                  frame_nb: int,
                  frame_interval_ms: int ):
        self.frame_nb = frame_nb
        self.frame_interval_ms = frame_interval_ms
        self.frame_interval_s = frame_interval_ms / 1000.0

    def __str__(self) -> str:
        return (
            f"Total frame number: {self.frame_nb}\n"
            f"Frame interval: {self.frame_interval_ms} ms" )

class AutomaticCameraCalibrationProcessor(ImageProcessor, KeysProcessor):
    def __init__( self, 
                  calibration_parameters:CameraCalibrationParameters,
                  automatic_parameters:AutomaticCalibrationParameters ):
        self.calibration_parameters = calibration_parameters
        self.automatic_parameters = automatic_parameters

        self.__last_start_time:float
        self.__is_calibrating = False
        self.__is_started = False
        self.__camera:Optional[Camera] = None

        self.__sub_menu:dict[str,KeyProcessor] = {
            'b' : KeyProcessor( 'b', f"Start automatic calibration.", lambda im, proc : self.start() ),
            'e' : KeyProcessor( 'e', f"Stop automatic calibration.", lambda im, proc : self.stop() ),
            's' : KeyProcessor( 's', f"Save calibration in {self.calibration_parameters.calibration_path}", lambda im, proc : self.save_calibration() )
        }

    @property
    def is_started( self ):
        return self.__is_started

    def start( self ):
        if ( self.__is_calibrating ): return
        print( "Calibration started." )
        self.__is_started = True
        self.__last_start_time = time.time()

    def stop( self ):
        self.__is_started = False
        if ( self.__is_calibrating ): return
        print( "Calibration stopped." )
        if ( len( self.calibration_parameters.chessboard_images ) >= self.automatic_parameters.frame_nb ):
            self.start_calibration()

    def _run_calibration( self ):
        self.__is_calibrating = True
        self.__camera = CameraCalibration.calibrate( self.calibration_parameters, False )
        self.__is_calibrating = False
        print( self.menu() )

    def start_calibration( self ):
        self.__is_calibrating = True
        calib_thread = threading.Thread( target=self._run_calibration, name="CameraCalibration" )
        calib_thread.start()

    def save_calibration( self ):
        if ( self.__is_calibrating or self.__is_started ):
            print( "Unable to save camera calibration file, calibration is still running" )
            return
        if ( self.__camera is None ):
            print( "Unable to save camera calibration file, run calibration first" )
            return

        CameraCalibration.save( self.calibration_parameters, self.__camera ) 

    def title(self) -> str:
        return "Automatic camera calibration"
    
    def sub_menus(self) -> dict[str, KeyProcessor]:
        return self.__sub_menu

    def process_key(self, key: int, img: MatLike, process: Optional[MatLike] ) -> None:
        return super().process_key(key, img, process)

    def process_img( self, img:MatLike ) -> MatLike:
        ret = CameraCalibration.find_chessboard_corners( img, self.calibration_parameters )

        if ( ret is not None ):
            new_time = time.time()
            if ( self.is_started and 
                 new_time - self.__last_start_time >= self.automatic_parameters.frame_interval_s ):
                self.calibration_parameters.chessboard_images.append( img )
                self.__last_start_time = new_time
                img_cnt = len( self.calibration_parameters.chessboard_images )
                print( f"Image added, total : {img_cnt}" )
                if ( img_cnt >= self.automatic_parameters.frame_nb ):
                    self.stop()

            return ret[1]
        return img
    

def parse_args():
    parser = argparse.ArgumentParser(description="Process chessboard images.")

    # camera index
    parser.add_argument(
        "--camera",
        type=int,
        default=CAMERA_INDEX,
        help=f"Camera index. (default: {CAMERA_INDEX})"
    )

    # live calibration
    parser.add_argument(
        "--live",
        type=bool,
        default=LIVE_CALIBRATION,
        help=f"Is inlive calibration. (default: {LIVE_CALIBRATION})"
    )

    # chessboard folder path
    parser.add_argument(
        "--chessboard-path",
        type=str,
        default=CHESSBOARD_PATH,
        help=f"Folder path to chessboard files (default: {CHESSBOARD_PATH})"
    )

    # chessboard dimensions
    parser.add_argument(
        "--chessboard",
        type=int,
        nargs=2, 
        default=CHESSBOARD,
        metavar=("WIDTH", "HEIGHT"),
        help=f"Optional chessboard dimensions as (WIDTH, HEIGHT) (default: {CHESSBOARD})"
    )

    # output path
    parser.add_argument(
        "--output-path",
        type=str,
        default=CAMERA_PATH,
        help=f"Folder path to save the camera calibration file. (default: {CAMERA_PATH})"
    )

    args = parser.parse_args()

    chessboard = None
    if args.chessboard:
        chessboard = tuple(args.chessboard)

    return args.chessboard_path, args.camera, args.live, chessboard, args.output_path


def run_automatic_calibration():
    chessboard_path, camera_index, live, chessboard, output_path = parse_args()

    calibration_parameters = CameraCalibrationParameters( chessboard, chessboard_path, output_path )
    automatic_parameters = AutomaticCalibrationParameters( FRAME_NB, FRAME_INTERVAL )
    
    print( ( 
        f"=======================\n"
        f"Calibration parameters:\n"
        f"-----------------------\n"
        f"{calibration_parameters}\n"
        f"=======================\n"
        f"\n"
        f"=======================\n"
        f"Automatic parameters\n"
        f"-----------------------\n"
        f"{automatic_parameters}\n"
        f"=======================\n"
     ) )

    img_loader_params = ImageLoaderParameters( chessboard_path, IMAGE_EXTENSION )
    img_saver_params = ImageSaverParameters( chessboard_path, IMAGE_BASE_NAME, IMAGE_EXTENSION, False )
    process_img_saver_params = ImageSaverParameters( DATA_PROCESSED_PATH, IMAGE_BASE_NAME, IMAGE_EXTENSION, False )
    
    if ( camera_index >= 0 ):
        processor = AutomaticCameraCalibrationProcessor( 
            calibration_parameters, 
            automatic_parameters )
    
        launcher_params = LauncherParameters( 
            img_loader_params,
            img_saver_params,
            process_img_saver_params,
            camera_index, 
            LaunchOption.CAPTURE_VIDEO )
    
        launcher = Launcher( launcher_params, processor, processor )
        launcher.launch()
    else:
        print( f"Camera index must match hardware: {camera_index}")

if __name__ == "__main__":
    run_automatic_calibration()