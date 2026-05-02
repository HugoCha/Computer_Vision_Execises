#!/usr/bin/python3

from cv2.typing import MatLike

from src.common.launcher import Launcher, LauncherParameters
from src.common.object_pose2d import ObjectPose2d
from src.common.processors import ImageProcessor, KeyProcessor, KeysProcessor
from src.common.vision_utils import *
from src.common.visualization import *

from .config import *

class PoseEstimationProcessor( ImageProcessor, KeysProcessor ):
    def __init__( self ):
        self.object_poses:List[ObjectPose2d] = []
        self.sub_menus__: dict[str, KeyProcessor] = {
            'p': KeyProcessor( 'p', "Display obj poses", lambda img,process : self.print_poses() )
        }

    def process_img( self, img:MatLike ) -> MatLike:
        self.object_poses.clear()
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

                self.object_poses.append( ObjectPose2d( center, box ) )
            else:
                result = get_orientation(hull)

                if result is None:
                    continue
                
                center, angle, axis = result
                pose:ObjectPose2d = ObjectPose2d( center, box, angle, axis )
                self.object_poses.append( pose )

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
    
    def title( self ) -> str:
        return "Pose estimation"
    
    def sub_menus(self) -> dict[str, KeyProcessor]:
        return self.sub_menus__
    
    def print_poses( self ):
        for obj in self.object_poses:
            print( obj )

def main():
    processor = PoseEstimationProcessor()
    launcher_params = LauncherParameters( CAMERA_INDEX, IMAGE_PATH, IMAGE_EXTENSION, IMAGE_PROCESS_PATH, LAUNCH_OPTION )
    launcher = Launcher( launcher_params, processor, processor )
    launcher.launch()

if ( __name__ == "__main__" ):
    main()