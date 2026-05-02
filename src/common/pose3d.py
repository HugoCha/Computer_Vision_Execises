#!/usr/bin/python3

import cv2
import numpy as np

from cv2.typing import MatLike

class Pose3d:
    def __init__( self, rvec:MatLike, tvec:MatLike, pts:MatLike ):
        self.rvec = rvec
        self.tvec = tvec
        self.pts = pts

        R, _ = cv2.Rodrigues(rvec)
        transform = np.eye(4)
        transform[:3, :3] = R
        transform[:3, 3] = tvec.flatten()
        self.transform__ = transform

        inverse_transform = np.eye(4)
        inverse_transform[:3, :3] = R.T
        inverse_transform[:3, 3] = -R.T @ tvec.reshape(3,)
        self.inverse_transform__ = inverse_transform

    @property
    def transform( self ):
        return self.transform__
    
    @property
    def inverse_transform( self ):
        return self.inverse_transform__
    
    def __str__( self ) -> str:
        return f"{self.transform}"
    