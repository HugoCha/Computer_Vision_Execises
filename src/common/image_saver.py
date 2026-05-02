#!/usr/bin/python3

from posixpath import dirname
from typing import Optional

import cv2
import glob
import os
import re

from cv2.typing import MatLike

from src.common.file_utils import is_directory, is_valid_path, is_valid_filename, is_valid_image_extension

class ImageSaverParameters:
    def __init__( self, 
                img_fpath:str, 
                img_bname:str, 
                img_extension:str,
                can_override:bool = False ):
        self.img_fpath = img_fpath
        self.img_bname = img_bname
        self.img_extension = img_extension
        self.can_override = can_override

    def is_valid( self ):
        return is_valid_path( self.img_fpath ) and\
               is_valid_filename( self.img_bname ) and\
               is_valid_image_extension( self.img_extension )

    def get_dirpath( self ) -> Optional[str]:
        if not is_valid_path( self.img_fpath ):
            return None
        
        if is_directory( self.img_fpath ):
            return self.img_fpath
        
        return dirname( self.img_fpath )

    
    def get_filename( self, index:int ) -> Optional[str]:
        if ( not is_valid_filename( self.img_bname ) or
             not is_valid_image_extension( self.img_extension ) ):
            return None
        
        return f"{self.img_bname}{index}{self.img_extension}"
    
    def get_filepath( self, index:int ) -> Optional[str]:
        img_dpath = self.get_dirpath()
        img_fname = self.get_filename( index )
        
        if ( img_dpath is None or img_fname is None ):
            return None
        
        return os.path.join( img_dpath, img_fname )
    
    def get_extension( self ):
        if ( not is_valid_image_extension( self.img_extension ) ):
            return None
        return self.img_extension
    
class ImageSaver:
    def __init__( self, parameters:ImageSaverParameters ):
        self.__parameters = parameters
        self.__curr_idx = self._find_last_index( parameters )

    def get_dirpath( self ) -> Optional[str]:
        return self.__parameters.get_dirpath()

    def get_filename( self ) -> Optional[str]:
        return self.__parameters.get_filename( self.__curr_idx )

    def get_filepath( self ) -> Optional[str]:
        return self.__parameters.get_filepath( self.__curr_idx )

    def get_extension( self ) -> Optional[str]:
        return self.__parameters.get_extension()

    def can_save( self ) -> bool:
        return self.__parameters.is_valid() 

    def save( self, 
              img:MatLike ) -> bool:
        if ( not self.can_save() ):
            return False
        
        index:int
        if ( self.__parameters.can_override ):
            index = self.__curr_idx if self.__curr_idx >= 0 else 0
        else:
            index = self.__curr_idx + 1 if self.__curr_idx + 1 >= 0 else 0

        img_fpath = self.__parameters.get_filepath( index )
        if ( img_fpath is None ):
            return False
        
        cv2.imwrite( img_fpath, img )
        print( f"Image saved at {img_fpath}" )
        self.__curr_idx = index 
        return True

    @staticmethod
    def _find_last_index( parameters:ImageSaverParameters ) -> int:
        if ( not parameters.is_valid() ):
            return -1
        
        pattern = re.escape(parameters.img_bname) + r"(\d+)" + re.escape(parameters.img_extension)
        files = glob.glob(os.path.join(parameters.get_dirpath(), f"{parameters.img_bname}*{parameters.img_extension}"))

        max_index = -1
        for file in files:
            match = re.search(pattern, file)
            if match:
                index = int(match.group(1))
                if index > max_index:
                    max_index = index
        return max_index