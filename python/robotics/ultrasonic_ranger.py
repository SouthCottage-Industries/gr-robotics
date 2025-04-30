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
import threading
import pmt

class ultrasonic_ranger(gr.sync_block):
    """
    docstring for block ultrasonic_ranger
    """
    def __init__(self, samp_rate = 10, trig_pin = 7, echo_pin = 11, tolerance=1):
        gr.sync_block.__init__(self,
            name="ultrasonic_ranger",
            in_sig=None,
            out_sig=None)
        
        self.t = 1/samp_rate
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        #speed of sound & conversion data for calculating range
        self.v_sound = 34000
        self.s_to_ns = 1000000000
        self.max_dt = self.s_to_ns * 800 / self.v_sound

        #variables to hold current measurement (range), past measurement (mem),
        # and tolerance (how large of a change is required to send out a new range)
        self.range = 0
        self.mem = 0
        self.tol = tolerance
        self.run = True

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

        self.message_port_register_out(pmt.intern('Range (cm)'))
        self.message_port_register_in(pmt.intern('Set Fs'))
        self.set_msg_handler(pmt.intern('Set Fs'), self.change_frequency)

        dist_thread = threading.Thread(target=self.dist, args=[])
        dist_thread.start()

    def update_v_sound_cmps(self, new_v):
        self.v_sound = new_v
        self.max_dt = self.s_to_ns * 800 / self.v_sound

    def stop(self):
        self.run = False

    def change_frequency(self, msg):
        self.t = 1/pmt.to_long(msg)

    def dist(self):
        
        def trigger(self):
            GPIO.output(self.trig_pin, 1)
            time.sleep(.00001)
            GPIO.output(self.trig_pin, 0)
        
        def echo(self):
            state = 0
            t2 = 0
            t1 = time.clock_gettime_ns(1)
            t_end = t1 + self.max_dt
            
            while (state == 0 and t1 < t_end):
                state = GPIO.input(self.echo_pin)
                t1 = time.clock_gettime_ns(1)
            
            t_end = t1 + self.max_dt

            while (state ==1 and t2 < t_end):
                state = GPIO.input(self.echo_pin)
                t2 = time.clock_gettime_ns(1)

            if (t2 > t_end):
                self.range = -1
            elif ( t2 <= t1):
                self.range = 0
            else:
                dt = t2 - t1
                self.range = 34000 * dt / (2 * self.s_to_ns)

        while self.run:
            trig_thread = threading.Thread(target=trigger, args=[self])
            echo_thread = threading.Thread(target=echo, args=[self])

            trig_thread.start()
            echo_thread.start()

            trig_thread.join()
            echo_thread.join()

            if (self.range > (self.mem + self.tol) or self.range < (self.mem - self.tol)):
                self.message_port_pub(pmt.intern('Range (cm)'), pmt.from_long(self.range))

            time.sleep(self.t)

