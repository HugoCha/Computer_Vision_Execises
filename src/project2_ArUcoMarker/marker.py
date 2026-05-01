#!/usr/bin/python3

import cv2
import numpy as np
import os

from typing import Optional
from cv2.typing import MatLike

from src.common.visualization import show_image

from .config import DATA_RAW_PATH, MARKER_DICTIONARY, MARKER_IDS, MARKER_SIZE

marker_dict = cv2.aruco.getPredefinedDictionary( MARKER_DICTIONARY ) 

class Marker:
    def __init__( self, id:int, corner: Optional[MatLike] = None ):
        self.corner = corner
        self.id = int(id)
        self.img__: Optional[MatLike] = None

    def image( self ) -> MatLike:
        if ( self.img__ is None ):
            self.img__ = cv2.aruco.generateImageMarker( marker_dict, self.id, MARKER_SIZE )
        return self.img__

    def show( self ):
        show_image( self.image(), "marker" + str(self.id) )

    def draw( self, img:MatLike ) -> MatLike:
        if ( self.corner is not None ):
            
            corners_list = [self.corner.astype(np.float32)]
            ids_array = np.array([[int(self.id)]], dtype=np.int32)
            cv2.aruco.drawDetectedMarkers(img, corners_list, ids_array)

        return img

    def save( self, path:str ):
        cv2.imwrite( os.path.join( path, "marker" + str( self.id ) + ".png" ), self.image() )

    def __str__( self ) -> str:
        return f"id: {self.id}, corner: {self.corner}"

def detect_markers( img:MatLike ) -> list[Marker]:
    detector_parameters = cv2.aruco.DetectorParameters()
    (corners, ids, _) = cv2.aruco.detectMarkers(
        img, 
        marker_dict,
	    parameters=detector_parameters )
    
    markers:list[Marker] = []

    for i in range(len(corners)):
        marker = Marker( ids[i][0], corners[i] )
        markers.append( marker )

    return markers

def main():
    for id in MARKER_IDS:
        marker = Marker( id )
        marker.save( DATA_RAW_PATH )
        marker.show()

if ( __name__ == "__main__" ):
    main()
