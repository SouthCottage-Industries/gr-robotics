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
import pmt

class Stepper(gr.sync_block):
    """
    docstring for block Stepper
    """
    def __init__(self, step_rate = 10, pins = [7, 11, 13, 15]):
        gr.sync_block.__init__(self,
            name="Stepper",
            in_sig=None,
            out_sig=None)
        self.step_rate = step_rate
        self.pins = pins
        self.position = 0
        self.nextStep = 0
        self.steps = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins, GPIO.OUT)
        self.t = 1/self.step_rate
        if self.t < .003:
            self.t = .003

        self.message_port_register_in(pmt.intern('Step Count'))
        self.set_msg_handler(pmt.intern('Step Count'), self.steps)

    def set_pos(self, newPos):
        self.position = newPos

    def stepForward(self):
        self.nextStep = (self.nextStep + 1) % 4
        GPIO.output(self.pins, self.steps[self.nextStep])

    def stepBackward(self):
        self.nextStep = (self.nextStep - 1) % 4
        if self.nextStep == -1:
            self.nextStep = 3
        GPIO.output(self.pins, self.steps[self.nextStep])

    def steps(self, msg):
        count = pmt.to_long(msg)
        
        # <+signal processing here+>
        if (count > 0):
            while (count > 0):
                Stepper.stepForward(self)
                time.sleep(self.t)
                count = count - 1
        else:
            while (count < 0):
                Stepper.stepBackward(self)
                time.sleep(self.t)
                count = count + 1
