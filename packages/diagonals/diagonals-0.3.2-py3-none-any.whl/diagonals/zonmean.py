import logging
import numpy as np

import numba
from numba import vectorize

import diagonals

logger = logging.getLogger(__name__)

__all__ = ['compute_zonmean', 'get_basin_area']


def compute_zonmean(var, lats, area):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    lats : float32
        Masked array containing latitude points.
    area : float32
        Masked array containing cell area.

    Returns
    -------
    zonmean: float32
        List containing zonal mean for variable var
    """
    if diagonals.CONFIG.use_gpu:
        logger.warning('GPU routines not implemented yet'
                       'for zonmean diagnostic due to a compiler bug.'
                       'Using CPU instead until bug gets fixed')

    zonmean = _compute_zonal_mean_cpu(var, lats, area)
    return zonmean


def _compute_zonal_mean_cpu(var, lats, area):
    """Function that calls computing functions in the CPU.

    Loops over time-steps and depth levels to compute the zonal mean:

    Parameters
    ----------
    var : float32
        Masked array containing variable to average.
    lats: float32
        Masked array containing latitude points.
    area: float32
        List of masked arrays containing the area for each basin.

    Returns
    -------
    value: float32
        List of masked arrays containing a variable's zonal mean for
        each depth level and timestep.
    """
    if len(var.shape) == 4:
        value = _compute_zonal_mean_cpu_3d(var, lats, area)
    else:
        value = _compute_zonal_mean_cpu_2d(var, lats, area)
    return value


def _compute_zonal_mean_cpu_3d(var, lats, area):
    times = var.shape[0]
    levs = var.shape[1]
    value = {}
    for basin, mask in area.items():
        weight = np.squeeze(area[basin])
        value[basin] = np.empty((times, levs, 180))
        for t in range(times):
            for lev in range(levs):
                value[basin][t][lev][:] = _zonal_mean_cpu(
                    var[t, lev, :, :], weight, lats
                )
    return value


def _compute_zonal_mean_cpu_2d(var, lats, area):
    times = var.shape[0]
    value = {}
    for basin, mask in area.items():
        weight = np.squeeze(area[basin])
        value[basin] = np.empty((times, 180))
        for t in range(times):
            value[basin][t, :] = _zonal_mean_cpu(
                var[t, :, :], weight, lats)
    return value


# def _compute_zonal_mean_gpu(var, latitudes, area):
#    times = var.shape[0]
#    levs = var.shape[1]
#    lats = var.shape[2]
#    lons = var.shape[3]
#    value = {}

#    block = (128, 1, 1)
#    grid_size = (lons // block[0]) + 1
#    grid = (grid_size, lats)
#    gpu_var = cuda.to_device(var.astype(np.float32))
#    gpu_lats = cuda.to_device(latitudes.astype(np.float32))
#    gpu_total = cuda.device_array(180, dtype=np.float32)
#    gpu_weights = cuda.device_array(180, dtype=np.float32)
#    for basin, mask in area.items():
#        value[basin] = np.empty((times, levs, 180))
#        gpu_area = cuda.to_device(np.squeeze(area[basin]).astype(np.float32))
#        for t in range(times):
#            for lev in range(levs):
#                _zonal_mean_gpu[block, grid](gpu_var[t, lev, :, :], gpu_area,
#                                             gpu_lats, gpu_total, gpu_weights)
#                value[basin][t][lev][:] = (gpu_total.copy_to_host() /
#                                           gpu_weights.copy_to_host())
#    del gpu_area, gpu_value, gpu_var

#    return value


@numba.njit()
def _zonal_mean_cpu(variable, weight, latitude):
    """Compiled function in executed on the CPU.

    Computes the zonal mean.

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    latitude : float32
        Masked array containing latitude points.
    weight : float32
        Masked array containing cell weights.

    Returns
    -------
    zonmean: float32
        List containing zonal mean for variable var
    """
    total = np.zeros(180, np.float32)
    weights = np.zeros(180, np.float32)
    for i in range(variable.shape[0]):
        for j in range(variable.shape[1]):
            if weight[i, j] == 0:
                continue
            bin_value = int(round(latitude[i, j]) + 90)
            weights[bin_value-1] += weight[i, j]
            total[bin_value-1] += variable[i, j] * weight[i, j]
    return total / weights


# @cuda.jit()
# def _zonal_mean_gpu(variable, weight, latitude, total, weights):
#    i, j = cuda.grid(2)
#    if(i >= total.shape[0]):
#        return
#    if(weight[i, j] != 0.0):

#        bin_value = int(round(latitude[i, j]) + 90)
#        weights[bin_value] += weight[i, j]
#        total[bin_value] += variable[i, j] * weight[i, j]


def get_basin_area(areacello, basins):
    basin_areas = {}
    for basin in basins:
        basin_areas[basin] = _compute_basin_area(areacello, basins[basin])
    return basin_areas


@vectorize(['float32(float32, float32)'], target='cpu')
def _compute_basin_area(areacello, basin):
    """Vectorized numba function executed on the cpu that computes the area
       for each basin:

    Parameters
    ----------
    areacello : float32
        Masked array containing areacello.
    basin: float32
        Masked array containing the mask for a given basin.

    Returns
    -------
    areacello*basin : float32
        Masked array containing the area for a given basin.
    """
    return areacello*basin
