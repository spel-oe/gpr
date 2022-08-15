#import pyvisa as visa
import numpy as np
import time
import datetime
from datetime import datetime
from os import path, makedirs


import socket
import sys
import struct

#worker for librevna
#saving touchstone


"""
functions: 
  def init(self):
  def make_filename(self):
  def gpib_alloc(self):
  def save_s2p(self):
  def save_s2p_lin(self):
  def save_s2p_log(self):
  def save_s2p(self,touchFileName):
  def save_s2p(self,touchFileName,linlog):

import LibreVNA_class
a=LibreVNA_class.LibreVNA_class()
a.init()


#:VNA:TRACE:TOUCHSTONE? S11 S12 S21 S22
#:VNA:CALibration:LOAD ./SOLT_1.00M-6.00G_501pt_eachport_60cm.cal
#:VNA:CALibration:LOAD /home/spel/Downloads/LibreVNA/Software/PC_Application/SOLT_1.00M-6.00G_501pt_eachport_60cm

#:VNA:CALibration:TYP SOLT
#:VNA:TRACe:MINFrequency? => error
#:VNA:TRACe:MAXFrequency? 

#:VNA:FREQuency:START? => ok
#:VNA:FREQuency:STOP? => OK
#:VNA:TRAC:LIST? => ok

#:VNA:ACQuisition:POINTS? => OK

#:VNA:TRAC:PAUSE S11
#:VNA:TRAC:PAUSE S12
#:VNA:TRAC:PAUSE S22
#:VNA:TRAC:PAUSE S21


##
# class settings
#	ip 
#   port


#absolute maximum of libreVNA
#
# 20dBm 	3.162 Vp (ADL5801, mixer)
# 31dBm 	11.218 Vp (QPC6324, switch)
#
# 

##starting libreVNA
# ./LibreVNA-GUI -p 9091 --no-gui
# ./LibreVNA-GUI -p 9091 
#     easier with gui


"""
	
