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
    def __init__(self, debug = False, expression = "X"):
        gr.sync_block.__init__(self,
            name="conditioning",
            in_sig=None,
            out_sig=None)
        
        if(self.eval(expression)):
            self.expr = expression
        else:
            self.expr = "X"
        
        self.dbg = debug
        
        self.message_port_register_out(pmt.intern('Out'))
        self.message_port_register_in(pmt.intern('In'))
        self.set_msg_handler(pmt.intern('In'), self.condition)

    def eval(self, expr):
        whitelist = [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+", "-", "*", "/", "^", "(", ")", "X", "."]

        for x in expr:
            if(x not in whitelist):
                return False
        
        return True


    def condition(self, msg):
        X = pmt.to_long(msg)

        out = eval(self.expr)

        if(self.dbg):
            print("Input = ", msg, " Output = ", out)

        self.message_port_pub(pmt.intern('Out'), pmt.from_long(out))