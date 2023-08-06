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
def run_perf_nms():
    np.random.seed(0)

    n_range = [2 ** k for k in range(10)]

    def setup(n: int) -> np.ndarray:
        bbs = cs.bbox.utils.random(n)
        return bbs

    perfplot.show(
        setup=setup,
        kernels=[
            lambda a: cs.bbox.nms(a, thresh=0.85),
            lambda a: cs.bbox.nms.py_func(a, thresh=0.85),
        ],
        labels=[
            "nms",
            "nms_pyfunc",
        ],
        n_range=n_range,
        xlabel="#bbs",
        logx=True,
        logy=True,
        title="NMS performance",
        equality_check=np.allclose,
        time_unit="ms",
    )


if __name__ == "__main__":
    run_perf_nms()
