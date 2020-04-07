/* -*- c++ -*- */
/*
 * Copyright 2020 Grant Iraci.
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

#ifndef INCLUDED_KC2QOL_LDPC_DECODER_CB_H
#define INCLUDED_KC2QOL_LDPC_DECODER_CB_H

#include <kc2qol/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace kc2qol {

    /*!
     * \brief <+description of block+>
     * \ingroup kc2qol
     *
     */
    class KC2QOL_API ldpc_decoder_cb : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<ldpc_decoder_cb> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of kc2qol::ldpc_decoder_cb.
       *
       * To avoid accidental use of raw pointers, kc2qol::ldpc_decoder_cb's
       * constructor is in a private implementation
       * class. kc2qol::ldpc_decoder_cb::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace kc2qol
} // namespace gr

#endif /* INCLUDED_KC2QOL_LDPC_DECODER_CB_H */
