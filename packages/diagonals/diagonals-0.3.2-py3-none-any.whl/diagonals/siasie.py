import numpy as np

from numba import vectorize
from numba import cuda

import diagonals

__all__ = ['compute']


def compute(gphit, area, sic_slices, basins, sit):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Iris cubelist containing variable sic sliced over time.
    masks: float32
        List containing basin names and masks.

    Returns
    -------
    extn: float64
        List containing sea ice extent in the northern hemisphere at each
        timestep and basin.
    exts: float64
        List containing sea ice extent in the southern hemisphere at each
        timestep and basin.
    arean: float64
        List containing sea ice area in the northern hemisphere at each
        timestep and basin.
    areas: float64
        List containing sea ice area in the southern hemisphere at each
        timestep and basin.
    device: string
        Device where the computations are being performed (CPU or GPU)
    """
    if diagonals.CONFIG.use_gpu:
        if sit:
            extn, exts, arean, areas, voln, vols = _compute_sic_gpu(
                gphit, area, sic_slices, basins, sit
            )
            return extn, exts, arean, areas, voln, vols
        else:
            extn, exts, arean, areas = _compute_sic_gpu(
                gphit, area, sic_slices, basins, sit
            )
    else:
        if sit:
            extn, exts, arean, areas, voln, vols = _compute_sic_cpu(
                gphit, area, sic_slices, basins, sit
            )
            return extn, exts, arean, areas, voln, vols
        else:
            extn, exts, arean, areas = _compute_sic_cpu(
                gphit, area, sic_slices, basins, sit
            )

    return extn, exts, arean, areas


def _compute_sic_cpu(gphit, area, sic_slices, basins, sithick):
    """Function that computes sea ice are and extension on the CPU.

    Loops over time and basins and reduces over lat and lon:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic_slices: float32
        Iris cubelist containing variable sic sliced over time.
    basins: float32
        List containing basin names and masks.

    Returns
    -------
    extn: float64
        List containing sea ice extent in the northern hemisphere at each
        timestep and basin.
    exts: float64
        List containing sea ice extent in the southern hemisphere at each
        timestep and basin.
    arean: float64
        List containing sea ice area in the northern hemisphere at each
        timestep and basin.
    areas: float64
        List containing sea ice area in the southern hemisphere at each
        timestep and basin.
    """
    extn = np.empty((len(basins), len(sic_slices)))
    exts = np.empty((len(basins), len(sic_slices)))
    arean = np.empty((len(basins), len(sic_slices)))
    areas = np.empty((len(basins), len(sic_slices)))

    if sithick:
        voln = np.empty((len(basins), len(sic_slices)))
        vols = np.empty((len(basins), len(sic_slices)))

    for time, sic_data in enumerate(sic_slices):
        sic = sic_data.data
        b = 0
        for basin, tmask in basins.items():
            temp = _extn_cpu(gphit, area, tmask, sic)
            extn[b][time] = np.sum(temp, axis=(1, 2))

            temp = _exts_cpu(gphit, area, tmask, sic)
            exts[b][time] = np.sum(temp, axis=(1, 2))

            temp = _arean_cpu(gphit, area, tmask, sic)
            arean[b][time] = np.sum(temp, axis=(1, 2))

            temp = _areas_cpu(gphit, area, tmask, sic)
            areas[b][time] = np.sum(temp, axis=(1, 2))

            if sithick:
                sit = sithick[time].data
                temp = _voln_cpu(gphit, area, tmask, sic, sit)
                voln[b][time] = np.sum(temp, axis=(1, 2))

                temp = _vols_cpu(gphit, area, tmask, sic, sit)
                vols[b][time] = np.sum(temp, axis=(1, 2))

            b += 1

    del gphit, area, sic_slices, temp

    if sithick:
        return extn, exts, arean, areas, voln, vols

    return extn, exts, arean, areas


def _compute_sic_gpu(gphit, area, sic_slices, basins, sithick):
    """Function that computes sea ice are and extension on the GPU.

    Loops over time and basins and reduces over lat and lon:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic_slices: float32
        Iris cubelist containing variable sic sliced over time.
    basins: float32
        List containing basin names and masks.

    Returns
    -------
    extn: float64
        List containing sea ice extent in the northern hemisphere at each
        timestep and basin.
    exts: float64
        List containing sea ice extent in the southern hemisphere at each
        timestep and basin.
    arean: float64
        List containing sea ice area in the northern hemisphere at each
        timestep and basin.
    areas: float64
        List containing sea ice area in the southern hemisphere at each
        timestep and basin.
    """
    extn = np.empty((len(basins), len(sic_slices)))
    exts = np.empty((len(basins), len(sic_slices)))
    arean = np.empty((len(basins), len(sic_slices)))
    areas = np.empty((len(basins), len(sic_slices)))

    gpu_gphit = cuda.to_device(gphit.astype(np.float32))
    gpu_area = cuda.to_device(area.astype(np.float32))
    gpu_temp = cuda.device_array(area.shape[1]*area.shape[2], dtype=np.float32)

    block = (128, 1)
    grid_size = ((area.shape[2]) // block[0]) + 1
    grid = (grid_size, area.shape[1])
    del gphit, area

    if sithick:
        voln = np.empty((len(basins), len(sic_slices)))
        vols = np.empty((len(basins), len(sic_slices)))

    for time, sic_data in enumerate(sic_slices):
        extn[time] = {}
        exts[time] = {}
        arean[time] = {}
        areas[time] = {}
        sic = sic_data.data.astype(np.float32)
        gpu_sic = cuda.to_device(sic.astype(np.float32))
        b = 0
        for basin, tmask in basins.items():
            gpu_tmask = cuda.to_device(tmask.astype(np.float32))

            _extn_gpu[grid, block](gpu_gphit, gpu_area, gpu_tmask,
                                   gpu_sic, gpu_temp)
            extn[b][time] = _sum_red_cuda(gpu_temp)

            _exts_gpu[grid, block](gpu_gphit, gpu_area, gpu_tmask,
                                   gpu_sic, gpu_temp)
            exts[b][time] = _sum_red_cuda(gpu_temp)

            _arean_gpu[grid, block](gpu_gphit, gpu_area, gpu_tmask,
                                    gpu_sic, gpu_temp)
            arean[b][time] = _sum_red_cuda(gpu_temp)

            _areas_gpu[grid, block](gpu_gphit, gpu_area, gpu_tmask,
                                    gpu_sic, gpu_temp)
            areas[b][time] = _sum_red_cuda(gpu_temp)

            if sithick:
                sit = sithick[time].data.astype(np.float32)
                gpu_sit = cuda.to_device(sit.astype(np.float32))
                _voln_gpu[grid, block](gpu_gphit, gpu_area, gpu_tmask,
                                       gpu_sic, gpu_sit, gpu_temp)
                voln[b][time] = _sum_red_cuda(gpu_temp)

                _vols_gpu[grid, block](gpu_gphit, gpu_area, gpu_tmask,
                                       gpu_sic, gpu_sit, gpu_temp)
                vols[b][time] = _sum_red_cuda(gpu_temp)

            b += 1

    if sithick:
        return extn, exts, arean, areas, voln, vols

    del gpu_gphit, gpu_area, gpu_tmask, gpu_sic, gpu_temp
    return extn, exts, arean, areas


@vectorize(['float32(float32, float32, float32, float32)'],
           target='cpu')
def _arean_cpu(gphit, area, tmask, sic):
    """Vectorized numba function executed on the cpu that computes the
       percentage of sea ice in the northern hemisphere for a given timestep
       and basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin

    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain sea ice area
    """
    if gphit > 0:
        temp = area * tmask * sic / 100
    return temp


@cuda.jit()
def _arean_gpu(gphit, area, tmask, sic, temp):
    """Numba kernel executed on the gpu that computes the percentage of sea ice
    in the northern hemisphere for a given timestep and basin:

     Parameters
     ----------
     gphit : float32
         Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
     sic: float32
         Masked array containing variable sic for a given timestep.
     tmask: float32
         Masked array for a given basin

     Returns
     -------
     temp : float32
         Masked array to be summed over lat and lon to obtain the sea ice area
         value. Needs to be a one dimensional array in order to be the input
         for the reduction kernel.
     """
    i, j = cuda.grid(2)
    x = i + j * sic.shape[1]
    if(i >= sic.shape[1]):
        return
    temp[x] = 0.0
    if(gphit[0, j, i] > 0):
        temp[x] = (area[0, j, i] * tmask[0, j, i] * sic[j, i]
                   / 100)


@vectorize(['float32(float32, float32, float32, float32)'],
           target='cpu')
def _extn_cpu(gphit, area, tmask, sic):
    """Vectorized numba function executed on the cpu that computes the sea ice
    extent per unit of area in the northern hemisphere for a given timestep and
    basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin

    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain sea ice extent
        value
    """
    if(gphit > 0 and sic > 15):
        temp = area * tmask
    return temp


@cuda.jit()
def _extn_gpu(gphit, area, tmask, sic, temp):
    """Numba kernel executed on the gpu that computes the percentage of sea ice
    extent value per unit of area in the northern hemisphere for a given
    timestep and basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin

    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain the sea ice extent
        value. Needs to be a one dimensional array in order to be the input
        for the reduction kernel.
    """
    i, j = cuda.grid(2)
    x = i + j * sic.shape[1]
    if(i >= sic.shape[1]):
        return
    temp[x] = 0.0
    if(gphit[0, j, i] > 0 and sic[j, i] > 15):
        temp[x] = area[0, j, i] * tmask[0, j, i]


@vectorize(['float32(float32, float32, float32, float32)'],
           target='cpu')
def _areas_cpu(gphit, area, tmask, sic):
    """Vectorized numba function executed on the cpu that computes the
       percentage of sea ice in the southern hemisphere for a given timestep
       and basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin

    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain sea ice area
    """
    if gphit < 0:
        temp = area * tmask * sic / 100
    return temp


@cuda.jit()
def _areas_gpu(gphit, area, tmask, sic, temp):
    """Numba kernel executed on the gpu that computes the percentage of sea ice
    in the southern hemisphere for a given timestep and basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin

    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain the sea ice area
        value. Needs to be a one dimensional array in order to be the input
        for the reduction kernel.
    """
    i, j = cuda.grid(2)
    x = i + j * sic.shape[1]
    if(i >= sic.shape[1]):
        return
    temp[x] = 0.0
    if(gphit[0, j, i] < 0):
        temp[x] = area[0, j, i] * tmask[0, j, i] * sic[j, i] / 100


@vectorize(['float32(float32, float32, float32, float32)'],
           target='cpu')
def _exts_cpu(gphit, area, tmask, sic):
    """Vectorized numba function executed on the cpu that computes the sea ice
    extent per unit of area in the southern hemisphere for a given timestep and
    basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin

    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain sea ice extent
        value
    """
    if(gphit < 0 and sic > 15):
        temp = area * tmask
    return temp


@cuda.jit()
def _exts_gpu(gphit, area, tmask, sic, temp):
    """Numba kernel executed on the gpu that computes the percentage of sea ice
    extent value per unit of area in the southern hemisphere for a given
    timestep and basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin

    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain the sea ice extent
        value. Needs to be a one dimensional array in order to be the input
        for the reduction kernel.
    """
    i, j = cuda.grid(2)
    x = i + j * sic.shape[1]
    if(i >= sic.shape[1]):
        return
    temp[x] = 0.0
    if(gphit[0, j, i] < 0 and sic[j, i] > 15):
        temp[x] = area[0, j, i] * tmask[0, j, i]


@vectorize(['float32(float32, float32, float32, float32, float32)'],
           target='cpu')
def _voln_cpu(gphit, area, tmask, sic, sit):
    """Vectorized numba function executed on the cpu that computes the
       percentage of sea ice volume in the northern hemisphere for a given
       timestep and basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin
    sit: float32
        Masked array containing variable sit for a given timestep.
    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain sea ice volume
    """
    if gphit > 0:
        temp = area * tmask * sic * sit / 100
    return temp


@cuda.jit()
def _voln_gpu(gphit, area, tmask, sic, sit, temp):
    """Numba kernel executed on the gpu that computes the percentage of sea ice
    volume in the northern hemisphere for a given timestep and basin:

     Parameters
     ----------
     gphit : float32
         Masked array containing variable gphit.
     area : float32
        Masked array containing cell area.
     sic: float32
         Masked array containing variable sic for a given timestep.
     tmask: float32
         Masked array for a given basin
     sit: float32
        Masked array containing variable sit for a given timestep.

     Returns
     -------
     temp : float32
         Masked array to be summed over lat and lon to obtain the sea ice area
         value. Needs to be a one dimensional array in order to be the input
         for the reduction kernel.
     """
    i, j = cuda.grid(2)
    x = i + j * sic.shape[1]
    if(i >= sic.shape[1]):
        return
    temp[x] = 0.0
    if(gphit[0, j, i] > 0):
        temp[x] = (area[0, j, i] * tmask[0, j, i] * sic[j, i] * sit[j, i]
                   / 100)


@vectorize(['float32(float32, float32, float32, float32, float32)'],
           target='cpu')
def _vols_cpu(gphit, area, tmask, sic, sit):
    """Vectorized numba function executed on the cpu that computes the
       percentage of sea ice volume in the southern hemisphere for a given
       timestep and basin:

    Parameters
    ----------
    gphit : float32
        Masked array containing variable gphit.
    area : float32
        Masked array containing cell area.
    sic: float32
        Masked array containing variable sic for a given timestep.
    tmask: float32
        Masked array for a given basin
    sit: float32
        Masked array containing variable sit for a given timestep.
    Returns
    -------
    temp : float32
        Masked array to be summed over lat and lon to obtain sea ice volume
    """
    if gphit < 0:
        temp = area * tmask * sic * sit / 100
    return temp


@cuda.jit()
def _vols_gpu(gphit, area, tmask, sic, sit, temp):
    """Numba kernel executed on the gpu that computes the percentage of sea ice
    volume in the southern hemisphere for a given timestep and basin:

     Parameters
     ----------
     gphit : float32
         Masked array containing variable gphit.
     area : float32
        Masked array containing cell area.
     sic: float32
         Masked array containing variable sic for a given timestep.
     tmask: float32
         Masked array for a given basin
     sit: float32
        Masked array containing variable sit for a given timestep.

     Returns
     -------
     temp : float32
         Masked array to be summed over lat and lon to obtain the sea ice area
         value. Needs to be a one dimensional array in order to be the input
         for the reduction kernel.
     """
    i, j = cuda.grid(2)
    x = i + j * sic.shape[1]
    if(i >= sic.shape[1]):
        return
    temp[x] = 0.0
    if(gphit[0, j, i] < 0):
        temp[x] = (area[0, j, i] * tmask[0, j, i] * sic[j, i] * sit[j, i]
                   / 100)


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
