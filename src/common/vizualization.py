#!/usr/bin/python3

import cv2

def draw_contours(image, contours):
    output = image.copy()

    for cnt in contours:
        cv2.drawContours(output, [cnt], -1, (0,255,0), 2)

    return output


def show_image(image, title="Result"):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()