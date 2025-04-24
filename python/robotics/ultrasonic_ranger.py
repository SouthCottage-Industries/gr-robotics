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

class ultrasonic_ranger(gr.sync_block):
    """
    docstring for block ultrasonic_ranger
    """
    def __init__(self, samp_rate = 10, trig_pin = 7, echo_pin = 11):
        gr.sync_block.__init__(self,
            name="ultrasonic_ranger",
            in_sig=None,
            out_sig=[numpy.float32, ])
        
        self.t = 1/samp_rate
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.v_sound = 34000
        self.s_to_ns = 1000000000
        self.max_dt = self.s_to_ns * 800 / self.v_sound
        self.range = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def update_v_sound_cmps(self, new_v):
        self.v_sound = new_v
        self.max_dt = self.s_to_ns * 800 / self.v_sound

    def work(self, input_items, output_items):
        out = output_items[0]
        # <+signal processing here+>
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
                self.range = 0
            elif ( t2 <= t1):
                self.range = 0
            else:
                dt = t2 - t1
                self.range = 34000 * dt / (2 * self.s_to_ns)

        nout = int(1/self.t)

        i = 0
        for x in range(nout):
            trig_thread = threading.Thread(target=trigger, args=[self])
            echo_thread = threading.Thread(target=echo, args=[self])

            trig_thread.start()
            echo_thread.start()

            trig_thread.join()
            echo_thread.join()

            out[i] = self.range
            #print("Range = ", out[i])
            i = i + 1
            time.sleep(self.t)

        return len(output_items[0])
