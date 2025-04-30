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
import pmt

class gpo(gr.sync_block):
    """
    docstring for block gpo
    """

    def __init__(self, platform="pi3", gpio_pin=11):
    #def __init__(self, gpio_pin=11):
        gr.sync_block.__init__(self,
            name="gpio",
            in_sig=None,
            out_sig=None)
        
        self.gpop = gpio_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.gpop, GPIO.OUT)

        self.message_port_register_in(pmt.intern('In'))
        self.set_msg_handler(pmt.intern('In'), self.handle_in)

    def handle_in(self, msg):
        if(pmt.is_long(msg)):
            GPIO.output(self.gpop, pmt.to_long(msg))

    '''def work(self, input_items, output_items):
        in0 = input_items[0]

        for x in in0:
            GPIO.output(self.gpop, x)

        return len(input_items[0])'''
