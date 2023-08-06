import logging
import datetime
import numpy as np

import iris
import iris.cube
import iris.analysis

import diagonals
import diagonals.ohc as ohc
from diagonals.mesh_helpers.nemo import Nemo

MESH_FILE = "/esarchive/autosubmit/con_files/mesh_mask_nemo.Ec3.2_O1L75.nc"
DATA_FILE = "/esarchive/exp/ecearth/t05l/cmorfiles/CMIP/EC-Earth-Consortium" \
            "/EC-Earth3-LR/historical/r1i1p1f1/Omon/thetao/gn/v20190205" \
            "/thetao_Omon_EC-Earth3-LR_historical_r1i1p1f1_gn_199001-199001.nc"
REGIONS_FILE = "/esarchive/autosubmit/con_files/mask.regions.Ec3.2_O1L75.nc"

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    start = datetime.datetime.now()
    logger.info('Starting at %s', start)
    one_layer = ((0, 300),)
    mesh = Nemo(MESH_FILE, REGIONS_FILE)
    # multiple_layers = ((0, 200), (200, 700), (700, 2000),
    #                    (0, 100), (100, 200),(200, 300), (300, 400),
    #                    (400, 500), (500, 1000),)
    with diagonals.CONFIG.context(use_gpu=True):
        e3t = mesh.get_k_length()
        mask = mesh.get_landsea_mask()
        depth = mesh.get_depth(cell_point='W')
        weights = ohc.get_weights(one_layer, mask, e3t, depth)
        del mask, depth, e3t

        basin_name, basins = load_basins()
        areacello = mesh.get_areacello()
        area = ohc.get_basin_area(areacello, basins)
        del areacello, basins

        thetao = load_thetao()
        thetao += 273.15
        ohc_2D, ohc_1D = ohc.compute(one_layer, weights, thetao, area)
        del weights, thetao, area
        if diagonals.CONFIG.use_gpu:
            device = 'GPU'
        else:
            device = 'CPU'
        save_data(one_layer, basin_name, ohc_2D, ohc_1D, device)
    ellapsed = datetime.datetime.now() - start
    logger.info('Total ellapsed time on the %s: %s', device, ellapsed)


def load_basins():
    regions = iris.load(REGIONS_FILE)
    basins = {}
    basin_name = []
    for region in regions:
        name = region.name()
        if name in ('nav_lat', 'nav_lon'):
            continue
        basin_name.append(name)
        extract_region = region.extract(iris.Constraint(z=1))
        basins[name] = extract_region.data.astype(np.float32)
    return basin_name, basins


def load_areas():
    e1t = iris.load_cube(MESH_FILE, 'e1t').data.astype(np.float32)
    e2t = iris.load_cube(MESH_FILE, 'e2t').data.astype(np.float32)
    return e1t, e2t


def load_thetao():
    thetao = iris.load_cube(DATA_FILE, 'sea_water_potential_temperature')
    thetao_data = thetao.data.astype(np.float32)
    return thetao_data


def save_data(layers, basins, ohc_2d, ohc_1d, device):
    ohc_cube = []
    logger.info('ohc1d length is %s', len(ohc_1d))
    for i, layer in enumerate(layers):
        ohc_cube.append(iris.cube.Cube(ohc_2d[i],
                                       long_name='Ocean heat content'
                                                 ' {0[0]} to {0[1]} meters'
                                       .format(layer)))
        ohc_1s = []
        for j, basin in enumerate(basins):
            ohc_1s.append(iris.cube.Cube(ohc_1d[j][:],
                          long_name='{0}'.format(basin)))
        iris.save(ohc_1s,
                  '/esarchive/scratch/sloosvel/numba_outputs'
                  '/ohc_1D_{1}_{0[0]}_{0[1]}.nc'
                  .format(layer, device), zlib=True)
    iris.save(ohc_cube,
              '/esarchive/scratch/sloosvel/numba_outputs/ohc_{0}.nc'
              .format(device), zlib=True)


if __name__ == '__main__':
    main()
