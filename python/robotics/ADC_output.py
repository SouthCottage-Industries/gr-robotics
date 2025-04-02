#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 SouthCottage Industries.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
import RPi.GPIO as GPIO 
from smbus2 import SMBus
from gnuradio import gr

class ADC_output(gr.sync_block):
    """
    docstring for block ADC_output
    """
    def __init__(self, chn=0, i2c_addr=0x4b):
        gr.sync_block.__init__(self,
            name="ADC_output",
            in_sig=None,
            out_sig=[numpy.float32, ])
            
        self.i2c_addr = i2c_addr


    def work(self, input_items, output_items):
        out = output_items[0]

        i2c_bus = SMBus(1)
        bus_output = i2c_bus.read_byte_data(self.i2c_addr, 1)

        i = 0
        for x in out:
            out[i] = bus_output
            i = i + 1
            
        return len(output_items[0])
