import numpy as np

from ..core import jitted

__all__ = [
    "_nms_order",
]


@jitted
def _nms_order(
    bbs: np.ndarray,
) -> np.ndarray:
    N, C = bbs.shape
    if C > 4:
        scores = bbs[:, 4]
        order = scores.argsort()[::-1]
    else:
        order = np.arange(N)
    return order
