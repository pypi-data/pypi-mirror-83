import logging
import datetime
import numpy as np

import iris
import iris.cube
import iris.analysis

import diagonals
import diagonals.regsum as regsum
from diagonals.mesh_helpers.nemo import Nemo

MESH_FILE = "/esarchive/autosubmit/con_files/mesh_mask_nemo.Ec3.2_O1L75.nc"
TOS_FILE = "/esarchive/exp/ecearth/a16l/cmorfiles/CMIP/EC-Earth-Consortium"\
            "/EC-Earth3-LR/historical/r1i1p1f1/Omon/tos/gn/v20180711"\
            "/tos_Omon_EC-Earth3-LR_historical_r1i1p1f1_gn_196101-196112.nc"
THETAO_FILE = "/esarchive/exp/ecearth/a16l/cmorfiles/CMIP/EC-Earth-Consortium"\
              "/EC-Earth3-LR/historical/r1i1p1f1/Omon/thetao/gn/v20180711/"\
              "thetao_Omon_EC-Earth3-LR_historical_r1i1p1f1_gn_"\
              "196101-196112.nc"
REGIONS_FILE = "/esarchive/autosubmit/con_files/mask.regions.Ec3.2_O1L75.nc"

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    start = datetime.datetime.now()
    logger.info('Starting at %s', start)
    mesh = Nemo(MESH_FILE, REGIONS_FILE)
    with diagonals.CONFIG.context(use_gpu=True):
        areacello = mesh.get_areacello()
        tos = load_tos()
        basins = load_masks()
        tossum = regsum.compute_regsum_2d(tos, basins, areacello)
        volcello = mesh.get_volcello()
        tmask = mesh.get_landsea_mask()
        thetao = load_thetao()
        thetaosum = regsum.compute_regsum_levels(thetao, basins,
                                                 volcello, tmask)
        thetaosum_3d = regsum.compute_regsum_3d(
            thetao, basins, volcello, tmask)
        device = 'CPU'
        save_cubes(tossum, thetaosum, thetaosum_3d, basins, device)
    ellapsed = datetime.datetime.now() - start
    logger.info('Total ellapsed time on the %s: %s', device, ellapsed)


def load_masks():
    basins = {}
    cubes = iris.load(REGIONS_FILE)
    for cube in cubes:
        name = cube.name()
        if name in ('nav_lat', 'nav_lon', 'Caspian_Sea'):
            continue
        cube = cube.extract(iris.Constraint(z=1))
        basins[name] = cube.data.astype(np.float32)
    return basins


def load_tos():
    tos = iris.load_cube(TOS_FILE, 'sea_surface_temperature')
    tos_data = tos.data.astype(np.float32)
    return tos_data


def load_thetao():
    thetao = iris.load_cube(THETAO_FILE, 'sea_water_potential_temperature')
    thetao_data = thetao.data.astype(np.float32)
    return thetao_data


def save_cubes(tossum, thetaosum, thetaosum3d, basins, device):
    cubes_tossum = iris.cube.CubeList()
    cubes_thetaosum = iris.cube.CubeList()
    cubes_thetaosum3d = iris.cube.CubeList()
    for basin in basins.items():
        cube_tossum = iris.cube.Cube(tossum[basin])
        cube_thetaosum = iris.cube.Cube(thetaosum[basin])
        cube_thetaosum3d = iris.cube.Cube(thetaosum3d[basin])

        cube_tossum.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
        cube_thetaosum.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
        cube_thetaosum3d.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))

        cubes_tossum.append(cube_tossum)
        cubes_thetaosum.append(cube_thetaosum)
        cubes_thetaosum3d.append(cube_thetaosum)

    iris.save(cubes_tossum.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/tossum_{0}.nc'.format(device), zlib=True)
    iris.save(cubes_thetaosum.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/thetaosum_{0}.nc'.format(device), zlib=True)
    iris.save(cubes_thetaosum3d.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/thetaosum3D_{0}.nc'.format(device), zlib=True)


if __name__ == '__main__':
    main()
