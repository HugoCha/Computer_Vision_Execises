#!/usr/bin/python3

import os

from src.camera.camera import Camera
from src.camera.config import CAMERA_PATH, CAMERA_INDEX
from src.common.image_loader import ImageLoaderParameters
from src.common.image_saver import ImageSaverParameters
from src.common.launcher import Launcher, LauncherParameters
from src.common.processors import ImageProcessor, KeyProcessor, DefaultKeysProcessor
from src.common.vision_utils import *
from src.common.visualization import *

from .marker import Marker, detect_markers
from .config import *

class ArUcoProcessor( ImageProcessor, DefaultKeysProcessor ):
    def __init__( self,
                  camera:Camera,
                  img_saver_params:ImageSaverParameters, 
                  process_img_saver_params:ImageSaverParameters ):
        
        DefaultKeysProcessor.__init__( self, img_saver_params, process_img_saver_params )

        self.markers:list[Marker] = []
        self.camera = camera
        self.sub_menus().update( {
            'd' : KeyProcessor( 'd', "Display markers", lambda img, process : self.display_markers() ),
        } )

    def process_img( self, img:MatLike ) -> MatLike:
        self.markers = detect_markers( img, self.camera )
        for marker in self.markers:
            img = marker.draw( img )
        return img
    
    def title(self) -> str:
        return "ArUco marker processor"

    def display_markers( self ):
        print( "Markers:" )
        for marker in self.markers:
            print( marker )

    def save_img( self, process:Optional[MatLike] ):
        img_fpath = os.path.join( DATA_PROCESSED_PATH, "img.jpg" )
        if ( process is not None ):
            if ( cv2.imwrite( img_fpath, process ) ):
                print( f"ArUco markers image saved: {img_fpath}")


def main():
    camera = Camera.load_from_json( CAMERA_PATH )

    img_loader_params = ImageLoaderParameters( DATA_RAW_PATH, IMAGE_EXTENSION, IMAGE_BASE_NAME )
    img_saver_params = ImageSaverParameters( DATA_RAW_PATH, IMAGE_BASE_NAME, IMAGE_EXTENSION, CAN_OVERRIDE )
    process_img_saver_params = ImageSaverParameters( DATA_PROCESSED_PATH, IMAGE_BASE_NAME, IMAGE_EXTENSION, CAN_OVERRIDE )
    
    aruco_processor = ArUcoProcessor( camera, 
                                      img_saver_params, 
                                      process_img_saver_params )
    
    launcher_params = LauncherParameters( 
        img_loader_params,
        img_saver_params,
        process_img_saver_params,
        CAMERA_INDEX, 
        LAUNCH_OPTION,
        SHOW_IMAGE )
    
    launcher = Launcher( 
        launcher_params, 
        aruco_processor, 
        aruco_processor )
    
    launcher.launch()

if ( __name__ == "__main__" ):
    main()