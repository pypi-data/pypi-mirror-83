"""Module containing helper functions for IOU computations
"""
import numpy as np

from ..core import jitted

__all__ = [
    "_intersection_bb_size",
]


@jitted
def _intersection_bb_size(
    bb_0: np.ndarray,
    bb_1: np.ndarray,
) -> np.ndarray:
    """Computes the size of the intersection between two bboxes

    :param bb_0: 1-dimensional np.ndarray of shape (4,) representing the first bbox
    :param bb_1: 1-dimensional np.ndarray of shape (4,) representing the second bbox
    :return: 1-dimensional np.ndarray of shape (2,) representing the [width, height] of the
    intersection between bb_0 and bb_1
    """

    left = max(bb_0[0], bb_1[0])
    right = min(bb_0[2], bb_1[2])

    width = max(0, right - left)

    top = max(bb_0[1], bb_1[1])
    bottom = min(bb_0[3], bb_1[3])

    height = max(0, bottom - top)

    return np.array([width, height])
