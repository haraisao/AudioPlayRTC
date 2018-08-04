#
#
# Audio Player 
# Copyright(C) 2018 Isao Hara,AIST,JP
# All rights reserved
#
import os
import sys
import glob
import re
import wave
import pyaudio
import time
import threading
from pydub import AudioSegment
from pydub.playback import play

class audio_player(object):
  def __init__(self, dirname='sounds', activate=True):
    self.snd_ext=["mp3", "wav", "ogg", "flv", "wma", "mp4"]
    self.dirname=dirname
    self.files={}
    self.target=None
    self.chunk=4096
    self.pyaudio=None
    self.wf=None
    self.stream=None
    self.pause_flag=False
    self.terminate=False
    self.thread=False
    self._audio_data=None
    self._audio_len_p_s=0
    self._audio_nchannels=2
    self._audio_samplewidth=2
    self._audio_fromat=None
    self._audio_framerate=16000

    self.load_sndfiles()

    if activate :
      self.activate()

  #
  #
  def set_audio_dir(self, dirname):
    self.dirname=dirname
    self.load_sndfiles()

  #
  #
  def load_sndfiles(self):
    for x in self.snd_ext:
      self.files[x]=glob.glob(self.dirname+os.path.sep+"*."+x)
  #
  #
  def get_file(self, ext):
    self.load_sndfiles()
    res=[]
    pat=self.dirname+os.path.sep+"([A-Z,a-z,0-9,_]+)\."+ext
    for x in self.files[ext]:
      mm=re.match(pat,x)
      if mm :
        fname=mm.group(1)
        res.append(fname+"."+ext)
    return res

  #
  #
  def get_files(self):
    self.load_sndfiles()
    res=[]
    for x in self.snd_ext:
      res.extend(self.get_file(x))
    return res

  #
  #
  def get_audiosegment(self, name):
    ext=name.split('.')[1]
    fname=self.dirname+os.path.sep+name
    snd=AudioSegment.from_file(fname, ext)
    return  snd

  #
  #
  def convert_to_wav(self, name):
    snd=self.get_audiosegment(name)
    newname=self.dirname+os.path.sep+'_'.join(name.split('.'))+'.wav'
    snd.export( newname, format='wav')

  #
  #
  def get_wav_name(self, name):
    ext=name.split('.')[1]
    if ext == 'wav': return name
    else: return '_'.join(name.split('.'))+'.wav'
    
  #
  #
  def open_wav(self, name):
    fname=self.get_wav_name(name)
    if not os.path.exists(self.dirname+os.path.sep+fname) :
      self.convert_to_wav(name)

    wf=wave.open(self.dirname+os.path.sep+fname, 'rb')
    return wf

  #
  #
  def activate(self):
    if not self.pyaudio :
      self.pyaudio=pyaudio.PyAudio()
    return True

  #
  #
  def wait_for_thread(self):
    if self.thread :
      self.thread.join()
    return True

  #
  #
  def read_audio_file(self, fname):
    if self.pyaudio is None:
      print "Not activated"
      return False

    if self.is_playing():
      print "Other audio playing"
      return False

    if fname in self.get_files():
      self.wf=self.open_wav(fname)
      self._audio_nchannels=self.wf.getnchannels()
      self._audio_samplewidth=self.wf.getsampwidth()
      self._audio_format=fmt=self.pyaudio.get_format_from_width(self._audio_samplewidth)
      self._audio_framerate=self.wf.getframerate(),
      self._audio_len_p_s=self._audio_nchannels*self._audio_samplewidth*self._audio_framerate[0]
      self._audio_data=self.wf.readframes(self.wf.getnframes())

      return True
    else:
      print("No such file", fname)
      return False

  #
  #
  def open_stream(self,rate=1):
      try:
        self.stream.close()
      except:
        pass

      self.stream=self.pyaudio.open(format=self._audio_format,
                      channels=self._audio_nchannels,
                      rate=(int(self._audio_framerate[0]*rate)),
                      output=True)
      return

  #
  #
  def is_playing(self):
    if self.thread and self.thread.is_alive():
      return True
    else:
      return False

  #
  #
  def play(self, start=0, end=-1, reverse=False, rate=1, loop=False,wait=False):
    if self.is_playing():
      if wait: 
        self.thread.join()
      else:
        print "Other audio playing"
        return False

    args=(start,end,reverse,rate,loop)

    self.thread=threading.Thread(target=self.play_audio, args=args)
    self.thread.start()
    return True

  #
  #
  def pause(self):
    self.pause_flag= not self.pause_flag

  #
  #
  def stop(self):
    self.terminate=True

  #
  #
  def play_audio(self, start=0, end=-1, reverse=False, rate=1,loop=False):
    #
    # clip audio data
    data=self.clip_data(self._audio_data, start, end)

    #
    #  reverse audio data
    if reverse: data=self.reverse_data(data)

    #
    # open audio stream 
    self.open_stream(rate)

    #
    # play audio
    if loop:
      while not self.terminate : 
        self.play_audio_data(data)
    else:
      self.play_audio_data(data)

    #
    #  
    self.terminate=False
    self.pause_flag=False
    return True

  #
  #
  def clip_data(self, data, start, end):
    start_point=int(start*self._audio_len_p_s)

    if end < 0:
      res=data[start_point:]
    else:
      end_point=int(end*self._audio_len_p_s)
      res=data[start_point:end_point]

    return res

  #
  #
  def reverse_data(self, data):
    data_r=b""
    n=self._audio_nchannels*self._audio_samplewidth

    for i in range(len(data),0,-n):
      data_r += data[i-n:i]
    return data_r
 
  #
  #
  def play_audio_data(self, data):
    len_idx=len(data)/self.chunk
    i = 0
    while i < len_idx:
      if self.terminate : break
      if not self.pause_flag :
        ss=i*self.chunk
        sdata=data[ss:ss+self.chunk]
        self.stream.write(sdata)
        i += 1
      else: time.sleep(0.01)



  def deactivate(self):
    self.stream.close()
    self.pyaudio.terminate() 
    self.pyaudio=None
    return True

  def remove_wav_file(self,fname):
    wav_fname=self.get_wav_name(fname)
    if wav_fname != fname:
      print("remove ", fname)
      os.remove(self.dirname+os.path.sep+wav_fname)

    return True

