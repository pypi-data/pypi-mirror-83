import numpy as num
import os

from pyrocko import moment_tensor, model
from pyrocko.gui.snuffling import Snuffling, Param, Choice, EventMarker
from pyrocko import gf

km = 1000.


class Seismosizer(Snuffling):
    '''
    Generate synthetic traces on the fly
    ====================================

    Activate an event (press `e`) to generate synthetic waveforms for it.
    If no stations have been loaded pripor to execution, two stations will be
    generated at lat/lon = (5., 0) and (-5., 0.).

    All geometrical units are kilometers (if not stated otherwise).
    `GF Stores` will be loaded on start from `gf_store_superdirs` defined
    in your pyrocko config file located at `$HOME/.pyrocko/config.pf`.
    '''

    def __init__(self):
        Snuffling.__init__(self)
        self.stf_types = ['half sin', 'triangular', 'boxcar', 'None']
        self.stf_instances = [gf.HalfSinusoidSTF(), gf.TriangularSTF(),
                              gf.BoxcarSTF(), None]

    def setup(self):
        '''Customization of the snuffling.'''

        self.set_name('Seismosizer')
        self.add_parameter(
            Param('Time', 'time', 0.0, -50., 50.))
        # self.add_parameter(
        #     Param('Latitude', 'lat', 0.0, -90., 90.))
        # self.add_parameter(
        #     Param('Longitude', 'lon', 0.0, -180., 180.))
        self.add_parameter(
            Param('North shift', 'north_km', 0.0, -50., 50.))
        self.add_parameter(
            Param('East shift', 'east_km', 0.0, -50., 50.))
        self.add_parameter(
            Param('Depth', 'depth_km', 10.0, 0.0, 600.0))
        self.add_parameter(
            Param('Magnitude', 'magnitude', 6.0, 0.0, 10.0))
        self.add_parameter(
            Param('Strike', 'strike', 0., -180., 180.))
        self.add_parameter(
            Param('Dip', 'dip', 90., 0., 90.))
        self.add_parameter(
            Param('Rake', 'rake', 0., -180., 180.))
        self.add_parameter(
            Param('Length', 'length', 0., 0., 1000*km))
        self.add_parameter(
            Param('Width', 'width', 0., 0., 500*km))
        self.add_parameter(
            Param('Nucleation X', 'nucleation_x', -1., -1., 1.))
        self.add_parameter(
            Param('Rupture velocity', 'velocity', 3500.0, 0.0, 5000.0))
        self.add_parameter(
            Param('STF duration', 'stf_duration', 0., 0., 20.))
        self.add_parameter(
            Choice('STF type', 'stf_type', self.stf_types[0], self.stf_types))
        self.add_parameter(
            Choice('GF Store', 'store_id',
                   '<not loaded yet>', ['<not loaded yet>']))
        self.add_parameter(
            Choice('Waveform type', 'waveform_type', 'Displacement [m]',
                   ['Displacement [m]',
                    'Displacement [nm]',
                    'Velocity [m/s]',
                    'Velocity [nm/s]',
                    'Acceleration [m/s^2]',
                    'Acceleration [nm/s^2]']))

        self.add_trigger('Set Engine', self.set_engine)
        self.add_trigger('Set Params from Event', self.mechanism_from_event)
        self.add_trigger('Add Stores', self.add_store)

        self.store_ids = None
        self.offline_config = None
        self._engine = None

    def panel_visibility_changed(self, bool):
        if bool:
            if self._engine is None:
                self.set_engine()

    def set_engine(self):
        self._engine = None
        self.store_ids = self.get_store_ids()
        if self.store_ids == []:
            return

        self.set_parameter_choices('store_id', self.store_ids)
        self.store_id = self.store_ids[0]

    def get_engine(self):
        if not self._engine:
            self._engine = gf.LocalEngine(use_config=True)

        return self._engine

    def get_store_ids(self):
        return self.get_engine().get_store_ids()

    def get_stf(self):
        stf = dict(zip(self.stf_types, self.stf_instances))[self.stf_type]
        if stf is not None:
            stf.duration = self.stf_duration

        return stf

    def call(self):
        '''Main work routine of the snuffling.'''
        self.cleanup()

        # get time range visible in viewer
        viewer = self.get_viewer()

        event = viewer.get_active_event()
        if event:
            event, stations = self.get_active_event_and_stations(
                missing='warn')
        else:
            # event = model.Event(lat=self.lat, lon=self.lon)
            event = model.Event(lat=0., lon=0.)
            stations = []

        stations = self.get_stations()

        s2c = {}
        for traces in self.chopper_selected_traces(fallback=True,
                                                   mode='visible'):
            for tr in traces:
                net, sta, loc, cha = tr.nslc_id
                ns = net, sta
                if ns not in s2c:
                    s2c[ns] = set()

                s2c[ns].add((loc, cha))

        if not stations:
            stations = []
            for (lat, lon) in [(5., 0.), (-5., 0.)]:
                s = model.Station(station='(%g, %g)' % (lat, lon),
                                  lat=lat, lon=lon)
                stations.append(s)
                viewer.add_stations(stations)

        for s in stations:
            ns = s.nsl()[:2]
            if ns not in s2c:
                s2c[ns] = set()

            for cha in 'NEZ':
                s2c[ns].add(('', cha))

        source = gf.RectangularSource(
            time=event.time+self.time,
            lat=event.lat,
            lon=event.lon,
            north_shift=self.north_km*km,
            east_shift=self.east_km*km,
            depth=self.depth_km*km,
            magnitude=self.magnitude,
            strike=self.strike,
            dip=self.dip,
            rake=self.rake,
            length=self.length,
            width=self.width,
            nucleation_x=self.nucleation_x,
            velocity=self.velocity,
            stf=self.get_stf())

        source.regularize()

        m = EventMarker(source.pyrocko_event())
        self.add_marker(m)

        targets = []

        if self.store_id == '<not loaded yet>':
            self.fail('Select a GF Store first')

        for station in stations:

            nsl = station.nsl()
            if nsl[:2] not in s2c:
                continue

            for loc, cha in s2c[nsl[:2]]:

                target = gf.Target(
                    codes=(
                        station.network,
                        station.station,
                        loc + '-syn',
                        cha),
                    quantity='displacement',
                    lat=station.lat,
                    lon=station.lon,
                    depth=station.depth,
                    store_id=self.store_id,
                    optimization='enable',
                    interpolation='nearest_neighbor')

                _, bazi = source.azibazi_to(target)

                if cha.endswith('T'):
                    dip = 0.
                    azi = bazi + 270.
                elif cha.endswith('R'):
                    dip = 0.
                    azi = bazi + 180.
                elif cha.endswith('1'):
                    dip = 0.
                    azi = 0.
                elif cha.endswith('2'):
                    dip = 0.
                    azi = 90.
                else:
                    dip = None
                    azi = None

                target.azimuth = azi
                target.dip = dip

                targets.append(target)

        req = gf.Request(
            sources=[source],
            targets=targets)

        req.regularize()

        try:
            resp = self.get_engine().process(req)
        except (gf.meta.OutOfBounds, gf.store_ext.StoreExtError)as e:
            self.fail(e)

        traces = resp.pyrocko_traces()

        if self.waveform_type.startswith('Velocity'):
            for tr in traces:
                tr.set_ydata(num.diff(tr.ydata) / tr.deltat)

        elif self.waveform_type.startswith('Acceleration'):
            for tr in traces:
                tr.set_ydata(num.diff(num.diff(tr.ydata)) / tr.deltat**2)

        if self.waveform_type.endswith('[nm]') or \
                self.waveform_type.endswith('[nm/s]') or \
                self.waveform_type.endswith('[nm/s^2]'):

            for tr in traces:
                tr.set_ydata(tr.ydata * 1e9)

        self.add_traces(traces)

    def mechanism_from_event(self):

        event = self.get_viewer().get_active_event()

        if event is None:
            self.fail('No active event set.')

        if event.moment_tensor is not None:
            strike, dip, slip_rake = event.moment_tensor\
                .both_strike_dip_rake()[0]
            moment = event.moment_tensor.scalar_moment()
            self.set_parameter('magnitude',
                               moment_tensor.moment_to_magnitude(moment))
            self.set_parameter('strike', strike)
            self.set_parameter('dip', dip)
            self.set_parameter('rake', slip_rake)
        else:
            self.warn(
                'No source mechanism available for event %s. '
                'Only setting location' % event.name)

        self.set_parameter('lat', event.lat)
        self.set_parameter('lon', event.lon)
        self.set_parameter('depth_km', event.depth/km)

    def add_store(self):
        self._engine = self.get_engine()
        superdir = self.input_directory()
        if self.has_config(superdir):
            self._engine.store_dirs.append(superdir)
        else:
            self._engine.store_superdirs.append(superdir)
        self.store_ids = self._engine.get_store_ids()

        self.set_parameter_choices('store_id', self.store_ids)

    def has_config(self, directory):
        return 'config' in os.listdir(directory)


def __snufflings__():
    '''Returns a list of snufflings to be exported by this module.'''
    return [Seismosizer()]
