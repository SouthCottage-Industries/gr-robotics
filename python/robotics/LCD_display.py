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

#set modes--sets rw and rs pins
READ_MODE  = 0x03
WRITE_MODE = 0x01
CMD_MODE   = 0x00

LCD_BACKLIGHT = 0x08
EN_DELAY      = 0.0005
ENABLE        = 0x04

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
        
    def toggle_enable(self, bits):
        time.sleep(EN_DELAY)
        self.i2c_bus.write_byte_data(self.i2c_addr, 0, (bits | ENABLE))
        time.sleep(EN_DELAY)
        self.i2c_bus.write_byte_data(self.i2c_addr, 0, (bits & ~ENABLE))
        time.sleep(EN_DELAY)
        
    def write_byte(self, data, mode):
        bits_high = (data & 0xF0) | LCD_BACKLIGHT | mode
        bits_low = ((data<<4) & 0xF0) | LCD_BACKLIGHT | mode
        self.i2c_bus.write_byte_data(self.i2c_addr, 0, bits_high) #write first 4 bits
        self.toggle_enable(bits_high)
        self.i2c_bus.write_byte_data(self.i2c_addr, 0, bits_low) #write last 4 bits
        self.toggle_enable(bits_low)
        
    def put_string(self, string):
        for char in string:
            self.write_byte(ord(char), WRITE_MODE)
        
    def print_message(self, msg):
        if msg == None:
            return
        #initialize LCD
        self.write_byte(0x33, CMD_MODE)
        self.write_byte(0x32, CMD_MODE)
        self.write_byte(0x06, CMD_MODE)
        self.write_byte(0x0C, CMD_MODE)
        self.write_byte(0x28, CMD_MODE)
        self.write_byte(0x01, CMD_MODE)
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
