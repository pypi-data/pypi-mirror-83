import numpy as np


from numba import vectorize
from numba import guvectorize
from numba import cuda
from numba import float32

import diagonals

__all__ = ['compute']


def compute(basins, e1v, e3v, vo):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    basins : list
        List of masked arrays containing the mask for each basin.
    e1v: float32
        Masked array containing variable e1v
    e3v: float32
        Masked array containing variable e3v
    vo : float32
        Masked array containing Sea Water Y Velocity data.

    Returns
    -------
    moc: list
        List of masked arrays containing the moc index for each basin.
    """
    area = {}
    for basin in basins:
        area[basin] = _compute_area(e1v, e3v, basins[basin])

    del e1v, e3v

    if diagonals.CONFIG.use_gpu:
        moc = _compute_moc_gpu(
            vo, area
        )
    else:
        moc = _compute_moc_cpu(
            vo, area
        )
    return moc


def _compute_moc_cpu(vo, area):
    """Function that calls computing functions in the CPU.

    Computes moc index for each basin and appends them to a list:

    Parameters
    ----------
    area: list
        List containing the areas for every basin.

    vo : float32
        Masked array containing Sea Water Y Velocity data.

    Returns
    -------
    moc: list
        List of masked arrays containing the moc index for each basin.
    """
    moc = {}
    for basin, mask in area.items():
        moc_basin = np.sum(_multiply_vo_basin(vo, mask), axis=3)
        _vertical_cumsum(moc_basin, moc_basin)
        moc[basin] = moc_basin
    return moc


def _compute_moc_gpu(vo, area):
    """Function that calls computing functions in the GPU.

    Computes moc index for each basin and appends them to a list:

    Parameters
    ----------
    area: list
        List containing the areas for every basin.

    vo : float32
        Masked array containing Sea Water Y Velocity data.

    Returns
    -------
    moc: list
        List of masked arrays containing the moc index for each basin.
    """
    times = vo.shape[0]
    levels = vo.shape[1]
    lats = vo.shape[2]

    block = (128, 1, 1)
    grid_size = (lats // block[0]) + 1
    grid_3d = (grid_size, levels, times)
    gpu_vo = cuda.to_device(vo.astype(np.float32))
    gpu_moc = cuda.device_array((times, levels, lats), dtype=np.float32)
    grid_2d = (grid_size, times)

    moc = {}
    for basin, mask in area.items():
        gpu_area = cuda.to_device(mask.astype(np.float32))
        _horizontal_integral[grid_3d, block](gpu_vo, gpu_area, gpu_moc)
        _vertical_cumsum_gpu[grid_2d, block](gpu_moc)
        moc[basin] = gpu_moc.copy_to_host()

    del gpu_area, gpu_moc, gpu_vo

    return moc


@vectorize(['float32(float32, float32, float32)'], target='cpu')
def _compute_area(e1v, e3v, basin):
    """Vectorized numba function executed in the CPU.

    Calculates cell area for each basin:

    Parameters
    ----------
    e1v: float32
        Masked array containing variable e1v.
    e3v: float32
        Masked array containing variable e3v.
    basin : float32
        Masked array containing a basin mask.

    Returns
    -------
    area: float32
        Masked array containing the cell area for a given basin.
    """
    area = - e1v * e3v * basin / 1e6
    return area


@vectorize(['float32(float32, float32)'], target='cpu')
def _multiply_vo_basin(vo, basin):
    """Vectorized numba function executed in the CPU.

    Weights vo with a given basin area:

    Parameters
    ----------
    e1v: float32
        Masked array containing variable e1v.
    e3v: float32
        Masked array containing variable e3v.
    basin : float32
        Masked array containing a basin mask.

    Returns
    -------
    area: float32
        Masked array containing the cell area for a given basin.
    """
    return vo*basin


@guvectorize([(float32[:, :, :], float32[:, :, :])], '(t, l, j)->(t, l, j)',
             target='cpu')
def _vertical_cumsum(moc, out):
    """Numba gu-function executed in the CPU.

    Performs vertical cummulative sum in order to compute the moc index:

    Parameters
    ----------
    moc: float32
        Masked array containing horizontal integration of vo.

    Returns
    -------
    moc: float32
        Masked array containing the moc index for a given basin.
    """
    for lev in range(moc.shape[1] - 2, -1, -1):
        moc[:, lev, :] = moc[:, lev, :] + moc[:, lev+1, :]


@cuda.jit()
def _vertical_cumsum_gpu(moc):
    """Numba kernel executed in the GPU.

    Performs vertical cummulative sum in order to compute the moc index:

    Parameters
    ----------
    moc: float32
        Masked array containing horizontal integration of vo.

    Returns
    -------
    moc: float32
        Masked array containing the moc indes for a given basin.
    """
    j, t = cuda.grid(2)
    if(j >= moc.shape[2]):
        return
    for lev in range(moc.shape[1]-2, -1, -1):
        moc[t, lev, j] = moc[t, lev, j] + moc[t, lev+1, j]


@cuda.jit()
def _horizontal_integral(vo, area, moc):
    """Numba kernel executed in the GPU.

    Integrates along the longitudes in order to compute the moc index:

    Parameters
    ----------
    vo : float32
        Masked array containing Sea Water Y Velocity data.

    area: float32
        List containing the areas for every basin.

    Returns
    -------
    moc: float32
        Masked array containing vo horizontally integrated for a given basin.
    """
    j, lev, t = cuda.grid(3)
    moc[t, lev, j] = 0.0
    temp = 0.0
    if(j >= vo.shape[2]):
        return
    for i in range(vo.shape[3]):
        temp += vo[t, lev, j, i] * area[0, lev, j, i]
    moc[t, lev, j] = temp
