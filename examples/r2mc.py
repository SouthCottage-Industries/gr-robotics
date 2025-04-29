#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import robotics




class r2mc(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1
        self.min_speed = min_speed = .25
        self.min_range = min_range = 5
        self.max_range = max_range = 25

        ##################################################
        # Blocks
        ##################################################
        self.robotics_ultrasonic_ranger_0 = robotics.ultrasonic_ranger(samp_rate, 38, 40)
        self.robotics_gpo_pwm_0 = robotics.gpo_pwm('pi3', samp_rate, 13, 100)
        self.robotics_debug_2 = robotics.debug('add const', True)
        self.robotics_debug_1 = robotics.debug('mult const', True)
        self.robotics_debug_0 = robotics.debug('subtract', True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff((1-min_speed)/(max_range-min_range))
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(min_speed)
        self.analog_rail_ff_0 = analog.rail_ff(.25, 1)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, min_range)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.analog_rail_ff_0, 0), (self.robotics_gpo_pwm_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.robotics_debug_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.robotics_debug_1, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.robotics_debug_0, 0))
        self.connect((self.robotics_debug_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.robotics_debug_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.robotics_debug_2, 0), (self.analog_rail_ff_0, 0))
        self.connect((self.robotics_ultrasonic_ranger_0, 0), (self.blocks_sub_xx_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_min_speed(self):
        return self.min_speed

    def set_min_speed(self, min_speed):
        self.min_speed = min_speed
        self.blocks_add_const_vxx_0.set_k(self.min_speed)
        self.blocks_multiply_const_vxx_0.set_k((1-self.min_speed)/(self.max_range-self.min_range))

    def get_min_range(self):
        return self.min_range

    def set_min_range(self, min_range):
        self.min_range = min_range
        self.analog_const_source_x_0.set_offset(self.min_range)
        self.blocks_multiply_const_vxx_0.set_k((1-self.min_speed)/(self.max_range-self.min_range))

    def get_max_range(self):
        return self.max_range

    def set_max_range(self, max_range):
        self.max_range = max_range
        self.blocks_multiply_const_vxx_0.set_k((1-self.min_speed)/(self.max_range-self.min_range))




def main(top_block_cls=r2mc, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
