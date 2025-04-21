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
import time
from gnuradio import gr

class ADC_output(gr.sync_block):
    """
    docstring for block ADC_output

    requires enabled I2C inferface on raspberry pi. To enable run the following command

    >> sudo raspi-config

    in the config window select "Interface Options" then "I2C", "Yes", then "Finish" 
    """
    def __init__(self, samp_rate = 10, chn=0, i2c_addr=0x4b):
        gr.sync_block.__init__(self,
            name="ADC_output",
            in_sig=None,
            out_sig=[numpy.float32, ])
        
        self.t = 1/samp_rate
            
        self.i2c_addr = i2c_addr
        self.i2c_bus = SMBus(1)


    def work(self, input_items, output_items):
        out = output_items[0]

        nout = 1/self.t

        if(nout < 1):
            nout = 1

        i = 0
        for x in out:
            bus_output = self.i2c_bus.read_byte_data(self.i2c_addr, 1)
            out[i] = bus_output
            i = i + 1
            time.sleep(self.t)
            
        return nout
