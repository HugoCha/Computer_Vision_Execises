#!/usr/bin/python3

import cv2
import numpy as np
import os

from cv2.typing import MatLike
from typing import Optional

from src.camera.camera import Camera
from src.common.file_utils import is_directory, is_valid_path
from src.common.vision_utils import grayscale

from .camera_calibration_score import CameraCalibrationScore
from .config import *

class CameraCalibrationParameters:
    def __init__( self, 
                  chessboard:tuple[int,int], 
                  chessboard_path:Optional[str],
                  calibration_path:str,
                  chessboard_images:list[MatLike] = [] ):
        self.chessboard = chessboard
        self.chessboard_images = chessboard_images
        self.chessboard_path = chessboard_path
        self.calibration_path = calibration_path

    def chessboard_image_count( self ) -> int:
        return len( self.chessboard_images )

    def __str__( self ) -> str:
        return (
            f"Chessboard: {self.chessboard}\n"
            f"Chessboard image cnt: {self.chessboard_image_count()}\n"
            f"Chessboard folder: {self.chessboard_path}\n"
            f"Calibration folder: {self.calibration_path}"
        )

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
    def calibrate( parameters:CameraCalibrationParameters, save_file:bool ) -> Optional[Camera]:
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

        if len(objpoints) == 0 or len(imgpoints) == 0:
            print( f"Camera calibration failed: Unable to extract points from images" )
            return None

        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            objpoints, imgpoints, image_size, np.eye(3), np.zeros(5))

        if ret:
            camera = Camera(matrix, distortion, r_vecs, t_vecs)
            calibration_score = CameraCalibrationScore( camera, objpoints, imgpoints )
            
            print( 
                f"=========================\n"
                f"Camera calibration result\n"
                f"=========================\n"
                f"{calibration_score}\n"
                f"{camera}"
            )

            if ( save_file ):
                CameraCalibration.save( parameters, camera )

            return camera
        
        print( f"Camera calibration failed:\n{parameters}")
        return None

    @staticmethod
    def save( parameters:CameraCalibrationParameters, camera:Camera ):
        calibration_path = parameters.calibration_path
            
        camera_fpath = calibration_path
        if ( is_directory( calibration_path ) ):
            os.makedirs( calibration_path, exist_ok=True )
            camera_fname = "camera.json"
            camera_fpath = os.path.join( parameters.calibration_path, camera_fname )

        camera.save_to_json( camera_fpath )
        print( f"Camera calibration file saved to: {camera_fpath}")

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