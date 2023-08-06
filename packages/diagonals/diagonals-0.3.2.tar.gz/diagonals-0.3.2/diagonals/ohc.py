import numpy as np
import dask.array as da

from numba import vectorize
from numba import cuda

import diagonals

__all__ = ['get_weights', 'compute', 'get_basin_area']


def get_weights(layers, mask, cell_height, cell_top_depth):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    layers : list
        List containing the minimum and maximum depth values for the layer.
    mask : float32
        Masked array containing the Global basin mask.
    cell_height: float32
        Masked array containing variable e3t.
    cell_top_depth: float32
        Masked array containing variable gwdep.

    Returns
    -------
    weights: float32
        List of masked arrays containing the weights for each layer.
    """
    if diagonals.CONFIG.use_gpu:
        weights = _compute_weights_gpu(
            layers, mask, cell_height, cell_top_depth
        )
    else:
        weights = _compute_weights_cpu(
            layers, mask, cell_height, cell_top_depth
        )
    return weights


def compute(layers, weights, thetao, area):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    layers : list
        List containing the minimum and maximum depth values for the layer.
    weights: float32
        List of masked arrays containing the weights for each layer.
    thetao: float32
        Masked array containing variable thetao.
    area: float32
        List of masked arrays containing the area for each basin.

    Returns
    -------
    ohc: float32
        List of masked arrays containing the global 2D ocean heat content for
        each layer and timestep.
    ohc_1D: float32
        List of masked arrays containing the 1D ocean heat content for each
        layer, basin and timestep.
    """
    if diagonals.CONFIG.use_gpu:
        ohc, ohc_1D = _compute_ohc_gpu(layers, thetao, weights, area)
    else:
        ohc, ohc_1D = _compute_ohc_cpu(layers, thetao, weights, area)
    return ohc, ohc_1D


def _compute_weights_cpu(layers, mask, e3t, depth):
    """Function that calls computing functions in the CPU.

    Computes weights for each layer and appends them to a list:

    Parameters
    ----------
    layers : list
        List containing the minimum and maximum depth values for the layer.
    mask : float32
        Masked array containing the Global basin mask.
    e3t: float32
        Masked array containing variable e3t.
    depth: float32
        Masked array containing variable gwdep.

    Returns
    -------
    weights: float32
        List of masked arrays containing the weights for each layer.
    """
    weights = []
    for min_depth, max_depth in layers:
        weights.append(
            _calculate_weight_numba(min_depth, max_depth, e3t, depth, mask)
        )
    return weights


def _compute_weights_gpu(layers, mask, e3t, depth):
    """Function that calls computing functions in the GPU.

    Computes weights for each layer and appends them to a list:

    Parameters
    ----------
    layers : list
        List containing the minimum and maximum depth values for the layer.
    mask : float32
        Masked array containing the Global basin mask.
    e3t: float32
        Masked array containing variable e3t.
    depth: float32
        Masked array containing variable gwdep.

    Returns
    -------
    weights: float32
        List of masked arrays containing the weights for each layer.
    """
    gpu_mask = cuda.to_device(mask.data.astype(np.float32))
    gpu_e3t = cuda.to_device(e3t.data.astype(np.float32))
    gpu_depth = cuda.to_device(depth.data.astype(np.float32))
    weights = []
    for min_depth, max_depth in layers:
        weights.append(_calculate_weight_numba_cuda(min_depth, max_depth,
                       gpu_e3t, gpu_depth, gpu_mask))
    del gpu_depth, gpu_mask, gpu_e3t
    return weights


