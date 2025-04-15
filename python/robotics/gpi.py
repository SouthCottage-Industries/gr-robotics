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
        GPIO.setup(self.gpip, GPIO.IN)


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>

        #This is the cleanest way I know to create a reasonable limit 
        #   to the number of samples.
        # TODO: find better way to limit output_item size for a given sample rate
         
        nout = int(1/self.t)

        i = 0
        for x in range(nout):
            out[i] = GPIO.input(self.gpip)
            i = i + 1
            time.sleep(self.t)

        return nout