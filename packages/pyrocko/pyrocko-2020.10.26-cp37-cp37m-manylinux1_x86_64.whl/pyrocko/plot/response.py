# http://pyrocko.org - GPLv3
#
# The Pyrocko Developers, 21st Century
# ---|P------/S----------~Lg----------
'''
This module contains functions to plot instrument response transfer functions
in Bode plot style using Matplotlib.

Example

* :download:`test_response_plot.py </../../examples/test_response_plot.py>`

::

    from pyrocko.plot import response
    from pyrocko.example import get_example_data

    get_example_data('test_response.resp')

    resps, labels = response.load_response_information(
        'test_response.resp', 'resp')

    response.plot(
        responses=resps, labels=labels, filename='test_response.png',
        fmin=0.001, fmax=400., dpi=75.)


.. figure :: /static/test_response.png
    :align: center

    Example response plot
'''
from __future__ import absolute_import

import logging

import numpy as num

from pyrocko import util
from pyrocko import guts


logger = logging.getLogger('plot.response')


def normalize_on_flat(f, tf, factor=10000.):
    df = num.diff(num.log(f))
    tap = 1.0 / (1.0 + factor * (num.diff(num.log(num.abs(tf)))/df)**2)
    return tf / (num.sum(num.abs(tf[1:]) * tap) / num.sum(tap))


def draw(
        response,
        axes_amplitude=None, axes_phase=None,
        fmin=0.01, fmax=100., nf=100,
        normalize=False,
        style={},
        label=None):

    '''Draw instrument response in Bode plot style to given Matplotlib axes

    :param response: instrument response as a
        :py:class:`pyrocko.trace.FrequencyResponse` object
    :param axes_amplitude: :py:class:`matplotlib.axes.Axes` object to use when
        drawing the amplitude response
    :param axes_phase: :py:class:`matplotlib.axes.Axes` object to use when
        drawing the phase response
    :param fmin: minimum frequency [Hz]
    :param fmax: maximum frequency [Hz]
    :param nf: number of frequencies where to evaluate the response
    :param style: :py:class:`dict` with keyword arguments to tune the line
        style
    :param label: string to be passed to the ``label`` argument of
        :py:meth:`matplotlib.axes.Axes.plot`
    '''

    f = num.exp(num.linspace(num.log(fmin), num.log(fmax), nf))
    tf = response.evaluate(f)

    if normalize:
        tf = normalize_on_flat(f, tf)

    ta = num.abs(tf)

    if axes_amplitude:
        axes_amplitude.plot(f, ta, label=label, **style)

    if axes_phase:
        dta = num.diff(num.log(ta))
        iflat = num.argmin(num.abs(num.diff(dta)) + num.abs(dta[:-1]))
        tp = num.unwrap(num.angle(tf))
        ioff = int(num.round(tp[iflat] / (2.0*num.pi)))
        tp -= ioff * 2.0 * num.pi
        axes_phase.plot(f, tp/num.pi, label=label, **style)
    else:
        tp = [0.]

    return (num.min(ta), num.max(ta)), (num.min(tp)/num.pi, num.max(tp)/num.pi)


def setup_axes(axes_amplitude=None, axes_phase=None):
    '''Configure axes in Bode plot style.'''

    if axes_amplitude is not None:
        axes_amplitude.set_ylabel('Amplitude ratio')
        axes_amplitude.set_xscale('log')
        axes_amplitude.set_yscale('log')
        axes_amplitude.grid(True)
        axes_amplitude.axhline(1.0, lw=0.5, color='black')
        if axes_phase is None:
            axes_amplitude.set_xlabel('Frequency [Hz]')
            axes_amplitude.set_xscale('log')
        else:
            axes_amplitude.xaxis.set_ticklabels([])

    if axes_phase is not None:
        axes_phase.set_ylabel('Phase [$\\pi$]')
        axes_phase.set_xscale('log')
        axes_phase.set_xlabel('Frequency [Hz]')
        axes_phase.grid(True)
        axes_phase.axhline(0.0, lw=0.5, color='black')


