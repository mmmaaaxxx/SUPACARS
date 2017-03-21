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

import numpy
import pmt
import requests
import string
from bs4 import BeautifulSoup
from gnuradio import gr
import types
from time import gmtime, strftime
import wget
import Tkinter
import Image, ImageTk
import os



class label_state:
    LABEL_UNDEFINED = 1
    LABEL__DEL = 2
    LABEL_H1 = 3
    LABEL_5U = 4
    LABEL_5R = 5
    LABEL_00 = 6
    LABEL_B5 = 7
    LABEL_Q0 = 8
    LABEL_54 = 9
    LABEL_5D = 10
    LABEL_SQ = 11
    LABEL_F3 = 12
    LABEL_B1 = 13
    LABEL_B2 = 14
    LABEL_B3 = 15
    LABEL_B4 = 16
    LABEL_B6 = 17
    LABEL_QA = 18
    LABEL_QK = 19
    LABEL_QL = 20   
    LABEL_Q1 = 21
    LABEL_Q2 = 22
    
class mode_state:
    MODE_UNDEFINED = 1
    MODE_2 = 2
    MODE_AtoG = 3
    MODE_GtoA = 4

    
class acars_dictionary:
    def translate(self, decimal_vect):
        if (not all(isinstance(item, numpy.uint8) for item in decimal_vect)): # List contains non integer numbers
            return ''

        if ((min(decimal_vect) < 0) or (max(decimal_vect) > 127)):
            return ''

        return [self.dictionary[x] for x in decimal_vect]


    def __init__(self): # ACARS dictionary
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
        


