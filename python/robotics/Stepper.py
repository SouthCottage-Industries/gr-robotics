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

class Stepper(gr.sync_block):
    """
    docstring for block Stepper
    """
    def __init__(self, samp_rate = 10, pins = [7, 11, 13, 15]):
        gr.sync_block.__init__(self,
            name="Stepper",
            in_sig=[numpy.float32, ],
            out_sig=None)
        self.samp_rate = samp_rate
        self.pins = pins
        self.position = 0
        self.nextStep = 0
        self.steps = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pins, GPIO.OUT)
        self.t = 1/self.samp_rate
        if self.t < .003:
            self.t = .003

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

    def hold(self):
        GPIO.output(self.pins, self.steps[self.nextStep])


    def work(self, input_items, output_items):
        in0 = input_items[0]
        # <+signal processing here+>
        for i in in0:
            if(i > 0):
                Stepper.stepForward(self)
                time.sleep(self.t)
            elif(i < 0):
                Stepper.stepBackward(self)
                time.sleep(self.t)
            else:
                Stepper.hold(self)
                time.sleep(self.t)
        
        return len(input_items[0])
