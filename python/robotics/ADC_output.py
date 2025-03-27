#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 SouthCottage Industries.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
import RPi.GPIO as GPIO 
from gnuradio import gr

class ADC_output(gr.sync_block):
    """
    docstring for block ADC_output
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="ADC_output",
            in_sig=[<+numpy.float32+>, ],
            out_sig=[<+numpy.float32+>, ])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = in0
        return len(output_items[0])
