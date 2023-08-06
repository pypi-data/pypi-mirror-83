# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------
from __future__ import absolute_import, division

import os
import re
import math
import os.path as op

from pyrocko import config, util
from .srtmgl3 import SRTMGL3, AuthenticationRequired  # noqa
from .etopo1 import ETOPO1
from . import dataset, tile

__doc__ = util.parse_md(__file__)

positive_region = tile.positive_region

earthradius = 6371000.0
r2d = 180./math.pi
d2r = 1./r2d
km = 1000.
d2m = d2r*earthradius
m2d = 1./d2m

topo_data_dir = config.config().topo_dir

srtmgl3 = SRTMGL3(
    name='SRTMGL3',
    data_dir=op.join(topo_data_dir, 'SRTMGL3'))

srtmgl3_d2 = dataset.DecimatedTiledGlobalDataset(
    name='SRTMGL3_D2',
    base=srtmgl3,
    ndeci=2,
    data_dir=op.join(topo_data_dir, 'SRTMGL3_D2'))

srtmgl3_d4 = dataset.DecimatedTiledGlobalDataset(
    name='SRTMGL3_D4',
    base=srtmgl3_d2,
    ndeci=2,
    data_dir=op.join(topo_data_dir, 'SRTMGL3_D4'))

srtmgl3_d8 = dataset.DecimatedTiledGlobalDataset(
    name='SRTMGL3_D8',
    base=srtmgl3_d4,
    ndeci=2,
    ntx=1001,
    nty=1001,
    data_dir=op.join(topo_data_dir, 'SRTMGL3_D8'))

etopo1 = ETOPO1(
    name='ETOPO1',
    data_dir=op.join(topo_data_dir, 'ETOPO1'))

etopo1_d2 = dataset.DecimatedTiledGlobalDataset(
    name='ETOPO1_D2',
    base=etopo1,
    ndeci=2,
    data_dir=op.join(topo_data_dir, 'ETOPO1_D2'))

etopo1_d4 = dataset.DecimatedTiledGlobalDataset(
    name='ETOPO1_D4',
    base=etopo1_d2,
    ndeci=2,
    data_dir=op.join(topo_data_dir, 'ETOPO1_D4'))

etopo1_d8 = dataset.DecimatedTiledGlobalDataset(
    name='ETOPO1_D8',
    base=etopo1_d4,
    ndeci=2,
    data_dir=op.join(topo_data_dir, 'ETOPO1_D8'))

srtmgl3_all = [
    srtmgl3,
    srtmgl3_d2,
    srtmgl3_d4,
    srtmgl3_d8]

etopo1_all = [
    etopo1,
    etopo1_d2,
    etopo1_d4,
    etopo1_d8]

dems = srtmgl3_all + etopo1_all


def make_all_missing_decimated():
    for dem in dems:
        if isinstance(dem, dataset.DecimatedTiledGlobalDataset):
            dem.make_all_missing()


def cpt(name):
    if os.path.exists(name):
        return name

    if not re.match(r'[A-Za-z0-9_]+', name):
        raise Exception('invalid cpt name')

    fn = util.data_file(os.path.join('colortables', '%s.cpt' % name))
    if not os.path.exists(fn):
        raise Exception('cpt file does not exist: %s' % fn)

    return fn


def comparison(region, dems=dems):
    import matplotlib.pyplot as plt

    west, east, south, north = tile.positive_region(region)

    fig = plt.gcf()

    for idem, dem_ in enumerate(dems):
        fig.add_subplot(len(dems), 1, idem+1)
        t = dem_.get(region)
        if t:
            plt.pcolormesh(t.x(), t.y(), t.data)
            plt.title(dem_.name)
            plt.xlim(west, east)
            plt.ylim(south, north)

    plt.show()


class UnknownDEM(Exception):
    pass


def dem_names():
    return [dem.name for dem in dems]


def dem(dem_name):
    for dem in dems:
        if dem.name == dem_name:
            return dem

    raise UnknownDEM(dem_name)


def get(dem_name, region):
    return dem(dem_name).get(region)


def elevation(lat, lon):
    '''
    Get elevation at given point.

    Tries to use SRTMGL3, falls back to ETOPO01 if not available.
    '''

    for dem in ['SRTMGL3', 'ETOPO1']:
        r = get(dem, (lon, lat))
        if r is not None and r != 0:
            return r


def select_dem_names(kind, dmin, dmax, region):
    assert kind in ('land', 'ocean')
    ok = []
    if kind == 'land':
        for dem in srtmgl3_all:
            if dem.is_suitable(region, dmin, dmax):
                ok.append(dem.name)
                break

    for dem in etopo1_all:
        if dem.is_suitable(region, dmin, dmax):
            ok.append(dem.name)
            break

    return ok


if __name__ == '__main__':
    # comparison((-180., 180., -90, 90), dems=[etopo1_d8])
    util.setup_logging('topo', 'info')
    comparison((30, 31, 30, 31), dems=[srtmgl3, srtmgl3_d2])
