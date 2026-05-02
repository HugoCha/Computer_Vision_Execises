#!/usr/bin/python3

import cv2
import os

from cv2.typing import MatLike
from posixpath import dirname
from typing import Optional

from src.common.file_utils import get_files_by_extension, is_directory, is_valid_path, is_valid_filename, is_valid_image_extension

class ImageLoaderParameters:
    def __init__( self, 
                img_dpath:str, 
                img_extension:str,
                img_bname:Optional[str] = None ):
        self.img_dpath = img_dpath
        self.img_bname = img_bname
        self.img_extension = img_extension

    @classmethod
    def from_filepath( cls, img_fpath:str ):
        if ( not is_valid_path( img_fpath ) ):
            return None
        if ( is_directory( img_fpath ) ):
            return None

        img_fname = os.path.basename( img_fpath )
        img_bname, img_extension = os.path.splitext( img_fname )
        if ( not img_bname or not is_valid_image_extension( img_extension ) ):
            return None
        
        img_dname = dirname( img_fpath )
        return cls( img_dname, img_extension, img_bname )

    def is_directory( self ):
        return not self.img_bname

    def is_valid( self ):
        is_valid = is_valid_path( self.img_dpath )
        is_valid &= is_valid_image_extension( self.img_extension )
        return is_valid

    def can_load( self ):
        if not self.is_valid():
            return False
        
        if not self.img_bname:
            return os.path.exists( self.img_dpath )
        
        return os.path.exists( self.get_filepath() )

    def get_dirpath( self ) -> Optional[str]:
        if not is_valid_path( self.img_dpath ):
            return None
        return self.img_dpath

    def get_filename( self ) -> Optional[str]:
        if ( not self.img_bname or 
             not is_valid_filename( self.img_bname ) or
             not is_valid_image_extension( self.img_extension ) ):
            return None
        
        return f"{self.img_bname}{self.img_extension}"
    
    def get_filepath( self ) -> Optional[str]:
        img_dpath = self.get_dirpath()
        img_fname = self.get_filename()
        
        if ( img_dpath is None or img_fname is None ):
            return None
        
        return os.path.join( img_dpath, img_fname )
    
    def get_extension( self ):
        if ( not is_valid_image_extension( self.img_extension ) ):
            return None
        
        return self.img_extension
    
class ImageLoader:
    def __init__( self, parameters:ImageLoaderParameters ):
        self.__parameters = parameters

    def is_directory( self ):
        return self.__parameters.is_directory()

    def get_dirpath( self ) -> Optional[str]:
        return self.__parameters.get_dirpath()

    def get_filename( self ) -> Optional[str]:
        return self.__parameters.get_filename()

    def get_filepath( self ) -> Optional[str]:
        return self.__parameters.get_filepath()

    def get_extension( self ) -> Optional[str]:
        return self.__parameters.get_extension()

    def can_load( self ) -> bool:
        return self.__parameters.can_load()

    @classmethod
    def from_filepath( cls, img_fpath:str ):
        params = ImageLoaderParameters.from_filepath( img_fpath )
        
        if ( not params ):
            return None
        
        return cls( params )

    def load( self ) -> list[MatLike]:
        if ( not self.can_load() ):
            return []
        
        imgs:list[MatLike] = []

        if ( self.__parameters.is_directory() ):
            img_dpath = self.__parameters.get_dirpath()
            img_extension = self.__parameters.get_extension()
            fpathes = get_files_by_extension( img_dpath, img_extension )
            for fpath in fpathes:
                ret = cv2.imread( fpath )
                print( f"Image loaded from {fpath}" )
                if ret is not None:
                    imgs.append( ret )
        else:
            img_fpath = self.__parameters.get_filepath()
            ret = cv2.imread( img_fpath )
            if ret is not None:
                imgs.append( ret )
                print( f"Image loaded from {img_fpath}" )
        
        return imgs