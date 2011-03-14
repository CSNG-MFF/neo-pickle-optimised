# encoding: utf-8
"""
Tests of io.base
"""

from __future__ import division

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from neo.core import objectlist
from neo.io.exampleio import ExampleIO

import numpy

class TestExampleIO(unittest.TestCase):
    def test_read_segment_lazy(self):
        r = ExampleIO( filename = None)
        seg = r.read_segment(cascade = True, lazy = True)
        for ana in seg._analogsignals:
            self.assertEqual(ana.size, 0)
            assert hasattr(ana, '_data_description')
        for st in seg._spiketrains:
            self.assertEqual(st.size, 0)
            assert hasattr(st, '_data_description')
        
        seg = r.read_segment(cascade = True, lazy = False)
        for ana in seg._analogsignals:
            self.assertNotEqual(ana.size, 0)
        for st in seg._spiketrains:
            self.assertNotEqual(st.size, 0)
        
    def test_read_segment_cascade(self):
        r = ExampleIO( filename = None)
        seg = r.read_segment(cascade = False)
        self.assertEqual( len(seg._analogsignals), 0)
        seg = r.read_segment(cascade = True , num_analogsignal = 4)
        self.assertEqual( len(seg._analogsignals), 4)

    
    def test_read_analogsignal(self):
        r = ExampleIO( filename = None)
        ana = r.read_analogsignal( lazy = False,segment_duration = 15., t_start = -1)
        

        
    

    def read_spiketrain(self):
        r = ExampleIO( filename = None)
        st = r.read_spiketrain( lazy = False,)




if __name__ == "__main__":
    unittest.main()
