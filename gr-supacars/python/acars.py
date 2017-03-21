#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

from __future__ import division
import pmt
import numpy
import sys
from gnuradio import gr

class State:
    SCAN = 1
    BITSYNC = 2
    ENDPREKEY = 3
    PLUSSYNC = 4
    STARSYNC = 5
    SYN1SYNC = 6
    SOHSYNC = 7
    FRAMESYNC = 8
    ETX = 9
    CRC_1 = 10
    CRC_2 = 11

class acars_dictionary:
    def translate(self, decimal_vect):
        if (not all(isinstance(item, numpy.uint8) for item in decimal_vect)): #List contains non integer numbers
            return ''

        if ((min(decimal_vect) < 0) or (max(decimal_vect) > 127)):
            return ''

        return [self.dictionary[x] for x in decimal_vect]


    def __init__(self):
        self.dictionary = {}
        self.dictionary[0] = 'NUL'
        self.dictionary[1] = 'SOH'
        self.dictionary[2] = 'STX'
        self.dictionary[3] = 'ETX'
        self.dictionary[4] = 'EOT'
        self.dictionary[5] = 'ENQ'
        self.dictionary[6] = 'ACK'
        self.dictionary[7] = 'BEL'
        self.dictionary[8] = 'BS'
        self.dictionary[9] = 'HT'
        self.dictionary[10] = 'LF'
        self.dictionary[11] = 'VT'
        self.dictionary[12] = 'FF'
        self.dictionary[13] = 'CR'
        self.dictionary[14] = 'SO'
        self.dictionary[15] = 'SI'
        self.dictionary[16] = 'DLE'
        self.dictionary[17] = 'DC1'
        self.dictionary[18] = 'DC2'
        self.dictionary[19] = 'DC3'
        self.dictionary[20] = 'DC4'
        self.dictionary[21] = 'NAK'
        self.dictionary[22] = 'SYN'
        self.dictionary[23] = 'ETB'
        self.dictionary[24] = 'CAN'
        self.dictionary[25] = 'EM'
        self.dictionary[26] = 'SUB'
        self.dictionary[27] = 'ESC'
        self.dictionary[28] = 'FS'
        self.dictionary[29] = 'GS'
        self.dictionary[30] = 'RS'
        self.dictionary[31] = 'US'
        self.dictionary[32] = 'SP'
        self.dictionary[33] = '!'
        self.dictionary[34] = '"'
        self.dictionary[35] = '#'
        self.dictionary[36] = '$'
        self.dictionary[37] = '%'
        self.dictionary[38] = '&'
        self.dictionary[39] = "'"
        self.dictionary[40] = '('
        self.dictionary[41] = ')'
        self.dictionary[42] = '*'
        self.dictionary[43] = '+'
        self.dictionary[44] = ','
        self.dictionary[45] = '-'
        self.dictionary[46] = '.'
        self.dictionary[47] = '/'
        self.dictionary[48] = '0'
        self.dictionary[49] = '1'
        self.dictionary[50] = '2'
        self.dictionary[51] = '3'
        self.dictionary[52] = '4'
        self.dictionary[53] = '5'
        self.dictionary[54] = '6'
        self.dictionary[55] = '7'
        self.dictionary[56] = '8'
        self.dictionary[57] = '9'
        self.dictionary[58] = ':'
        self.dictionary[59] = ''
        self.dictionary[60] = '<'
        self.dictionary[61] = '='
        self.dictionary[62] = '>'
        self.dictionary[63] = '?'
        self.dictionary[64] = '@'
        self.dictionary[65] = 'A'
        self.dictionary[66] = 'B'
        self.dictionary[67] = 'C'
        self.dictionary[68] = 'D'
        self.dictionary[69] = 'E'
        self.dictionary[70] = 'F'
        self.dictionary[71] = 'G'
        self.dictionary[72] = 'H'
        self.dictionary[73] = 'I'
        self.dictionary[74] = 'J'
        self.dictionary[75] = 'K'
        self.dictionary[76] = 'L'
        self.dictionary[77] = 'M'
        self.dictionary[78] = 'N'
        self.dictionary[79] = 'O'
        self.dictionary[80] = 'P'
        self.dictionary[81] = 'Q'
        self.dictionary[82] = 'R'
        self.dictionary[83] = 'S'
        self.dictionary[84] = 'T'
        self.dictionary[85] = 'U'
        self.dictionary[86] = 'V'
        self.dictionary[87] = 'W'
        self.dictionary[88] = 'X'
        self.dictionary[89] = 'Y'
        self.dictionary[90] = 'Z'
        self.dictionary[91] = '['
        self.dictionary[92] = '\\'
        self.dictionary[93] = ']'
        self.dictionary[94] = '^'
        self.dictionary[95] = '_'
        self.dictionary[96] = '`'
        self.dictionary[97] = 'a'
        self.dictionary[98] = 'b'
        self.dictionary[99] = 'c'
        self.dictionary[100] = 'd'
        self.dictionary[101] = 'e'
        self.dictionary[102] = 'f'
        self.dictionary[103] = 'g'
        self.dictionary[104] = 'h'
        self.dictionary[105] = 'i'
        self.dictionary[106] = 'j'
        self.dictionary[107] = 'k'
        self.dictionary[108] = 'l'
        self.dictionary[109] = 'm'
        self.dictionary[110] = 'n'
        self.dictionary[111] = 'o'
        self.dictionary[112] = 'p'
        self.dictionary[113] = 'q'
        self.dictionary[114] = 'r'
        self.dictionary[115] = 's'
        self.dictionary[116] = 't'
        self.dictionary[117] = 'u'
        self.dictionary[118] = 'v'
        self.dictionary[119] = 'w'
        self.dictionary[120] = 'x'
        self.dictionary[121] = 'y'
        self.dictionary[122] = 'z'
        self.dictionary[123] = '['
        self.dictionary[124] = '|'
        self.dictionary[125] = ')'
        self.dictionary[126] = '~'
        self.dictionary[127] = 'DEL'

