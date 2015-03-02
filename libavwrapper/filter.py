# -*- coding: utf-8 -*-
"""
    libavwrapper.filter
    ~~~~~~~~~~~~~~~~~~~~

    This module provides filter methods for video and audio.

    :copyright: (c) 2012 by Mathias Koehler, Conrado Buhrer.
    :license: BSD, see LICENSE for more details.
"""

from itertools import chain
from .parameters import ParameterContainer


class FilterContainer(ParameterContainer):
    """Contains filters which you can append to an output file."""

    def __str__(self):
        return ",".join(FilterContainer.__iter__(self))

    def __iter__(self):
        for key, value in ParameterContainer.iteritems(self):
            if value is not None:
                yield "=".join([key, str(value)])
            else:
                yield key


class VideoFilter(FilterContainer):
    """FilterContainer for Videofilters.

    .. seealso::

        `AVConv documentation, Videofilter`_
            Documentation of all filters and which effect they have.

    .. _AVConv documentation, Videofilter:
        http://libav.org/libavfilter.html#Video-Filters
    """

    def blackframe(self, amount, threshold):
        return self.add_formatparam('blackframe', amount, threshold)

    def copy(self):
        return self.add_parameter('copy', None)

    def crop(self, out_w, out_h=None, x=None, y=None):
        return self.add_formatparam('crop', out_w, out_h, x, y)

    def cropdetect(self, limit=None, round=None, reset=None):
        return self.add_formatparam('cropdetect', limit, round, reset)

    def drawbox(self, x, y, width, height, color):
        return self.add_formatparam('drawbox', x, y, width, height, color)

    def drawtext(self, **kwargs):
        return self.add_formatparam('drawtext', **kwargs)

    def fade(self, type, start, number):
        return self.add_formatparam('fade', type, start, number)

    def fieldorder(self, type):
        if str(type) not in ['0', '1', 'bff', 'tff']:
            raise ValueError('Invalid Parameter for fieldorder. '
                             'Read avconv manual!')
        return self.add_formatparam('fieldorder', type)

    def fifo(self):
        return self.add_parameter('fifo', None)

    def format(self, *args):
        return self.add_formatparam('format', *args)

    def freior(self, name, *args):
        return self.add_formatparam('frei0r', name, *args)

    def gradfun(self, strength='', radius=''):
        return self.add_formatparam('gradfun', strength, radius)

    def hflip(self):
        return self.add_parameter('hflip', None)

    def hqdn3d(self, luma_sp=None, chroma_sp=None,
               luma_tmp=None, chroma_tmp=None):
        return self.add_formatparam('hqdn3d',
            luma_sp, chroma_sp, luma_tmp, chroma_tmp)

    def mp(self, **kwargs):
        return self.add_formatparam('mp', **kwargs)

    def negate(self):
        return self.add_parameter('negate', 1)

    def noformat(self, *args):
        return self.add_formatparam('noformat', *args)

    def null(self):
        return self.add_parameter('null', None)

    def overlay(self, x, y):
        return self.add_formatparam('overlay', x, y)

    def pad(self, width, height, x, y, color):
        return self.add_formatparam('pad', width, height, x, y, color)

    def scale(self, width=-1, height=-1):
        return self.add_formatparam('scale', width, height)

    def select(self, expression):
        return self.add_formatparam('select', expression)

    def setdar(self, x, y):
        return self.add_formatparam('setdar', x, y)

    def setpts(self, expression):
        return self.add_formatparam('setpts', expression)

    def setsar(self, x, y):
        return self.add_formatparam('setsar', x, y)

    def slicify(self, height=16):
        return self.add_formatparam('slicify', height)

    def transpose(self, type):
        if str(type) not in ['0', '1', '2', '3']:
            raise ValueError('Invalid Parameter for transpose. '
                             'Read avconv manual')
        return self.add_formatparam('transpose', type)

    def unsharp(self, *args):
        if len(args) > 6:
            message = 'unsharp() takes exactly 6 positional arguments'
            raise TypeError(message)
        return self.add_formatparam('unsharp', *args)

    def vflip(self):
        return self.add_parameter('vflip', None)

    def yadif(self, mode=0, parity=-1):
        return self.add_formatparam('yadif', mode, parity)

    def __iter__(self):
        return chain(['-vf', FilterContainer.__str__(self)])


class AudioFilter(FilterContainer):
    """FilterContainer for Audiofilters.

    .. seealso::

        `LibAV documentation, Audiofilter`_
            Documentation of all filters and which effect they have.

    .. _LibAV documentation, Audiofilter:
        http://libav.org/libavfilter.html#Audio-Filters
    """

    def null(self):
        """does nothing"""
        self.add_parameter('null', None)
        return self

    def __iter__(self):
        return chain(['-af', FilterContainer.__str__(self)])
