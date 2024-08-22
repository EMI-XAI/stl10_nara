# Non-strict Attentional Region Annotation for STL-10 Dataset

<img src="blend_00000.png" width="192" height="192"
 alt="Example of blended image">

This repository provides non-strict attentional region annotations
(NARA) for [STL-10](https://cs.stanford.edu/~acoates/stl10/) dataset.
- NARA is a rough region annotaion where humans focus maximum
  attention while judging the category of each image.
  It can be annotated with less workload than strict region
  annotation such as bouding boxes and region contours.
- NARA improves classification accuracy of a Convolutional Neural
  Network (CNN) as additional human knowledge other than labels.

We collected three annotaions per image for train and test images
of STL-10 dataset. These annotations are done by non-expert
annotators in Amazon MTurk.

More details are described in our publication below:

> Satoshi Arai, Shinichi Shirakawa, and Tomoharu Nagao,
> "Non-strict Attentional Region Annotation to Improve Image
> Classification Accuracy," IEEE SMC 2021.

## stl10_nara.csv

This file contains a list of annotation results that consists of
geometry information of attentional regions.

Original [STL-10](https://cs.stanford.edu/~acoates/stl10/) images
are NOT included.

Each column means below:

| Column Name | Content |
|:-|:-|
| Split | train or test. |
| Image | Image filename. |
| CategoryGT | Image category provided by original STL-10 dataset. |
| Category | Image category collected with NARA. |
| CenterX, CenterY | Center position of ellipse. |
| RadiusX, RadiusY | Radius of ellipse. |
| Angle | Rotation of ellipse in radian. |
| WorkTime | Working time for each image including both category annotation and region annotation. |

## draw_annotation_maps.py

This file converts geometry information of annotations to 2D
annotation maps.

```
python draw_annotation_maps.py
```

Output maps are like below:

<img src="map_00000.png" width="192" height="192"
 alt="Example of annotation map">

Details are printed with `--help` option.

## Acknowledgements

This result is based on results obtained from a project,
JPNP20001221-0, commissioned by the New Energy and Industrial
Technology Development Organization (NEDO).
