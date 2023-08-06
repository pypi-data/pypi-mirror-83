"""Module implementing functions to compute the area of a bounding box
"""
import numpy as np

from ..core import jitted

__all__ = [
    "area",
    "areas",
]


@jitted
def area(
    bb: np.ndarray,
) -> float:
    """Computes the area of the bbox passed as argument
    :param bb: 1-dimensional np.ndarray of shape (4,) representing the bbox for which to compute
    the area
    :return: the area of the bbox passed as argument
    """

    width = bb[2] - bb[0]
    height = bb[3] - bb[1]

    return width * height


@jitted
def areas(
    bbs: np.ndarray,
) -> np.ndarray:
    """Computes the area of the bboxes passed as argument
    :param bbs: 2-dimensional np.ndarray of shape (N,4) representing the bboxes for which to
    compute the area.
    :return 1-dimensional np.ndarray of shape (N,) of areas
    """
    N = len(bbs)

    areas_ = np.empty(shape=(N,), dtype=np.float32)
    for i in range(N):
        bbox = bbs[i]
        areas_[i] = area(bbox)

    return areas_
