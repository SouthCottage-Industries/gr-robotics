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

class gpo_pwm(gr.sync_block):
    """
    docstring for block gpo_pwm
    """
    def __init__(self, platform="pi3", samp_rate = 10, gpio_pin=11, frequency=100, dc=0):
        gr.sync_block.__init__(self,
            name="gpo_pwm",
            in_sig=[numpy.float32, ],
            out_sig=None)
        
        self.gpop = gpio_pin
        self.freq = frequency
        self.dc = dc
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpop, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpop, self.freq)
        self.pwm.start(self.dc)
        self.t = 1/samp_rate
        

    def change_frequency(self,new_freq):
        self.freq = new_freq

    def work(self, input_items, output_items):
        in0 = input_items[0]

        for x in in0:
            if x*100 != self.dc:
                self.dc = x*100
                self.pwm.ChangeDutyCycle(self.dc)
                time.sleep(self.t)
            

        return len(input_items[0])
