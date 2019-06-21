# !/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 18:28:49 2019

@author: pi
"""

from smbus import SMBus
from time import sleep


bus = SMBus(1)

while True:
    try:    
         print(bus.read_i2c_block_data(0x32,0x23,16))
    except:
            print("eeror")
    sleep(2)