class acars(gr.sync_block):
    """
    docstring for block acars
    """
    def __init__(self, samp_rate, corr_thres):
        gr.sync_block.__init__(self,
            name="acars",
            in_sig=[numpy.float32],
            out_sig=None)
        self.set_corr_thres(corr_thres)
        self.fs = samp_rate
        self.init_constants()
        self.message_port_register_out(pmt.intern("raw_output"))
        self.message_port_register_out(pmt.intern("parser_output"))
        self.queue = []
        self.state = State.SCAN
        self.init_states()
        self.acars_dic = acars_dictionary()

    def set_corr_thres(self, corr_thres):
        self.corr_thres = corr_thres

    def init_constants(self):
        self.min_symbols_window_size = 50

        self.f1 = 2400
        self.f2 = 1200
        
        samples_per_symbol_float = self.fs / self.f1

        if( samples_per_symbol_float <= 10):
            sys.exit("Error: Sample rate must be at least 24k samples/s")

        if( not samples_per_symbol_float.is_integer()):
            sys.exit("Error: Sample rate must be a multiple of 2400 samples/s (and above 24k samples/s)")

        self.pow_vect = [1, 2, 4, 8, 16, 32, 64, 0]
        self.pow_vect_with_parity = [1, 2, 4, 8, 16, 32, 64, 128]
        self.samples_per_symbol = int(self.fs / self.f1)
        self.k = numpy.arange(0,int(15*self.fs/self.f1))
        self.gamma = numpy.sin(2*numpy.pi*(self.f1/self.fs)*numpy.asarray(self.k))
        self.k2 = range(0,int(self.fs/self.f1))
        self.h1 = numpy.sin(2*numpy.pi*self.f1/self.fs*numpy.asarray(self.k2))
        self.h1 = numpy.reshape(self.h1, (len(self.h1),1))
        self.h0 = numpy.sin(2*numpy.pi*self.f2/self.fs*numpy.asarray(self.k2))
        self.h0 = numpy.reshape(self.h0, (len(self.h0),1))
        
        self.parity_fails_tolerance = 0.4

        self.PLUS = [True, True, False, True, False, True, False, True]
        self.STAR = [False, True, False, True, False, True, False, False]
        self.SYN = [False, True, True, False, True, False, False, False]
        self.SOH = [True, False, False, False, False, False, False, False]
        self.ETX = [True, True, False, False, False, False, False, True]
        self.BCS = [True, True, True, True, True, True, True, False]

    def init_states(self):
        self.remaining_samples = []
        self.last_decoded_bit = True
        self.remaining_bits = numpy.zeros(0, dtype = bool)
        self.current_message = numpy.zeros(0, dtype = bool)
        self.current_crc = numpy.zeros(0, dtype = bool)

    def raw_output(self, mat_frame, parity_ok = True, crc_ok = True):

        decimal_vect = numpy.sum(mat_frame*self.pow_vect, axis = 1, dtype = numpy.uint8)
        decimal_vect_with_parity = numpy.sum(mat_frame*self.pow_vect_with_parity, axis = 1, dtype = numpy.uint8)
        out_str = []
        for i in range(0, len(decimal_vect_with_parity)):
            out_str.append(chr(decimal_vect_with_parity[i]))
        
        translated_vect = self.acars_dic.translate(decimal_vect)
        if(not parity_ok):
            translated_vect.append(' WARNING - INVALID PARITY CHECKS')
        translated_vect.append('\n')
        separator = " "
        s = separator.join(translated_vect)
        nvec = numpy.fromstring(s, dtype=numpy.uint8, count=len(s))
        vec = pmt.to_pmt(nvec)
        self.message_port_pub(pmt.intern("raw_output"), pmt.cons(pmt.PMT_NIL, vec))
        
    def parser_output(self, mat_frame, parity_ok = True, crc_ok = True):

        # Reshaping the mat_frame into a simple row vector and convert the vector to a string
        size_mat_frame = mat_frame.shape
        mat_vect = numpy.reshape(mat_frame,(size_mat_frame[0]*size_mat_frame[1],1))
        mat_vect = numpy.array(mat_vect)
        mat_vect_str = mat_vect.tostring()
        
        # Creation of dictionnary with the matrix and the crc_ok & parity_ok boolean
        key_crc = pmt.intern("crc_ok")
        val_crc = pmt.to_pmt(crc_ok)
        key_parity = pmt.intern("parity_ok")
        val_parity = pmt.to_pmt(parity_ok)
        key_mat = pmt.intern("mat_vect_str")
        val_mat = pmt.to_pmt(mat_vect_str)
                
        dic = pmt.make_dict()
        dic = pmt.dict_add(dic,key_crc,val_crc)
        dic = pmt.dict_add(dic,key_parity,val_parity)
        dic = pmt.dict_add(dic,key_mat,val_mat)
        
        # Sending the dictionnary to the acarsparser block
        self.message_port_pub(pmt.intern("parser_output"), pmt.cons(pmt.PMT_NIL, dic))
        

    def parity_check(self, binary_vect):
        if(len(binary_vect) != 8):
            return False
        else:
            return (numpy.mod(numpy.sum(binary_vect[0:7]), 2) == binary_vect[7])

    def parity_check_matrix(self, binary_mat):
        return (numpy.mod(numpy.sum(binary_mat[:, 0:7], axis = 1), 2) == binary_mat[:,7])


    def work(self, input_items, output_items):
        self.queue.extend(input_items[0])

        while(len(self.queue) > (self.min_symbols_window_size * self.samples_per_symbol)):
            self.main(self.queue[0 : self.min_symbols_window_size * self.samples_per_symbol])
            del self.queue[0 : self.min_symbols_window_size * self.samples_per_symbol]

        return len(input_items[0])

    def bit_demod(self, in0):
        n_symbols = int(len(in0)/ self.samples_per_symbol)

        in0_reshaped = numpy.transpose(numpy.reshape(in0, (n_symbols, self.samples_per_symbol)))

        delta = numpy.zeros(n_symbols)
            
        H0= numpy.tile(self.h0,(1,n_symbols));
        H1= numpy.tile(self.h1,(1,n_symbols));
        
        Gamma1 = numpy.sum(H1 * in0_reshaped , axis=0)
        Gamma0 = numpy.sum(H0 * in0_reshaped , axis=0)
        delta = numpy.square(Gamma1) - numpy.square(Gamma0)
        
        bitstream_uncoded = delta < 0

        bitstream = numpy.zeros(len(bitstream_uncoded), dtype = bool)
        bitstream[0] = (self.last_decoded_bit != bitstream_uncoded[0])

        for j in range(1, len(bitstream_uncoded)):
            bitstream[j] = (bitstream[j-1] != bitstream_uncoded[j])

        self.last_decoded_bit = bitstream[-1]

        return bitstream


    def main(self, in0):
        if(self.state == State.SCAN):
            self.init_states()
            prekey_correlation = numpy.correlate(in0, self.gamma, 'valid')
            max_corr_index = numpy.argmax(prekey_correlation)
            if(prekey_correlation[max_corr_index] > self.corr_thres): #The prekey has been found
                self.state = State.BITSYNC
                del in0[0:max_corr_index]
            else:
                return

        in0 = numpy.concatenate((self.remaining_samples, in0))
        self.remaining_samples = []
        sample_limit = int(len(in0) / self.samples_per_symbol)
        self.remaining_samples = in0[self.samples_per_symbol*sample_limit:]
        in0 = in0[:self.samples_per_symbol*sample_limit]

        if(len(in0) <= 0):
            return

        bitstream = self.bit_demod(in0)

        if(self.state == State.BITSYNC):
            where_end_prekey = numpy.where(bitstream == 0)[0]
            if(len(where_end_prekey) <= 0): #End of prekey not detected
                return
            else:
                bitstream = bitstream[where_end_prekey[0] - 2 :]
                self.state = State.ENDPREKEY

        bitstream = numpy.concatenate((self.remaining_bits, bitstream))
        self.remaining_bits = numpy.zeros(0, dtype = bool)
        bit_limit = int(len(bitstream) / 8 )
        self.remaining_bits = bitstream[bit_limit*8:]
        bitstream = bitstream[:bit_limit*8]

        if(len(bitstream) <= 0):
            return

        mat_block = numpy.reshape(bitstream, (bit_limit, 8))

        if(self.state == State.ENDPREKEY):
            if(numpy.array_equal(mat_block[0,:], self.PLUS)):
                mat_block = mat_block[1:, :]
                self.state = State.PLUSSYNC
            else:
                self.state = State.SCAN
                return

        if(len(mat_block) <= 0):
            return

        if(self.state == State.PLUSSYNC):
            if(numpy.array_equal(mat_block[0,:],self.STAR)):
                mat_block = mat_block[1:, :]
                self.state = State.STARSYNC
            else:
                self.state = State.SCAN
                return

        if(len(mat_block) <= 0):
            return

        if(self.state == State.STARSYNC):
            if(numpy.array_equal(mat_block[0,:], self.SYN)):
                mat_block = mat_block[1:, :]
                self.state = State.SYN1SYNC
            else:
                self.state = State.SCAN
                return

        if(len(mat_block) <= 0):
            return

        if(self.state == State.SYN1SYNC):
            if(numpy.array_equal(mat_block[0,:],self.SYN)):
                mat_block = mat_block[1:, :]
                self.state = State.SOHSYNC
            else:
                self.state = State.SCAN
                return

        if(len(mat_block) <= 0):
            return

        if(self.state == State.SOHSYNC):
            if(numpy.array_equal(mat_block[0,:],self.SOH)):
                mat_block = mat_block[1:, :]
                self.state = State.FRAMESYNC
            else:
                self.state = State.SCAN
                return

        if(len(mat_block) <= 0):
            return


        if(self.state == State.FRAMESYNC):
            size_mat_block = mat_block.shape
            mat_compare= numpy.tile(numpy.reshape((self.ETX),(1,8)),(size_mat_block[0],1))
            mat_compare = (mat_compare == mat_block)
            vec_compare = numpy.all(mat_compare,axis=1)
            where_indice_ETX = numpy.where(vec_compare == True)[0]

            if(len(where_indice_ETX) <= 0): #No ETX found, appending block to current frame and checking parity
                if(len(self.current_message) <= 0):
                    self.current_message = mat_block
                else:
                    self.current_message = numpy.concatenate((self.current_message, mat_block), axis = 0)
                
                parity_vector = self.parity_check_matrix(mat_block)
                
                if(numpy.count_nonzero(parity_vector)/len(parity_vector) >= self.parity_fails_tolerance): #Too many parity checks errors, dropping frame                 
                    self.state = State.SCAN
                    return
                    
            else:
                indice_ETX = where_indice_ETX[0]
                if(len(self.current_message) <= 0):
                    self.current_message = mat_block[:indice_ETX,:]
                else:
                    self.current_message = numpy.concatenate((self.current_message, mat_block[:indice_ETX,:]), axis = 0)
                self.state = State.ETX
                mat_block = mat_block[indice_ETX:,:]
                if(len(mat_block) <= 0):
                    return
                mat_block = mat_block[1:,:]
                if(len(mat_block) <= 0):
                    return

        if(self.state == State.ETX):
            self.current_crc = numpy.zeros(0, dtype = bool)
            self.current_crc = mat_block[0,:]
            mat_block = mat_block[1:,:]
            self.state = State.CRC_1
            if(len(mat_block) <= 0):
                return

        if(self.state == State.CRC_1):
            self.current_crc = numpy.concatenate((self.current_crc, mat_block[0,:]))
            mat_block = mat_block[1:,:]
            self.state = State.CRC_2
            if(len(mat_block) <= 0):
                return

        if(self.state == State.CRC_2):
            if(numpy.array_equal(mat_block[0,:],self.BCS)):
                self.raw_output(self.current_message, True, True)
                self.parser_output(self.current_message, True, True) #  Sending the frame to the acarsparser in an asynchronous msg                
                self.state = State.SCAN
                return
            else:
                self.state = State.SCAN
                return




        return 0
