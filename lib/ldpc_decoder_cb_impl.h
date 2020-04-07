/* -*- c++ -*- */
/*
 * Copyright 2018,2019,2020 Ahmet Inan, Ron Economos, Grant Iraci.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef INCLUDED_KC2QOL_LDPC_DECODER_CB_IMPL_H
#define INCLUDED_KC2QOL_LDPC_DECODER_CB_IMPL_H

#include <kc2qol/ldpc_decoder_cb.h>

#include "ldpc/alloc.hh"
#include "ldpc/encoder.hh"
#include "ldpc/simd.hh"
#include "ldpc/algorithms.hh"
#include "ldpc/interleaver.hh"
#include "ldpc/modulation.hh"

#ifdef __AVX2__
const int SIZEOF_SIMD = 32;
#else
const int SIZEOF_SIMD = 16;
#endif

typedef int8_t code_type;
const int SIMD_WIDTH = SIZEOF_SIMD / sizeof(code_type);
typedef SIMD<code_type, SIMD_WIDTH> simd_type;

const int FACTOR = 2;

#include "ldpc/layered_decoder.hh"
typedef NormalUpdate<simd_type> update_type;
typedef OffsetMinSumAlgorithm<simd_type, update_type, FACTOR> algorithm_type;
const int TRIALS = 25;

namespace gr {
  namespace kc2qol {

    class ldpc_decoder_cb_impl : public ldpc_decoder_cb
    {
     private:
      unsigned int frame_size;
      unsigned int nbch;

      LDPCInterface *ldpc;
      LDPCDecoder<simd_type, algorithm_type> decode;
      void *aligned_buffer;

     public:
      ldpc_decoder_cb_impl();
      ~ldpc_decoder_cb_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);

    };

  } // namespace kc2qol
} // namespace gr

#endif /* INCLUDED_KC2QOL_LDPC_DECODER_CB_IMPL_H */

