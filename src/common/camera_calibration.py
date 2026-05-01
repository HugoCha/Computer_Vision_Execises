#!/usr/bin/python3

import argparse
import cv2
import numpy as np
import os

from typing import Callable, Optional, Sequence, Tuple

from cv2.typing import MatLike

from src.common.camera import Camera
from src.common.utils import get_files_by_extension, grayscale
from src.common.visualization import capture_video, show_image

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
            f"Chessboard folder: {self.chessboard_path}"
            f"Calibration folder: {self.calibration_path}"
        )

class LiveCameraCalibrationMenu:
    def __init__(self, parameters:CameraCalibrationParameters):
        self.parameters = parameters

    def process_key( self, key:int, img:MatLike, process_img:Optional[MatLike] ):
        if key < 0: return None

        match chr(key):
            case 'm':
                print( self.menu() )
            case 'p':
                print( self.parameters )
            case 'a':
                self.add( img )
            case 'r':
                self.remove()
            case 'c':
                self.clear()
            case 's':
                self.save( img )
            case _:
                print( f"Unknown key: {chr(key)}" )
    
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
        if ( self.parameters.chessboard_path is None ):
            print( f"Failed to save img at: {self.parameters.chessboard_path}" )
            return None
        
        img_index = len(self.parameters.chessboard_images)
        img_fname = "chessboard_" + str(img_index) + ".json" 
        img_fpath = os.path.join( self.parameters.chessboard_path, img_fname )
        if ( cv2.imwrite( img_fpath, img ) ):
            print( f"Chessboard img saved at: {img_fpath}" )
        else:
            print( f"Failed to save img at: {img_fpath}" )

    def menu( self ) -> str:
        return ( 
            f"Camera calibration menu:\n"
            f"'h': Display menu\n"
            f"'p': Display calibration parameters\n"
            f"'a': Add image to calibration images\n"
            f"'r': Remove last image from calibration images\n"
            f"'s': Add and Save image to file in {self.parameters.chessboard_path}"
            f"'q': Quit and Save calibration file in {self.parameters.calibration_path}"
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
        if ( not os.path.exists( parameters.calibration_path ) ):
            print( f"Invalid calibration parameters: Invalid save path {parameters.calibration_path}" )
            return False
        if ( not parameters.chessboard_path or not os.path.exists( parameters.chessboard_path ) ):
            print( f"Unable to save chessboard img to {parameters.chessboard_path}" )

        return True

    @staticmethod
    def run_from_images( parameters:CameraCalibrationParameters ):
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
            ret_corner = CameraCalibration._find_chessboard_corners( img, parameters )
            if ret_corner is None:
                continue
            
            corners, corner_img = ret_corner
            objpoints.append(objp.copy())
            imgpoints.append(corners)

            if ( parameters.show_corner_image ):
                show_image( corner_img, "corners" )

        if not objpoints or not imgpoints is None:
            print( f"Camera calibration failed: Unable to extract points from images" )
            return None

        ret, matrix, distortion, r_vecs, t_vecs = cv2.calibrateCamera(
            objpoints, imgpoints, image_size, np.eye(3), np.zeros(5))

        if ret:
            camera = Camera(matrix, distortion, r_vecs, t_vecs)
            camera.save_to_json( os.path.join( parameters.save_path, "camera.json" ) )
            print( 
                f"=========================\n"
                f"Camera calibration result\n"
                f"=========================\n"
                f"{camera}"
            )
            print( f"Camera calibration file saved to: {parameters.save_path}")
        else:
            print( f"Camera calibration failed:\n{parameters}")

    @staticmethod
    def run_from_path( parameters:CameraCalibrationParameters, images_directory:str, extension:str=".jpg" ):
        image_names = get_files_by_extension( images_directory, extension )

        parameters.chessboard_images = []
        for fname in image_names:
            img = cv2.imread( fname )
            if ( img is None ):
                continue
            parameters.chessboard_images.append( img )

        CameraCalibration.run_from_images( parameters )
        

    @staticmethod
    def run_from_camera( parameters:CameraCalibrationParameters, 
                         camera_index:int ):
        def draw_corner_func(img: MatLike) -> MatLike:
            ret = CameraCalibration._find_chessboard_corners(img, parameters)
            return ret[1] if ret is not None else img
        
        live_menu = LiveCameraCalibrationMenu( parameters )
        print( live_menu.menu() )
        
        capture_video( camera_index, draw_corner_func, live_menu.process_key )

        CameraCalibration.run_from_images( parameters )

    
    @staticmethod
    def _find_chessboard_corners( img:Optional[MatLike], 
                                  parameters:CameraCalibrationParameters ) -> Optional[tuple[MatLike, MatLike]]:
        if img is None:
            return None

        gray = grayscale(img)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        ret, corners = cv2.findChessboardCorners(gray, parameters.chessboard, None)

        if ret:
            corners = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            corners_img = cv2.drawChessboardCorners( img, parameters.chessboard, corners, True )
            return ( corners, corners_img )

        return None

def parse_args():
    parser = argparse.ArgumentParser(description="Process chessboard images.")

    # camera index
    parser.add_argument(
        "--camera",
        type=int,
        default=-1,
        help="Camera index. (default: -1)"
    )

    # chessboard folder path
    parser.add_argument(
        "--chessboard-path",
        type=str,
        default=None,
        help="Folder path to chessboard files (default: None)"
    )

    # chessboard dimensions
    parser.add_argument(
        "--chessboard",
        type=int,
        nargs=2, 
        default=None,
        metavar=("WIDTH", "HEIGHT"),
        help=f"Optional chessboard dimensions as (WIDTH, HEIGHT) (default: {DEFAULT_CHESSBOARD})"
    )

    # output path
    parser.add_argument(
        "--output-path",
        type=str,
        default=os.getcwd(),
        help="Folder path to save the camera calibration file. (default: current directory)"
    )

    args = parser.parse_args()

    dimensions = None
    if args.chessboard:
        dimensions = tuple(args.dimensions)

    return args.chessboard_path, args.camera, dimensions, args.output_path

if __name__ == "__main__":
    chessboard_path, camera_index, chessboard, output_path = parse_args()

    if ( chessboard is None ):
        chessboard = DEFAULT_CHESSBOARD

    if ( chessboard_path is None ):
        camera_index = camera_index if camera_index >=0 else 0
        
    parameters = CameraCalibrationParameters( chessboard, chessboard_path, output_path )
    print( f"Calibration parameters:\n{parameters}")

    if ( camera_index >= 0 ):
        print(f"Camera index: {camera_index}")
        CameraCalibration.run_from_camera( parameters, camera_index )
    elif parameters.chessboard_path is not None:
        print(f"Chessboard Folder Path: {parameters.chessboard_path}")
        CameraCalibration.run_from_path( parameters, parameters.chessboard_path )