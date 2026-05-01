#!/usr/bin/python3

from .marker import detect_markers
from src.common.utils import *
from src.common.visualization import *
from .config import *

def process( img:MatLike ) -> MatLike:
    markers = detect_markers( img )
    for marker in markers:
        img = marker.draw( img )
    return img

def main():
    capture_video( CAMERA_INDEX, process )

if ( __name__ == "__main__" ):
    main()