# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 11:46:11 2019

@author: divyanshu
"""

class source_param:
    def __init__(self):
        self.ip_address=None
        self.port=None 
        self.id=None 
        self.type=None 
        self.value=None 
        self.voltage=0
        self.min_volt=0 
        self.max_volt=0
        self.min_curr=0 
        self.max_curr=0 
        self.current_aval=0
        self.state=0
        self.actual_curr=0
        

class load_param:
    def __init__(self):
        self.ip_address=None
        self.port=0 
        self.id=0 
        self.type=0 
        self.value=0
        self.voltage=0
        self.min_volt=0 
        self.max_volt=0
        self.min_curr=0 
        self.max_curr=0 
        self.current_reqd=0
        self.state=0
        self.actual_curr=0
        
class par_var:
    def __init__(self):
        
        self.DIRECTION='d'
        self.VOLTAGE='v'
        self.CURRENT='c'
        self.SLAVEID='sid'
        self.DIRECTION='dir'
        
        #IN BYTES
        self.DIRECTION_TYPE_SIZE=1
        self.VOLTAGE_TYPE_SIZE = 4
        self.CURRENT_TYPE_SIZE = 4
        self.SLAVEID_TYPE_SIZE = 1
        
        self.START_UPDATE_STATE = 0
        self.PARAM_UPDATE_STATE = 1
        self.STOP_UPDATE_STATE = 2
        
        self.START_COMMAND = 0x11
        self.PARAM_COMMAND = 0x12
        self.STOP_COMMAND = 0x30
        
        self.SOURCE_DIRECTION =2
        self.LOAD_DIRECTION = 1
        
        
        self.READ_COMMAND = 0x80
        
        self.Load_list=[]
        self.Source_list=[]
        
        self.conv_max_current=1.5
        
        self.PARAM_COMMAND = 0x12
        self.STOP_COMMAND = 0x30
        
        self.slaveid=[0x32,0x33,0x34]
        self.ports = 3

class fb_var:
    def __init__(self):
        self.voltage_port1=0
        self.voltage_port2=0
        self.current_port1=0
        self.current_port2=0