def plot(
        responses,
        filename=None,
        dpi=100,
        fmin=0.01, fmax=100., nf=100,
        normalize=False,
        fontsize=10.,
        figsize=None,
        styles=None,
        labels=None):

    '''
    Draw instrument responses in Bode plot style.

    :param responses: instrument responses as
        :py:class:`pyrocko.trace.FrequencyResponse` objects
    :param fmin: minimum frequency [Hz]
    :param fmax: maximum frequency [Hz]
    :param nf: number of frequencies where to evaluate the response
    :param normalize: if ``True`` normalize flat part of response to be ``1``
    :param styles: :py:class:`list` of :py:class:`dict` objects  with keyword
        arguments to be passed to matplotlib's
        :py:meth:`matplotlib.axes.Axes.plot` function when drawing the response
        lines. Length must match number of responses.
    :param filename: file name to pass to matplotlib's ``savefig`` function. If
        ``None``, the plot is shown with :py:func:`matplotlib.pyplot.show`.
    :param fontsize: font size in points used in axis labels and legend
    :param figsize: :py:class:`tuple`, ``(width, height)`` in inches
    :param labels: :py:class:`list` of names to show in legend. Length must
        correspond to number of responses.
    '''

    from matplotlib import pyplot as plt
    from pyrocko.plot import mpl_init, mpl_margins, mpl_papersize
    from pyrocko.plot import graph_colors, to01

    mpl_init(fontsize=fontsize)

    if figsize is None:
        figsize = mpl_papersize('a4', 'portrait')

    fig = plt.figure(figsize=figsize)
    labelpos = mpl_margins(
        fig, w=7., h=5., units=fontsize, nw=1, nh=2, hspace=2.)
    axes_amplitude = fig.add_subplot(2, 1, 1)
    labelpos(axes_amplitude, 2., 1.5)
    axes_phase = fig.add_subplot(2, 1, 2)
    labelpos(axes_phase, 2., 1.5)

    setup_axes(axes_amplitude, axes_phase)

    if styles is None:
        styles = [
            dict(color=to01(graph_colors[i % len(graph_colors)]))
            for i in range(len(responses))]
    else:
        assert len(styles) == len(responses)

    if labels is None:
        labels = [None] * len(responses)
    else:
        assert len(labels) == len(responses)

    a_ranges, p_ranges = [], []
    have_labels = False
    for style, resp, label in zip(styles, responses, labels):
        a_range, p_range = draw(
            response=resp,
            axes_amplitude=axes_amplitude,
            axes_phase=axes_phase,
            fmin=fmin, fmax=fmax, nf=nf,
            normalize=normalize,
            style=style,
            label=label)

        if label is not None:
            have_labels = True

        a_ranges.append(a_range)
        p_ranges.append(p_range)

    if have_labels:
        axes_amplitude.legend(loc='lower right', prop=dict(size=fontsize))

    if a_ranges:
        a_ranges = num.array(a_ranges)
        p_ranges = num.array(p_ranges)

        amin, amax = num.min(a_ranges), num.max(a_ranges)
        pmin, pmax = num.min(p_ranges), num.max(p_ranges)

        amin *= 0.5
        amax *= 2.0

        pmin -= 0.5
        pmax += 0.5

        axes_amplitude.set_ylim(amin, amax)
        axes_phase.set_ylim(pmin, pmax)
        axes_amplitude.set_xlim(fmin, fmax)
        axes_phase.set_xlim(fmin, fmax)

    if filename is not None:
        fig.savefig(filename, dpi=dpi)
    else:
        plt.show()


def tts(t):
    if t is None:
        return '?'
    else:
        return util.tts(t, format='%Y-%m-%d')


