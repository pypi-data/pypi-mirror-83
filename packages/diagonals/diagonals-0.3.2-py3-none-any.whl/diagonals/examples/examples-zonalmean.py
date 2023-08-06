import logging
import datetime
import numpy as np

import iris
import iris.cube
import iris.analysis
import iris.coords
import iris.coord_categorisation
import iris.analysis

import diagonals
import diagonals.zonmean as zonmean
from diagonals.mesh_helpers.nemo import Nemo

MESH_FILE = "/esarchive/autosubmit/con_files/mesh_mask_nemo.Ec3.2_O1L75.nc"
REGIONS_FILE = "/esarchive/autosubmit/con_files/mask.regions.Ec3.2_O1L75.nc"
THETAO_FILE = "/esarchive/exp/ecearth/a1tr/cmorfiles/CMIP/EC-Earth-Consortium"\
              "/EC-Earth3/historical/r24i1p1f1/Omon/thetao/gn/v20190312/"\
              "thetao_Omon_EC-Earth3_historical_r24i1p1f1_gn_"\
              "185001-185012.nc"

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    start = datetime.datetime.now()
    logger.info('Starting at %s', start)
    mesh = Nemo(MESH_FILE, REGIONS_FILE)
    with diagonals.CONFIG.context(use_gpu=True):
        lats = mesh.get_mesh_var('nav_lat', dtype=np.float32)
        areacello = mesh.get_areacello()
        var = load_thetao()
        basins = load_masks()
        area_basin = zonmean.get_basin_area(areacello, basins)
        zonalmean = zonmean.compute_zonmean(var, lats, area_basin)
        if diagonals.CONFIG.use_gpu:
            device = 'GPU'
        else:
            device = 'CPU'
        save_data(zonalmean, basins, device)
    ellapsed = datetime.datetime.now() - start
    logger.info('Total ellapsed time on the %s: %s', device, ellapsed)


def load_thetao():
    thetao = iris.load_cube(THETAO_FILE, 'sea_water_potential_temperature')
    thetao_data = thetao.data.astype(np.float32)
    return thetao_data


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


def save_data(zonalmean, basins, device):
    cubes_zonmean = iris.cube.CubeList()
    for basin in basins.keys():
        cube_zonmean = iris.cube.Cube(zonalmean[basin])
        cube_zonmean.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
        cubes_zonmean.append(cube_zonmean)
    iris.save(cubes_zonmean.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/zonmean_{0}.nc'.format(device), zlib=True)


if __name__ == '__main__':
    main()
