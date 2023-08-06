import numpy as np

from ._iou_helper import _intersection_bb_size
from ._nms_helper import _nms_order
from .area import areas
from ..core import jitted

__all__ = [
    "nms",
]


@jitted
def _nms_v1(
    bbs: np.ndarray,
    thresh: float,
) -> np.ndarray:
    """Computes Non Maxima Suppression indices on the bboxes passed as argument

    :param bbs: 2-dimensional np.ndarray of shape (N,C), where C in (4, 5),
    each row [l, t, r, b, (score)]
    :param thresh: threshold used to determine whether one of two two bboxes needs to be suppressed
    :return:1-dimensional np.ndarray of shape (M,) of indices in bboxs to retain
    """

    N = len(bbs)
    order = _nms_order(bbs)
    areas_ = areas(bbs)

    suppressed = np.zeros(shape=(N,), dtype=np.bool_)

    keep = []
    for _i in range(N):
        i = order[_i]
        if suppressed[i]:
            continue
        keep.append(i)

        i_bb = bbs[i]
        i_area = areas_[i]

        for _j in range(_i + 1, N):
            j = order[_j]
            if suppressed[j] > 0:
                continue

            j_bb = bbs[j]
            j_area = areas_[j]

            ij_bb_size = _intersection_bb_size(i_bb, j_bb)
            w, h = ij_bb_size[0], ij_bb_size[1]
            ij_area = w * h

            ovr = ij_area / (i_area + j_area - ij_area)
            if ovr >= thresh:
                suppressed[j] = 1

    return np.array(keep, dtype=np.int32)


nms = _nms_v1
