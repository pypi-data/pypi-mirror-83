import logging
import datetime
import numpy as np

import iris
import iris.cube
import iris.analysis
import iris.coords
import iris.coord_categorisation
from iris.experimental.equalise_cubes import equalise_attributes

import diagonals
import diagonals.siasie as siasie
from diagonals.mesh_helpers.nemo import Nemo


MESH_FILE = "/esarchive/autosubmit/con_files/mesh_mask_nemo.Ec3.2_O1L75.nc"
REGIONS_FILE = "/esarchive/autosubmit/con_files/mask.regions.Ec3.2_O1L75.nc"
SIC_FILE = "/esarchive/exp/ecearth/a1tr/cmorfiles/CMIP/EC-Earth-Consortium"\
           "/EC-Earth3/historical/r24i1p1f1/SImon/siconc/gn/v20190312"\
           "/siconc_SImon_EC-Earth3_historical_r24i1p1f1_gn_185001-185012.nc"

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(level=logging.INFO)
    start = datetime.datetime.now()
    logger.info('Starting at %s', start)
    mesh = Nemo(MESH_FILE, REGIONS_FILE)
    with diagonals.CONFIG.context(use_gpu=True):
        areacello = mesh.get_areacello()
        gphit = mesh.get_grid_latitude()
        cube_sic = load_cube(SIC_FILE, 'sea_ice_area_fraction')
        sic_slices = load_data(cube_sic)
        masks = load_masks(REGIONS_FILE)
        extn, exts, arean, areas = siasie.compute(gphit, areacello,
                                                  sic_slices, masks)
        del areacello, gphit, cube_sic, sic_slices
        if diagonals.CONFIG.use_gpu:
            device = 'GPU'
        else:
            device = 'CPU'
        save_cubes(extn, exts, arean, areas, masks, device)
    ellapsed = datetime.datetime.now() - start
    logger.info('Total ellapsed time on the %s: %s', device, ellapsed)


def save_cubes(extn, exts, arean, areas, basins, device):
    cubes_extn = iris.cube.CubeList()
    cubes_exts = iris.cube.CubeList()
    cubes_arean = iris.cube.CubeList()
    cubes_areas = iris.cube.CubeList()
    for time in extn.keys():
        for basin in basins.keys():
            cube_extn = iris.cube.Cube(extn[time][basin] / 1e12)
            cube_exts = iris.cube.Cube(exts[time][basin] / 1e12)
            cube_arean = iris.cube.Cube(arean[time][basin] / 1e12)
            cube_areas = iris.cube.Cube(areas[time][basin] / 1e12)

            cube_extn.add_aux_coord(iris.coords.AuxCoord(time, 'time'))
            cube_exts.add_aux_coord(iris.coords.AuxCoord(time, 'time'))
            cube_arean.add_aux_coord(iris.coords.AuxCoord(time, 'time'))
            cube_areas.add_aux_coord(iris.coords.AuxCoord(time, 'time'))

            cube_extn.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
            cube_exts.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
            cube_arean.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))
            cube_areas.add_aux_coord(iris.coords.AuxCoord(basin, 'region'))

            cubes_extn.append(cube_extn)
            cubes_exts.append(cube_exts)
            cubes_arean.append(cube_arean)
            cubes_areas.append(cube_areas)

    iris.save(cubes_extn.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/extn_{0}.nc'.format(device), zlib=True)
    iris.save(cubes_exts.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/exts_{0}.nc'.format(device), zlib=True)
    iris.save(cubes_arean.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/arean_{0}.nc'.format(device), zlib=True)
    iris.save(cubes_areas.merge_cube(), '/esarchive/scratch/sloosvel/'
              'numba_outputs/areas_{0}.nc'.format(device), zlib=True)


def load_data(cube_sic):
    sic_slices = []
    for sic_data in cube_sic.slices_over('time'):
        sic_data.data = np.ma.filled(sic_data.data, 0.0).astype(np.float32)
        sic_slices.append(sic_data)
    return sic_slices


def load_cube(filepath, variable):
    cubes = iris.load(filepath, variable)
    if len(cubes) > 1:
        equalise_attributes(cubes)
        iris.util.unify_time_units(cubes)
        cube = cubes.concatenate_cube()
    else:
        cube = cubes[0]
    return cube


def load_masks(filepath):
    basins = {}
    cubes = iris.load(filepath)
    for cube in cubes:
        name = cube.name()
        if name in ('nav_lat', 'nav_lon'):
            continue
        cube = cube.extract(iris.Constraint(z=1))
        basins[name] = cube.data.astype(np.float32)
    return basins


if __name__ == '__main__':
    main()
