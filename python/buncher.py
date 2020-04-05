#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Grant Iraci.
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

class buncher(gr.basic_block):
    """
    docstring for block buncher
    """
    def __init__(self, length, tpye=numpy.uint8):
        gr.basic_block.__init__(self,
            name="buncher",
            in_sig=[tpye],
            out_sig=[tpye])

        self.set_output_multiple(length)

        self.buf = numpy.empty(length, dtype=tpye)
        self.length = length
        self.index = 0

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        sym_in = input_items[0]
        num_in = len(input_items[0])

        if (num_in <= self.length - self.index):
            self.buf[self.index:self.index + num_in] = sym_in
            consumed = num_in
        else:
            consumed = self.length - self.index
            self.buf[self.index:] = sym_in[:consumed]
        
        self.index += consumed
        
        produced = 0
        if self.index >= self.length:
            output_items[0][:self.length] = self.buf
            produced = self.length
            self.index = 0

        self.consume(0, consumed)
        return produced
