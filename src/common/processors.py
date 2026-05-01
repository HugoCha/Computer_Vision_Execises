#!/usr/bin/python3

from typing import Callable, Optional

from abc import ABC, abstractmethod
from cv2.typing import MatLike

class ImageProcessor(ABC):
    @abstractmethod
    def process_img( self, img:MatLike ) -> MatLike:
        pass

class KeyProcessor:
    def __init__( self, key:str, description:str, func:Callable[[Optional[MatLike], Optional[MatLike]], None] ):
        self.key = key
        self.description = description
        self.func = func

class KeysProcessor(ABC):
    def process_key( self, key:int, img:MatLike, process:Optional[MatLike] ) -> None:
        if ( key < 0 ): return None
        if ( chr( key ) == 'h' ):
            print( self.menu() )
            return None

        if ( chr( key ) in self.sub_menus() ):
            self.sub_menus()[chr( key )].func( img, process )
        else:
            print( f"Unknown key: {chr(key)}" )

    @abstractmethod
    def title( self ) -> str:
        pass
    
    @abstractmethod
    def sub_menus( self ) -> dict[str,KeyProcessor]:
        pass

    def quit_menu( self ) -> str:
        return "Quit"

    def menu( self ) -> str:
        menu = []
        menu.append( f"================================\n" )
        menu.append( f"{self.title()} menu:\n" )
        menu.append( f"================================\n" )
        menu.append( f"'h': Display menu\n" )

        sub_menus = self.sub_menus()
        if sub_menus is not None:
            for key in sub_menus:
                menu.append( f"'{key}' : {sub_menus[key].description}\n")
        menu.append( f"'q': {self.quit_menu()}\n" )
        return "".join( menu )

class DefaultImageProcessor(ImageProcessor):
    def process_img( self, img:MatLike ) -> MatLike:
        return img
    
class DefaultKeysProcessor(KeysProcessor):
    def process_key( self, key:int, img:MatLike, process:Optional[MatLike] ) -> None:
        return None

    def title( self ) -> str:
        return "Default menu"
    
    def sub_menus(self) -> dict[str, KeyProcessor]:
        return {}