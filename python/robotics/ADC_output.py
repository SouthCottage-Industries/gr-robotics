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

class ADC_output(gr.sync_block):
    """
    docstring for block ADC_output

    requires enabled I2C inferface on raspberry pi. To enable run the following command

    >> sudo raspi-config

    in the config window select "Interface Options" then "I2C", "Yes", then "Finish" 
    """
    def __init__(self, samp_rate = 10, chn=0, i2c_addr=0x4b):
        gr.sync_block.__init__(self,
            name="ADC_output",
            in_sig=None,
            out_sig=None)
            #out_sig=[numpy.float32, ])
        
        self.t = 1/samp_rate
        self.run = True
            
        self.i2c_addr = i2c_addr
        self.i2c_bus = SMBus(1)
        
        self.message_port_register_out(pmt.intern('ADC Value'))
        
        listen_thread = threading.Thread(target=self.listen, args=[])
        listen_thread.start()
        
    def stop(self):
        self.run = False
        
    def listen(self):
        out = 0
        print("In Listen")
        while self.run:
            tmp = self.i2c_bus.read_byte_data(self.i2c_addr, 1)
            print("tmp = ", tmp)
            if(tmp != out):
                out = tmp
                self.message_port_pub(pmt.intern('ADC Value'), pmt.from_float(out))
            time.sleep(self.t)

        '''def work(self, input_items, output_items):
        out = output_items[0]

        nout = int(1/self.t)

        if(nout < 1):
            nout = 1

        i = 0
        for x in range(nout):
            bus_output = self.i2c_bus.read_byte_data(self.i2c_addr, 1)
            out[i] = bus_output
            self.set_msg_handler(pmt.intern('ADC Value'), bus_output)
            i = i + 1
            time.sleep(self.t)
            
        return nout'''
