import logging
import datetime
import numpy as np

import iris
import iris.cube
import iris.analysis
import iris.util
import iris.coords

import diagonals
import diagonals.moc as moc
from diagonals.mesh_helpers.nemo import Nemo

MESH_FILE = "/esarchive/autosubmit/con_files/mesh_mask_nemo.Ec3.2_O1L75.nc"
REGIONS_FILE = "/esarchive/autosubmit/con_files/mask.regions.Ec3.2_O1L75.nc"
VO_FILE = "/esarchive/exp/ecearth/a16l/cmorfiles/CMIP/EC-Earth-Consortium/" \
          "EC-Earth3-LR/historical/r1i1p1f1/Omon/vo/gn/v20180711/" \
          "vo_Omon_EC-Earth3-LR_historical_r1i1p1f1_gn_196101-196112.nc"

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    start = datetime.datetime.now()
    logger.info('Starting at %s', start)
    mesh = Nemo(MESH_FILE, REGIONS_FILE)
    with diagonals.CONFIG.context(use_gpu=True):
        e1v = mesh.get_i_length(cell_point='V')
        e3v = mesh.get_k_length(cell_point='V')
        basins = load_masks()
        vo = load_vo()
        moc_index = moc.compute(basins, e1v, e3v, vo)
        del e1v, e3v, vo
        if diagonals.CONFIG.use_gpu:
            device = 'GPU'
        else:
            device = 'CPU'
        save_cubes(moc_index, basins, device)
    ellapsed = datetime.datetime.now() - start
    logger.info('Total ellapsed time on the %s: %s', device, ellapsed)


def load_vo():
    vo = iris.load_cube(VO_FILE, 'sea_water_y_velocity')
    vo_data = np.ma.filled(vo.data, 0.0).astype(np.float32)
    return vo_data


def load_masks():
    basins = {}
    global_mask = iris.load_cube(MESH_FILE, 'vmask')
    basin_name = []
    basin_name.append('Global_Ocean')
    global_mask.data[..., 0] = 0.0
    global_mask.data[..., -1] = 0.0
    basins['Global_Ocean'] = global_mask.data.astype(np.float32)
    cubes = iris.load(REGIONS_FILE)
    for cube in cubes:
        name = cube.name()
        if name in ('nav_lat', 'nav_lon', 'Caspian_Sea', 'Global_Ocean'):
            continue
        cube = cube.extract(iris.Constraint(z=1))
        basins[name] = cube.data.astype(np.float32)
    return basins


def save_cubes(moc, basins, device):
    cubes_moc = iris.cube.CubeList()
    for basin in basins.keys():
        cube_moc = iris.cube.Cube(moc[basin])
        cube_moc.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
        cubes_moc.append(cube_moc)
    iris.save(cubes_moc.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/moc_{0}_merged.nc'.format(device), zlib=True)


if __name__ == '__main__':
    main()
