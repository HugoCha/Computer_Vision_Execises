#!/usr/bin/python3

import cv2
import numpy as np

from enum import Enum
from cv2.typing import MatLike
from typing import Sequence

from src.camera.camera import Camera
from src.common.colors import Colors

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