def _compute_ohc_cpu(layers, thetao, weights, area):
    """Function that calls computing functions in the CPU.

    Loops over layers to compute the global ocean heat content in 2D. This
    value then gets weighted by each basin area in order to compute the ocean
    heat content in 1D:

    Parameters
    ----------
    layers : list
        List containing the minimum and maximum depth values for the layer.
    weights: float32
        List of masked arrays containing the weights for each layer.
    thetao: float32
        Masked array containing variable thetao.
    area: float32
        List of masked arrays containing the area for each basin.

    Returns
    -------
    ohc: float32
        List of masked arrays containing the global 2D ocean heat content for
        each layer and timestep.
    ohc_1D: float32
        List of masked arrays containing the 1D ocean heat content for each
        layer, basin and timestep.
    """
    ohc = []
    for layer in range(len(layers)):
        ohc_layer = da.sum(
            _multiply_array(thetao, weights[layer]),
            axis=1
        )
        ohc.append(ohc_layer)
        ohc1d_total = []
        for i, basin in enumerate(area):
            ohc_basin = _multiply_array(ohc_layer, area[basin])
            ohc1d = np.sum(ohc_basin, axis=(1, 2))
            ohc1d_total.append(ohc1d)
    return ohc, ohc1d_total


def _compute_ohc_gpu(layers, thetao, weights, area):
    """Function that calls computing functions in the GPU.

    Loops over layers to compute the global ocean heat content in 2D. This
    value then gets weighted by each basin area in order to compute the ocean
    heat content in 1D:

    Parameters
    ----------
    layers : list
        List containing the minimum and maximum depth values for the layer.
    weights: float32
        List of masked arrays containing the weights for each layer.
    thetao: float32
        Masked array containing variable thetao.
    area: float32
        List of masked arrays containing the area for each basin.

    Returns
    -------
    ohc: float32
        List of masked arrays containing the global 2D ocean heat content for
        each layer and timestep.
    ohc1D_total: float32
        List of masked arrays containing the 1D ocean heat content for each
        layer, basin and timestep.
    """
    levels = thetao.shape[1]
    times = thetao.shape[0]
    lats = thetao.shape[2]
    lons = thetao.shape[3]
    basins = len(area)

    area_basin = np.empty((basins, lats, lons))
    block = (128, 1, 1)
    grid_size = (lons // block[0]) + 1
    grid = (grid_size, lats, times)
    ohc = []
    gpu_ohc = cuda.device_array((times, lats, lons), dtype=np.float32)
    gpu_temp = cuda.device_array((basins, times, lats*lons), dtype=np.float32)
    for i, basin in enumerate(area):
        area_basin[i, :, :] = area[basin]
    gpu_basins_area = cuda.to_device(area_basin.astype(np.float32))
    gpu_thetao = cuda.to_device(thetao.astype(np.float32))

    for layer in range(len(layers)):
        _compute_ohc[grid, block](gpu_thetao, weights[layer], gpu_ohc, levels)
        ohc.append(gpu_ohc.copy_to_host())  # moure al final
        _multiply_ohc_basin[grid, block](gpu_ohc, gpu_basins_area, gpu_temp)
        ohc1d_basin = []
        for basin in range(basins):
            ohc_1d = np.empty(times, dtype=np.float32)
            for time in range(times):
                ohc_1d[time] = _sum_red_cuda(gpu_temp[basin, time, :])
            ohc1d_basin.append(ohc_1d)
    del gpu_ohc, gpu_temp, gpu_basins_area

    return ohc, ohc1d_basin


@vectorize(['float32(int32, int32, float32, float32, float32)'], target='cuda')
def _calculate_weight_numba_cuda(min_depth, max_depth, e3t, depth, mask):
    """Vectorized numba function executed on the gpu.

    Calculates the weight for each cell:

    Parameters
    ----------
    min_depth : int
        Integer indicating the minimum depth of the layer.
    max_depth : int
        Integer indicating the maximum depth of the layer.
    e3t: float32
        Masked array containing variable e3t.
    depth: float32
        Masked array containing variable gwdep.
    mask : float32
        Masked array containing the Global basin mask.

    Returns
    -------
    weight: float32
        Masked array containing the weights for a given layer.
    """
    top = depth
    bottom = top + e3t
    if bottom < min_depth or top > max_depth:
        return 0
    else:
        if top < min_depth:
            top = min_depth
        if bottom > max_depth:
            bottom = max_depth
        if not mask:
            return np.nan

        return (bottom - top) * 1020 * 4000


@cuda.jit()
def _compute_ohc(thetao, weight, ohc, levels):
    """Numba kernel executed on the gpu that computes the global ocean heat
    content in 2D for a given layer and timestep:

    Parameters
    ----------
    thetao: float32
        Masked array containing variable thetao in Kelvin.
    weight: float32
        Masked array containing the weights for a given layer.
    ohc: float32
        Empty array to store the ocean heat content results.
    levels: int
        Indicates the number depth levels over which the product of thetao and
        weight needs to be summed over in order to compute ohc.

    Returns
    -------
    ohc: float32
        Masked array containing the global 2D ocean heat content results
    """
    i, j, t = cuda.grid(3)
    ohc[t, j, i] = 0.0
    temp = 0.0
    if(i >= thetao.shape[3]):
        return
    for lev in range(levels):
        temp += thetao[t, lev, j, i] * weight[0, lev, j, i]
    ohc[t, j, i] = temp


@cuda.jit()
def _multiply_ohc_basin(ohc, area, temp):
    """Numba kernel executed on the gpu that weights the global ocean heat
    content over the area for each basin for and timestep:

    Parameters
    ----------
    ohc: float32
        Masked array containing the global 2D ocean heat content results
    area: float32
        Masked array containing the area for a given basin..
    temp: float32
        Empty array to store the results.

    Returns
    -------
    temp: float32
        Masked array containing the product of of ohc and weight. The lat lon
        coordinates are merged into a single dimension in order to compute the
        reduction later on.
    """
    i, j, t = cuda.grid(3)
    basins = area.shape[0]
    x = i + j * ohc.shape[2]
    if i >= ohc.shape[2]:
        return
    for basin in range(basins):
        temp[basin, t, x] = 0.0
        temp[basin, t, x] = ohc[t, j, i] * area[basin, j, i]


@vectorize(['float32(int32, int32, float32, float32, float32)'], target='cpu')
def _calculate_weight_numba(min_depth, max_depth, e3t, depth, mask):
    """Vectorized numba function executed on the cpu.

    Calculates the weight for each cell:

    Parameters
    ----------
    min_depth : int
        Integer indicating the minimum depth of the layer.
    max_depth : int
        Integer indicating the maximum depth of the layer.
    e3t: float32
        Masked array containing variable e3t.
    depth: float32
        Masked array containing variable gwdep.
    mask : float32
        Masked array containing the Global basin mask.

    Returns
    -------
    weight: float32
        Masked array containing the weights for a given layer.
    """
    top = depth
    bottom = top + e3t
    if bottom < min_depth or top > max_depth:
        return 0
    else:
        if top < min_depth:
            top = min_depth
        if bottom > max_depth:
            bottom = max_depth
        if not mask:
            return np.nan

        return (bottom - top) * 1020 * 4000


@vectorize(['float64(float32, float32)', 'float64(float64, float64)'],
           target='cpu')
def _sum_red(x, y):
    """Vectorized numba function executed on the cpu that performs a sum
    reduction:

    Parameters
    ----------
    x : float32
        Numpy array.
    y : float32
        Numpy array.

    Returns
    -------
    x+y : float64
        Reduction operation.
    """
    return x+y


@vectorize(['float32(float32, float32)', 'float64(float64, float64)'],
           target='cpu')
def _multiply_array(a, b):
    """Vectorized numba function executed on the cpu that performs an
    element-wise multiplication of two arrays:

    Parameters
    ----------
    a : float32
        Numpy array.
    b : float32
        Numpy array.

    Returns
    -------
    a*b : float64
        Numpy array containing an element-wise multiplication of the input
        arrays.
    """
    return a*b


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


@cuda.reduce
def _sum_red_cuda(x, y):
    """Numba kernel executed on the gpu that performs a sum reduction:

    Parameters
    ----------
    x : float32
        Numpy array.
    y : float32
        Numpy array.

    Returns
    -------
    x+y : float64
        Reduction operation.
    """
    return x+y
