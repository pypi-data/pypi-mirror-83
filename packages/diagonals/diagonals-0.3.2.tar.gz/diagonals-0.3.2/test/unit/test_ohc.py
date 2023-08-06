import unittest

import numpy as np
import diagonals.ohc as ohc


class TestOhc(unittest.TestCase):

    def test_weights(self):
        weights = ohc.get_weights(
            layers=((0, 2),),
            mask=np.ones((2, 2), dtype=np.float32),
            cell_height=np.array(((1., 2.), (4., 3.)), dtype=np.float32),
            cell_top_depth=np.array(((0., 0.), (1., 2.)), dtype=np.float32)
        )
        expected_result = 1020 * 4000 * np.array(((1., 2.), (1., 0.)))
        self.assertTrue(np.all(weights == expected_result))

    def test_weights_all_land(self):
        weights = ohc.get_weights(
            layers=((0, 2),),
            mask=np.zeros((2, 2), dtype=np.float32),
            cell_height=np.array(((1., 2.), (4., 3.)), dtype=np.float32),
            cell_top_depth=np.array(((0., 0.), (1., 2.)), dtype=np.float32)
        )
        self.assertTrue(np.all(np.isnan(weights)))

    def test_weights_mul_layers(self):
        weights = ohc.get_weights(
            layers=((0, 2), (2, 4)),
            mask=np.ones((2, 2), dtype=np.float32),
            cell_height=np.array(((1., 2.), (4., 3.)), dtype=np.float32),
            cell_top_depth=np.array(((0., 0.), (1., 2.)), dtype=np.float32)
        )
        print(weights)
        expected_result = 1020 * 4000 * np.array((
            ((1., 2.), (1., 0.)),
            ((0., 0.), (2., 2.))
        ))
        self.assertTrue(np.all(weights == expected_result))
