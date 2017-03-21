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
from gnuradio import gr

class State:
    SCAN = 1 # No frame detected yet, or BCS of previous frame ended
    SYNC = 2 # Prekey detected, frame synchronized
    ETX = 3 # ETX detected, computing CR

    
class acarsdecoder(gr.sync_block):
    """
    docstring for block acarsdecoder
    """
    
    
    def __init__(self, samp_rate, corr_thres):
        gr.sync_block.__init__(self,
            name="acarsdecoder",
            in_sig=[numpy.float32],
            out_sig=None)
        self.message_port_register_out(pmt.intern("raw_output"))
        self.message_port_register_out(pmt.intern("parsed_output"))
        self.set_corr_thres(corr_thres)
        self.fs = samp_rate
        self.current_message = numpy.zeros(0, dtype = numpy.uint8) # Message corresponding to the current frame
        self.remaining_samples = [] # If a symbol is split between 2 buffers, we keep it for the next one
        self.remaining_bits = numpy.zeros(0, dtype = bool) # If a 8-bit character is split between 2 buffers, we keep it for the next one
        self.last_decoded_bit = True   
        self.state = State.SCAN
        self.f1 = 2400
        self.f2 = 1200
        
        #self.set_min_ninput_items(2048)
        self.samples_per_symbol = int(self.fs / self.f1)
        self.k = numpy.arange(0,int(15*self.fs/self.f1))
        self.gamma = numpy.sin(2*numpy.pi*(self.f1/self.fs)*numpy.asarray(self.k))
        self.k2 = range(0,int(self.fs/self.f1))
        self.h1 = numpy.sin(2*numpy.pi*self.f1/self.fs*numpy.asarray(self.k2))
        self.h0 = numpy.sin(2*numpy.pi*self.f2/self.fs*numpy.asarray(self.k2))
        self.pow_vect = [1, 2, 4, 8, 16, 32, 64, 0]
        self.sync_sequence = [43, 42, 22, 22, 1] #Including the SOH in this sequence 
        self.sync_sequence_ok = False
        self.bit_sync = False
        self.checksum_depth = 20 # window of running mean for the character checksum validation
        self.checksum_tolerance = 10 # Number of characters that are allowed to be wrong in the checksum window
        self.ETX = 3
        self.DEL = 127
        self.max_frame_size = 248 # 248 bytes, without pre-key, ETX, CRC and BCS
        self.acaDic = ["" for x in range(0,129)]
        self.acaDic[1] = 'NUL'
        self.acaDic[2] = 'SOH'
        self.acaDic[3] = 'STX'
        self.acaDic[4] = 'ETX'
        self.acaDic[5] = 'EOT'
        self.acaDic[6] = 'ENQ'
        self.acaDic[7] = 'ACK'
        self.acaDic[8] = 'BEL'
        self.acaDic[9] = 'BS'
        self.acaDic[10] = 'HT'
        self.acaDic[11] = 'LF'
        self.acaDic[12] = 'VT'
        self.acaDic[13] = 'FF'
        self.acaDic[14] = 'CR'
        self.acaDic[15] = 'SO'
        self.acaDic[16] = 'SI'
        self.acaDic[17] = 'DLE'
        self.acaDic[18] = 'DC1'
        self.acaDic[19] = 'DC2'
        self.acaDic[20] = 'DC3'
        self.acaDic[21] = 'DC4'
        self.acaDic[22] = 'NAK'
        self.acaDic[23] = 'SYN'
        self.acaDic[24] = 'ETB'
        self.acaDic[25] = 'CAN'
        self.acaDic[26] = 'EM'
        self.acaDic[27] = 'SUB'
        self.acaDic[28] = 'ESC'
        self.acaDic[29] = 'FS'
        self.acaDic[30] = 'GS'
        self.acaDic[31] = 'RS'
        self.acaDic[32] = 'US'
        self.acaDic[33] = 'SP'
        self.acaDic[34] = '!'
        self.acaDic[35] = '"'
        self.acaDic[36] = '#'
        self.acaDic[37] = '$'
        self.acaDic[38] = '%'
        self.acaDic[39] = '&'
        self.acaDic[40] = "'"
        self.acaDic[41] = '('
        self.acaDic[42] = ')'
        self.acaDic[43] = '*'
        self.acaDic[44] = '+'
        self.acaDic[45] = ','
        self.acaDic[46] = '-'
        self.acaDic[47] = '.'
        self.acaDic[48] = '/'
        self.acaDic[49] = '0'
        self.acaDic[50] = '1'
        self.acaDic[51] = '2'
        self.acaDic[52] = '3'
        self.acaDic[53] = '4'
        self.acaDic[54] = '5'
        self.acaDic[55] = '6'
        self.acaDic[56] = '7'
        self.acaDic[57] = '8'
        self.acaDic[58] = '9'
        self.acaDic[59] = ':'
        self.acaDic[60] = ''
        self.acaDic[61] = '<'
        self.acaDic[62] = '='
        self.acaDic[63] = '>'
        self.acaDic[64] = '?'
        self.acaDic[65] = '@'
        self.acaDic[66] = 'A'
        self.acaDic[67] = 'B'
        self.acaDic[68] = 'C'
        self.acaDic[69] = 'D'
        self.acaDic[70] = 'E'
        self.acaDic[71] = 'F'
        self.acaDic[72] = 'G'
        self.acaDic[73] = 'H'
        self.acaDic[74] = 'I'
        self.acaDic[75] = 'J'
        self.acaDic[76] = 'K'
        self.acaDic[77] = 'L'
        self.acaDic[78] = 'M'
        self.acaDic[79] = 'N'
        self.acaDic[80] = 'O'
        self.acaDic[81] = 'P'
        self.acaDic[82] = 'Q'
        self.acaDic[83] = 'R'
        self.acaDic[84] = 'S'
        self.acaDic[85] = 'T'
        self.acaDic[86] = 'U'
        self.acaDic[87] = 'V'
        self.acaDic[88] = 'W'
        self.acaDic[89] = 'X'
        self.acaDic[90] = 'Y'
        self.acaDic[91] = 'Z'
        self.acaDic[92] = '['
        self.acaDic[93] = '\\'
        self.acaDic[94] = ']'
        self.acaDic[95] = '^'
        self.acaDic[96] = '_'
        self.acaDic[97] = '`'
        self.acaDic[98] = 'a'
        self.acaDic[99] = 'b'
        self.acaDic[100] = 'c'
        self.acaDic[101] = 'd'
        self.acaDic[102] = 'e'
        self.acaDic[103] = 'f'
        self.acaDic[104] = 'g'
        self.acaDic[105] = 'h'
        self.acaDic[106] = 'i'
        self.acaDic[107] = 'j'
        self.acaDic[108] = 'k'
        self.acaDic[109] = 'l'
        self.acaDic[110] = 'm'
        self.acaDic[111] = 'n'
        self.acaDic[112] = 'o'
        self.acaDic[113] = 'p'
        self.acaDic[114] = 'q'
        self.acaDic[115] = 'r'
        self.acaDic[116] = 's'
        self.acaDic[117] = 't'
        self.acaDic[118] = 'u'
        self.acaDic[119] = 'v'
        self.acaDic[120] = 'w'
        self.acaDic[121] = 'x'
        self.acaDic[122] = 'y'
        self.acaDic[123] = 'z'
        self.acaDic[124] = '['
        self.acaDic[125] = '|'
        self.acaDic[126] = ')'
        self.acaDic[127] = '~'
        self.acaDic[128] = 'DEL'
        
    def binToACARS(self, trame):
        str_result = []
        for i in range(0,len(trame)):
            str_result.append(self.acaDic[trame[i] + 1])
        
        str_result.append('\n')
        separator = ' '
        return separator.join(str_result)
        
    
    def set_corr_thres(self, corr_thres):
        self.corr_thres = corr_thres
        
        
        
        
        
        
    # TODO
        
    # Replace all the deletions and indice shifts by python masked arrays
        
    # When deleting messages that don't match the +*SYNSYN, put the remaining samples for the next buffer
        
    # Implement BCS
        
    # Be sure of the exact number of samples that need to be kept until the next call to the work function, in cases:
        # End of frame detected

    # Make sure that the synchronization is not lost during a long frame

    # Decide on a paradigm for the new implementation: handle the data sample by sample, or fill a buffer to wait until 4096 samples ?

    # Implement a listener on the "correlation threshold" slider in GNU Radio companion

    # Replace the power squelch by a noise estimator for "auto gain control"

    # Parser

    # Output to file

    # Output network

    # Improve decisions on parity checks

    # Write dictionary in a separate file

    def work(self, input_items, output_items):
        if(len(self.remaining_samples) < 4096):
            self.remaining_samples = numpy.concatenate((self.remaining_samples, input_items[0]))
        else:

           
            in0 = []
            
            in0 = numpy.concatenate((self.remaining_samples, input_items[0]))
            self.remaining_samples = []

