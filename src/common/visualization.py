#!/usr/bin/python3

import cv2
import numpy as np
from typing import Callable, List, Optional
from cv2.typing import MatLike

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

def load_image( full_img_path:str, 
                process_img_path:Optional[str] = None, 
                func:Optional[Callable[[MatLike], MatLike]] = None ):
    img = read( full_img_path )

    if ( img is None ):
        return
    
    if ( func is not None ):
        processed = func( img )
        if ( process_img_path is not None ):
            cv2.imwrite(process_img_path, processed)
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

def capture_video( camera_index:int, func:Optional[Callable[[MatLike], MatLike]] = None ):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"Error: Could not open camera {camera_index}.")
        exit()

    while True:
        ret, frame = cap.read()
        if ret:
            if ( func is not None ):
                img = func( frame )
            else:
                img = frame

            cv2.imshow( 'camera', img )

        else:
            print("Error: Could not capture frame.")

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()