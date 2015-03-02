# -*- coding: utf-8 -*-

import unittest

from mock import patch

from libavwrapper import AVConv, Input, Output, \
    VideoCodec, AudioCodec, VideoFilter
from libavwrapper.parameters import Parameter


class AVConvTestCase(unittest.TestCase):

    def setUp(self):
        self.patcher = patch('libavwrapper.avconv.Popen')
        popen = self.patcher.start()
        self.instance = popen.return_value

        read_value = list('this is a line\nthis too\n')
        poll = lambda: None if read_value else 0

        def read(*args):
            try:
                return read_value.pop(0).encode('utf-8')
            except IndexError:
                return ''.encode('utf-8')

        self.instance.poll.side_effect = poll
        self.instance.stdout.read.side_effect = read

    def test_input_interface(self):
        input = Input('/old')
        self.assertEqual(list(input), ['-i', '/old'])
        self.assertEqual(input.file_path, '/old')

        parameter = Parameter('-vf', 'x11grab')
        input.append(parameter)
        self.assertEqual(list(input), ['-vf', 'x11grab', '-i', '/old'])
        self.assertEqual(input.pop(), parameter)

        input = input.add_formatparam('-vf', 'x11grab')
        self.assertEqual(input.container_list, [parameter])

    def test_output_interface(self):
        output = Output('/new')
        self.assertEqual(list(output), ['/new'])
        self.assertEqual(output.file_path, '/new')

        parameter = Parameter('-vcodec', 'libx264')
        output.append(parameter)
        self.assertEqual(list(output), ['-vcodec', 'libx264', '/new'])
        self.assertEqual(output.pop(), parameter)

        output = output.add_formatparam('-vcodec', 'libx264')
        self.assertEqual(output.container_list, [parameter])

    def test_codec_interface(self):
        codec = VideoCodec('libx264')
        self.assertEqual(list(codec), ['-vcodec', 'libx264'])

        codec = AudioCodec('ac3')
        self.assertEqual(list(codec), ['-acodec', 'ac3'])

    def test_filter_interface(self):
        filter = VideoFilter()
        filter = filter.blackframe(1, 2).crop(792)
        self.assertEqual(list(filter), ['-vf', 'blackframe=1:2,crop=792'])

        output = Output('/new', filter)
        self.assertEqual(
            list(output), ['-vf', 'blackframe=1:2,crop=792', '/new'])

    def test_avconv_interface(self):
        input = Input('/old')
        output = Output('/new')

        avconv = AVConv('avconv', input, output)
        self.assertEqual(list(avconv), ['avconv', '-i', '/old', '/new'])

        with avconv as process:
            result = list(process.readlines())
            self.assertEqual(result, ['this is a line', 'this too'])

    def tearDown(self):
        self.patcher.stop()