class acarsparser(gr.sync_block):
    """
    docstring for block acarsparser
    """
    def __init__(self, db_request_mode, api_key):
        gr.sync_block.__init__(self,
            name="acarsparser",
            in_sig=None,
            out_sig=None)
        self.db_request_mode = db_request_mode
        self.api_key = api_key
        self.acars_dic = acars_dictionary()
        self.pow_vect = [1, 2, 4, 8, 16, 32, 64, 0]
        
        self.label_state = label_state.LABEL_UNDEFINED
        self.mode_state = label_state.LABEL_UNDEFINED
        
        # Create message ports
        self.message_port_register_out(pmt.intern("parsed_output"))
        self.message_port_register_in(pmt.intern("in"))
        self.set_msg_handler(pmt.intern("in"), self.msg_handler_method)
        
    def mode_reader(*arg):
        self = arg[0]
        mode = arg[2]

        if (mode == "2"): # 2 case
            self.mode_state=mode_state.MODE_2
            mode = mode + " ==> Category A - Broadcasting to all the stations - Bi-directionnal transmission"
        else:
            if(mode.isupper()):
                self.mode_state=mode_state.MODE_AtoG
                mode = mode + " ==> Category B - Transmitting to a specific station - Air to Ground transmission"
            else:
                self.mode_state=mode_state.MODE_GtoA
                mode = mode + " ==> Category B - Transmitting from a specific station - Ground to Air transmission"            
        return mode
        
    def label_reader(*arg):
        self = arg[0]
        label = arg[2]
        
        if (label == "_ DEL"): # _DEL case
            self.label_state=label_state.LABEL__DEL
            label = label + " ==> General response, demand mode, no information to transmit"
        elif (label== "0 0"): # 00 case
            self.label_state=label_state.LABEL_00
            label = label + " ==> Emergency Situation Report (Aircraft Hijack)"
        elif (label == "5 4"): # 54 case
            label = label + " ==> Voice Contact Request / Voice Go-ahead"
            self.label_state=label_state.LABEL_54
        elif (label == "H 1"): # H1 case
            self.label_state=label_state.LABEL_H1
            label = label + " ==> Message to/from terminal"
        elif (label == "5 D"): # 5D case
            label = label + " ==> Automatic Terminal Information Service (ATIS) Request"
            self.label_state=label_state.LABEL_5D
        elif (label == "5 R"): # 5R case
            label = label + " ==> Aircrew Initiated Position Report"
            self.label_state=label_state.LABEL_5R
        elif (label == "5 U"): # 5U case
            label = label + " ==> Weather Request"
            self.label_state=label_state.LABEL_5U
        elif (label == "B 1"): # B1 case
            label = label + " ==> Request Oceanic Clearance"
            self.label_state=label_state.LABEL_B1
        elif (label == "B 2"): # B2 case
            label = label + " ==> Request Oceanic Readback"
            self.label_state=label_state.LABEL_B2
        elif (label == "B 3"): # B3 case
            label = label + " ==> Request Departure Clearance"
            self.label_state=label_state.LABEL_B3
        elif (label == "B 4"): # B4 case
            label = label + " ==> Ackn. Departure Clearance"
            self.label_state=label_state.LABEL_B4  
        elif (label == "B 5"): # B5 case
            label = label + " ==> Waypoint Position Report"
            self.label_state=label_state.LABEL_B5
        elif (label == "B 6"): # B6 case
            label = label + " ==> Provide Automatic Dependent Surveillance (ADS) Report"
            self.label_state=label_state.LABEL_B6
        elif (label == "Q 0"): # B5 case
            label = label + " ==> Link Test"
            self.label_state=label_state.LABEL_Q0
        elif (label == "Q 1"): # B5 case
            label = label + " ==> Estimated Time of Arrival (ETA) Departure/Arrival Reports"
            self.label_state=label_state.LABEL_Q1
        elif (label == "Q 2"): # B5 case
            label = label + " ==> Estimated Time of Arrival (ETA) Report"
            self.label_state=label_state.LABEL_Q2
        elif (label == "Q A"):
            label = label + " ==> OUT/fuel Report (IATA Airport Code)"
            self.label_state=label_state.LABEL_QA
        elif (label == "Q K"):
            label = label + " ==> Landing Report (IATA Airport Code)"
            self.label_state=label_state.LABEL_QK
        elif (label == "Q L"):
            label = label + " ==> Arrival Report (IATA Airport Code)"
            self.label_state=label_state.LABEL_QL
        elif (label == "S Q"):
            label = label + " ==> Squitter Message"
            self.label_state=label_state.LABEL_SQ
        elif (label == "F 3"):
            label = label + " ==> Dedicated Transiver Advisory"
            self.label_state=label_state.LABEL_F3
        else:
            self.label_state=label_state.LABEL_UNDEFINED
               
        # Add new cases here !            
        return label
        
    def sublabel_reader(*arg): # used for H1 label ACARS frames
        self = arg[0]
        sublabel = arg[2]
        if (sublabel == "# M 1"): # M1 case
            sublabel = sublabel + " ==> Flight Management Computer, Left"
        elif (sublabel == "# M 2"): # M2 case
            sublabel = sublabel + " ==> Flight Management Computer, Right"
        elif (sublabel == "# C F"): # CF case
            sublabel = sublabel + " ==> Central Fault Display"
        elif (sublabel == "# D F"): # DF case
            sublabel = sublabel + " ==> Digital Flight Data Acquisition Unit"
        # Add new cases here !            
        return sublabel
        
    def label_sq_parser(*arg):
        self = arg[0]
        mat_frame = arg[2]
        size_mat_frame = mat_frame.shape
        separator = " " # used latter to turn a table of chars into a string
        no_separator = "" # used latter to turn the table of chars into a string
        
        # Version Number Parsing
        decimal_vp = numpy.sum(mat_frame[13:15,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
        translated_vp = self.acars_dic.translate(decimal_vp)
        tempo = separator.join(translated_vp)
        vp = no_separator.join(translated_vp)
        vp_char = "Version Number : "+ tempo +"\n"
        
        # Service Provider Parsing
        decimal_sp = numpy.sum(mat_frame[15:17,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
        translated_sp = self.acars_dic.translate(decimal_sp)
        tempo = separator.join(translated_sp)
        sp_char = "Service Provider : "+ tempo +"\n"
                
        if (vp == "00"): #Format of version 0
            
            if (size_mat_frame[0]>18):
                # Text Parsing
                decimal_txt = numpy.sum(mat_frame[17:,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
                translated_txt = self.acars_dic.translate(decimal_txt)
                tempo = separator.join(translated_txt)
                txt_char = "Text : "+ tempo +"\n"
            else:
                txt_char ="";
            
            output_char =  vp_char + sp_char + txt_char
                    
        elif(vp == "01"): #Format of version 1
        
            # IATA Station ID Parsing
            decimal_iata_si = numpy.sum(mat_frame[17:20,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
            translated_iata_si = self.acars_dic.translate(decimal_iata_si)
            tempo = separator.join(translated_iata_si)
            iata_si_char = "IATA Station ID : "+ tempo +"\n"
                    
            # ICAO Station ID Parsing
            decimal_icao_si = numpy.sum(mat_frame[20:24,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
            translated_icao_si = self.acars_dic.translate(decimal_icao_si)
            tempo = separator.join(translated_icao_si)
            icao_si_char = "ICAO Station ID : "+ tempo +"\n"
            
            # Station Number ID
            decimal_sid = numpy.sum(numpy.reshape(mat_frame[24,:]*self.pow_vect, (1,8)) , axis = 1 , dtype = numpy.uint8)
            translated_sid = self.acars_dic.translate(decimal_sid)
            tempo = separator.join(translated_sid)
            sid_char = "Station Number ID : "+ tempo +"\n"
            
            if (size_mat_frame[0]>26):
                # Text Parsing
                decimal_txt = numpy.sum(mat_frame[25:,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
                translated_txt = self.acars_dic.translate(decimal_txt)
                tempo = separator.join(translated_txt)
                txt_char = "Text : "+ tempo +"\n"
            else:
                txt_char ="";
            
            output_char =  vp_char + sp_char + iata_si_char + icao_si_char + sid_char + txt_char
                    
        elif(vp == "02"): #Format of version 2
        
            # IATA Station ID Parsing
            decimal_iata_si = numpy.sum(mat_frame[17:20,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
            translated_iata_si = self.acars_dic.translate(decimal_iata_si)
            tempo = separator.join(translated_iata_si)
            iata_si_char = "IATA Station ID : "+ tempo +"\n"
            
            # ICAO Station ID Parsing
            decimal_icao_si = numpy.sum(mat_frame[20:24,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
            translated_icao_si = self.acars_dic.translate(decimal_icao_si)
            tempo = separator.join(translated_icao_si)
            icao_si_char = "ICAO Station ID : "+ tempo +"\n"
            
            # Station Number ID
            decimal_sid = numpy.sum(numpy.reshape(mat_frame[24,:]*self.pow_vect, (1,8)) , axis = 1 , dtype = numpy.uint8)
            translated_sid = self.acars_dic.translate(decimal_sid)
            tempo = separator.join(translated_sid)
            sid_char = "Station Number ID : "+ tempo +"\n"
            
            # Latitude Parsing
            decimal_lat = numpy.sum(mat_frame[25:30,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
            translated_lat = self.acars_dic.translate(decimal_lat)
            tempo = separator.join(translated_lat)
            lat_char = "Latitude : "+ tempo +"\n"
            
            # Longitude Parsing
            decimal_long = numpy.sum(mat_frame[30:36,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
            translated_long = self.acars_dic.translate(decimal_long)
            tempo = separator.join(translated_long)
            long_char = "Longitude : "+ tempo +"\n"
            
            # The rest of the frame parsing is to be continued ...
            decimal_txt = numpy.sum(mat_frame[36:,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
            translated_txt = self.acars_dic.translate(decimal_txt)
            tempo = separator.join(translated_txt)
            txt_char = "Text : "+ tempo +"\n"
            
            output_char =  vp_char + sp_char + iata_si_char + icao_si_char + sid_char + lat_char + long_char + txt_char

        return output_char
        
    def label_h1_parser(*arg):
        self = arg[0]
        mat_frame = arg[2]
        separator = " " # used latter to turn a table of chars into a string
        
        # Sub Label parsing
        decimal_sublabel = numpy.sum(mat_frame[23:26,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
        translated_sublabel = self.acars_dic.translate(decimal_sublabel)
        tempo = separator.join(translated_sublabel)
        tempo = self.sublabel_reader(self,tempo)
        sublabel_char = "Sublabel : "+ tempo +"\n"
        
        decimal_txt = numpy.sum(mat_frame[26:,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
        translated_txt = self.acars_dic.translate(decimal_txt)
        tempo = separator.join(translated_txt)
        tempo = string.replace(tempo,'SP',' ')
        tempo = string.replace(tempo,'CR LF','\n')
        txt_char = "Text : "+ tempo +"\n"
        output_char = sublabel_char + txt_char
        
        return output_char
            

    def msg_handler_method(self, msg):
        dic = pmt.cdr(msg)
        
        # Extracting the values of the dictionnary with the keys defined in acars.py
        mat_pmt = pmt.dict_ref(dic, pmt.intern("mat_vect_str"),pmt.PMT_NIL)
        crc_pmt =  pmt.dict_ref(dic, pmt.intern("crc_ok"),pmt.PMT_NIL)
        parity_pmt = pmt.dict_ref(dic, pmt.intern("parity_ok"),pmt.PMT_NIL)

        mat_vec_str =pmt.to_python(mat_pmt)
        parity_ok = pmt.to_python(parity_pmt)
        crc_ok = pmt.to_python(crc_pmt)

        mat_vec = numpy.fromstring(mat_vec_str,dtype=bool) # Converting the string into a vector
        mat_frame = numpy.reshape(mat_vec,(len(mat_vec)/8,8)) # Reshaping the vector into a matrix
        
        intro_char = "--------------------------------------------------------- \nNew Frame ! \nTime : "+strftime("%Y-%m-%d %H:%M:%S", gmtime()) + "\n"
        separator = " " # used latter to turn a table of chars into a string
        no_separator = "" # used latter to turn the table of chars into a string
               
        # Mode parsing
        decimal_mode = numpy.sum(numpy.reshape(mat_frame[0,:]*self.pow_vect, (1,8)) , axis = 1 , dtype = numpy.uint8)
        translated_mode = self.acars_dic.translate(decimal_mode)
        tempo = separator.join(translated_mode)
        tempo = self.mode_reader(self,tempo)
        mode_char = "Transmission Mode : "+ tempo + "\n"
               
        # Address parsing
        decimal_address = numpy.sum(mat_frame[1:8,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
        translated_address = self.acars_dic.translate(decimal_address)
        tempo = separator.join(translated_address)
        tempo_ = no_separator.join(translated_address)
        
        request_address = string.replace(tempo_,'.','') # If the address plane is smaller than 6 chars, '.' are used for padding. We have to remove them to do the request.        
        if (self.db_request_mode == True) : # If the db_request_mode is On, it will parse an HTML page from https://planefinder.net to get the aircraft model and the arrival/departue airports         
            headers= "User-Agent': 'Mozilla/5.0'"
            url='https://planefinder.net/data/aircraft/'
            
            try:
                r= requests.get(url+request_address,headers)
                soup = BeautifulSoup(r.text,'html.parser')
                airplane = soup.body.find('h1')
                if type(airplane) is types.NoneType:
                      airplane_char = "No Information Available (from https://planefinder.net)" 
                else: 
                    airplane_char = str(airplane.text.encode('ascii','ignore'))
                    #airplane_char = string.replace(airplane_char,' ̶','')
                request_adress_char = " - Aircraft Model : "+ airplane_char +"\n"
                
                global airports
                 
                if len(soup.body.find_all('table'))==0:
                    airports_char = "Departure & Arrival Airports : No Information Available (from https://planefinder.net)" 
                else:
                    for airports in soup.body.find_all('table'):
                        airports
                    departure_airport_char = str(airports.td.a.next)
                    departure_airport_char= departure_airport_char.encode('ascii','ignore')
                    arrival = airports.td.a.previous
                    arrival_airport_char = str(arrival.contents[2]['title'][21:len(arrival.contents[2]['title'])])
                    arrival_airport_char= arrival_airport_char.encode('ascii','ignore')
                    airports_char = "Departure Airport : " +departure_airport_char + " - Arrival Airport : "+arrival_airport_char
               
                request_adress_char = request_adress_char + airports_char  
                
            except Exception as e:
                #print e # print the exception in the gnuradio terminal
                request_adress_char = " - Request Failed :( from " +url+request_address
            tempo = tempo + request_adress_char
            
        address_char = "Airplane Address : "+ tempo +"\n"
        
        # ACK/NAK parsing
        decimal_ack = numpy.sum(numpy.reshape(mat_frame[8,:]*self.pow_vect, (1,8)) , axis = 1 , dtype = numpy.uint8)
        translated_ack = self.acars_dic.translate(decimal_ack)
        tempo = separator.join(translated_ack)
        ack_char = "ACK/NAK : "+ tempo +"\n"
        
        # Label parsing
        decimal_label = numpy.sum(mat_frame[9:11,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
        translated_label = self.acars_dic.translate(decimal_label)
        tempo = separator.join(translated_label)
        tempo = self.label_reader(self,tempo)
        label_char = "Label : "+ tempo +"\n"
        
        # Block ID parsing
        decimal_blockid = numpy.sum(numpy.reshape(mat_frame[11,:]*self.pow_vect, (1,8)) , axis = 1 , dtype = numpy.uint8)
        translated_blockid = self.acars_dic.translate(decimal_blockid)
        tempo = separator.join(translated_blockid)
        blockid_char = "Block ID : "+ tempo +"\n"
        
        output_char = intro_char + mode_char + address_char + ack_char + label_char + blockid_char
        
        size_mat_frame = mat_frame.shape
        if (size_mat_frame[0]>12): # Some ACARS frames are stopped after the Block ID for specific labels
            
            # Block STX
            decimal_stx = numpy.sum(numpy.reshape(mat_frame[12,:]*self.pow_vect, (1,8)) , axis = 1 , dtype = numpy.uint8)
            translated_stx = self.acars_dic.translate(decimal_stx)
            tempo = separator.join(translated_stx)
            stx_char = tempo +"\n"
            output_char = output_char + stx_char;
            
            if (self.label_state == label_state.LABEL_SQ):
                
                output_char = output_char + self.label_sq_parser(self,mat_frame)
            
            else:
                   
                # Message Sequence Number parsing
                decimal_msn = numpy.sum(mat_frame[13:17,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
                translated_msn = self.acars_dic.translate(decimal_msn)
                tempo = separator.join(translated_msn)
                msn_char = "Message Sequence Number : "+ tempo +"\n"
                
                output_char = output_char + msn_char
                
                if (size_mat_frame[0]>18): # Some ACARS frames are stopped after the Message Sequence Number
                    
                    # Flight Number parsing
                    decimal_fn = numpy.sum(mat_frame[17:23,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
                    translated_fn = self.acars_dic.translate(decimal_fn)
                    tempo = separator.join(translated_fn)
                    
                    request_fn = no_separator.join(translated_fn)
                    if (self.db_request_mode == True) : # If the db_request_mode is On, it will make a json request to get the departure and arrival airports of the plane from IATA DB
                        if (len(self.api_key)>0): # You need to define an api_key in the parameters of the acarsparser block
                            try:
                                r = requests.get('https://iatacodes.org/api/v6/routes?&api_key='+self.api_key+'&flight_number='+request_fn+'')
                                data =  r.json()
                                if (len(data['response'])==0):
                                    request_arrival_departure_char = " - No Information Available about Departure and Arrival (in IATA DB)"
                                else:
                                    departure = data ['response'][0]['departure']
                                    arrival= data ['response'][0]['arrival']
                                    r = requests.get('https://iatacodes.org/api/v6/airports?code='+departure+'&api_key='+self.api_key+'')
                                    data =  r.json()
                                    departure_name = data ['response'][0]['name']
                                    departure_name_char = str(departure_name.encode('ascii','ignore'))
                                    r = requests.get('https://iatacodes.org/api/v6/airports?code='+arrival+'&api_key='+self.api_key+'')
                                    data =  r.json()
                                    arrival_name = data ['response'][0]['name']
                                    arrival_name_char = str(arrival_name.encode('ascii','ignore'))
                                    request_arrival_departure_char = " - Departure Airport : "+departure_name_char +" - Arrival Airport : "+arrival_name_char +" (from IATA DB)"
                                
                            except Exception as e:
                                #print e
                                request_arrival_departure_char = " - Request Failed :( from " + ' https://iatacodes.org/api/v6/routes?&api_key='+self.api_key+'&flight_number='+request_fn+''
                            tempo = tempo + request_arrival_departure_char
                        
                        
                    fn_char = "Flight Number : "+ tempo +"\n"
                    output_char = output_char + fn_char
                    
                    if (size_mat_frame[0]>23):
                        # Text parsing
                        if (self.label_state == label_state.LABEL_H1):
                            
                           output_char = output_char + self.label_h1_parser(self,mat_frame)
                        
                        else: # For all the other label
                            
                            decimal_txt = numpy.sum(mat_frame[23:,:]*self.pow_vect, axis = 1, dtype = numpy.uint8)
                            translated_txt = self.acars_dic.translate(decimal_txt)
                            tempo = separator.join(translated_txt)
                            tempo_ = string.replace(tempo,'SP','')
                            tempo = string.replace(tempo_,'CR LF','\n')
                            txt_char = "Text : "+ tempo +"\n"
                            output_char = output_char + txt_char
                        
    
        output_char = output_char + "ETX\n--------------------------------------------------------- \n"
        if (not parity_ok):
            output_char = output_char + "WARNING - INVALID PARITY CHECKS\n"
        if (not crc_ok):
            output_char = output_char + "WARNING - INVALID BLOCK CHECK SEQUENCE\n"
        nvec = numpy.fromstring(output_char, dtype=numpy.uint8, count=len(output_char))
        vec = pmt.to_pmt(nvec)
        self.message_port_pub(pmt.intern("parsed_output"), pmt.cons(pmt.PMT_NIL, vec))
        
        if (self.db_request_mode == True) : # If the db_request_mode is On, it will parse an HTML page from https://planefinder.net to get the aircraft picture and display it         
            filename = ""
            try:
                if len(soup.find_all('div',attrs={'class' : 'technical-image'}))>0:
                    for airplane_image in soup.find_all('div',attrs={'class' : 'technical-image'}):
                        airplane_image.get('style')
                    
                    image=str(airplane_image.get('style')[22:len(airplane_image.get('style'))])
                    url_image = 'https:'+ image.replace(')','')
                    filename = wget.download(url_image,"plane_picture.jpg")
                    im = Image.open(filename)
                    w = 480
                    h = 167
                    size_picture = w, h
                    im.thumbnail(size_picture, Image.ANTIALIAS)
                    root = Tkinter.Tk()
                    tkimage = ImageTk.PhotoImage(im)
                    root.title(airplane_char)
                    Tkinter.Label(root, image=tkimage).pack()
                    # get screen width and height
                    ws = root.winfo_screenwidth() # width of the screen
                    hs = root.winfo_screenheight() # height of the screen
                    
                    # calculate x and y coordinates for the Tk root window
                    x = (3*ws/4) - (w/2)
                    y = (hs/2) - (h/2)
                    
                    # set the dimensions of the screen 
                    # and where it is placed
                    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
                    root.after(4000, lambda: root.destroy())
                    root.mainloop()
                    os.remove(filename)
                                
            except Exception as e:
                 if os.path.isfile(filename):
                     os.remove(filename)
                 #print e
      
    def work(self, input_items, output_items):
        pass

