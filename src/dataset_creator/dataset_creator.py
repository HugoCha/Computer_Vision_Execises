#!/usr/bin/python3

from cv2.typing import MatLike

from common.processors import KeyProcessor
from src.common.image_saver import ImageSaver, ImageSaverParameters
from src.common.launcher import LauncherParameters, Launcher
from src.camera.config import CAMERA_INDEX
from src.common.processors import ImageProcessor, KeysProcessor

from .config import *

class DatasetCreator( ImageProcessor, KeysProcessor ):
    def __init__( self, 
                  dataset_dpath:str,
                  categories:dict[int,str] ):
        self.img_savers:list[ImageSaver]
        self.__sub_menus = {}

    def title( self ) -> str:
        return "Dataset creator"
    
    def sub_menus(self) -> dict[str, KeyProcessor]:
        return self.__sub_menus

    def process_img(self, img: MatLike ) -> MatLike:
        return img

def main():
    img_loader_params = None
    if ( IMAGE_LOAD_PATH is not None ):
        img_loader_params = ImageLoaderParameters.from_filepath( IMAGE_LOAD_PATH )
    if ( img_loader_params is None or not img_loader_params.is_valid() ):
        img_loader_params = ImageLoaderParameters( DATA_RAW_PATH, IMAGE_EXTENSION, None )

    img_saver_params = ImageSaverParameters( DATA_RAW_PATH, IMAGE_BASE_NAME, IMAGE_EXTENSION, CAN_OVERRIDE )
    process_img_saver_params = ImageSaverParameters( DATA_PROCESSED_PATH, IMAGE_BASE_NAME, IMAGE_EXTENSION, CAN_OVERRIDE )
    
    processor = DatasetCreator( categories )
    
    launcher_params = LauncherParameters( 
        img_loader_params,
        img_saver_params,
        process_img_saver_params,
        CAMERA_INDEX, 
        LAUNCH_OPTION,
        True )
    
    launcher = Launcher( launcher_params, processor, processor )
    launcher.launch()

if __name__ == "__main__":
    main()