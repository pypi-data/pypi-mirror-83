"""Module implementing functions to compute the IOU between bounding boxes
"""
import numpy as np

from ._iou_helper import _intersection_bb_size
from .area import area
from ..core import jitted

__all__ = [
    "iou_single",
    "iou",
]


@jitted
def _iou_single_v1(
    bb_0: np.ndarray,
    bb_1: np.ndarray,
) -> float:
    """Computes the IOU between the two bboxes passed as argument

    The computation of the iou is performed by computing the size of the intersecting bbox
    and by computing the ratio between the resulting area and the sum of the individual areas
    subtracted the intersection area.

    :param bb_0: 1-dimensional np.ndarray of shape (4,) representing the first bbox
    :param bb_1: 1-dimensional np.ndarray of shape (4,) representing the second bbox
    :return: The intersection of union (IOU) between the two bounding bb_1 passed as argument
    """

    # Compute the coordinates of the intersecting rectangle
    in_size = _intersection_bb_size(bb_0, bb_1)
    w_in, h_in = in_size[0], in_size[1]
    intersection_area = w_in * h_in

    # Compute the areas of the individual bboxes
    area_0 = area(bb_0)
    area_1 = area(bb_1)

    return intersection_area / (area_0 + area_1 - intersection_area)


@jitted
def _iou_v1(
    bbs_0: np.ndarray,
    bbs_1: np.ndarray,
) -> np.ndarray:
    """Computes the iou between the bbs in bbs_0 abd bbs_1

    :param bbs_0: 2-dimensional np.ndarray of shape (N, 4) representing the first set of bboxes
    :param bbs_1: 2-dimensional np.ndarray of shape (M, 4) representing the second set of bboxes
    :return: 2-dimensional np.ndarray of shape (N, M), where the entry at [i, j] corresponds to the
    iou between bbs_0[i] and bbs_1[j]
    """
    N = bbs_0.shape[0]
    M = bbs_1.shape[0]
    ious = np.empty(shape=(N, M), dtype=np.float32)
    for i in range(N):
        bb_0_i = bbs_0[i]
        for j in range(M):
            bb_1_j = bbs_1[j]
            ious[i, j] = _iou_single_v1(bb_0_i, bb_1_j)
    return ious


iou_single = _iou_single_v1
iou = _iou_v1
