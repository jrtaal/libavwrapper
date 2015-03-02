# -*- coding: utf-8 -*-
"""
    libavwrapper.codec
    ~~~~~~~~~~~~~~~~~~~

    This module provides an Audio and VideoCodec
    class with methods to change various settings.

    :copyright: (c) 2012 by Mathias Koehler, Conrado Buhrer.
    :license: BSD, see LICENSE for more details.
"""

from itertools import chain
from .parameters import ParameterContainer


NO_AUDIO = ('-an',)
NO_VIDEO = ('-vn',)


class Codec(ParameterContainer):
    """ Container for Codecs-Settings"""

    def __init__(self, name, *args):
        self.name = name
        ParameterContainer.__init__(self, *args)

    def __copy__(self):
        return type(self)(self.name, *list(self.container_list))

class VideoCodec(Codec):
    """This represent an video codec.

    You can append this class to an :class:`Output` object to tell
    which AVConv which codec you want.
    """

    def bitrate(self, bitrate):
        return self.add_formatparam('-b:v', str(bitrate))
        

    def frames(self, number):
        return self.add_formatparam('-vframes', str(number))
        
    def fps(self, fps):
        return self.add_formatparam('-r', str(fps))
        
    def keyint_min(self, keyint):
        return self.add_formatparam('-keyint_min', str(keyint))
        

    def gopsize(self, gopsize):
        return self.add_formatparam('-g', str(gopsize))
                
    def size(self, x, y):
        filter = "{x}x{y}".format(x=x, y=y)
        return self.add_formatparam('-s', filter)
        
    def aspect(self, x, y):
        return self.add_formatparam('-aspect', x, y)
        
    def bitrate_tolerance(self, tolerance):
        return self.add_formatparam('-bt', str(tolerance))
        
    def max_bitrate(self, rate):
        return self.add_formatparam('-maxrate', str(rate))
        
    def min_bitrate(self, rate):
        return self.add_formatparam('-minrate', str(rate))
        
    def buffer_size(self, size):
        return self.add_formatparam('-bufsize', str(size))
       
    def pass_number(self, number):
        return self.add_formatparam('-pass', str(number))
        
    def __iter__(self):
        return chain(['-vcodec', self.name], Codec.__iter__(self))


class AudioCodec(Codec):
    """This represent an audio codec.

    You can append this class to an :class:`Output` object to tell
    which AVConv which codec you want.
    """

    def frames(self, number):
        return self.add_formatparam('-aframes', str(number))
        
    def frequence(self, freq):
        return self.add_formatparam('-ar', str(freq))

    def bitrate(self, rate):
        return self.add_formatparam('-b:a', str(rate))

    def quality(self, number):
        return self.add_formatparam('-aq', str(number))

    def channels(self, number):
        return self.add_formatparam('-ac', str(number))

    def __iter__(self):
        return chain(['-acodec', self.name], Codec.__iter__(self))