def load_response_information(
        filename, format, nslc_patterns=None, fake_input_units=None):

    from pyrocko import pz, trace
    from pyrocko.io import resp as fresp

    resps = []
    labels = []
    if format == 'sacpz':
        if fake_input_units is not None:
            raise Exception(
                'cannot guess true input units from plain SAC PZ files')

        zeros, poles, constant = pz.read_sac_zpk(filename)
        resp = trace.PoleZeroResponse(
            zeros=zeros, poles=poles, constant=constant)

        resps.append(resp)
        labels.append(filename)

    elif format == 'pf':
        if fake_input_units is not None:
            raise Exception(
                'cannot guess true input units from plain response files')

        resp = guts.load(filename=filename)
        resps.append(resp)
        labels.append(filename)

    elif format == 'resp':
        for resp in list(fresp.iload_filename(filename)):
            if nslc_patterns is not None and not util.match_nslc(
                    nslc_patterns, resp.codes):
                continue

            units = ''
            if resp.response.instrument_sensitivity:
                s = resp.response.instrument_sensitivity
                if s.input_units and s.output_units:
                    units = ', %s -> %s' % (
                        fake_input_units or s.input_units.name,
                        s.output_units.name)

            resps.append(resp.response.get_pyrocko_response(
                resp.codes, fake_input_units=fake_input_units))

            labels.append('%s (%s.%s.%s.%s, %s - %s%s)' % (
                (filename, ) + resp.codes +
                (tts(resp.start_date), tts(resp.end_date), units)))

    elif format == 'stationxml':
        from pyrocko.fdsn import station as fs

        sx = fs.load_xml(filename=filename)
        for network in sx.network_list:
            for station in network.station_list:
                for channel in station.channel_list:
                    nslc = (
                        network.code,
                        station.code,
                        channel.location_code,
                        channel.code)

                    if nslc_patterns is not None and not util.match_nslc(
                            nslc_patterns, nslc):
                        continue

                    if not channel.response:
                        logger.warn(
                            'no response for channel %s.%s.%s.%s given.'
                            % nslc)
                        continue

                    units = ''
                    if channel.response.instrument_sensitivity:
                        s = channel.response.instrument_sensitivity
                        if s.input_units and s.output_units:
                            units = ', %s -> %s' % (
                                fake_input_units or s.input_units.name,
                                s.output_units.name)

                    resps.append(channel.response.get_pyrocko_response(
                        nslc, fake_input_units=fake_input_units))

                    labels.append(
                        '%s (%s.%s.%s.%s, %s - %s%s)' % (
                            (filename, ) + nslc +
                            (tts(channel.start_date),
                             tts(channel.end_date),
                             units)))

    return resps, labels


if __name__ == '__main__':
    import sys
    from optparse import OptionParser

    util.setup_logging('pyrocko.plot.response.__main__', 'warning')

    usage = 'python -m pyrocko.plot.response <filename> ... [options]'

    description = '''Plot instrument responses (transfer functions).'''

    allowed_formats = ['sacpz', 'resp', 'stationxml', 'pf']

    parser = OptionParser(
        usage=usage,
        description=description,
        formatter=util.BetterHelpFormatter())

    parser.add_option(
        '--format',
        dest='format',
        default='sacpz',
        choices=allowed_formats,
        help='assume input files are of given FORMAT. Choices: %s' % (
            ', '.join(allowed_formats)))

    parser.add_option(
        '--fmin',
        dest='fmin',
        type='float',
        default=0.01,
        help='minimum frequency [Hz], default: %default')

    parser.add_option(
        '--fmax',
        dest='fmax',
        type='float',
        default=100.,
        help='maximum frequency [Hz], default: %default')

    parser.add_option(
        '--normalize',
        dest='normalize',
        action='store_true',
        help='normalize response to be 1 on flat part')

    parser.add_option(
        '--save',
        dest='filename',
        help='save figure to file with name FILENAME')

    parser.add_option(
        '--dpi',
        dest='dpi',
        type='float',
        default=100.,
        help='DPI setting for pixel image output, default: %default')

    parser.add_option(
        '--patterns',
        dest='nslc_patterns',
        metavar='NET.STA.LOC.CHA,...',
        help='show only responses of channels matching any of the given '
             'patterns')

    parser.add_option(
        '--fake-input-units',
        dest='fake_input_units',
        choices=['M', 'M/S', 'M/S**2'],
        metavar='UNITS',
        help='show converted response for given input units, choices: '
             '["M", "M/S", "M/S**2"]')

    (options, args) = parser.parse_args(sys.argv[1:])

    if len(args) == 0:
        parser.print_help()
        sys.exit(1)

    fns = args

    resps = []
    labels = []

    for fn in fns:

        if options.nslc_patterns is not None:
            nslc_patterns = options.nslc_patterns.split(',')
        else:
            nslc_patterns = None

        resps_this, labels_this = load_response_information(
            fn, options.format, nslc_patterns,
            fake_input_units=options.fake_input_units)

        resps.extend(resps_this)
        labels.extend(labels_this)

    plot(
        resps,
        fmin=options.fmin, fmax=options.fmax, nf=200,
        normalize=options.normalize,
        labels=labels, filename=options.filename, dpi=options.dpi)
