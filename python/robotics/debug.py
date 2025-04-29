#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 SouthCottage Industries.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr

class debug(gr.sync_block):
    """
    docstring for block debug
    """
    def __init__(self, UID = "debug", debug = True):
        gr.sync_block.__init__(self,
            name="debug",
            in_sig=[numpy.float32, ],
            out_sig=[numpy.float32, ])
        self.uid = UID
        self.debug = debug


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        if self.debug:
            for x in in0:
                print("UID ", self.uid, " = ", x)
        out[:] = in0
        return len(output_items[0])
