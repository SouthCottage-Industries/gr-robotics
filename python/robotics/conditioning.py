#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2025 SouthCottage Industries.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
import pmt

class conditioning(gr.sync_block):
    """
    docstring for block conditioning
    """
    def __init__(self, debug = False, expression = "X", data_in = "Float", data_out = "Int", min = -9999, max = 9999):
        gr.sync_block.__init__(self,
            name="conditioning",
            in_sig=None,
            out_sig=None)
        
        if(self.eval(expression)):
            self.expr = expression
        else:
            self.expr = "X"
        
        self.d_in = data_in
        self.d_out = data_out
        self.dbg = debug
        self.min = min
        self.max = max
        
        self.message_port_register_out(pmt.intern('Out'))
        self.message_port_register_in(pmt.intern('In'))
        self.set_msg_handler(pmt.intern('In'), self.condition)

    def eval(self, expr):
        whitelist = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", "^", "(", ")", "X", "."]

        for x in expr:
            if(x not in whitelist):
                return False
        
        return True


    def condition(self, msg):

        if(self.d_in == "Int"):
            X = pmt.to_long(msg)
        elif(self.d_in == "Float"):
            X = pmt.to_float(msg)
        else:
            X = 0

        out = eval(self.expr)

        if(out < self.min):
            out = self.min
        elif(out > self.max):
            out = self.max

        if(self.dbg):
            print("Input = ", msg, " Output = ", out, " Expr = ", self.expr)

        if(self.d_out == "Int"):
            self.message_port_pub(pmt.intern('Out'), pmt.from_long(int(out)))
        elif(self.d_out == "Float"):
            self.message_port_pub(pmt.intern('Out'), pmt.from_float(float(out)))