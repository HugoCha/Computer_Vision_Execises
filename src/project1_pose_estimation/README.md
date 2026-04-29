# Project 1 — Object Pose Estimation for Pick-and-Place

## Statement

A robot must pick flat mechanical parts placed randomly on a table.

The objective is to detect for each part:

 - center position (x, y)
 - orientation angle θ
 - grasp point
 - invalid or overlapping detections

The output should be directly usable by a robotic arm for pick-and-place operations.

## Deliverable

For each detected object:

```bash
Object 1
Center: (320, 180)
Angle: 42°
Grasp point: (318, 176)
```

Visual output should include:

 - contour
 - center point
 - orientation axis
 - grasp direction
 - rotated bounding box