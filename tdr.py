'''
Documentation, License etc.

@package tdr
'''
import argparse

import logging
import math

import numpy as np
import scipy.signal as signal

#for Touchstone files
import skrf as rf

import glob
import sys
import struct
import os

class TDR():
    def __init__(self):
        self.freq = []
        self.im = []
        self.re = []

    def listFolder(self,folder,output):
        files = glob.glob(folder + '*.s2p')
        files.sort()
        self.gpr = [None] * 2**10
        for d in files:
            self.readP2S(d)
            self.gpr = np.vstack([self.gpr, self.td])
        print("done")
        self.writeDZT(output)
    
    def readP2S(self,file):
        ts=  rf.Network(file)
        self.re= ts.s21.s_re[:,0,0]
        self.im= ts.s21.s_im[:,0,0]
        self.freq=ts.f 
        self.calcTDR()


    def calcTDR(self):
        c = 299792458
        # TODO: Let the user select whether to use high or low resolution TDR?
        #FFT_POINTS = 2**14
        FFT_POINTS = 2**10

        if len(self.freq) < 2:
            return

        step_size = self.freq[1] - self.freq[0]
        if step_size == 0:
            self.tdr_result_label.setText("")
            print("Cannot compute cable length at 0 span")
            return

        s21 = []
        l = len(self.freq)
        for d in range(0,l):
            s21.append(np.complex(self.re[d], self.im[d]))

        window = np.blackman(len(self.freq))

        windowed_s21 = window * s21
        self.td = np.abs(np.fft.ifft(windowed_s21, FFT_POINTS))
        step = np.ones(FFT_POINTS)
        self.step_response = signal.convolve(self.td, step)

        self.step_response_Z = 50 * (1 + self.step_response) / (1 - self.step_response)

        time_axis = np.linspace(0, 1/step_size, FFT_POINTS)
        self.time = time_axis * 10**9 # s to ns
        self.distance_axis = time_axis * c
       
        index_peak = np.argmax(self.td)
        #print (self.distance_axis)
        l = len(time_axis)
        #f = open("tdr.csv", "a")
        #for i in range(0,l):
        #    f.write(str(time_axis[i]) + "   " + str(self.td[i]) + "\n")
        #f.close()

    def writeDZT(self,output):
        #filename = "test1.DZT"
        filename = output
        #header
        #
        # struct.pack
        # > big endian
        # B unsigned char (1 byte)
        # f float (4 bytes)
        # H unsigned short (2 bytes)
        # I unsigned int (4 bytes)
        # Q long lon (8 bytes)
        # s [] string
        if os.path.exists(filename):
            os.remove(filename) #this deletes the file
        fh = open(filename, "wb")
        rh_tag = 0x0700 #static?
        fh.write(struct.pack('<H', rh_tag))
        rh_data = 1024 #constant
        fh.write(struct.pack('<H', rh_data))
        rh_nsamp = len(self.gpr[0]) #samples  per scan
        fh.write(struct.pack('<H', rh_nsamp))
        rh_bits = 16 # bits per data word
        fh.write(struct.pack('<H', rh_bits))
        rh_zero = 0x8000 #constant
        fh.write(struct.pack('<H', rh_zero))
        rhf_sps = 1.0 #scans per second
        fh.write(struct.pack('<f', rhf_sps))
        rhf_spm = 4.0 #scans per meter
        fh.write(struct.pack('<f', rhf_spm))
        rhf_mpm = 0.0 # meters per mark
        fh.write(struct.pack('<f', rhf_mpm))
        rhf_position = 0.0 # position
        fh.write(struct.pack('<f', rhf_position))
        rhf_range = self.time[len(self.time)-1] # range in ns
        print (str(rhf_range))
        fh.write(struct.pack('<f', rhf_range))
        ###ok until here
        rh_npass = 0 # passes
        fh.write(struct.pack('<H', rh_npass))
        rhb_cft = 0 #creation date & time
        fh.write(struct.pack('<I', rhb_cft))
        rhb_mdt = 0 #last modification date & time
        fh.write(struct.pack('<I', rhb_mdt))
        rh_rgain = 1 #offset ti range gain function
        fh.write(struct.pack('<H', rh_rgain))
        rh_nrgain = 1 #size of range gain function
        fh.write(struct.pack('<H', rh_nrgain))
        rh_text = 0x0200 #offset to text
        fh.write(struct.pack('<H', rh_text))
        rh_ntext = 0 #size of text
        fh.write(struct.pack('<H', rh_ntext))
        rh_proc = 0 #0x0080 #offset to processing history
        fh.write(struct.pack('<H', rh_proc))
        rh_nproc = 0x0000 #size of processing history
        fh.write(struct.pack('<H', rh_nproc))
        rh_nchan = 1 #number of channels 
        fh.write(struct.pack('<H', rh_nchan))
        rhf_epsr = 1.0 #average dielectric constant
        fh.write(struct.pack('<f', rhf_epsr))
        rhf_top = 0.1 #position in meters
        fh.write(struct.pack('<f', rhf_top))
        rhf_depth = 5.0 #range in meters
        fh.write(struct.pack('<f', rhf_depth))
        rhc_coordX = 0 #X coordinates 
        fh.write(struct.pack('<Q', rhc_coordX))
        rhf_servo_level = 0.0 # gain servo level
        fh.write(struct.pack('<f', rhf_servo_level))
        reserved = myArray=np.chararray(3) #3 bytes reserved
        fh.write(reserved)
        rh_accomp = 0 #ant conf component
        fh.write(struct.pack('<B', rh_accomp))
        rh_sconfig = 1 #setup configuration number
        fh.write(struct.pack('<H', rh_sconfig))
        sh_spp = 0 #scans per pass
        fh.write(struct.pack('<H', rh_accomp))
        rh_linenum = 1 #line number
        fh.write(struct.pack('<H', rh_linenum))
        rhc_coordY = 0
        fh.write(struct.pack('<Q', rhc_coordY))
        rh_lineorder = 0 # slice type
        fh.write(struct.pack('<B', rh_lineorder))
        rh_dtype = 0 #
        fh.write(struct.pack('<B', rh_dtype))
        rh_antname = "Testfile      "  # 14 char
        fh.write(rh_antname.encode())
        rh_pass = 1 #active TX mask
        fh.write(struct.pack('<B', rh_pass))
        rh_version = 0b0100000 # first 3 bits = 1 for NO GPS, 2 for GPS
        fh.write(struct.pack('<B', rh_version))
        rh_name = "default1.dzt" # orginial file name 12 chars
        fh.write(rh_name.encode())
        rh_chksum = 0
        #fh.write(len(self.gpr[0]))
        #fillup = bytearray(896) # empty data to fill header to 1024 byte
        fillup = bytearray(898) # empty data to fill header to 1024 byte
        fh.write(fillup)
        
        #content
        l = self.gpr.shape
        for c in range(1,l[0]):
            col= self.gpr[c]
            for m in col:
                val= m*10**7
                val= int(val)
                #fh.write(struct.pack('>H', val))
                fh.write(val.to_bytes(2, byteorder="little"))
        fh.close()


parser = argparse.ArgumentParser(
description=__doc__,
formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-i", "--input", type=str,
                help="input location of touchstone files (.s2p, folder)")
parser.add_argument("-o", "--output", type=str,
                help="ouput file name for DZT, .DZT will be added")

args = parser.parse_args()
input = args.input
output = args.output + ".DZT"

#get last char of input and check if "/"
if input[-1] != '/' :
    input = input + "/"


print('start')
a = TDR()
a.listFolder(input, output)
#a.readP2S('/home/spel/Downloads/nanovna-saver/0.25m_200-1000MHz_Heizung_Brockmanngasse_20200805/11.s2p')
#a.calcTDR();
