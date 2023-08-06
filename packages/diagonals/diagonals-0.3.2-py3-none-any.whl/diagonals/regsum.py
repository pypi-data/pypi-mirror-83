import logging
import numpy as np
from numba import vectorize

import diagonals

logger = logging.getLogger(__name__)

__all__ = ['compute_regsum_2d', 'compute_regsum_3d', 'compute_regsum_levels']


def compute_regsum_2d(var, basins, area):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    area : float32
        Masked array containing cell area.

    Returns
    -------
    regmean: float32
        List containing regional mean for variable var
    """
    if diagonals.CONFIG.use_gpu:
        logger.warning('GPU routines not implemented for regmean diagnostic.'
                       'Using CPU instead')
    regsum = _compute_regsum_2d_cpu(var, basins, area)
    return regsum


def compute_regsum_3d(var, basins, volume, tmask):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    area : float32
        Masked array containing cell area.

    Returns
    -------
    regmean: float32
        List containing regional mean for variable var
    """
    if diagonals.CONFIG.use_gpu:
        logger.warning('GPU routines not implemented for regmean diagnostic.'
                       'Using CPU instead')
    regsum = _compute_regsum_3d_cpu(var, basins, volume, tmask)
    return regsum


def _compute_regsum_2d_cpu(var, basins, area):
    """Function that computes the regional sum for 2D vars in the cpu.

       Computes the weights for each region and performs a weighted sum.

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    area : float32
        Masked array containing cell area.

    Returns
    -------
    regmean_total: float32
        List containing regional mean for variable var.
    """
    regsum = {}
    for basin, mask in basins.items():
        weighted_var = _weigh_var_2d(var, mask, area)
        regsum[basin] = np.sum(weighted_var, axis=(1, 2))
    return regsum


def _compute_regsum_3d_cpu(var, basins, volume, tmask):
    """Function that computes the regional sum for 3D vars in the cpu.

    Computes the weights for each region and performs a weighted sum.

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    volume : float32
        Masked array containing cell volume

    Returns
    -------
    regmean_total: float32
        List containing regional mean for variable var.
    """
    regsum = {}
    for basin, mask in basins.items():
        weighted_var = _weigh_var_3d(var, mask, volume, tmask)
        regsum[basin] = np.sum(weighted_var, axis=(1, 2, 3))
    return regsum


def compute_regsum_levels(var, basins, volume, tmask):
    """Function that computes the regional sum for 3D vars in the cpu.

    Computes the weights for each region and performs a weighted sum.

    Parameters
    ----------
    var : float32
        Masked array containing variable data.
    basins : float32
        List containing basin names and masks.
    volume : float32
        Masked array containing cell volume
    Returns
    -------
    regmean_total: float32
        List containing regional mean for variable var.
    """
    regsum = {}
    for basin, mask in basins.items():
        weighted_var = _weigh_var_3d(var, mask, volume, tmask)
        regsum[basin] = np.sum(weighted_var, axis=(2, 3))
    return regsum


@vectorize(['float32(float32, float32, float32)'], target='cpu')
def _weigh_var_2d(var, mask, area):
    """Function that weights a 2D variable for each region.

    Parameters
    ----------
    var: float32
        Masked array containing variable to sum.
    mask : float32
        Mask array containing a region mask.
    area: float32
        Masked array containing cell area.

    Returns
    -------
    weights: float32
        Masked array containing the weights for a given region.
    """
    weighted_var = var * mask * area
    return weighted_var


@vectorize(['float32(float32, float32, float32, float32)'],
           target='cpu')
def _weigh_var_3d(var, mask, volume, tmask):
    """Function that weights a 3D variable for each region.

    Parameters
    ----------
    var: float32
        Masked array containing variable to sum.
    mask : float32
        Mask array containing a region mask.
    volume: float32
        Masked array containing cell volume.
    tmask: float32
        Masked array containing land-sea mask for any grid-point type

    Returns
    -------
    weights: float32
        Masked array containing the weights for a given region.
    """
    weighted_var = var * mask * volume * tmask
    return weighted_var
