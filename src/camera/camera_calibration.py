#!/usr/bin/python3

import argparse
import cv2
import numpy as np
import os

from enum import Enum
from cv2.typing import MatLike
from typing import Optional, Sequence

from src.camera.camera import Camera
from src.common.colors import Colors
from src.common.file_utils import is_directory, is_valid_path
from src.common.image_loader import ImageLoader, ImageLoaderParameters
from src.common.image_saver import ImageSaver, ImageSaverParameters
from src.common.launcher import Launcher, LauncherParameters, LaunchOption
from src.common.processors import DefaultKeysProcessor, ImageProcessor, KeyProcessor, KeysProcessor
from src.common.vision_utils import grayscale
from src.common.visualization import capture_video, show_image

from .config import *

DEFAULT_CHESSBOARD=(8,8)

class CameraCalibrationParameters:
    def __init__( self, 
                  chessboard:tuple[int,int], 
                  chessboard_path:Optional[str],
                  calibration_path:str,
                  chessboard_images:list[MatLike] = [],
                  show_corner_image:bool = False ):
        self.chessboard = chessboard
        self.chessboard_images = chessboard_images
        self.chessboard_path = chessboard_path
        self.calibration_path = calibration_path
        self.show_corner_image = show_corner_image

    def chessboard_image_count( self ) -> int:
        return len( self.chessboard_images )

    def __str__( self ) -> str:
        return (
            f"Chessboard: {self.chessboard}\n"
            f"Chessboard image cnt: {self.chessboard_image_count()}\n"
            f"Chessboard folder: {self.chessboard_path}\n"
            f"Calibration folder: {self.calibration_path}"
        )

class CameraCalibrationScore:
    class ScoreQuality( Enum ):
        EXCELLENT   =(0.3, Colors.BG_GREEN)
        GOOD        =(0.8, Colors.BG_BLUE)
        ACCEPTABLE  =(1.5, Colors.BG_YELLOW)
        POOR        =(2.0, Colors.BG_RED)

    def __init__( self, camera: Camera, 
                  points3d: Sequence[MatLike], 
                  pixels2d: Sequence[MatLike] ):
        self.score__ = CameraCalibrationScore.reprojection_error( camera, points3d, pixels2d )
        
        if self.score__ < self.ScoreQuality.EXCELLENT.value[0]:
            self.score_quality__ = self.ScoreQuality.EXCELLENT
        elif self.score__ < self.ScoreQuality.GOOD.value[0]:
            self.score_quality__ = self.ScoreQuality.GOOD
        elif self.score__ < self.ScoreQuality.ACCEPTABLE.value[0]:
            self.score_quality__ = self.ScoreQuality.ACCEPTABLE
        else:
            self.score_quality__ = self.ScoreQuality.POOR

    @property
    def score( self ) -> float:
        return self.score__

    @property
    def score_quality( self ) -> ScoreQuality:
        return self.score_quality__

    def __str__( self ) -> str:
        return f"{Colors.BOLD}{self.score_quality.value[1]}calibration score: {self.score} ({self.score_quality.name}){Colors.RESET}"

    @staticmethod
    def reprojection_error( camera:Camera, objpoints:Sequence[MatLike], imgpoints:Sequence[MatLike] ) -> float:
        mean_error = 0
        for i in range(len(objpoints)):
            imgpoints2, _ = cv2.projectPoints(objpoints[i], camera.rvecs[i], camera.tvecs[i], camera.matrix, camera.distortion )
            error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2SQR) / len(imgpoints2)
            mean_error += error
        mean_error = np.sqrt(mean_error/len(objpoints))
        return mean_error

