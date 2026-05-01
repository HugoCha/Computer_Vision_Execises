#!/usr/bin/python3

import os

from src.common.camera import Camera
from src.common.utils import *
from src.common.visualization import *

from .marker import Marker, detect_markers
from .config import *

class ArUcoProcessor:
    def __init__( self, camera:Optional[Camera] = None ):
        self.markers:list[Marker] = []
        self.camera = camera

    def process( self, img:MatLike ) -> MatLike:
        self.markers = detect_markers( img, self.camera )
        for marker in self.markers:
            img = marker.draw( img )
        return img

    def process_key( self, key:int, img:MatLike, process:Optional[MatLike] ):
        if ( key < 0 ): return None

        match chr( key ):
            case 'm':
                print( "Markers:" )
                for marker in self.markers:
                    print( marker )
            case 's':
                img_fpath = os.path.join( DATA_PROCESSED_PATH, "img.jpg" )
                if ( process is not None ):
                    if ( cv2.imwrite( img_fpath, process ) ):
                        print( f"ArUco markers image saved: {img_fpath}")

def main():
    camera = Camera.load_from_json( CAMERA_PATH )
    aruco_processor = ArUcoProcessor( camera )
    capture_video( 
        CAMERA_INDEX, 
        aruco_processor.process, 
        aruco_processor.process_key )

if ( __name__ == "__main__" ):
    main()