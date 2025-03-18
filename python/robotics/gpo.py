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

gpop = 0

class gpo(gr.sync_block):
    """
    docstring for block gpo
    """

    def __init__(self, platform="pi3", gpio_pin=11):
        gr.sync_block.__init__(self,
            name="gpio",
            in_sig=[numpy.float32, ],
            out_sig=None)
        gpop = gpio_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(11, GPIO.OUT)
#        GPIO.output(gpop, GPIO.LOW)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        
#        for x in in0:
#            GPIO.output(gpop, x != 0)

        if any(in0) == 1:
            GPIO.output(11, GPIO.HIGH)
        else:
            GPIO.output(11,GPIO.LOW)
        return len(input_items[0])