class CameraCalibration:
    @staticmethod
    def is_valid_parameters( parameters:CameraCalibrationParameters ) -> bool:
        if ( parameters.chessboard[0] <=2 or parameters.chessboard[1] <= 2 ):
            print( f"Invalid calibration parameters: Invalid chessboard size {parameters.chessboard}" )
            return False
        if ( parameters.chessboard_image_count() <= 0 ):
            print( "Invalid calibration parameters: No chessboard images" )
            return False
        if ( not is_valid_path( parameters.calibration_path ) ):
            print( f"Invalid calibration parameters: Invalid save path {parameters.calibration_path}" )
            return False
        if ( not is_valid_path( parameters.chessboard_path ) ):
            print( f"Unable to save chessboard img to {parameters.chessboard_path}" )

        return True

    @staticmethod
    def calibrate( parameters:CameraCalibrationParameters ):
        if ( not CameraCalibration.is_valid_parameters( parameters ) ):
            return None

        chessboard = parameters.chessboard
        
        objp = np.zeros((chessboard[0] * chessboard[1], 3), np.float32)
        objp[:,:2] = np.mgrid[0:chessboard[0],0:chessboard[1]].T.reshape(-1,2)

        objpoints: list[MatLike] = []  # 3d point in real world space
        imgpoints: list[MatLike] = []  # 2d points in image plane.
        image_size = ( parameters.chessboard_images[0].shape[1],\
                       parameters.chessboard_images[0].shape[0] )

        for img in parameters.chessboard_images:
            ret_corner = CameraCalibration.find_chessboard_corners( img, parameters )
            if ret_corner is None:
                continue
            
            corners, corner_img = ret_corner
            objpoints.append(objp.copy())
            imgpoints.append(corners)

            if ( parameters.show_corner_image ):
                show_image( corner_img, "corners" )

        if len(objpoints) == 0 or len(imgpoints) == 0:
            print( f"Camera calibration failed: Unable to extract points from images" )
            return None

        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            objpoints, imgpoints, image_size, np.eye(3), np.zeros(5))

        if ret:
            camera = Camera(matrix, distortion, r_vecs, t_vecs)
            calibration_path = parameters.calibration_path
            
            camera_fpath = calibration_path
            if ( is_directory( calibration_path ) ):
                os.makedirs( calibration_path, exist_ok=True )
                camera_fname = "camera.json"
                camera_fpath = os.path.join( parameters.calibration_path, camera_fname )

            camera.save_to_json( camera_fpath )
            calibration_score = CameraCalibrationScore( camera, objpoints, imgpoints )
            print( 
                f"=========================\n"
                f"Camera calibration result\n"
                f"=========================\n"
                f"{calibration_score}\n"
                f"{camera}"
            )
            print( f"Camera calibration file saved to: {camera_fpath}")
        else:
            print( f"Camera calibration failed:\n{parameters}")
    
    @staticmethod
    def find_chessboard_corners( img:Optional[MatLike], 
                                 parameters:CameraCalibrationParameters ) -> Optional[tuple[MatLike, MatLike]]:
        if img is None:
            return None

        gray = grayscale(img)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        ret, corners = cv2.findChessboardCorners(gray, parameters.chessboard, None)

        if ret:
            corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            corners_img = img.copy()
            corners_img = cv2.drawChessboardCorners( corners_img, parameters.chessboard, corners, True )
            return ( corners, corners_img )

        return None

class CameraCalibrationProcessor(ImageProcessor, DefaultKeysProcessor):
    def __init__(self, 
                 parameters:CameraCalibrationParameters,
                 img_saver_params:ImageSaverParameters, 
                 process_img_saver_params:ImageSaverParameters ):
        DefaultKeysProcessor.__init__( self, img_saver_params, process_img_saver_params )


        self.parameters = parameters
        self.sub_menus().update( {
            'p': KeyProcessor( 'p', "Display calibration parameters", lambda im, proc: print( self.parameters ) ),
            'a': KeyProcessor( 'a', "Add image to calibration images", lambda im, proc: self.add( im )  ),
            'r': KeyProcessor( 'r', "Remove last image from calibration images", lambda im, proc: self.remove()  ),
            'c': KeyProcessor( 'c', "Clear calibration images", lambda im, proc: self.clear()  ),
            's': KeyProcessor( 's', f"Add and Save image to file in {self.parameters.chessboard_path}", lambda im, proc: self.save( im ) )
        } )

    def add( self, img:MatLike ):
        self.parameters.chessboard_images.append( img )
        print( f"Image added, image cnt: {len(self.parameters.chessboard_images)}")

    def remove( self ):
        if ( self.parameters.chessboard_image_count() > 0 ):
            self.parameters.chessboard_images.pop()
            print( f"Image remove, image cnt: {self.parameters.chessboard_image_count()}")

    def clear( self ):
        self.parameters.chessboard_images.clear()
        print( f"Chessboard images cleared" )

    def save( self, img:MatLike ):
        if self.raw_image_saver.can_save() and self.raw_image_saver.save( img ):
            self.add( img )

    def title(self) -> str:
        return "Camera calibration"

    def quit_menu(self) -> str:
        return f"Quit and Save calibration file in {self.parameters.calibration_path}"

    def process_img(self, img:MatLike ) -> MatLike:
        ret = CameraCalibration.find_chessboard_corners( img, self.parameters )
        if ( ret is not None ):
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

if __name__ == "__main__":

    chessboard_path, camera_index, live, chessboard, output_path = parse_args()

    parameters = CameraCalibrationParameters( chessboard, chessboard_path, output_path )
    print( f"Calibration parameters:\n{parameters}")
    
    img_loader_params = ImageLoaderParameters( chessboard_path, IMAGE_EXTENSION )
    img_saver_params = ImageSaverParameters( chessboard_path, IMAGE_BASE_NAME, IMAGE_EXTENSION, False )
    process_img_saver_params = ImageSaverParameters( DATA_PROCESSED_PATH, IMAGE_BASE_NAME, IMAGE_EXTENSION, False )
    
    if ( live and camera_index >= 0 ):
        processor = CameraCalibrationProcessor( 
            parameters, 
            img_saver_params, 
            process_img_saver_params )
    
        launcher_params = LauncherParameters( 
            img_loader_params,
            img_saver_params,
            process_img_saver_params,
            camera_index, 
            LaunchOption.CAPTURE_VIDEO )
    
        launcher = Launcher( launcher_params, processor, processor )
        launcher.launch()
    else:
        img_loader = ImageLoader( img_loader_params )
        parameters.chessboard_images = img_loader.load()
    
    #try
    CameraCalibration.calibrate( parameters )
    # except:
    #     print( "Camera calibration failed" )