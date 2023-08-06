from typing import Tuple

import numpy as np
import perfplot

try:
    import cartesio as cs
except ImportError:
    import os
    import sys

    sys.path.insert(
        0, os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )

    import cartesio as cs


# noinspection PyUnresolvedReferences
def run_perf_iou():
    np.random.seed(0)

    n_range = [2 ** k for k in range(10)]

    def setup(n: int) -> Tuple[np.ndarray, np.ndarray]:
        bbs_0 = cs.bbox.utils.random(n)
        bbs_1 = cs.bbox.utils.random(n)
        return bbs_0, bbs_1

    perfplot.show(
        setup=setup,
        kernels=[
            lambda a: cs.bbox.iou(a[0], a[1]),
            lambda a: cs.bbox.iou.py_func(a[0], a[1]),
        ],
        labels=[
            "iou",
            "iou_pyfunc",
        ],
        n_range=n_range,
        xlabel="#bbs",
        logx=True,
        logy=True,
        title="IOU performance",
        equality_check=np.allclose,
        time_unit="ms",
    )


if __name__ == "__main__":
    run_perf_iou()
