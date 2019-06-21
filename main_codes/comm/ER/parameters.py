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
        self.port=None 
        self.id=None 
        self.type=None 
        self.value=None 
        self.min_volt=0 
        self.max_volt=0
        self.min_curr=0 
        self.max_curr=0 
        self.current_reqd=0
        self.state=0
        self.actual_curr=0
    