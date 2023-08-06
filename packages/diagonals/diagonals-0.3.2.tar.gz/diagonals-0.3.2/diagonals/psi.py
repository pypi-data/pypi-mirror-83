import numpy as np

from numba import vectorize, float32 # noqa

__all__ = ['compute']


def compute(basins, e2u, e1v, e3u, e3v, uo, vo):
    """Function that checks device and calls computing functions.

    Checks if the computations are going performed in the CPU or the GPU:

    Parameters
    ----------
    basins : list
        List of masked arrays containing the mask for each basin.
    e1u: float32
        Masked array containing variable e1u.
    e1v: float32
        Masked array containing variable e1v.
    e3u: float32
        Masked array containing variable e3u.
    e3v: float32
        Masked array containing variable e3v.
    uo : float32
        Masked array containing Sea Water X Velocity data.
    vo : float32
        Masked array containing Sea Water Y Velocity data.

    Returns
    -------
    vsftbarot: list
        List of masked arrays containing the gyre strength.
    """
    area_u = _compute_area(e2u, e3u)
    area_v = _compute_area(e1v, e3v)

    del e2u, e1v, e3u, e3v

    vsftbarot = _compute_psi_cpu(
        uo, vo, area_u, area_v, basins
    )

    return vsftbarot


def _compute_psi_cpu(uo, vo, area_u, area_v, basins):

    psi = {}
    uo_lev = np.sum(uo*area_u, axis=1)
    vo_lev = np.sum(vo*area_v, axis=1)

    del uo, vo, area_u, area_v

    for basin, mask in basins.items():

        dpsiu = _u_cumsum(uo_lev)
        dpsiv = _v_cumsum(vo_lev)

        dpsi = 0.5 * (dpsiu + dpsiv)

        ref_point = dpsi[:, -1, -1]

        psi[basin] = (
                       dpsi - ref_point[:, np.newaxis, np.newaxis]
                     ) * mask

    return psi

# @njit looks like it's not worth it


def _u_cumsum(uo):
    dpsiu = np.zeros(uo.shape)
    for j in range(1, dpsiu.shape[1]):
        dpsiu[:, j, :] = dpsiu[:, j-1, :] - uo[:, j, :]
    return dpsiu

# @njit looks like it's not worth it


def _v_cumsum(vo):
    dpsiv = np.zeros(vo.shape)
    for i in range(dpsiv.shape[2]-2, -1, -1):
        dpsiv[:, :, i] = dpsiv[:, :, i+1] - vo[:, :, i]
    return dpsiv


@vectorize(['float32(float32, float32)'], target='cpu')
def _compute_area(e, e3):
    """Vectorized numba function executed in the CPU.

    Calculates cell area for each basin:

    Parameters
    ----------
    e1: float32
        Masked array containing variable e1 or e2.
    e3: float32
        Masked array containing variable e3.
    basin : float32
        Masked array containing a basin mask.

    Returns
    -------
    area: float32
        Masked array containing the cell area for a given basin.
    """
    area = e * e3
    return area
