/* -*- c++ -*- */

#define KC2QOL_API

%include "gnuradio.i"           // the common stuff

//load generated python docstrings
%include "kc2qol_swig_doc.i"

%{
#include "kc2qol/ldpc_decoder_fb.h"
%}

%include "kc2qol/ldpc_decoder_fb.h"
GR_SWIG_BLOCK_MAGIC2(kc2qol, ldpc_decoder_fb);
