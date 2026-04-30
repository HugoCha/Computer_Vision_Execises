#!/usr/bin/python3

from typing import Optional

class object_pose:
    def __init__( self, 
                  center:tuple[int,int], 
                  angle: Optional[float] = None, 
                  axis:Optional[tuple[float,float]] = None ):
        self.center = center
        self.angle = angle
        self.axis = axis

    def __str__( self ) -> str:
        return f"center: {self.center}, angle: {self.angle}, axis: {self.axis}"
