# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------
from __future__ import absolute_import, division, print_function

import numpy as num
from ..base import Generator


class TargetGenerator(Generator):

    def get_time_range(self, sources):
        ''' Get the target's time range.

        In the easiest case this is the sources' time range, yet for waveform
        targets we have to consider vmin, vmax
        '''
        times = num.array([source.time for source in sources],
                          dtype=num.float)

        return num.min(times), num.max(times)

    def get_targets(self):
        ''' Returns a list of targets, used class-internally to forward model.
        '''
        return []

    def get_stations(self):
        return []

    def get_onsets(self, engine, sources, tmin=None, tmax=None):
        return []

    def get_waveforms(self, engine, sources, tmin=None, tmax=None):
        return []

    def get_insar_scenes(self, engine, sources, tmin=None, tmax=None):
        return []

    def get_gnss_campaigns(self, engine, sources, tmin=None, tmax=None):
        return []

    def ensure_data(self, engine, sources, path, tmin=None, tmax=None):
        pass

    def add_map_artists(self, engine, sources, automap):
        pass


class NoiseGenerator(Generator):
    pass
