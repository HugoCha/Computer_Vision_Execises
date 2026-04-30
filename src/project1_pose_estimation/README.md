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
Axis: (10, 0)
```

Visual output should include:

 - contour
 - center point
 - orientation axis
 - rotated bounding box

## Result

<div style="display: flex; justify-content: space-around">
  <img src="/data/raw/project1/img0.jpg" alt="Raw Image" width="45%" />
  <img src="/data/processed/project1/img0.jpg" alt="Processed Image" width="45%" />
</div>
