#!/usr/bin/python3

import cv2
import numpy as np
import os

from cv2.typing import MatLike
from typing import Callable, List, Optional

from src.common.file_utils import get_filename, get_files_by_extension, is_path_valid

def draw_contours(image:MatLike, contours: List[np.ndarray] ) -> MatLike:
    output = image.copy()

    for cnt in contours:
        cv2.drawContours(output, [cnt], -1, (0,255,0), 2)

    return output

def read( path:str ) -> MatLike | None:
    return cv2.imread( path )

def show_image(image:MatLike, title:str="Result"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def load_images( img_folder:str,
                 img_extension:str=".jpg",
                 process_img_folder:Optional[str] = None,
                 func:Optional[Callable[[MatLike], MatLike]] = None,
                 can_show_image:bool = False ):
    
    img_pathes = get_files_by_extension( img_folder, img_extension )
    
    for img_fpath in img_pathes:
        img_fname = get_filename( img_fpath )
        process_fpath = None
        if ( is_path_valid( process_img_folder ) ):
            process_fpath = os.path.join( process_img_folder, img_fname )
        load_image( img_fpath, process_fpath, func, can_show_image )


def load_image( img_path:str, 
                process_img_path:Optional[str] = None, 
                func:Optional[Callable[[MatLike], MatLike]] = None,
                can_show_image:bool = False ):
    img = read( img_path )

    if ( img is None ):
        return
    
    if ( func is not None ):
        processed = func( img )
        if ( process_img_path is not None ):
            cv2.imwrite(process_img_path, processed)
            if ( can_show_image ):
                show_image( processed )
        else:
            show_image( processed )

    else:
        show_image( img )
    
def capture_image( camera_index:int, 
                   full_img_path:str, 
                   process_img_path:Optional[str] = None,
                   func:Optional[Callable[[MatLike], MatLike]] = None ):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}.")
        exit()

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(full_img_path, frame)
        print(f"Image saved as {full_img_path}.")

        if ( func is not None ):
            processed = func( frame )
            if ( process_img_path is not None ):
                cv2.imwrite(process_img_path, processed)

            show_image( processed )

    cap.release()
    cv2.destroyAllWindows()

def capture_video( camera_index:int, 
                   process_img:Optional[Callable[[MatLike], MatLike]] = None,
                   process_key:Optional[Callable[[int, MatLike, Optional[MatLike]],None]] = None ):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}.")
        exit()

    while True:
        ret, frame = cap.read()
        img = None
        if ret:
            if ( process_img is not None ):
                img = process_img( frame )
            else:
                img = frame

            cv2.imshow( 'camera', img )

        else:
            print("Error: Could not capture frame.")

        key = cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key < 0:
            continue 
        elif process_key:
            process_key( key, frame, img )

    cap.release()
    cv2.destroyAllWindows()