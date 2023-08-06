"""Tests for `cartesio.bbox` subpackage and modules."""
import numpy as np

import cartesio as cs
from .utils import TestCase


class TestCartesioBBox(TestCase):
    """Tests for `cartesio.bbox` subpackage and modules."""

    def test_utils(self):

        ltrb = np.array([[0, 1, 2, 3]])
        xywh = cs.bbox.utils.ltrb_to_xywh(ltrb)

        self.assertArrayEqual(xywh, np.array([[1, 2, 2, 2]]), type_strict=False)

        xywh = np.array([[0, 1, 2, 3]])
        ltrb = cs.bbox.utils.xywh_to_ltrb(xywh)

        self.assertArrayEqual(ltrb, np.array([[-1, -0.5, 1, 2.5]]), type_strict=False)
        n = 42
        cx_range = (0, 20)
        cy_range = (100, 200)
        w_range = (4, 5)
        h_range = (10, 20)

        random_ltrb = cs.bbox.utils.random(
            n=n,
            cx_range=cx_range,
            cy_range=cy_range,
            w_range=w_range,
            h_range=h_range,
        )
        self.assertTupleEqual(random_ltrb.shape, (n, 4))

        random_xywh = cs.bbox.utils.ltrb_to_xywh(random_ltrb)
        for xywh in random_xywh:
            self.assertGreaterEqual(xywh[0], cx_range[0])
            self.assertLessEqual(xywh[0], cx_range[1])

            self.assertGreaterEqual(xywh[1], cy_range[0])
            self.assertLessEqual(xywh[1], cy_range[1])

            self.assertGreaterEqual(xywh[2], w_range[0] / 2)  # Due to padding for x
            self.assertLessEqual(xywh[2], w_range[1])

            self.assertGreaterEqual(xywh[3], h_range[0] / 2)  # Due to padding for y
            self.assertLessEqual(xywh[3], h_range[1])

    def test_area(self):
        bb = np.array([0, 0, 0, 0])
        self.assertEqual(cs.bbox.area(bb), 0)

        bb = np.array([0, 0, 0, 1])
        self.assertEqual(cs.bbox.area(bb), 0)

        bb = np.array([0, 0, 1, 0])
        self.assertEqual(cs.bbox.area(bb), 0)

        bb = np.array([0, 0, 1, 1])
        self.assertEqual(cs.bbox.area(bb), 1)

        bb = np.array([1, 1, 2, 2])
        self.assertEqual(cs.bbox.area(bb), 1)

        bb = np.array([1.5, 1.5, 2.0, 3.5])
        self.assertEqual(cs.bbox.area(bb), 1)

    def test_iou_single(self):
        bb_0 = np.array([0, 0, 1, 1])
        bb_1 = np.array([0, 0, 1, 1])
        self.assertEqual(cs.bbox.iou_single(bb_0, bb_1), 1)

        bb_0 = np.array([0, 0, 1, 1])
        bb_1 = np.array([0, 0, 2, 2])
        self.assertEqual(cs.bbox.iou_single(bb_0, bb_1), 1 / 4)

        bb_0 = np.array([1, 1, 2, 2])
        bb_1 = np.array([0, 0, 2, 2])
        self.assertEqual(cs.bbox.iou_single(bb_0, bb_1), 1 / 4)

        bb_0 = np.array([1.5, 1.5, 2.5, 2.5])
        bb_1 = np.array([0, 0, 2, 2])
        self.assertEqual(cs.bbox.iou_single(bb_0, bb_1), 0.5 ** 2 / (5 - 0.5 ** 2))

    def test_iou(self):
        bbs_0 = np.array([[0, 0, 1, 1]])
        bbs_1 = np.array([[0, 0, 1, 1]])

        ious = cs.bbox.iou(bbs_0, bbs_1)
        self.assertArrayEqual(
            ious, np.array([[1.0]], dtype=np.float32), type_strict=True
        )

        bbs_0 = np.array([[0, 0, 1, 1], [0, 0, 2, 2]])
        bbs_1 = np.array([[0, 0, 1, 1], [0, 0, 2, 2]])

        ious = cs.bbox.iou(bbs_0, bbs_1)
        self.assertArrayEqual(
            ious,
            np.array(
                [
                    [1.0, 0.25],
                    [0.25, 1.0],
                ],
                dtype=np.float32,
            ),
            type_strict=True,
        )

        bbs_0 = np.array([[0, 0, 1, 1], [0, 0, 2, 2]])
        bbs_1 = np.array([[0, 0, 1, 2]])

        ious = cs.bbox.iou(bbs_0, bbs_1)
        self.assertArrayEqual(
            ious,
            np.array(
                [
                    [0.5],
                    [0.5],
                ],
                dtype=np.float32,
            ),
            type_strict=True,
        )

    def test_nms(self):
        bbs = np.array(
            [
                [0, 0, 100, 100],
                [0, 0, 90, 90],
            ]
        )
        iou = cs.bbox.iou_single(bbs[0], bbs[1])
        keep = cs.bbox.nms(bbs, thresh=iou - 0.0001)
        self.assertArrayEqual(keep, np.array([0], dtype=np.int32), type_strict=True)

        keep = cs.bbox.nms(bbs, thresh=iou + 0.0001)
        self.assertArrayEqual(
            keep,
            np.array(
                [0, 1],
                dtype=np.int32,
            ),
            type_strict=True,
        )

    def test_nms_with_score(self):
        bbs = np.array(
            [
                [0, 0, 100, 100, 10],
                [0, 0, 90, 90, 20],
            ]
        )
        iou = cs.bbox.iou_single(bbs[0, :4], bbs[1, :4])
        keep = cs.bbox.nms(bbs, thresh=iou - 0.0001)
        self.assertArrayEqual(keep, np.array([1], dtype=np.int32), type_strict=True)

        keep = cs.bbox.nms(bbs, thresh=iou + 0.0001)
        self.assertArrayEqual(
            keep,
            np.array(
                [1, 0],
                dtype=np.int32,
            ),
            type_strict=True,
        )

    def test_nms_longer(self):
        bbs = np.array(
            [
                [0, 0, 100, 100],
                [0, 0, 90, 90],
                [50, 50, 200, 200],
                [0, 0, 110, 110],
            ]
        )

        keep = cs.bbox.nms(bbs, thresh=0.35)
        self.assertArrayEqual(
            keep,
            np.array(
                [0, 2],
                dtype=np.int32,
            ),
            type_strict=True,
        )
