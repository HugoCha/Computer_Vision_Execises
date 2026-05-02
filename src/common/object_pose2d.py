#!/usr/bin/python3

from cv2.typing import MatLike
from typing import Optional

class ObjectPose2d:
    def __init__( self, 
                  center:tuple[int,int], 
                  bounding_box:MatLike,
                  angle: Optional[float] = None, 
                  axis:Optional[tuple[float,float]] = None ):
        self.center = center
        self.bounding_box = bounding_box
        self.angle = angle
        self.axis = axis

    def __str__( self ) -> str:
        if ( self.angle is None ):
            return f"center: {self.center}\nbox: {self.bounding_box}"
        return f"center: {self.center}, angle: {self.angle}, axis: {self.axis}\nbox:\n{self.bounding_box}"
