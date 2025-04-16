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

class servo(gr.sync_block):
    """
    docstring for block gpo
    """

    def __init__(self, gpio_pin=12, frequency=50):
        gr.sync_block.__init__(self,
            name="servo",
            in_sig=[numpy.int32, ],
            out_sig=None)
        self.gpop = gpio_pin
        self.freq = frequency
        self.duty_cycle = 2.5
        self.angle = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpop, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpop, self.freq)
        self.pwm.start(self.duty_cycle)
        
    def change_frequency(self,new_freq):
        self.freq = new_freq
        
    def set_angle(self, angle):
        if angle > 180 or angle < 0:
            return
        self.duty_cycle = (((angle/180.0 * 2) + 0.5) / 20) * 100
        print("angle = " + str(angle) + ". duty cycle = " + str(self.duty_cycle))

    def work(self, input_items, output_items):
        in0 = input_items[0]

        for x in in0:
            if x != self.angle:
                self.angle = x
                self.set_angle(self.angle)
                self.pwm.ChangeDutyCycle(self.duty_cycle)
                

        return len(input_items[0])
