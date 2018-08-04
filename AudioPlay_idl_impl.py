#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 Copyright(C) 2018 Isao Hara,AIST,JP
 All rights reserved

"""
from __future__ import print_function
import omniORB
from omniORB import CORBA, PortableServer
import AudioPlay, AudioPlay__POA

import RTC
from audioplay import *

#
#  AudioPlay.idl
#
class AudioPlay_Player_i (AudioPlay__POA.Player):
    def __init__(self):
        self._rtc=None
        self._player=audio_player()
    #
    def play_file(self, fname):
        try:
          res=self._player.read_audio_file(fname)
          if res :
            if self._rtc:
              sp=self._rtc._start_time[0]
              ep=self._rtc._end_time[0]
              reverse=(self._rtc._reverse[0] == 1)
              rate=self._rtc._speed_rate[0]
              loop=(self._rtc._loop[0] == 1)
              res=self._player.play(sp, ep, reverse,rate, loop)
            else:
              res=self._player.play()

            if res: return 1
            else: return 0
          else:
            return -1

        except AttributeError:
          raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
    #
    def pause(self):
        try:
          res=self._player.pause()
          return 1

        except AttributeError:
          raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
    #
    def stop(self):
        try:
          res=self._player.stop()
          return 1

        except AttributeError:
          raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
    #
    def get_files(self):
        try:
          res=RTC.TimedStringSeq(RTC.Time(0,0),[])
          res.data=self._player.get_files()
          return 1,res

        except AttributeError:
          raise CORBA.NO_IMPLEMENT(0, CORBA.COMPLETED_NO)
