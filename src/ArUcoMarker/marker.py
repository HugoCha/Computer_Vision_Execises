#!/usr/bin/python3

import cv2
import numpy as np
import os

from typing import Optional
from cv2.typing import MatLike

from src.camera.camera import Camera
from src.common.visualization import show_image
from src.common.pose3d import Pose3d

from .config import *

marker_dict = cv2.aruco.getPredefinedDictionary( MARKER_DICTIONARY ) 

class Marker:
    def __init__( self, id:int, corners: Optional[MatLike] = None, camera:Optional[Camera] = None ):
        self.corners = corners
        self.id = int(id)
        self.camera = camera
        self.marker_pose__:Optional[Pose3d] = None
        self.img__: Optional[MatLike] = None

    def image( self ) -> MatLike:
        if ( self.img__ is None ):
            self.img__ = cv2.aruco.generateImageMarker( marker_dict, self.id, MARKER_SIZE_MM )
        return self.img__

    def show( self ):
        show_image( self.image(), "marker" + str(self.id) )

    def draw( self, img:MatLike ) -> MatLike:
        if ( self.corners is not None ):
            
            corners_list = [self.corners.astype(np.float32)]
            ids_array = np.array([[int(self.id)]], dtype=np.int32)
            cv2.aruco.drawDetectedMarkers(img, corners_list, ids_array)

            marker_pose = self.marker_pose()
            if ( marker_pose is not None and 
                 self.camera is not None ):
                cv2.drawFrameAxes(\
                    img,\
                    self.camera.matrix,\
                    self.camera.distortion, 
                    marker_pose.rvec, 
                    marker_pose.tvec, 
                    0.1 )  
        return img

    def marker_pose( self ) -> Optional[Pose3d]:
        if ( self.marker_pose__ is None and 
             self.corners is not None and 
             self.camera is not None ):
            corners = self.corners
            rvec, tvec, marker_pts =\
                cv2.aruco.estimatePoseSingleMarkers(\
                    [corners],\
                    MARKER_SIZE_MM * 1e-3,\
                    self.camera.matrix,\
                    self.camera.distortion )
            self.marker_pose__ = Pose3d( rvec, tvec, marker_pts )
        return self.marker_pose__

    def save( self, path:str ):
        cv2.imwrite( os.path.join( path, "marker" + str( self.id ) + ".png" ), self.image() )

    def __str__( self ) -> str:
        return ( 
            f"id: {self.id}, corner: {self.corners}\n"
            f"pose:\n{self.marker_pose()}"
        )

def detect_markers( img:MatLike, camera:Optional[Camera] = None ) -> list[Marker]:
    detector_parameters = cv2.aruco.DetectorParameters()
    (corners, ids, _) = cv2.aruco.detectMarkers(
        img, 
        marker_dict,
	    parameters=detector_parameters )
    
    markers:list[Marker] = []

    for i in range(len(corners)):
        marker = Marker( ids[i][0], corners[i], camera )
        markers.append( marker )

    return markers

def main():
    for id in MARKER_IDS:
        marker = Marker( id )
        marker.save( DATA_RAW_PATH )
        marker.show()

if ( __name__ == "__main__" ):
    main()
