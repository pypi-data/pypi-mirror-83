"""This submodule contains implementations of functionalities related to bounding boxes.
A bounding box defined as follows:
  bbox = [left, top, right, bottom]
where:
 * left: represents the x-coordinate of the left side of the bbox
 * top: represents the y-coordinate of the top side of the bbox
 * right: represents the x-coordinate of the right side of the bbox
 * bottom: represents the y-coordinate of the bottom side of the bbox

A bounding box is represented as a 1-dimensional np.ndarray of shape (4,)
A collection of N bounding boxes can be represented as a 2-dimensional np.ndarray of shape (N,4)
"""

__all__ = [
    "utils",
    "area",
    "iou",
    "iou_single",
    "nms",
]

from . import utils
from .area import area
from .iou import iou
from .iou import iou_single
from .nms import nms
