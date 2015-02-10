#!/usr/bin/env python
 
import numpy as np
import struct
import math
import wave
import sys
import os
#FPS = 25.0
 
nFFT = 512
BUF_SIZE = 4 * nFFT
RATE = 44100
nBINS = 8
hBINS = 8
SPECTRUM_MAX_DB=60.0
SPECTRUM_MIN_DB=30.0
PASS_RATIO = 20

def calculate_levels(data, chunk, samplerate):
  # Use FFT to calculate volume for each frequency
 
  # Convert raw sound data to Numpy array
  fmt = "%dH"%(len(data)/2)
  data2 = struct.unpack(fmt, data)
  data2 = np.array(data2, dtype='h')

  # Apply FFT
  fourier = np.fft.fft(data2)
  ffty = np.abs(fourier[0:len(fourier)/2])/1000
  ffty1=ffty[:len(ffty)/2]
  ffty2=ffty[len(ffty)/2::]+2
  ffty2=ffty2[::-1]
  ffty=ffty1+ffty2
  ffty=np.log(ffty)-2
 
  fourier = list(ffty)[4:-4]
  fourier = fourier[:len(fourier)/2]
 
  size = len(fourier)

  # Add up for nBINS lights
  levels = [sum(fourier[i:(i+size/nBINS)]) \
     for i in xrange(0, size, size/nBINS)][:nBINS]
 
  return levels

def setPixels(levels,OUT):
  dbscalar=(SPECTRUM_MAX_DB-SPECTRUM_MIN_DB)
  for i in range(0,nBINS):
    tmp = levels[i]-SPECTRUM_MIN_DB
    if 2-i >0:
      tmp -= (2-i) * 3
    levels[i]=hBINS*(levels[i]-SPECTRUM_MIN_DB)/SPECTRUM_MIN_DB
    if levels[i]>hBINS:
      levels[i]=hBINS
    elif levels[i]<0:
      levels[i]=0
    levels[i]=bytes(int(math.floor(levels[i])))
    OUT.write(levels[i])
  return 0
 
def YNInput():
    while True:
        cmd = raw_input("Y/N --> ").upper()
        if cmd == "Y": return True
        elif cmd == "N": return False
        print "Invalid input. Try again."
 
def processed(fname):
    if ((os.path.splitext(fname)[0] + ".ebr") in os.listdir(os.getcwd())):
        print "Overwrite existing output?",
        return not(YNInput())
    return False

def main():
  song_filename = sys.argv[1]
  if processed(song_filename): return
  elif song_filename.endswith('.wav'):
    musicfile = wave.open(song_filename, 'r')
  else:
    print "WAVE file only pls"
    return
  file = open(song_filename[0:(len(song_filename)-3)]+'ebr','wb')
  # Frequency range
  # Used for normalizing signal. If use paFloat32, then it's already -1..1.
  RATE=musicfile.getframerate()
  wSIZE = math.floor(RATE/(2 * nBINS)) 
  CHUNK = nFFT
  # read data
  data = musicfile.readframes(CHUNK)
  try:
  # play stream (3)
    h=0
    while data != '':
      levels=calculate_levels(data, CHUNK, RATE)
      setPixels(levels,file)
      if h%500==0:
        text="update("+str(h)+"):"
        for i in range(0,nBINS):
          text+=str(levels[i])+","
        print(text)
      data = musicfile.readframes(CHUNK)
      h+=1
    print "total frames "+str(h)
  except KeyboardInterrupt:
    print('ctrl C key interupted')
  finally:
    print "\nStopping"
 
if __name__ == '__main__':
  main()