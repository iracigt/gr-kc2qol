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

def strip_nearby(l, min_dist):
    out = []
    for x in l:
        if not any([abs(x - y) < min_dist for y in out]):
            out += [x]
    return out

class find_peaks(gr.sync_block):

    def __init__(self, min_dist, x_min, x_max, vlen):
        gr.sync_block.__init__(self,
            name="find_peaks",
            in_sig=[(numpy.float32, vlen)],
            out_sig=[numpy.float32, numpy.float32])

        self.min_dist = min_dist
        self.x_min = x_min
        self.x_max = x_max


    def work(self, input_items, output_items):
        in0 = input_items[0]

        for i in range(0, len(in0)):
            data = in0[i]

            raw_peaks = list(signal.argrelmax(data)[0])
            raw_peaks.sort(key=lambda x: data[x], reverse=True)
            stripped = strip_nearby(raw_peaks, (self.min_dist - self.x_min) / (self.x_max - self.x_min) * len(data))

            peaks = sorted(stripped[:2])

            if len(peaks) == 2:
                for j in range(0, len(peaks)):
                    output_items[j][i] = (peaks[j] + 0.5) / len(data) * (self.x_max - self.x_min) + self.x_min

        return len(output_items[0])