class VideoFilterTestCase(unittest.TestCase):

    def setUp(self):
        self.filter = VideoFilter()

    def prefix(self, *args):
        return ['-vf'] + list(args)

    def test_blackframe(self):
        filter = self.filter.blackframe(10, 100)
        self.assertEqual(list(filter),
            self.prefix('blackframe=10:100'))

    def test_copy(self):
        filter = self.filter.copy()
        self.assertEqual(list(filter),
            self.prefix('copy'))

    def test_crop(self):
        filter = self.filter.crop(100, 100)
        self.assertEqual(list(filter),
            self.prefix('crop=100:100'))

    def test_cropdetect(self):
        filter = self.filter.cropdetect(10)
        self.assertEqual(list(filter),
            self.prefix('cropdetect=10'))

    def test_drawbox(self):
        filter = self.filter.drawbox(10, 10, 10, 10, 'red')
        self.assertEqual(list(filter),
            self.prefix('drawbox=10:10:10:10:red'))

    def test_drawtext(self):
        filter = self.filter.drawtext(fontfile="./font.ttf", text="Title")
        self.assertEqual(list(filter),
            self.prefix('drawtext="fontfile=./font.ttf:text=Title"'))

    def test_fade(self):
        filter = self.filter.fade(10, 10, 10)
        self.assertEqual(list(filter),
            self.prefix('fade=10:10:10'))

    def test_fieldorder(self):
        filter = self.filter.fieldorder(1)
        self.assertEqual(list(filter),
            self.prefix('fieldorder=1'))

    def test_fifo(self):
        filter = self.filter.fifo()
        self.assertEqual(list(filter),
            self.prefix('fifo'))

    def test_format(self):
        filter = self.filter.format('yuv420p')
        self.assertEqual(list(filter),
            self.prefix('format=yuv420p'))

    def test_freior(self):
        filter = self.filter.freior('distort0r', 0.5, 0.01)
        self.assertEqual(list(filter),
            self.prefix('frei0r=distort0r:0.5:0.01'))

    def test_gradfun(self):
        filter = self.filter.gradfun(10, 100)
        self.assertEqual(list(filter),
            self.prefix('gradfun=10:100'))

    def test_hflip(self):
        filter = self.filter.hflip()
        self.assertEqual(list(filter),
            self.prefix('hflip'))

    def test_hqdn3d(self):
        filter = self.filter.hqdn3d(2)
        self.assertEqual(list(filter),
            self.prefix('hqdn3d=2'))

    def test_mp(self):
        filter = self.filter.mp(delogo=None)
        self.assertEqual(list(filter),
            self.prefix('mp="delogo"'))

    def test_negate(self):
        filter = self.filter.negate()
        self.assertEqual(list(filter),
            self.prefix('negate=1'))

    def test_noformat(self):
        filter = self.filter.noformat('yuv420p')
        self.assertEqual(list(filter),
            self.prefix('noformat=yuv420p'))

    def test_null(self):
        filter = self.filter.null()
        self.assertEqual(list(filter),
            self.prefix('null'))

    def test_overlay(self):
        filter = self.filter.overlay(10, 10)
        self.assertEqual(list(filter),
            self.prefix('overlay=10:10'))

    def test_scale(self):
        filter = self.filter.scale(792)
        self.assertEqual(list(filter),
            self.prefix('scale=792:-1'))

    def test_select(self):
        filter = self.filter.select(1)
        self.assertEqual(list(filter),
            self.prefix('select=1'))

    def test_setdar(self):
        filter = self.filter.setdar(16, 9)
        self.assertEqual(list(filter),
            self.prefix('setdar=16:9'))

    def test_setsar(self):
        filter = self.filter.setsar(16, 9)
        self.assertEqual(list(filter),
            self.prefix('setsar=16:9'))

    def test_slicify(self):
        filter = self.filter.slicify(20)
        self.assertEqual(list(filter),
            self.prefix('slicify=20'))

    def test_transpose(self):
        filter = self.filter.transpose(2)
        self.assertEqual(list(filter),
            self.prefix('transpose=2'))

    def test_unsharp(self):
        filter = self.filter.unsharp(1, 2, 3, 4, 5, 6)
        self.assertEqual(list(filter),
            self.prefix('unsharp=1:2:3:4:5:6'))

    def test_vflip(self):
        filter = self.filter.vflip()
        self.assertEqual(list(filter),
            self.prefix('vflip'))

    def test_yadif(self):
        filter = self.filter.yadif()
        self.assertEqual(list(filter),
            self.prefix('yadif=0:-1'))


class VideoCodecTestCase(unittest.TestCase):

    def setUp(self):
        self.codec = VideoCodec('libx264')

    def prefix(self, *args):
        return ['-vcodec', 'libx264'] + list(args)

    def test_bitrate(self):
        codec = self.codec.bitrate('300k')
        self.assertEqual(list(codec),
            self.prefix('-b:v', '300k'))

    def test_frames(self):
        codec = self.codec.frames(100)
        self.assertEqual(list(codec),
            self.prefix('-vframes', '100'))

    def test_fps(self):
        codec = self.codec.fps(24)
        self.assertEqual(list(codec),
            self.prefix('-r', '24'))

    def test_aspect(self):
        codec = self.codec.aspect(16, 9)
        self.assertEqual(list(codec),
            self.prefix('-aspect', '16:9'))

    def test_bitrate_tolerance(self):
        codec = self.codec.bitrate_tolerance(10)
        self.assertEqual(list(codec),
            self.prefix('-bt', '10'))

    def test_max_bitrate(self):
        codec = self.codec.max_bitrate('100k')
        self.assertEqual(list(codec),
            self.prefix('-maxrate', '100k'))

    def test_min_bitrate(self):
        codec = self.codec.min_bitrate('50k')
        self.assertEqual(list(codec),
            self.prefix('-minrate', '50k'))

    def test_buffer_size(self):
        codec = self.codec.buffer_size('20k')
        self.assertEqual(list(codec),
            self.prefix('-bufsize', '20k'))

    def test_pass_number(self):
        codec = self.codec.pass_number(2)
        self.assertEqual(list(codec),
            self.prefix('-pass', '2'))

class AudioCodecTestCase(unittest.TestCase):

    def setUp(self):
        self.codec = AudioCodec('AC3')

    def prefix(self, *args):
        return ['-acodec', 'AC3'] + list(args)

    def test_frames(self):
        codec = self.codec.frames(100)
        self.assertEqual(list(codec),
            self.prefix('-aframes', '100'))

    def test_frequence(self):
        codec = self.codec.frequence(48000)
        self.assertEqual(list(codec),
            self.prefix('-ar', '48000'))

    def test_bitrate(self):
        codec = self.codec.bitrate('320k')
        self.assertEqual(list(codec),
            self.prefix('-b:a', '320k'))

    def test_quality(self):
        codec = self.codec.quality(8)
        self.assertEqual(list(codec),
            self.prefix('-aq', '8'))


if __name__ == '__main__':
    unittest.main()
