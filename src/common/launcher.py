#!/usr/bin/python3

import os

from enum import Enum
from typing import Optional

from src.common.file_utils import is_path_valid, is_directory, is_valid_image_extension
from src.common.visualization import capture_image, capture_video, load_image, load_images
from src.common.processors import DefaultImageProcessor, DefaultKeysProcessor, ImageProcessor, KeysProcessor

class LaunchOption(Enum):
    CAPTURE_VIDEO=0
    CAPTURE_IMAGE=1
    LOAD_IMAGE=2

class LauncherParameters:
    def __init__( self, 
                  camera_index:Optional[int]=None,
                  image_path:Optional[str]=None,
                  image_extension:Optional[str]=None,
                  process_image_path:Optional[str]=None,
                  option:LaunchOption = LaunchOption.CAPTURE_VIDEO ):
        self.camera_index = camera_index
        self.image_path = image_path
        self.image_extension = image_extension
        self.process_image_path = process_image_path
        self.option = option

class Launcher:
    def __init__( self, 
                 parameters:LauncherParameters, 
                 img_processor:ImageProcessor = DefaultImageProcessor(),
                 key_processor:KeysProcessor = DefaultKeysProcessor() ):
        self.parameters = parameters
        self.img_processor___ = img_processor
        self.key_processor___ = key_processor

    def is_valid_parameters( self ):
        is_camera_index_valid = self.parameters.camera_index is not None and\
                                self.parameters.camera_index >= 0
        
        is_image_path_valid = is_path_valid( self.parameters.image_path )

        match self.parameters.option:
            case LaunchOption.CAPTURE_VIDEO:
                return is_camera_index_valid
            case LaunchOption.CAPTURE_IMAGE:
                return is_camera_index_valid and is_image_path_valid
            case LaunchOption.LOAD_IMAGE:
                if ( not is_image_path_valid ): return False
                if ( is_directory( self.parameters.image_path ) ):
                    return ( self.parameters.image_extension is not None and
                             is_valid_image_extension( self.parameters.image_extension ) )
                else:
                    return os.path.exists( self.parameters.image_path )

        return False

    def launch( self ):
        if ( not self.is_valid_parameters() ):
            print( "Launch parameters invalid" )
            return None

        match self.parameters.option:
            case LaunchOption.CAPTURE_VIDEO:
                print( self.key_processor___.menu() )
                capture_video(\
                    self.parameters.camera_index,\
                    self.img_processor___.process_img,\
                    self.key_processor___.process_key )
            case LaunchOption.CAPTURE_IMAGE:
                capture_image(\
                    self.parameters.camera_index,\
                    self.parameters.image_path,\
                    self.parameters.process_image_path,\
                    self.img_processor___.process_img )
            case LaunchOption.LOAD_IMAGE:
                if ( is_directory( self.parameters.image_path ) ):
                    load_images(
                        self.parameters.image_path,\
                        self.parameters.image_extension,
                        self.parameters.process_image_path,\
                        self.img_processor___.process_img )
                else:
                    load_image(
                        self.parameters.image_path,\
                        self.parameters.process_image_path,\
                        self.img_processor___.process_img )