#            s = str(len(in0))
#            nvec = numpy.fromstring(s, dtype=numpy.uint8, count=len(s))
#            vec = pmt.to_pmt(nvec)
#            self.message_port_pub(pmt.intern("parsed_out"), pmt.cons(pmt.PMT_NIL, vec))
            
            if(self.state == State.SCAN): # Lookin for the pre-key sequence
                self.current_message = numpy.zeros(0, dtype = numpy.uint8)
                self.remaining_bits = numpy.zeros(0, dtype = bool)
                self.bit_sync = False
                self.sync_sequence_ok = False
                self.last_decoded_bit = True
                self.sync_sequence = [43, 42, 22, 22, 1] #Including the SOH in this sequence 
                
                grandGamma = numpy.correlate(in0, self.gamma, 'valid')
                
                indiceMaxCorr = numpy.argmax(grandGamma)

                if(grandGamma[indiceMaxCorr] > self.corr_thres): #The prekey has been found
                    self.state = State.SYNC
                    in0 = in0[indiceMaxCorr:]     

                    
            if(self.state == State.SYNC):
                index_remain_samples_init = len(in0) - numpy.mod(len(in0), self.samples_per_symbol)
                
                self.remaining_samples = in0[index_remain_samples_init:]
                
                in0 = in0[:index_remain_samples_init]  

                trameCentered = in0;
                nombreSymboles = int(len(trameCentered)/ self.samples_per_symbol) 
                if(nombreSymboles > 0):
                    tramesReshaped = numpy.transpose(numpy.reshape(trameCentered, (nombreSymboles, self.samples_per_symbol)))
                    
                    delta = numpy.zeros(nombreSymboles)
                    
                    for j in range(0, nombreSymboles):
                        symbole = tramesReshaped[:,j]
                        
                        #print numpy.flipud(symbole) * self.h1
                        Gamma10 = numpy.sum(symbole * self.h1)
                        Gamma00 = numpy.sum(symbole * self.h0)
                        
                        delta[j] = numpy.square(Gamma10) - numpy.square(Gamma00)
                        
                    bitstream_uncoded = delta < 0
             
                    bitstream = numpy.zeros(len(bitstream_uncoded), dtype = bool)
                    bitstream[0] = (self.last_decoded_bit != bitstream_uncoded[0])
                    
                    for j in range(1, len(bitstream_uncoded)):
                        bitstream[j] = (bitstream[j-1] != bitstream_uncoded[j])
        
                    # Start of vector to consider; If we get the rest of a frame where bit sync has already been successful, we consider the first element
                    where_end_prekey = numpy.where(bitstream == 0)[0]    
                    if((len(where_end_prekey) == 0) and (not self.bit_sync)): # End of prekey not detected, because the current buffer only contains the prekey; We will see in the next buffer
                        self.bit_sync = False
                    else:
                        if(self.bit_sync):
                            indice_synch = 0
                        else:
                            indice_synch = where_end_prekey[0] - 2
                            self.bit_sync = True
        
                        bitstream = bitstream[indice_synch:]
                        
                        bitstream = numpy.concatenate((self.remaining_bits, bitstream))
                        
                        self.remaining_bits = numpy.zeros(0, dtype = bool)
                        
                        limit = int(len(bitstream) / 8 ) 
                        
                        if(limit < 0):
                            limit = 0
        
                        if(len(bitstream) > 0):
                            self.last_decoded_bit = bitstream[-1]
                        else:
                            self.last_decoded_bit = True
                            
                        self.remaining_bits = bitstream[limit*8:]
                        bitstream= bitstream[:limit*8]
                        
                        if(len(bitstream) > 0):
                            # Recopying the last bit so that the next buffer knows the convention for differential encoding
                            
                            charact = numpy.reshape(bitstream, (limit, 8))
                            decimalVect = numpy.sum(charact*self.pow_vect, axis = 1, dtype = numpy.uint8)
                            
                            if(not self.sync_sequence_ok): #Checking the +*SYNSYN sequence for the first time
                                sync_validation_test = True
                                
                                while(sync_validation_test and (len(self.sync_sequence) > 0) and (len(decimalVect) > 0)):
                                    if(self.sync_sequence[0] != decimalVect[0]):
                                        sync_validation_test = False
                                        self.state = State.SCAN
                                        # TO DO: KEEP THE REST OF THE SAMPLES FOR THE NEXT BUFFER
                                    else:
                                        decimalVect = numpy.delete(decimalVect, 0, axis = 0)
                                        charact = numpy.delete(charact, 0, axis = 0)
                                        self.sync_sequence = numpy.delete(self.sync_sequence, 0, axis = 0)
                                        if(len(decimalVect) == 0):
                                            sync_validation_test = False #Case where the SYNC sequence is split between 2 buffers
                                
                                self.sync_sequence_ok = sync_validation_test
                                
                            if(self.sync_sequence_ok):
                                
                                
                                    
                                find_etx = numpy.where(decimalVect == self.ETX)
                                
                                if(len(find_etx[0]) > 0): #ETX
                                    index_etx = find_etx[0][0]
                                    decimalVect = decimalVect[:index_etx+1]
                                    
                                    index_remain_samples = (len(decimalVect)*8 + len(self.remaining_bits) + indice_synch)*self.samples_per_symbol
                                    if(index_remain_samples >= len(in0)):
                                        index_remain_samples = len(in0) - 1
                                    self.remaining_samples = numpy.concatenate((self.remaining_samples,in0[index_remain_samples:]))
                                    self.current_message = numpy.concatenate((self.current_message, decimalVect))
                                    
                                    ## SEND MSG
                                    list_message = numpy.ndarray.tolist(self.current_message)
                                    s = self.binToACARS(list_message)
                                    nvec = numpy.fromstring(s, dtype=numpy.uint8, count=len(s))
                                    vec = pmt.to_pmt(nvec)
                                    self.message_port_pub(pmt.intern("raw_out"), pmt.cons(pmt.PMT_NIL, vec))
                                    
                                    self.state = State.SCAN
                                else:
                                    # Vector of checksums; Equals 1 when the checksum is not respected, 0 else
                                    checksum_vector = numpy.mod(numpy.sum(charact[:, 0:7], axis = 1), 2) == charact[:,7]
                                    cumsum = numpy.cumsum(numpy.insert(checksum_vector, 0, 0)) 
                                    running_checksum_mean = (cumsum[self.checksum_depth:] - cumsum[:-self.checksum_depth])
                                    find_checksum_fault = numpy.where(running_checksum_mean > self.checksum_tolerance)
                                    
                                    if(len(find_checksum_fault[0]) > 0): #The level of invalid checksums in the window exceeded the threshold                    
                                        index_checksum_fault = find_checksum_fault[0][0]
                                        index_remain_samples = ((len(checksum_vector) - index_checksum_fault) *8 + len(self.remaining_bits) + indice_synch)*self.samples_per_symbol
                                        if(index_remain_samples >= len(in0)):
                                            index_remain_samples = len(in0) - 1                        
                                        self.remaining_samples = numpy.concatenate((self.remaining_samples,in0[index_remain_samples:]))
                                        
                                        self.state = State.SCAN
                                        
                                    else:
                                        self.current_message = numpy.concatenate((self.current_message, decimalVect))
                                    
                                #if(len(self.current_message) > self.max_frame_size): #An issue occured, and for a reason the receiver read more than 248 bytes
                                #   self.state = State.SCAN
            
#        if(len(self.current_message) > 0):
#            list_message = numpy.ndarray.tolist(self.current_message)
#                            
#            s = self.binToACARS(list_message)
#        
#            nvec = numpy.fromstring((s), dtype=numpy.uint8, count=len(s))
#            vec = pmt.to_pmt(nvec)
#            self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.PMT_NIL, vec))
#            
#            if(self.state == State.SCAN):
#                s = str(len(self.current_message))
#        
#                nvec = numpy.fromstring((s), dtype=numpy.uint8, count=len(s))
#                vec = pmt.to_pmt(nvec)
#                self.message_port_pub(pmt.intern("out"), pmt.cons(pmt.PMT_NIL, vec))
        return len(input_items[0])

