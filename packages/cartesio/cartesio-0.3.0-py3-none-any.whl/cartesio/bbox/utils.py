from typing import Optional
from typing import Tuple

import numpy as np

__all__ = [
    "ltrb_to_xywh",
    "xywh_to_ltrb",
    "random",
]


def ltrb_to_xywh(
    ltrb: np.ndarray,
) -> np.ndarray:

    w = ltrb[:, 2] - ltrb[:, 0]
    h = ltrb[:, 3] - ltrb[:, 1]

    return np.hstack(
        (
            np.expand_dims(ltrb[:, 0] + w * 0.5, axis=1),
            np.expand_dims(ltrb[:, 1] + h * 0.5, axis=1),
            np.expand_dims(w, axis=1),
            np.expand_dims(h, axis=1),
        )
    )


def xywh_to_ltrb(
    xywh: np.ndarray,
) -> np.ndarray:

    return np.hstack(
        (
            np.expand_dims(xywh[:, 0] - xywh[:, 2] * 0.5, axis=1),
            np.expand_dims(xywh[:, 1] - xywh[:, 3] * 0.5, axis=1),
            np.expand_dims(xywh[:, 0] + xywh[:, 2] * 0.5, axis=1),
            np.expand_dims(xywh[:, 1] + xywh[:, 3] * 0.5, axis=1),
        )
    )


def random(
    n: int,
    cx_range: Optional[Tuple[int, int]] = (0.0, 1000.0),
    cy_range: Optional[Tuple[int, int]] = (0.0, 1000.0),
    w_range: Optional[Tuple[int, int]] = (0.0, 1000.0),
    h_range: Optional[Tuple[int, int]] = (0.0, 1000.0),
) -> np.ndarray:
    assert len(cx_range) == 2
    assert cx_range[0] < cx_range[1]
    assert len(cy_range) == 2
    assert cy_range[0] < cy_range[1]
    assert len(w_range) == 2
    assert w_range[0] < w_range[1]
    assert len(h_range) == 2
    assert h_range[0] < h_range[1]

    w_range = (max(w_range[0], 1), w_range[1])
    h_range = (max(h_range[0], 1), h_range[1])

    cx = np.random.randint(low=cx_range[0], size=n, high=cx_range[1]).astype(np.float32)
    cy = np.random.randint(low=cy_range[0], size=n, high=cy_range[1]).astype(np.float32)
    w = np.random.randint(low=w_range[0], size=n, high=w_range[1]).astype(np.float32)
    h = np.random.randint(low=h_range[0], size=n, high=h_range[1]).astype(np.float32)

    ltrb = xywh_to_ltrb(
        np.hstack(
            (
                np.expand_dims(cx, axis=1),
                np.expand_dims(cy, axis=1),
                np.expand_dims(w, axis=1),
                np.expand_dims(h, axis=1),
            )
        )
    )

    ltrb[:, 0] = np.minimum(
        np.maximum(ltrb[:, 0], np.array([cx_range[0]] * len(ltrb))),
        np.array([cx_range[1]] * len(ltrb)) - 1,
    )
    ltrb[:, 1] = np.minimum(
        np.maximum(ltrb[:, 1], np.array([cy_range[0]] * len(ltrb))),
        np.array([cy_range[1]] * len(ltrb)) - 1,
    )
    ltrb[:, 2] = np.minimum(
        np.maximum(ltrb[:, 2], np.array([cx_range[0]] * len(ltrb)) + 1),
        np.array([cx_range[1]] * len(ltrb)),
    )
    ltrb[:, 3] = np.minimum(
        np.maximum(ltrb[:, 3], np.array([cy_range[0]] * len(ltrb)) + 1),
        np.array([cy_range[1]] * len(ltrb)),
    )

    return ltrb
