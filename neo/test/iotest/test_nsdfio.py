# -*- coding: utf-8 -*-
"""
Tests of neo.io.NSDFIO
"""

# needed for python 3 compatibility
from __future__ import absolute_import, division

import numpy as np
import quantities as pq
from datetime import datetime
from os import remove

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from neo.io.nsdfio import HAVE_NSDF, NSDFIO
from neo.test.iotest.common_io_test import BaseTestIO
from neo.core import AnalogSignal, Segment, Block
from neo.test.tools import assert_same_attributes, assert_same_annotations


@unittest.skipUnless(HAVE_NSDF, "Requires NSDF")
class CommonTests(BaseTestIO, unittest.TestCase):
    ioclass = NSDFIO
    read_and_write_is_bijective = False


@unittest.skipUnless(HAVE_NSDF, "Requires NSDF")
class NSDFIOTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'nsdfio_testfile.h5'
        self.io = NSDFIO(self.filename)

    def tearDown(self):
        remove(self.filename)

    def compare_list_of_blocks(self, blocks1, blocks2):
        assert len(blocks1) == len(blocks2)
        for block1, block2 in zip(blocks1, blocks2):
            self.compare_blocks(block1, block2)

    def compare_blocks(self, block1, block2):
        self.compare_objects(block1, block2)
        self._compare_blocks_children(block1, block2)

    def _compare_blocks_children(self, block1, block2):
        assert len(block1.segments) == len(block2.segments)
        for segment1, segment2 in zip(block1.segments, block2.segments):
            self.compare_segments(segment1, segment2)

    def compare_segments(self, segment1, segment2):
        self.compare_objects(segment1, segment2)
        self._compare_segments_children(segment1, segment2)

    def _compare_segments_children(self, segment1, segment2):
        assert len(segment1.analogsignals) == len(segment2.analogsignals)
        for signal1, signal2 in zip(segment1.analogsignals, segment2.analogsignals):
            self.compare_analogsignals(signal1, signal2)

    def compare_analogsignals(self, signal1, signal2):
        self.compare_objects(signal1, signal2)

    def compare_objects(self, object1, object2):
        assert object1.__class__.__name__ == object2.__class__.__name__
        assert_same_attributes(object1, object2)
        assert_same_annotations(object1, object2)

    def create_list_of_blocks(self):
        blocks = []

        for i in range(3):
            blocks.append(self.create_block(name = 'Block #{}'.format(i)))

        return blocks

    def create_block(self, name = None):
        block = Block()

        self._assign_basic_attributes(block, name = name)
        self._assign_datetime_attributes(block)
        self._assign_index_attribute(block)

        self._create_block_children(block)

        self._assign_annotations(block)

        return block

    def _create_block_children(self, block):
        for i in range(5):
            block.segments.append(self.create_segment(block, name = 'Segment #{}'.format(i)))

    def create_segment(self, parent = None, name = None):
        segment = Segment()

        segment.block = parent

        self._assign_basic_attributes(segment, name = name)
        self._assign_datetime_attributes(segment)
        self._assign_index_attribute(segment)

        self._create_segment_children(segment)

        self._assign_annotations(segment)

        return segment

    def _create_segment_children(self, segment):
        for i in range(5):
            segment.analogsignals.append(self.create_analogsignal(segment, name = 'Signal #{}'.format(i * 3)))
            segment.analogsignals.append(self.create_analogsignal2(segment, name = 'Signal #{}'.format(i * 3 + 1)))
            segment.analogsignals.append(self.create_analogsignal3(segment, name = 'Signal #{}'.format(i * 3 + 2)))

    def _assign_index_attribute(self, object):
        object.index = 12

    def _assign_datetime_attributes(self, object):
        object.file_datetime = datetime(2017, 6, 11, 14, 53, 23)
        object.rec_datetime = datetime(2017, 5, 29, 13, 12, 47)

    def create_analogsignal(self, parent = None, name = None):
        signal = AnalogSignal([[1, 2], [2, 3], [3, 4]], units='mV',
                              sampling_rate = 100 * pq.Hz, t_start = 2 * pq.min)

        signal.segment = parent

        self._assign_basic_attributes(signal, name = name)

        self._assign_annotations(signal)

        return signal

    def create_analogsignal2(self, parent = None, name = None):
        signal = AnalogSignal([[1], [2], [3], [4], [5]], units='mA',
                              sampling_period = 0.5 * pq.ms)

        signal.segment = parent

        self._assign_annotations(signal)

        return signal

    def create_analogsignal3(self, parent = None, name = None):
        signal = AnalogSignal([[1, 2, 3], [4, 5, 6]], units='mV',
                              sampling_rate = 2 * pq.kHz, t_start = 100 * pq.s)

        signal.segment = parent

        self._assign_basic_attributes(signal, name = name)

        return signal

    def _assign_basic_attributes(self, object, name = None):
        if name is None:
            object.name = 'neo object'
        else:
            object.name = name
        object.description = 'Example of neo object'
        object.file_origin = 'datafile.pp'

    def _assign_annotations(self, object):
        object.annotations = {'str' : 'value',
                              'int' : 56,
                              'float' : 5.234}


@unittest.skipUnless(HAVE_NSDF, "Requires NSDF")
class NSDFIOTestWriteThenRead(NSDFIOTest):
    def test_write_then_read_block(self):
        block = self.create_block()
        self.io.write_block(block)
        block2 = self.io.read_block()
        self.compare_blocks(block, block2)

    def test_write_then_read_list_of_blocks(self):
        blocks = self.create_list_of_blocks()
        self.io.write(blocks)
        blocks2 = self.io.read()
        self.compare_list_of_blocks(blocks, blocks2)


if __name__ == "__main__":
    unittest.main()