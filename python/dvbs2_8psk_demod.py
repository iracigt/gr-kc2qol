#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Grant Iraci.
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

class dvbs2_8psk_demod(gr.interp_block):
    """
    docstring for block dvbs2_8psk_demod
    """
    def __init__(self, phase_tag):
        gr.interp_block.__init__(self,
            name="dvbs2_8psk_demod",
            in_sig=[numpy.complex64],
            out_sig=[numpy.float32], interp=3)

        self.rcp_sqrt_2 = 1 / numpy.sqrt(2)
        self.rot_cw = numpy.exp(numpy.pi / 8 * -1j)
        self.phase_tag = phase_tag
        self.set_tag_propagation_policy(gr.TPP_CUSTOM)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        
        in0 *= self.rot_cw
        b = numpy.real(in0)
        c = numpy.imag(in0)
        a = self.rcp_sqrt_2 * (numpy.abs(b) - numpy.abs(c))

        out[:] = numpy.empty((in0.size * 3,), dtype=out.dtype)
        out[0::3] = a
        out[1::3] = b
        out[2::3] = c
        tags = self.get_tags_in_window(0, 0, len(in0))
        for tag in tags:
            self.add_item_tag(0, tag.offset * 3, tag.key, tag.value, tag.srcid)
        return len(output_items[0])

