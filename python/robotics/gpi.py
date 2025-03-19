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

gpip = 0

class gpi(gr.sync_block):
    """
    docstring for block gpi
    """
    def __init__(self, platform="pi3", gpio_pin=11):
        gr.sync_block.__init__(self,
            name="gpi",
            in_sig=None,
            out_sig=[numpy.int32, ])
        
        global gpip

        gpip = gpio_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gpi, GPIO.IN)


    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>

        global gpip

        i = 0
        for x in out:
            out[i] = GPIO.input(gpip)
            i = i + 1
            
        return len(output_items[0])