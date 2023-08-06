import numpy as np
import iris
from iris.exceptions import ConstraintMismatchError
from numba import vectorize, float32 # noqa


class Nemo():

    def __init__(self, mesh_file, regions_file, default_cell_point='T'):
        self.mesh_file = mesh_file
        self.regions_file = regions_file
        self.default_cell_point = default_cell_point

    def get_areacello(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        e1 = self.get_i_length(cell_point, dtype)
        e2 = self.get_j_length(cell_point, dtype)
        return _get_area(e1, e2)

    def get_volcello(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        e1 = self.get_i_length(cell_point, dtype)
        e2 = self.get_j_length(cell_point, dtype)
        e3 = self.get_k_length(cell_point, dtype)
        return _get_volume(e1, e2, e3)

    def get_i_length(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        try:
            return self.get_mesh_var('e1' + cell_point.lower(), dtype)
        except ConstraintMismatchError:
            return self.get_mesh_var('e1' + cell_point.lower() + '_0', dtype)

    def get_j_length(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        try:
            return self.get_mesh_var('e2' + cell_point.lower(), dtype)
        except ConstraintMismatchError:
            return self.get_mesh_var('e2' + cell_point.lower() + '_0', dtype)

    def get_k_length(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        return self.get_mesh_var('e3' + cell_point.lower() + '_0', dtype)

    def get_depth(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        return self.get_mesh_var('gdep' + cell_point.lower() + '_0', dtype)

    def get_landsea_mask(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        return self.get_mesh_var(cell_point.lower() + 'mask', dtype)

    def get_grid_latitude(self, cell_point=None, dtype=np.float32):
        if cell_point is None:
            cell_point = self.default_cell_point
        return self.get_mesh_var('gphi' + cell_point.lower(), dtype)

    def get_mesh_var(self, var, dtype):
        return iris.load_cube(self.mesh_file, var).data.astype(dtype)

    def get_region_mask(self, min_lat, max_lat, min_lon, max_lon,
                        dtype=np.float32):
        try:
            lat = self.get_mesh_var('nav_lat', dtype)
            lon = self.get_mesh_var('nav_lon', dtype)
        except iris.exceptions.ConstraintMismatchError:
            lat = self.get_mesh_var('latitude', dtype)
            lon = self.get_mesh_var('latitude', dtype)
        mask = (_generate_mask(min_lat, max_lat, lat)
                * _generate_mask(min_lon, max_lon, lon))
        return mask


@vectorize(['float32(float32, float32)'], target='cpu')
def _get_area(e1, e2):
    """Vectorized numba function executed on the cpu that computes the area
    for each basin:

    Parameters
    ----------
    e1 : float32
        Masked array containing variable e1.
    e2 : float32
        Masked array containing variable e2.
    Returns
    -------
    e1*e2 : float32
        Masked array containing the area for the whole grid.
    """
    return e1*e2


@vectorize(['float32(float32, float32, float32)'], target='cpu')
def _get_volume(e1, e2, e3):
    """Vectorized numba function executed on the cpu that computes the area
    for each basin:

    Parameters
    ----------
    e1t : float32
        Masked array containing variable e1t.
    e2t : float32
        Masked array containing variable e2t.
    Returns
    -------
    e1*e2*e3 : float32
        Masked array containing the volume for the whole grid.
    """
    return e1 * e2 * e3


@vectorize(['float32(float32, float32, float32)'], nopython=True)
def _generate_mask(min, max, data):
    if data < min:
        return 0
    if data > max:
        return 0
    return 1