class LibreVNA_class():
	def __init__(self):
		self.ip= "127.0.0.1"
		self.port= 9091
		self.tcp_buffer= []
		self.sock= []
	def init(self):

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		# Connect the socket to the port where the server is listening
		server_address = (self.ip, self.port)
		print('connecting to {} port {}'.format(*server_address))
		self.sock.connect(server_address)
		print('connected')
		self.sock.setblocking(0)
		time.sleep(0.3)
	def make_filename(self):
		dateString = datetime.now().strftime("%Y%m%d")
		timeString = datetime.now().strftime("%H%M%S")
		fileName = dateString+'-'+timeString

		dataDir = 'LibreVNA'
		if not path.exists(dataDir):
		  makedirs(dataDir)
		touchFileName = dataDir + "/" + fileName + ".s2p"
		return touchFileName

	def set_start(self,qrg): # Hz
		self.sock.setblocking(1)
		self.sock.sendall((":VNA:FREQ:START "+str(qrg)+"\n").encode())
		self.sock.setblocking(0)

	def set_stop(self,qrg): #Hz
		self.sock.setblocking(1)
		self.sock.sendall((":VNA:FREQ:STOP "+str(qrg)+"\n").encode())
		self.sock.setblocking(0)

	def set_full(self): # useless, sets wring lower boundary
		self.sock.setblocking(1)
		self.sock.sendall((":VNA:FREQ:FULL\n").encode())
		self.sock.setblocking(0)

	def set_points(self,points):
		self.sock.setblocking(1)
		self.sock.sendall((":VNA:ACQ:POINTS "+str(points)+"\n").encode())
		self.sock.setblocking(0)

	def set_avg(self,avg): #max 10
		self.sock.setblocking(1)
		self.sock.sendall((":VNA:ACQ:AVG "+str(avg)+"\n").encode())
		self.sock.setblocking(0)

	def set_ifbw(self,ifbw): #6-50000   0 for default (1000)
		if ifbw == 0:
			ifbw=1000
		self.sock.setblocking(1)
		self.sock.sendall((":VNA:ACQ:IFBW "+str(ifbw)+"\n").encode())
		self.sock.setblocking(0)

	def set_lvl(self,lvl): #-40 - 0
		self.sock.setblocking(1)
		self.sock.sendall((":VNA:STIM:LVL "+str(lvl)+"\n").encode())
		self.sock.setblocking(0)

	def get_S2P_cont(self):
		# Create a TCP/IP socket

		# Connect the socket to the port where the server is listening	

		self.sock.setblocking(1)

		self.sock.sendall(":VNA:TRACE:TOUCHSTONE? S11 S12 S21 S22\n".encode())
		print('sent')
		try:
			# Send data
			# message = b'This is the message.  It will be repeated.'
			# print('sending {!r}'.format(message))
			#sock.sendall(message)


			buffer = self.sock.recv(1)
			#print (type(buffer))
			buffering= True
			b=buffer.decode("utf-8") 
			while True:
				if b.find("\n") != -1:
					
					lines = b.split("\n")
					b= lines[-1]
					del lines[-1]
					#print(lines)
					#attatch lines to global rPi_buffer
					self.tcp_buffer.extend(lines)
					buffer=self.tcp_buffer
					#print(lines)
					if (len(lines[0]) == 0):
						#buffer = self.sock.recv(1)

						break

				##Auswertung der lines, wenn zu viele neustart des Klienten,ev nur neueste betrachten?
					
				else:
					#print ('---nothing new---')
					more = self.sock.recv(1)
					if not more:
						buffering = False
					else:
						b += more.decode("utf-8")

		finally:
			print('reading vna finished')
			self.sock.setblocking(0)

	def get_S2P(self):
		# Create a TCP/IP socket

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# Connect the socket to the port where the server is listening	
		server_address = (self.ip, self.port)
		print('connecting to {} port {}'.format(*server_address))
		self.sock.connect(server_address)
		self.sock.setblocking(0)
		
		print('connected')
		self.sock.sendall("*IDN?\n".encode())
		time.sleep(0.3)

		self.sock.setblocking(1)


		self.sock.sendall(":VNA:TRACE:TOUCHSTONE? S11 S12 S21 S22\n".encode())
		print('sent')
		try:

			# Send data
			# message = b'This is the message.  It will be repeated.'
			# print('sending {!r}'.format(message))
			#sock.sendall(message)


			buffer = self.sock.recv(1)
			#print (type(buffer))
			buffering= True
			b=buffer.decode("utf-8") 
			while True:
				if b.find("\n") != -1:
					
					lines = b.split("\n")
					b= lines[-1]
					del lines[-1]
					#print(lines)
					#attatch lines to global rPi_buffer
					self.tcp_buffer.extend(lines)
					buffer=self.tcp_buffer
					print(lines)
					if (len(lines[0]) == 0):
						#buffer = self.sock.recv(1)
						break

				##Auswertung der lines, wenn zu viele neustart des Klienten,ev nur neueste betrachten?
					
				else:
					#print ('---nothing new---')
					more = self.sock.recv(1)
					if not more:
						buffering = False
					else:
						b += more.decode("utf-8")

		finally:
			print('closing socket')
			self.sock.sendall("*IDN?\n".encode())

			self.sock.setblocking(0)
			self.sock.close()

	def clean_buffer(self):
		
		self.tcp_buffer.clear()



	def run_buffer(self,file):
		#TODO save dmesg of fewer than X (50?) lines
		
		if (len(self.tcp_buffer) < 100 ):
		#if 1:
			for n in self.tcp_buffer:

				print(str(n))
				self.save_param_file(file,'#dmesg:'+str(n))	

				self.tcp_buffer.remove(n)
		else:
			self.clean_buffer()
			print("clean buffer")


	def save_param_file(self,file,content):
		f=open(file, "a")
		f.write(str(content)+ "\n")
		f.close
	def save_s2p(self):
		ret= self.save_s2p_lin()

		return ret
	def save_s2p_lin(self):
		filename= self.make_filename()
		print(filename)
		ret= self.save_s2p_long(filename,'lin')
		return ret
	def save_s2p_log(self):
		filename= self.make_filename()
		ret= self.save_s2p_long(filename,'log')
		return ret
		#def save_s2p(self,touchFileName):
		#  ret= self.save_s2p(touchFileName,'lin')
		#  return ret
	def save_s2p_long(self,touchFileName,linlog):
		#self.getS2P()  #each read out new tcp connection
		self.get_S2P_cont()
		s2p= "\n".join(self.tcp_buffer)
		if len(s2p) > 500:
			self.save_param_file(touchFileName,s2p)
		self.clean_buffer()
		return touchFileName
