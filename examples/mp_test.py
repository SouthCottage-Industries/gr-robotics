#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: emane
# GNU Radio version: 3.10.1.1

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import robotics




class mp_test(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.robotics_ultrasonic_ranger_0 = robotics.ultrasonic_ranger(samp_rate, 38, 40, 1)
        self.robotics_gpo_pwm_0 = robotics.gpo_pwm('pi3', samp_rate, 13, 100)
        self.robotics_conditioning_0 = robotics.conditioning(False, '3.75(X-5)+25')


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.robotics_conditioning_0, 'Out'), (self.robotics_gpo_pwm_0, 'Set DC'))
        self.msg_connect((self.robotics_ultrasonic_ranger_0, 'Range (cm)'), (self.robotics_conditioning_0, 'In'))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=mp_test, options=None):
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
