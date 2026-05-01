#!/usr/bin/python3

import json
import numpy as np

from typing import Sequence
from cv2.typing import MatLike

class Camera:
    def __init__( self,
                  camera_matrix: MatLike,
                  distortion: MatLike, 
                  rvecs: Sequence[MatLike],
                  tvecs: Sequence[MatLike] ):
        self.camera_matrix__ = camera_matrix
        self.distortion__ = distortion
        self.rvecs__ = rvecs
        self.tvecs__ = tvecs

    @property
    def matrix( self ): return self.camera_matrix__ 
    
    @property
    def distortion( self ): return self.distortion__ 

    @property
    def rvecs( self ): return self.rvecs__ 

    @property
    def tvecs( self ): return self.tvecs__

    def __str__( self ) -> str:
        return (
            f"Matrix:\n{self.matrix}\n"
            f"Distortion:\n{self.distortion}\n"
            f"Rvecs:\n{self.rvecs}\n"
            f"Tvecs:\n{self.tvecs}"
        )

    @classmethod
    def load_from_json(cls, file_path: str) -> "Camera":
        with open(file_path, "r") as f:
            data = json.load(f)

        camera_matrix = np.array(data["camera_matrix"])
        distortion = np.array(data["distortion"])
        rvecs = [np.array(rvec) for rvec in data["rvecs"]]
        tvecs = [np.array(tvec) for tvec in data["tvecs"]]

        return cls(camera_matrix, distortion, rvecs, tvecs)

    def save_to_json(self, file_path: str):
        data = {
            "camera_matrix": self.camera_matrix__.tolist(),
            "distortion": self.distortion__.tolist(),
            "rvecs": [rvec.tolist() for rvec in self.rvecs__],
            "tvecs": [tvec.tolist() for tvec in self.tvecs__],
        }

        with open(file_path, "w") as f:
            json.dump(data, f, indent=4) 
