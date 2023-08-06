import logging
import datetime
import numpy as np

import iris
import iris.cube
import iris.analysis

import diagonals
import diagonals.regmean as regmean
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
        tosmean = regmean.compute_regmean_2d(tos, basins, areacello)
        volcello = mesh.get_volcello()
        thetao = load_thetao()
        thetaomean = regmean.compute_regmean_levels(thetao, basins, volcello)
        thetaomean3d = regmean.compute_regmean_3d(thetao, basins, volcello)
        device = 'CPU'
        save_cubes(tosmean, thetaomean, thetaomean3d, basins, device)
    ellapsed = datetime.datetime.now() - start
    logger.info('Total ellapsed time on the %s: %s', device, ellapsed)


def load_masks():
    basins = {}
    basin_name = []
    cubes = iris.load(REGIONS_FILE)
    for cube in cubes:
        name = cube.name()
        if name in ('nav_lat', 'nav_lon', 'Caspian_Sea'):
            continue
        basin_name.append(name)
        cube = cube.extract(iris.Constraint(z=1))
        basins[name] = cube.data.astype(np.float32)
    return basins


def load_tos():
    tos = iris.load_cube(TOS_FILE, 'sea_surface_temperature')
    tos_data = tos.data.astype(np.float32)
    return tos_data


def load_thetao():
    thetao = iris.load_cube(THETAO_FILE, 'sea_water_conservative_temperature')
    thetao_data = thetao.data.astype(np.float32)
    return thetao_data


def save_cubes(tosmean, thetaomean, thetaomean_3d, basins, device):
    cubes_tosmean = iris.cube.CubeList()
    cubes_thetaomean = iris.cube.CubeList()
    cubes_thetaomean_3d = iris.cube.CubeList()
    for basin in basins.keys():
        cube_tosmean = iris.cube.Cube(tosmean[basin])
        cube_thetaomean = iris.cube.Cube(thetaomean[basin])
        cube_thetaomean_3d = iris.cube.Cube(thetaomean_3d[basin])

        cube_tosmean.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
        cube_thetaomean.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
        cube_thetaomean_3d.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))

        cubes_tosmean.append(cube_tosmean)
        cubes_thetaomean.append(cube_thetaomean)
        cubes_thetaomean_3d.append(cube_thetaomean_3d)

    iris.save(cubes_tosmean.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/tosmean_{0}.nc'.format(device), zlib=True)
    iris.save(cubes_thetaomean.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/thetaomean_{0}.nc'.format(device), zlib=True)
    iris.save(cubes_thetaomean_3d.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/thetaomean3D_{0}.nc'.format(device), zlib=True)


if __name__ == '__main__':
    main()
