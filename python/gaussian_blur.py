#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 Grant Iraci.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy
from scipy import signal
from gnuradio import gr

class gaussian_blur(gr.sync_block):
    """
    docstring for block gaussian_blur
    """
    def __init__(self, m, p, sigma, vlen):
        gr.sync_block.__init__(self,
            name="gaussian_blur",
            in_sig=[(numpy.float32, vlen)],
            out_sig=[(numpy.float32, vlen)])

        self.m = m
        self.p = p
        self.sigma = sigma

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]

        window = signal.general_gaussian(self.m, p=self.p, sig=self.sigma)

        for i in range(0, len(in0)):
            filtered = signal.fftconvolve(window, in0[i])
            filtered = (numpy.average(in0[i]) / numpy.average(filtered)) * filtered
            out0[i][:] = numpy.roll(filtered, -self.m/2)[:len(in0[i])]

        return len(in0)
