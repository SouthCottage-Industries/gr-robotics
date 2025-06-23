#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 SouthCottage Industries.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
import RPi.GPIO as GPIO 
from smbus2 import SMBus
import time
from gnuradio import gr
import threading
import pmt

class LCD_display(gr.sync_block):
    """
    docstring for block LCD_display
    """
    def __init__(self, samp_rate=10, i2c_addr=0x27, string_in="Hello World"):
        gr.sync_block.__init__(self,
            name="LCD_display",
            in_sig=[],
            out_sig=[])
            
        self.t = 1/samp_rate
        self.run = True
        
        self.i2c_addr = i2c_addr
        self.i2c_bus = SMBus(1)
        
        self.print_message(string_in)
        
        # self.message_port_register_in(pmt.intern('LCD Print Data'))
        # self.set_msg_handler(pmt.intern('LCD Print Data'), self.print_message)

    def stop(self):
        self.run = False
        
    def putChar(char):
        self.i2c_bus.write_word_data(self.i2c_addr, 1, char)
        
    def put_string(str):
        for i in str.length():
            putChar(str(i))
        
    def print_message(self, msg):
        if msg == null:
            return
        self.put_string(msg)
        print("message = " + msg)
        
    # def listen(self):
        # out = 0
        # print("In Listen")
        # while self.run:
            # tmp = self.i2c_bus.read_byte_data(self.i2c_addr, 1)
            # print("tmp = ", tmp)
            # if(tmp != out):
                # out = tmp
                # self.message_port_pub(pmt.intern('ADC Value'), pmt.from_float(out))
            # time.sleep(self.t)

    # def work(self, input_items, output_items):
        # in0 = input_items[0]
        # out = output_items[0]
        # # <+signal processing here+>
        # out[:] = in0
        # return len(output_items[0])
