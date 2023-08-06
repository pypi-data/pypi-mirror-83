import unittest
from typing import Optional

import numpy as np

__all__ = [
    "TestCase",
]


class TestCase(unittest.TestCase):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.addTypeEqualityFunc(np.ndarray, self.assertArrayEqual)

    def _check_array_shape(
        self,
        array1: np.ndarray,
        array2: np.ndarray,
        msg: Optional[str],
    ):
        try:
            s1 = array1.shape
        except AttributeError:
            message = "fist argument does not have 'shape' attribute"
            self.fail(self._formatMessage(msg, message))
        try:
            s2 = array2.shape
        except AttributeError:
            message = "second argument does not have 'shape' attribute"
            self.fail(self._formatMessage(msg, message))

        try:
            self.assertTupleEqual(s1, s2)
        except self.failureException:
            message = (
                "array shape mismatch: first array has shape: {},"
                " second array has shape {}".format(s1, s2)
            )
            self.fail(self._formatMessage(msg, message))

    def _check_array_dtype(
        self,
        array1: np.ndarray,
        array2: np.ndarray,
        msg: Optional[str],
    ):
        t1 = array1.dtype
        t2 = array2.dtype

        if t1 != t2:
            message = "array1 dtype ({}) is different from array2 dtype ({})".format(
                t1, t2
            )
            self.fail(self._formatMessage(msg, message))

    def assertArrayEqual(
        self,
        array1: np.ndarray,
        array2: np.ndarray,
        type_strict: Optional[bool] = False,
        msg: Optional[str] = None,
    ):
        """A np.ndarray-specific equality assertion

        :param array1: first np.ndarray to be checked
        :param array2: second np.ndarray to be checked
        :param type_strict: optional flag specifying whether to fail on type difference
        :param msg: optional message to use on failure instead of a list of differences
        """

        self._check_array_shape(array1, array2, msg)
        if type_strict:
            self._check_array_dtype(array1, array2, msg)

        try:
            np.testing.assert_array_equal(array1, array2)
        except AssertionError as e:
            message = str(e)
            self.fail(self._formatMessage(msg, message))
        else:
            return
