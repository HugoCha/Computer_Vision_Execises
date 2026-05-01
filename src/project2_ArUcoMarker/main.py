#!/usr/bin/python3

import os

from src.common.launcher import Launcher, LauncherParameters
from src.common.processors import ImageProcessor, KeyProcessor, KeysProcessor
from src.common.camera import Camera
from src.common.utils import *
from src.common.visualization import *

from .marker import Marker, detect_markers
from .config import *

class ArUcoProcessor( ImageProcessor, KeysProcessor ):
    def __init__( self, camera:Optional[Camera] = None ):
        self.markers:list[Marker] = []
        self.camera = camera
        self.sub_menu__: dict[str,KeyProcessor] = {
            'm' : KeyProcessor( 'm', "Display markers", lambda img, process : self.display_markers() ),
            's' : KeyProcessor( 's', "Save image to file", lambda img, process : self.save_img( process ) ),
        }

    def process_img( self, img:MatLike ) -> MatLike:
        self.markers = detect_markers( img, self.camera )
        for marker in self.markers:
            img = marker.draw( img )
        return img
    
    def title(self) -> str:
        return "ArUco marker processor"
    
    def sub_menus(self) -> dict[str, KeyProcessor]:
        return self.sub_menu__

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
    aruco_processor = ArUcoProcessor( camera )
    launcher_params = LauncherParameters( CAMERA_INDEX, IMAGE_PATH, IMAGE_EXTENSION, IMAGE_PROCESS_PATH, LAUNCH_OPTION )
    launcher = Launcher( launcher_params, aruco_processor, aruco_processor )
    launcher.launch()

if ( __name__ == "__main__" ):
    main()