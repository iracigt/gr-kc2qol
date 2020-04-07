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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "ldpc_decoder_fb_impl.h"
#include "ldpc/dvb_s2_tables.hh"

namespace gr {
  namespace kc2qol {

    ldpc_decoder_fb::sptr
    ldpc_decoder_fb::make()
    {
      return gnuradio::get_initial_sptr
        (new ldpc_decoder_fb_impl());
    }


    /*
     * The private constructor
     */
    ldpc_decoder_fb_impl::ldpc_decoder_fb_impl()
      : gr::block("ldpc_decoder_fb",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
      // Code Rate: 9 / 10
      nbch = 58320;
      ldpc = new LDPC<DVB_S2_TABLE_B11>();

      aligned_buffer = aligned_alloc(sizeof(simd_type), sizeof(simd_type) * ldpc->code_len());
      decode.init(ldpc);
      set_output_multiple(nbch);
    }

    /*
     * Our virtual destructor.
     */
    ldpc_decoder_fb_impl::~ldpc_decoder_fb_impl()
    {
      free(aligned_buffer);
      delete ldpc;
    }

    void
    ldpc_decoder_fb_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      const int CODE_LEN = ldpc->code_len();
      const int DATA_LEN = ldpc->data_len();
      ninput_items_required[0] = (noutput_items / DATA_LEN) * CODE_LEN;
    }

    int
    ldpc_decoder_fb_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];
      const int CODE_LEN = ldpc->code_len();
      const int DATA_LEN = ldpc->data_len();
      simd_type *simd = reinterpret_cast<simd_type *>(aligned_buffer);
      int trials = TRIALS;
      int consumed = 0;
      int bits_decoded = 0;

      // Make sure the we have enough input and output
      assert(noutput_items % (DATA_LEN) == 0);
      int nblocks = noutput_items / nbch;
      assert(ninput_items[0] >= nblocks * CODE_LEN);

      for (int j = 0; j < nblocks; j += SIMD_WIDTH) {
        // How many blocks in this batch?
        int blocks = j + SIMD_WIDTH > nblocks ? nblocks - j : SIMD_WIDTH;

        // Load bits into simd input array
        for (int n = 0; n < blocks; ++n) {
          for (int i = 0; i < CODE_LEN; ++i) {
            // Convert float [-1,1] to signed int [-127, 127]
            // If outside [-1,1], clamp it
            float f = in[(j+n)*CODE_LEN+i] * 127;
            int8_t soft_int = static_cast<int8_t>(std::max(std::min(f, 127.0f), -127.0f));
            //int8_t soft_int = static_cast<int8_t>(f);
            reinterpret_cast<code_type *>(simd+i)[n] = soft_int;
          }
        }

        // Run the decoder
        int trials = TRIALS;
        int count = decode(simd, simd + DATA_LEN, trials, blocks);

        // Extract decoded bits
        for (int n = 0; n < blocks; ++n) {
          for (int i = 0; i < DATA_LEN; ++i) {
            // out[(j+n)*DATA_LEN+i] = reinterpret_cast<code_type *>(simd+i)[n];
	    out[(j+n)*DATA_LEN+i] = reinterpret_cast<code_type *>(simd+i)[n] > 0 ? 1 : 0;
          }
        }

        // Update number of items
        consumed += blocks * CODE_LEN;
        bits_decoded += blocks * DATA_LEN;

        if (count < 0) {
          std::cerr << "decoder failed at converging to a code word!" << std::endl;
        } else {
          std::cerr << trials - count << " iterations were needed." << std::endl;
        }
      }

      // Tell runtime system how many input items we consumed on
      // each input stream.
      consume_each (noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace kc2qol */
} /* namespace gr */

