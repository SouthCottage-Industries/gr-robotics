#!/usr/bin/env python
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
    def __init__(self):
        gr.sync_block.__init__(self,
            name="LCD_display",
            in_sig=[<+numpy.float32+>, ],
            out_sig=[])
            
        addr = 0x27;


    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        # <+signal processing here+>
        out[:] = in0
        return len(output_items[0])
