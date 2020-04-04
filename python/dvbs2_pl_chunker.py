#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Grant Iraci KC2QOL.
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
import pmt

class dvbs2_pl_chunker(gr.basic_block):

    def __init__(self, packet_len=21600, start_tag=pmt.intern('corr_est'), hdr_len=90, tpye=numpy.uint8):
        gr.basic_block.__init__(self,
            name="dvbs2_pl_chunker",
            in_sig=[tpye, ],
            out_sig=[tpye, ])
        self.packet_len = packet_len
        self.hdr_len = hdr_len
        self.total_len = hdr_len + packet_len
        self.start_tag = start_tag
        self.rem = 0
        self.hdr_rem = 0

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):


        sym_in = input_items[0]
        num_in = len(input_items[0])
        sym_out = output_items[0]
        num_out = len(output_items[0])

        i = 0
        j = 0
        while (i < num_in and j < num_out):
            if self.rem > 0:
                tags = self.get_tags_in_window(0, i+1, min(num_in, i + self.rem, i + num_out - j), self.start_tag) if i < (num_in - 1) else []
                if not tags or self.rem == self.total_len:
                    avail = min(num_in - i, self.rem, num_out - j)
                    write = avail
                    self.rem -= avail
                    if self.hdr_rem:
                        if avail > self.hdr_rem:
                            write -= self.hdr_rem
                            self.hdr_rem = 0
                        else:
                            self.hdr_rem -= avail
                            write = 0
                    
                    if write:
                        sym_out[j:j+write] = sym_in[i+avail-write:i+avail]
                    
                    j += write
                    i += avail
                else:
                    avail = tags[0].offset - self.nitems_read(0) - i

                    write = avail
                    self.rem -= avail
                    if self.hdr_rem:
                        if avail > self.hdr_rem:
                            write -= self.hdr_rem
                            self.hdr_rem = 0
                        else:
                            self.hdr_rem -= avail
                            write = 0
                    
                    if write:
                        sym_out[j:j+write] = sym_in[i+avail-write:i+avail]
                    
                    j += write
                    i += avail
                    
                    self.rem = self.total_len
                    self.hdr_rem = self.hdr_len
            else:
                tags = self.get_tags_in_window(0, i, num_in, self.start_tag)
                if not tags:
                    i = num_in
                else:
                    
                    offset = tags[0].offset - self.nitems_read(0)
                    i = offset
                    self.rem = self.total_len
                    self.hdr_rem = self.hdr_len
        self.consume(0, i)
        output_items[0] = sym_out[:j]
        return j

