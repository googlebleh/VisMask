#!/usr/bin/env python
# Written by Yu-Jie Lin
# Public Domain
#
# Deps: PyAudio, NumPy, and Matplotlib
# Blog: http://blog.yjl.im/2012/11/frequency-spectrum-of-sound-using.html
 
import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import struct
import math
import wave
from bibliopixel.led import *
from bibliopixel.drivers.LPD8806 import *
import time
import shlex
import subprocess
import sys
TITLE = 'animalibera.wav'
#FPS = 25.0
 
nFFT = 512
BUF_SIZE = 4 * nFFT
RATE = 44100
nBINS = 8
hBINS = 8
SPECTRUM_MAX_DB=60.0
SPECTRUM_MIN_DB=30.0
PASS_RATIO = 7
DEBUG=0

def calculate_levels(file):
  levels=[]
  eof=0;
  for i in xrange(0, nBINS):
    raw=file.read(1)
    if raw!='':
      levels.append(int(ord(raw))-48)
    else:
      eof=1
  return levels

def setPixels(led,levels):
  #IMPLEMENT ---------------------------------------------------
  led.fillScreen((0,0,0));
  if nBINS>len(levels):
    return 0
  for i in range(0,nBINS):
    led.drawLine(i,8-levels[i],i,8,(0,000,200))
  led.update()
  return 0
 
def main():
  
  #create driver for a 12x12 grid, use the size of your display
  driver = DriverLPD8806(8*12)
  led = LEDMatrix(driver,width=8,height=12, rotation = MatrixRotation.ROTATE_180, vert_flip = True,)
  led.fillScreen((0,0,0))
  led.update()
  #fig = plt.figure()
  song_filename=sys.argv[1]
  '''30songs.wav'''
  FRAMES=5178.0
  RUN_TIME=60.0
  file = open(song_filename[0:(len(song_filename)-3)]+'ebr','rb')
  #stream.start_stream()
  #while(ostream.is_active()):
  #  time.sleep(0.1)
  CHUNK=nFFT
  # read data
  start_time=time.time()
  try:
  # play stream (3)
    f=0.0
    eof=0
    while not eof:
      while time.time()-start_time < f*RUN_TIME/FRAMES:
        continue
      gametime=f*RUN_TIME/FRAMES
      levels=[]
      eof=0;
      for i in xrange(0, nBINS):
        if not eof:
          raw=file.read(1)
        if raw!='':
          levels.append(int(ord(raw))-48)
        else:
          print "Got EOF"
          eof=1
      setPixels(led,levels)
      time.sleep(0.01)
      if time.time()-start_time > gametime + 0.3:
        print "skipping@" +str(f)+" time"+str(time.time()-start_time)+" ingame"+str(gametime)
        file.seek(nBINS,1)
        f+=1
      f+=1
  except KeyboardInterrupt:
    print('ctrl C key interupted')
  finally:
    print "\nStopping"
    led.fillScreen((0,0,0))
    led.update()
 
if __name__ == '__main__':
  main()