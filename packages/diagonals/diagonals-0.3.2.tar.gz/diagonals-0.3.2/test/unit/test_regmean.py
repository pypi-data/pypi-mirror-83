import unittest

import numpy as np
import diagonals.regmean as regmean


class TestRegmeanLevels(unittest.TestCase):

    def setUp(self):
        self.data = np.ones((2, 2, 2, 2))
        self.basins = {
            'basin1': np.ones((2, 2, 2), dtype=np.float32),
            'basin2': np.ones((2, 2, 2), dtype=np.float32)
        }
        self.volume = np.ones((2, 2, 2), dtype=np.float32)

    def test_basic(self):
        mean = regmean.compute_regmean_levels(
            self.data, self.basins, self.volume)
        expected = {
            'basin1': np.ones((2, 2), dtype=np.float32),
            'basin2': np.ones((2, 2), dtype=np.float32)
        }
        for key in expected:
            np.testing.assert_equal(expected[key], mean[key])

    def test_basin_with_nans(self):
        self.data[:, 1, ...] = 2
        self.basins['basin1'][0, 0] = float('nan')

        mean = regmean.compute_regmean_levels(
            self.data, self.basins, self.volume)
        expected = {
            'basin1': np.ones((2, 2), dtype=np.float32),
            'basin2': np.ones((2, 2), dtype=np.float32)
        }
        expected['basin1'][:, 1] = 2
        expected['basin2'][:, 1] = 2
        for key in expected:
            np.testing.assert_equal(expected[key], mean[key])

    def test_basin_with_zeros(self):
        self.data[:, 1, ...] = 2
        self.basins['basin1'][0, 0] = 0.

        mean = regmean.compute_regmean_levels(
            self.data, self.basins, self.volume)
        expected = {
            'basin1': np.ones((2, 2), dtype=np.float32),
            'basin2': np.ones((2, 2), dtype=np.float32)
        }
        expected['basin1'][:, 1] = 2
        expected['basin2'][:, 1] = 2
        for key in expected:
            np.testing.assert_equal(expected[key], mean[key])

    def test_data_with_nans(self):
        self.data[:, 1, ...] = 2
        self.data[:, 1, 0, 0] = float('nan')

        mean = regmean.compute_regmean_levels(
            self.data, self.basins, self.volume)
        expected = {
            'basin1': np.ones((2, 2), dtype=np.float32),
            'basin2': np.ones((2, 2), dtype=np.float32)
        }
        expected['basin1'][:, 1] = float('nan')
        expected['basin2'][:, 1] = float('nan')
        for key in expected:
            np.testing.assert_equal(expected[key], mean[key])

    def test_data_masked(self):
        self.data[:, 1, ...] = 2
        self.data = np.ma.masked_array(
            self.data, mask=np.zeros(self.data.shape))
        self.data.mask[:, 1, 0, 0] = True

        mean = regmean.compute_regmean_levels(
            self.data, self.basins, self.volume)
        expected = {
            'basin1': np.ones((2, 2), dtype=np.float32),
            'basin2': np.ones((2, 2), dtype=np.float32)
        }
        expected['basin1'][:, 1] = 2
        expected['basin2'][:, 1] = 2
        for key in expected:
            np.testing.assert_equal(expected[key], mean[key])


if __name__ == "__main__":
    unittest.main()
