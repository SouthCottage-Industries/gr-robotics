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
freq = 0
dc = 0
global pwm


class gpo_pwm(gr.sync_block):
    """
    docstring for block gpo_pwm
    """
    def __init__(self, platform="pi3", gpio_pin=11, frequency=100):
        gr.sync_block.__init__(self,
            name="gpo_pwm",
            in_sig=[<+numpy.float32+>, ],
            out_sig=None)
        gpop = gpio_pin
        freq = frequency
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(gpop, GPIO.OUT)
        pwm = GPIO.PWM(gpop, freq)
        pwm.start(dc)
        

    def change_frequency(new_freq):
        freq = new_freq

    def work(self, input_items, output_items):
        in0 = input_items[0]
        
        for x in in0:
            if x*100 != dc:
                dc = x*100
                pwm.ChangeDutyCycle(dc)
            

        return len(input_items[0])
