#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @license the MIT License

 Copyright(C) 2018 Isao Hara,AIST,JP
 All rights reserved.

"""
from DataFlowRTC_Base import *

##
# @class AudioPlayRTC
# 
# 
class AudioPlayRTC(DataFlowRTC_Base):
  ##
  # @brief constructor
  # @param manager Maneger Object
  # 
  def __init__(self, manager):
    DataFlowRTC_Base.__init__(self, manager)

  ##
  #
  # The initialize action (on CREATED->ALIVE transition)
  # formaer rtc_init_entry() 
  # 
  # @return RTC::ReturnCode_t
  # 
  #
  def onInitialize(self):
    DataFlowRTC_Base.onInitialize(self)

    
    return RTC.RTC_OK
  ##
  #
  # The activated action (Active state)
  #
  # @param ec_id target ExecutionContext Id
  #
  # @return RTC::ReturnCode_t
  #
  #  
  def onActivated(self, ec_id):
    self._player_service._rtc=self
    self._player_service._player.activate()
  
    return RTC.RTC_OK
  
  ##
  #
  # The deactivated action (Active state exit action)
  # former rtc_active_exit()
  #
  # @param ec_id target ExecutionContext Id
  #
  # @return RTC::ReturnCode_t
  #
  #
  def onDeactivated(self, ec_id):
    self._player_service._player.deactivate()
  
    return RTC.RTC_OK

  ##
  #
  # The execution action that is invoked periodically
  # former rtc_active_do()
  #
  # @param ec_id target ExecutionContext Id
  #
  # @return RTC::ReturnCode_t
  #
  #
  def onExecute(self, ec_id):

    return RTC.RTC_OK
  
  #
  # Callback method from RtcDataListenr
  # 
  def onData(self, name, data):
    print(name,data)

    return RTC.RTC_OK


#########################################
#  Initializers
#

def main():
  mgr = rtc_init("AudioPlayRTC", AudioPlayRTC, 'rtc.yaml')
  mgr.runManager()

if __name__ == "__main__":
  main()

