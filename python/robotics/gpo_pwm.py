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
import threading
import pmt

class gpo_pwm(gr.sync_block):
    """
    docstring for block gpo_pwm
    """
    def __init__(self, platform="pi3", gpio_pin=11, frequency=100, dc=0):
        gr.sync_block.__init__(self,
            name="gpo_pwm",
            in_sig=None,
            out_sig=None)
        
        self.gpop = gpio_pin
        self.freq = frequency
        self.dc = dc
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpop, GPIO.OUT)
        self.pwm = GPIO.PWM(self.gpop, self.freq)
        self.pwm.start(self.dc)

        self.message_port_register_in(pmt.intern('Set DC'))
        self.set_msg_handler(pmt.intern('Set DC'), self.set_dc)

        self.message_port_register_in(pmt.intern('Set Freq'))
        self.set_msg_handler(pmt.intern('Set Freq'), self.change_frequency)
        

    def change_frequency(self,msg):
        self.freq = pmt.to_long(msg)
        self.pwm.stop()
        self.pwm = GPIO.PWM(self.gpop, self.freq)
        self.pwm.start(self.dc)

    def set_dc(self, msg):
        
        x = pmt.to_long(msg)

        if (0 <= x <=100):
            if x != self.dc:
                self.dc = x
                self.pwm.ChangeDutyCycle(self.dc)
            
