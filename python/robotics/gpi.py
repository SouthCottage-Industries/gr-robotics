#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 SouthCottage Industries.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
import RPi.GPIO as GPIO # type: ignore
from gnuradio import gr
import time

gpip = 0

class gpi(gr.sync_block):
    """
    docstring for block gpi
    """
    def __init__(self, platform="pi3", samp_rate = 10, gpio_pin=11):
        gr.sync_block.__init__(self,
            name="gpi",
            in_sig=None,
            out_sig=[numpy.int32, ])
        
        self.gpip = gpio_pin
        self.t = 1/samp_rate

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gpi, GPIO.IN)


    def work(self, input_items, output_items):
        # <+signal processing here+>

        out = GPIO.input(self.gpip)
        time.sleep(self.t)
            
            
        return len(1)