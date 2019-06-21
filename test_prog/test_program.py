#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 19:35:28 2019

@author: div
"""
import time
from global_var import source_param, load_param

def main_th(list_change_event,Source_list,Load_list):
    i=1
    while True:
        time.sleep(3)
#        print "Test_program -> event set"
        list_change_event.set()
        if i%2==0:
            load=load_param()
            load.id = i
            load.port =i
#            if(load.port==2):
            load.current_reqd=0.2*i
            print "current required update"
            Load_list.append(load)
            
        else:
            source=source_param()
            source.id=i
            source.port =i 
#            if(source.port==3):
            source.current_aval=0.3*i
            print "current required update"
            Source_list.append(source)
        
        print "*************************************************"
        print Load_list
        print "*************************************************"
#        print "\n"
#        print (vars(Load_list[i]))
#        print "\n"
#        print "Load_list appended in TEST"
        print "i:      " + str(i)
#        if(i==3 or i==6):
#            print "Inside"
#            Load_list.pop(1)
#            Load_list.pop(0)
#            print Load_list
#            list_change_event.set()

        i=i+1
#        if(load.port==7):
#            Load_list[2].current_reqd=23
#            print "current required update"
        
        
#        time.sleep(2)
#        list_change_event.set()
#        Load_list.pop(0)