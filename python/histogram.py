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
from gnuradio import gr

class histogram(gr.basic_block):

    def __init__(self, points, nbins, range=None, density=False):
        gr.basic_block.__init__(self,
            name="histogram",
            in_sig = [numpy.float32],
            out_sig = [(numpy.float32, nbins)]
        )

        self.points = points
        self.nbins = nbins
        self.range = range
        self.density = density

        self.pts_remaining = points
        self.buffer = []

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            # Lie...
            ninput_items_required[i] = noutput_items


    def general_work(self, input_items, output_items):
        in0 = input_items[0]

        self.consume_each(len(input_items[0]))

        if (self.pts_remaining > len(in0)):
            self.buffer += [in0]
            self.pts_remaining -= len(in0)
            return 0
        else:
            self.buffer += [in0[:self.pts_remaining]]
            rem = in0[self.pts_remaining:]

            (hist, edges) = numpy.histogram(numpy.concatenate(self.buffer),
                                         bins=self.nbins, range=self.range,
                                         density=self.density)

            output_items[0][:] = [hist]
            self.buffer = [rem]
            self.pts_remaining = self.points - len(rem)
            return 1

        return 0
