#!/usr/bin/python3

from enum import Enum
from typing import Optional

from src.common.image_loader import ImageLoader, ImageLoaderParameters
from src.common.image_saver import ImageSaver, ImageSaverParameters
from src.common.processors import DefaultImageProcessor, DefaultKeysProcessor, ImageProcessor, KeysProcessor
from src.common.visualization import capture_image, capture_video, load_image, load_images

class LaunchOption(Enum):
    CAPTURE_VIDEO=0
    CAPTURE_IMAGE=1
    LOAD_IMAGE=2

class LauncherParameters:
    def __init__( self, 
                  img_loader_params:ImageLoaderParameters,
                  img_saver_params:ImageSaverParameters,
                  process_img_saver_params:ImageSaverParameters,
                  camera_index:Optional[int]=None,
                  option:LaunchOption = LaunchOption.CAPTURE_VIDEO,
                  show_img = False ):
        self.camera_index = camera_index
        self.img_loader_params = img_loader_params
        self.img_saver_params = img_saver_params
        self.process_img_saver_params = process_img_saver_params
        self.option = option
        self.show_img = show_img

class Launcher:
    def __init__( self, 
                 parameters:LauncherParameters, 
                 img_processor:ImageProcessor = DefaultImageProcessor(),
                 key_processor:Optional[KeysProcessor] = None ):
        self.parameters = parameters
        self.__img_loader = ImageLoader( parameters.img_loader_params )
        self.__img_saver = ImageSaver( parameters.img_saver_params )
        self.__process_img_saver = ImageSaver( parameters.process_img_saver_params )
        self.__img_processor = img_processor
        
        if ( key_processor ):
            self.__key_processor = key_processor
        else:
            self.__key_processor = DefaultKeysProcessor( parameters.img_saver_params, parameters.process_img_saver_params )

    def is_valid_parameters( self ):
        is_camera_index_valid = self.parameters.camera_index is not None and\
                                self.parameters.camera_index >= 0

        match self.parameters.option:
            case LaunchOption.CAPTURE_VIDEO:
                return is_camera_index_valid
            case LaunchOption.CAPTURE_IMAGE:
                return is_camera_index_valid and self.__img_saver.can_save()
            case LaunchOption.LOAD_IMAGE:
                return self.__img_loader.can_load()
        
        return False

    def launch( self ):
        if ( not self.is_valid_parameters() ):
            print( "Launch parameters invalid" )
            return None

        match self.parameters.option:
            case LaunchOption.CAPTURE_VIDEO:
                print( self.__key_processor.menu() )
                capture_video( 
                    self.parameters.camera_index,
                    self.__img_processor.process_img,
                    self.__key_processor.process_key )
            case LaunchOption.CAPTURE_IMAGE:
                print( self.__key_processor.menu() )
                capture_image(
                    self.parameters.camera_index,
                    self.__img_processor.process_img,
                    self.__key_processor.process_key  )
            case LaunchOption.LOAD_IMAGE:
                if ( self.parameters.show_img ):
                   print( self.__key_processor.menu() ) 

                if ( self.__img_loader.is_directory() ):
                    load_images(
                        self.__img_loader,
                        self.__process_img_saver,
                        self.__img_processor.process_img,
                        self.__key_processor.process_key,
                        self.parameters.show_img )
                else:
                    load_image(
                        self.__img_loader,
                        self.__process_img_saver,
                        self.__img_processor.process_img,
                        self.__key_processor.process_key,
                        self.parameters.show_img )