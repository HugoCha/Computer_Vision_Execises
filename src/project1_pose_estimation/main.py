#!/usr/bin/python3
import os

from cv2.typing import MatLike
from src.common.utils import *
from src.common.visualization import *
from .config import *

object_poses:List[object_pose] = []

def remove_shadow(image:MatLike) -> MatLike:
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    # Apply CLAHE to the L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(20, 20))
    l = clahe.apply(l)

    # Merge back
    lab = cv2.merge((l, a, b))
    result = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return result

def process( img:MatLike ) -> MatLike:
    gray = grayscale( img )
    blur = cv2.GaussianBlur(gray,(7,7),0)
    th = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,21,4 )
    kernel = np.ones((5,5), np.uint8)
    morphology = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=1)
    kernel = np.ones((7,7), np.uint8)
    morphology = cv2.morphologyEx(morphology, cv2.MORPH_ERODE, kernel, iterations=2)

    contours, _ = cv2.findContours(morphology, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        if not is_valid_contour(cnt):
            continue

        x,y,w,h = cv2.boundingRect(cnt)
        local_img = img[y:y+h, x:x+w]
        local_gray = th[y:y+h, x:x+w]
        local_th = otsu( local_gray )
        kernel = np.ones((3,3), np.uint8)
        local_morpho = cv2.morphologyEx( local_th, cv2.MORPH_ERODE, kernel )
        
        local_cnts, _ = cv2.findContours(255-local_morpho, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        local_cnts = sorted( local_cnts, key=lambda x: cv2.contourArea(x), reverse=True )
        if ( len(local_cnts) <= 0 ):
            continue
        
        hull = cv2.convexHull(local_cnts[0])

        cv2.drawContours(
            local_img,
            [hull],
            -1,
            (0, 255, 0),
            2
        )

        rect = cv2.minAreaRect(hull)
        box = cv2.boxPoints(rect)
        box = box.astype(np.int32).reshape(4, 1, 2)

        cv2.drawContours(
            local_img,
            [box],
            0,
            (255, 255, 0),
            2
        )

        circularity = compute_circularity(hull)

        if circularity > 0.80:
            M = cv2.moments(hull)

            if M["m00"] == 0:
                continue

            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            center = (cX, cY)
            cv2.circle(
                local_img,
                center,
                5,
                (255, 0, 0),
                -1
            )

            object_poses.append( object_pose( center ) )
        else:
            result = get_orientation(hull)

            if result is None:
                continue

            pose = result
            object_poses.append( pose )

            cv2.circle(
                local_img,
                pose.center,
                5,
                (255, 0, 0),
                -1
            )

            if pose.axis is not None:
                axis_length = 80
                axis_x, axis_y = pose.axis
                end_point = (
                    int(pose.center[0] + axis_length * float(axis_x)),
                    int(pose.center[1] + axis_length * float(axis_y))
                )

                cv2.line(
                    local_img,
                    pose.center,
                    end_point,
                    (0, 0, 255),
                    2
                )

    process = img

    return process

def main():
    img_raw_path = os.path.join( DATA_RAW_PATH, "img" + str(IMAGE_INDEX) + ".jpg" )
    processed_path = os.path.join( DATA_PROCESSED_PATH, "img" + str(IMAGE_INDEX) + ".jpg" )

    #capture_video( CAMERA_INDEX, process )
    capture_image( CAMERA_INDEX, img_raw_path, processed_path, process )
    #load_image( img_raw_path, processed_path, process )
    for obj in object_poses:
        print( obj )

if ( __name__ == "__main__" ):
    main()