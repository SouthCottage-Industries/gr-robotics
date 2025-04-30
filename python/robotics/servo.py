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

class servo(gr.sync_block):
    """
    docstring for block gpo
    """

    def __init__(self, samp_rate=10, gpio_pin=12, frequency=50):
        gr.sync_block.__init__(self,
            name="servo",
            in_sig=None,
            out_sig=None)
        self.t = 1/samp_rate
        self.gpop = gpio_pin
        self.freq = frequency
        self.duty_cycle = 2.5
        self.angle = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpop, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpop, self.freq)
        self.pwm.start(self.duty_cycle)

        self.message_port_register_in(pmt.intern('Set Angle'))
        self.set_msg_handler(pmt.intern('Set Angle'), self.set_angle)

        self.message_port_register_in(pmt.intern('Set Freq'))
        self.set_msg_handler(pmt.intern('Set Freq'), self.change_frequency)
        
    def change_frequency(self,msg):
        self.freq = pmt.to_long(msg)
        self.pwm = GPIO.PWM(self.gpop, self.freq)
        
    def set_angle(self, msg):
        angle = pmt.to_long(msg)

        if angle > 180 or angle < 0:
            return
        self.duty_cycle = (((angle/180.0 * 2) + 0.5) / 20) * 100
        print("angle = " + str(angle) + ". duty cycle = " + str(self.duty_cycle))
        self.pwm.ChangeDutyCycle(self.duty_cycle)
