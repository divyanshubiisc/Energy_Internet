#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 19:41:04 2019

@author: div
"""

import serial
import smbus
import time
from threading import Timer, Event, Thread
#from main_codes.message_slave import par_var
from global_var import par_var, fb_var, source_param, load_param
from main_codes.power import message_send
from global_var import parameters
from copy import deepcopy
import math
local_load_list=[]
local_source_list=[]

send_rs485_block_event = Event()
receive_rs485_block_event = Event()
state_switch_event = Event()
batt_voltage =0
def port_off(bus):
    
    par_obj=par_var()
    msg_c_obj = message_send()
    print "Inside port_off function"
    for rows in range(len(local_load_list)):
        
        if(local_load_list[rows].state == par_obj.STOP_UPDATE_STATE):
            print "_____________________________"
            if(local_load_list[rows].port=="1"):
                print "_________________Sending stop port 1"
                send_rs485_block_event.wait()
                if send_rs485_block_event.is_set():
                    #~ print ("|||||||||||||||||||||||||   block event set from port_off |||||||||||||||||||||||")
                    msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
                
            elif(local_load_list[rows].port=="2"):
                print "___________________Sending stop port 2"
                send_rs485_block_event.wait()
                if send_rs485_block_event.is_set():
                    #~ print ("|||||||||||||||||||||||||   block event set from port_off |||||||||||||||||||||||")
                    msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
            elif(local_load_list[rows].port=="3"):
                print "___________________Sending stop port 3"
                send_rs485_block_event.wait()
                if send_rs485_block_event.is_set():
                    #~ print ("|||||||||||||||||||||||||   block event set from port_off |||||||||||||||||||||||")
                    msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)

                
    for rows in range(len(local_source_list)):
        if(local_source_list[rows].state == par_obj.STOP_UPDATE_STATE):
            if(local_source_list[rows].port=="1"):
                print "__________________Sending stop port 1"
                send_rs485_block_event.wait()
                if send_rs485_block_event.is_set():
                    #~ print ("|||||||||||||||||||||||||   block event set from port_off |||||||||||||||||||||||")
                    msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
            elif(local_source_list[rows].port=="2"):
                print "__________________Sending stop port 2"
                send_rs485_block_event.wait()
                if send_rs485_block_event.is_set():
                    #~ print ("|||||||||||||||||||||||||   block event set from port_off |||||||||||||||||||||||")
                    msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
            elif(local_source_list[rows].port=="3"):
                print "__________________Sending stop port 3"
                send_rs485_block_event.wait()
                if send_rs485_block_event.is_set():
                    #~ print ("|||||||||||||||||||||||||   block event set from port_off |||||||||||||||||||||||")
                    msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)

def state_switch(bus,change_type,Source_list,Load_list,Feedback_list):
    
    par_obj = par_var()
    msg_c_obj = message_send()
    print "In the loop for changing the state of the switches"
    
    total_amp_av=0
    total_load_rq=0
    voltage=14
    
    #~ print par_obj.CURRENT
    
    for rows in range(len(Source_list)):
        total_amp_av += local_source_list[rows].current_aval
    
    for rows in range(len(Load_list)):
        if(local_load_list[rows].current_reqd <= par_obj.conv_max_current):                
            total_load_rq += local_load_list[rows].current_reqd
            local_load_list[rows].actual_curr = local_load_list[rows].current_reqd
            #~ print("***********_________ local_load_list[rows].actual_curr_________ ***********",local_load_list[rows].actual_curr)
        else:
            total_load_rq += par_obj.conv_max_current
            local_load_list[rows].actual_curr = par_obj.conv_max_current
            #~ print("***********_________ local_load_list[rows].actual_curr_________ ***********",local_load_list[rows].actual_curr)
##    print "loop"
##    star ='*' * 50
##    print (star)
##    print ("TOTAL AMP AVAILABLE")
##    print total_amp_av
##    print (star)
##    print ("TOTAL AMP REQUIRED")
##    print total_load_rq
##    print (star)
#    print i
    
    if not local_load_list:
        send_rs485_block_event.wait()
        if send_rs485_block_event.is_set():
            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> not local load |||||||||||||||||||||||")
            msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
        send_rs485_block_event.wait()
        if send_rs485_block_event.is_set():
            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> not local load |||||||||||||||||||||||")
            msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
        send_rs485_block_event.wait()
        if send_rs485_block_event.is_set():
            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> not local load |||||||||||||||||||||||")
            msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)

    elif local_load_list:
        #~ print "Entered state switch containing local loads"
        if(total_amp_av>=total_load_rq):
            if total_amp_av!=0:
                mul_factor=total_load_rq/total_amp_av
                print ("_____________MUL_factor_________",mul_factor)
            else:
                mul_factor=0
    #        print "if complete"
            for rows in range(len(local_load_list)):
                print ("local_load_list____________",vars(local_load_list[rows]))
                if(local_load_list[rows].state == par_obj.PARAM_UPDATE_STATE):
        
                    if(local_load_list[rows].port == "1"):
                        current = local_load_list[rows].actual_curr
                        voltage = local_load_list[rows].voltage
                        data=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.LOAD_DIRECTION]
                        data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]    
                        message=msg_c_obj.msg_pack(data,data_type_order)
                        
                        print "slave id"  + str(par_obj.slaveid[0])
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local load list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.PARAM_COMMAND,message,send_rs485_block_event)    
                    elif(local_load_list[rows].port == "2"):
                        current = local_load_list[rows].actual_curr
                        voltage = local_load_list[rows].voltage
                        data=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.LOAD_DIRECTION]
                        data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]    
                        message=msg_c_obj.msg_pack(data,data_type_order)
                        
                        print "slave id"  + str(par_obj.slaveid[1])
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local load list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.PARAM_COMMAND,message,send_rs485_block_event) 
                        
                    elif(local_load_list[rows].port == "3"):
                        current = local_load_list[rows].actual_curr
                        voltage = local_load_list[rows].voltage
                        data=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.LOAD_DIRECTION]
                        data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]    
                        message=msg_c_obj.msg_pack(data,data_type_order)
                        
                        print "slave id"  + str(par_obj.slaveid[2])
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local load list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.PARAM_COMMAND,message,send_rs485_block_event)    

                elif(local_load_list[rows].state == par_obj.STOP_UPDATE_STATE):
                    if(local_load_list[rows].port=="1"):
                        print "Sending start port 1"
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local load list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
                        local_load_list.pop(rows)
                        
                    elif(local_load_list[rows].port=="2"):
                        print "Sending start port 2"
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local load list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
                        local_load_list.pop(rows)
                    elif(local_load_list[rows].port=="3"):
                        print "Sending start port 3"
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local load list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
                        local_load_list.pop(rows)        
            for rows in range(len(local_source_list)):
                #~ print ("local_source_list all values", local_source_list)
                #~ print ("local_source_list____________",vars(local_source_list[rows]))
                if(local_source_list[rows].state == par_obj.PARAM_UPDATE_STATE):
    #                print ("1st enter if loop")
    #                print type(local_source_list[rows].port)
                    if(local_source_list[rows].port == "1"):
    #                    print"2nd enter if loop"
    #                    print mul_factor
                        local_source_list[rows].actual_curr = local_source_list[rows].current_aval * mul_factor
                        voltage= local_source_list[rows].voltage
                        current = local_source_list[rows].actual_curr
                        
                        #~ print("***********_________ source_list[rows].actual_curr_________ ***********",current)
                        data=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.SOURCE_DIRECTION]
    #                    data=[14,2.4,par_obj.SOURCE_DIRECTION]
                        data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]    
                        message=msg_c_obj.msg_pack(data,data_type_order)
                        
                        #print "slave id"  + str(par_obj.slaveid[0])
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local source list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.PARAM_COMMAND,message,send_rs485_block_event)    
                    elif(local_source_list[rows].port == "2"):
                        print mul_factor
                        local_source_list[rows].actual_curr = local_source_list[rows].current_aval * mul_factor
                        voltage= local_source_list[rows].voltage
                        current = local_source_list[rows].actual_curr
                        
                        data=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.SOURCE_DIRECTION]
                        data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]    
                        message=msg_c_obj.msg_pack(data,data_type_order)
                        
                        print "slave id"  + str(par_obj.slaveid[1])
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local source list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.PARAM_COMMAND,message,send_rs485_block_event)

                    elif(local_source_list[rows].port == "3"):
                        print mul_factor
                        local_source_list[rows].actual_curr = local_source_list[rows].current_aval * mul_factor
                        voltage= local_source_list[rows].voltage
                        current = local_source_list[rows].actual_curr
                        
                        data=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.SOURCE_DIRECTION]
                        data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]    
                        message=msg_c_obj.msg_pack(data,data_type_order)
                        
                        print "slave id"  + str(par_obj.slaveid[2])
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local source list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.PARAM_COMMAND,message,send_rs485_block_event) 
                        

                elif(local_source_list[rows].state == par_obj.STOP_UPDATE_STATE):
                    if(local_source_list[rows].port=="1"):
                        print "Sending start port 1"
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local source list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
                        local_source_list.pop(rows)
                        
                    elif(local_source_list[rows].port=="2"):
                        print "Sending start port 1"
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local source list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
                        local_source_list.pop(rows)
                    
                    elif(local_source_list[rows].port=="3"):
                        print "Sending start port 1"
                        send_rs485_block_event.wait()
                        if send_rs485_block_event.is_set():
                            #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> local source list |||||||||||||||||||||||")
                            msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
                        local_source_list.pop(rows)
        else:
            send_rs485_block_event.wait()
            if send_rs485_block_event.is_set():
                #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> not local load |||||||||||||||||||||||")
                msg_c_obj.send_i2c(bus,par_obj.slaveid[0],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
            send_rs485_block_event.wait()
            if send_rs485_block_event.is_set():
                #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> not local load |||||||||||||||||||||||")
                msg_c_obj.send_i2c(bus,par_obj.slaveid[1],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)
            send_rs485_block_event.wait()
            if send_rs485_block_event.is_set():
                #~ print ("|||||||||||||||||||||||||   block event set from state_switch -> not local load |||||||||||||||||||||||")
                msg_c_obj.send_i2c(bus,par_obj.slaveid[2],par_obj.STOP_COMMAND,[ord("0")],send_rs485_block_event)

            time.sleep(0.01)
        
        
        
        
#    if(i==1):
#        time.sleep(5)
#        Load_list[0].state=par_obj.STOP_UPDATE_STATE
#        Source_list[0].state=par_obj.STOP_UPDATE_STATE
#    elif(i==0):
#        time.sleep(1)
#    i=i+1     

#i=0

    
        
def batt_voltage_f(bus):
    global batt_voltage
    while True:
        batt_voltage=14.2
#        print "Battery_voltage Thread"
        time.sleep(1)

def poll_slave_f(bus,Feedback_list):
    global local_source_list
    param=[]
    value_received = []
#    par_obj = par_var()
    msg_c_obj = message_send()
    par_obj = par_var()
    time.sleep(5)
    print "Sending poll thread"
#    msg_c_obj.send_i2c(bus,0x32,0x80,[0])
#    time.sleep(3)
#    x=msg_c_obj.receive_i2c(bus,0x32,0x23,8)
#    param=msg_c_obj.msg_unpack(x,2)
#    print param
    while True:
        state_switch_event.wait()
        #~ print "poll_slave -> State switch event set"
        if state_switch_event.is_set():
            for slave in range(len(par_obj.slaveid)):
                message_send_poll =[0]
                send_rs485_block_event.wait()
                if send_rs485_block_event.is_set():
                    #print ("|||||||||||||||||||||||||____BEFORE___poll slave function |||||||||||||||||||||||")
                    value_received= msg_c_obj.send_i2c(bus,par_obj.slaveid[slave],0x80,message_send_poll,send_rs485_block_event)
                    #print ("|||||||||||||||||||||||||____AFTER___poll slave function |||||||||||||||||||||||")  
                if value_received[0]:
                    param=msg_c_obj.msg_unpack(value_received[1],4)
    #                print param
    #                
    #                print slave 
                
                if param :               
                    if not math.isnan(param[0]):
                        Feedback_list[slave].voltage_port1 = param[0]
                        print ("Feedback", Feedback_list[slave].voltage_port1)
                    else:
                        Feedback_list[slave].voltage_port1 = 0
                    if not math.isnan(param[1]):
                        Feedback_list[slave].voltage_port2 = param[1]
                    else:
                        Feedback_list[slave].voltage_port2 = 0
                    if not math.isnan(param[2]):
                        Feedback_list[slave].current_port1 = param[2]
                    else:
                        Feedback_list[slave].current_port1 = 0
                    if not math.isnan(param[3]):
                        Feedback_list[slave].current_port2 = param[3] 
                    else:
                        Feedback_list[slave].current_port1 = 0
                    """
                    print("************* poll slave thread******************")
                    print par_obj.slaveid[slave]
                    print vars(Feedback_list[slave])"""
                else:
                    print("poll_slave -> param  is None")
            time.sleep(5)
    #            except:
    #                print "Error"

    #            print len(Feedback_list)
    #            for i in range(len(Feedback_list)):
    #                print "YESE"+str(i)
    #                print vars(Feedback_list[i])
    #        print "Polling"
            
def list_add_check_f(Source_list, Load_list,list_type):
    
    global local_load_list
    global local_source_list
#   For LOAD conditions
    print "*************************************"
    print "Inside list_add_check_f"
    
    if list_type==1: 

        if (len(Load_list) == 0 and len(local_load_list) == 0):
            print "Both the GLobal and Local Load list empty : NOTHING TO DO"
        elif(len(Load_list) != 0 and len(local_load_list) == 0):
            print "Local load list empty but global not empty and adding all the load in local list"
            for rows in Load_list:
                print "Appending the load in local load list"
                local_load_list.append(rows)
        elif(len(Load_list) != 0 and len(local_load_list) != 0):
            for global_i in range(len(Load_list)):
                for local_i in range(len(local_load_list)):
                    if( Load_list[global_i].id == local_load_list[local_i].id and Load_list[global_i].port == local_load_list[local_i].port):
                        print "User id matched"
                        break
                    else:
                        if( local_i == (len(local_load_list)-1)): # new user detected
                            local_load_list.append(Load_list[global_i])
                            print "New user detected"
                        else:
                            print "Error in local load list add function"
    elif list_type==2:
        
        if (len(Source_list) == 0 and len(local_source_list) == 0):
            print "Both the GLobal and Local Source list empty : NOTHING TO DO"
        elif(len(Source_list) != 0 and len(local_source_list) == 0):
            print "Local source list empty but global not empty and adding all the sources in local list"
            for rows in Source_list:
                print "Appending the source in local source list"
                local_source_list.append(rows)
        elif(len(Source_list) != 0 and len(local_source_list) != 0):
            for global_i in range(len(Source_list)):
                for local_i in range(len(local_source_list)):
                    if( Source_list[global_i].id == local_source_list[local_i].id and Source_list[global_i].port == local_source_list[local_i].port):
                        print "User id matched"
                        break
                    else:
                        if( local_i == (len(local_source_list)-1)): # new user detected
                            local_source_list.append(Source_list[global_i])
                            print "New user detected"
                        else:
                            print "Error in local source list add function"
    else:
        print("Wrong list_type")
        pass

def list_del_check_f(Source_list, Load_list,list_type):
    
    global local_load_list
    global local_source_list
    
    delete_arr=[]
    if list_type==1:
        for local_i in range(len(local_load_list)):
            #print "LOAD"
            #~ print "LOCAL_I" + str(local_i)
            if Load_list:
                for global_i in range (len(Load_list)):
                    #~ print "GLOBAL_I" + str(global_i)                    
                    if( local_load_list[local_i].id == Load_list[global_i].id and local_load_list[local_i].port == Load_list[global_i].port):
                        #~ print "DELETE: User ID Matched"
                        break
                    else:
                        if(global_i == (len(Load_list)-1)):
    #                        delete_arr.append(local_i)
                            local_load_list[local_i].state=2
                            #~ print "Load"
                            print "Deleted"
                        else:
                            pass
                            #~ print "DELETE: NO LOOP"
            else:
                #~ print ("No load in Global list")
                local_load_list[local_i].state=2
        #~ print delete_arr
#        for i in reversed(range(len(delete_arr))): # for not changing the order of list for deleting
#            local_load_list.pop(delete_arr[i])
#        pass

    elif list_type==2:    
        for local_i in range(len(local_source_list)):
            
            print "LOCAL_I" + str(local_i)
            if Source_list:
                for global_i in range (len(Source_list)):
                    print "GLOBAL_I" + str(global_i)                    
                    if( local_source_list[local_i].id == Source_list[global_i].id and local_source_list[local_i].port == Source_list[global_i].port):
                        print "DELETE: User ID Matched"
                        break
                    else:
                        if(global_i == (len(Source_list)-1)):
    #                        delete_arr.append(local_i)
                            local_source_list[local_i].state=2
                            print "Source"
                            print "Deleted"
                        else:
                            print "DELETE: NO LOOP"
            else:
                print ("No source in Global list")                
                local_source_list[local_i].state=2
        print delete_arr
 #       for i in reversed(range(len(delete_arr))):
 #           local_source_list.pop(delete_arr[i])
 #       pass
        
    else:
        print ("Wrong list_type")

#    return delete_arr

def list_update_f(Source_list, Load_list,list_type):
    
    global local_load_list
    global local_source_list
    if list_type==1:
        for local_i in range(len(local_load_list)):
            for global_i in range (len(Load_list)):
                if( local_load_list[local_i].id == Load_list[global_i].id and Load_list[global_i].port == local_load_list[local_i].port):
                    #start checking for any update
                    local_load_list[local_i] = Load_list[global_i]
                    print "UPDATED"
    elif list_type==2:
        for local_i in range(len(local_source_list)):
            for global_i in range (len(Source_list)):
                if( local_source_list[local_i].id == Source_list[global_i].id and Source_list[global_i].port == local_source_list[local_i].port):
                    #start checking for any update
                    local_source_list[local_i] = Source_list[global_i]
                    print "UPDATED"
    else:
        print("Wrong list_type")

def list_check_f(bus,Source_list, Load_list):
    load_delete_arr=[]
    source_delete_arr=[]
#   Checking for the load list change in data
    
#    print len(local_load_list)
    
    global local_load_list
    global local_source_list
    
#    if len(local_load_list) == 0:
#        if(len(Load_list)==0):
#            print "\n\nGLOBAL LIST EMPTY  | LOCAL EMPTY"
#        else:
#            for i in range(len(Load_list)):
#                local_load_list.append(Load_list[i])
#                print "\n*************************************"
#                print "\n"
#                print (vars(Load_list[i]))
#            print "\n LOCAL LIST EMPTY  | GLOBAL NOT EMPTY"
#    else:
#        if(len(Load_list) == 0):
#            print "\n GLOBAL LIST EMPTY  | LOCAL NOT EMPTY"
#            for i in range(len(local_load_list)):
#                local_load_list[i].state=2
#        else:
#    list_add_check_f(Source_list,Load_list,1)
#    list_update_f(Source_list,Load_list,1)    
#    print         
    list_del_check_f(Source_list,Load_list,1)
    list_del_check_f(Source_list,Load_list,2)
    
    for rows in local_source_list:
        print vars(rows)
    for rows in local_load_list:
        print vars(rows)
    port_off(bus)
#    for rows in load_delete_arr:
#            rows.state=2
    
    
#    if len(local_source_list) == 0:
#        if(len(Source_list)==0):
#            print "\n\nGLOBAL LIST EMPTY  | LOCAL EMPTY"
#        else:
#            for i in range(len(Source_list)):
#                local_source_list.append(Source_list[i])
#                print "\n*************************************"
#                print "\n"
#                print (vars(Source_list[i]))
#            print "\n LOCAL LIST EMPTY  | GLOBAL NOT EMPTY"
#    else:
#        if(len(Source_list) == 0):
#            print "\n GLOBAL LIST EMPTY  | LOCAL NOT EMPTY"
#            for i in range(len(local_source_list)):
#                local_source_list[i].state=2
#        else:
#    list_add_check_f(Source_list,Load_list,2)            
#    source_delete_arr= list_del_check_f(Source_list,Load_list,2)
#    list_update_f(Source_list,Load_list,2)
            
#            for rows in source_delete_arr:
#                    rows.state=2
        
#    local_load_list.append(Load_list[0])
#    print local_load_list

    
    
def table(local_load_list,local_source_list):
    
#            self.ip_address=None
#        self.port=None 
#        self.id=None 
#        self.type=None 
#        self.value=None 
#        self.min_volt=0 
#        self.max_volt=0
#        self.min_curr=0 
#        self.max_curr=0 
#        self.current_reqd=0
#        self.state=0
#        self.actual_curr=0
    dash = '-' * 40
    for i in range(len(local_load_list)):
        if i==0:
            print(dash)
            print "LOAD LIST"
            print(dash)
            print('{:<18s}{:>6s}{:>6s}{:>12s}{:>6s}{:>13s}{:>13s}'.format("IP_ADDRESS","PORT","ID","TYPE","STATE","CURRENT","ACTUAL_CURR"))
            print (dash)
        
        try:
            print ('{:<18s}{:>6d}{:>6s}{:>12s}{:>6d}{:>13f}{:>13f}'.format(local_load_list[i].ip_address,local_load_list[i].port,local_load_list[i].id,str(local_load_list[i].type),local_load_list[i].state,local_load_list[i].current_reqd,local_load_list[i].actual_curr))
        except:
            pass
    for i in range(len(local_source_list)):
        if i==0:
            print(dash)
            print "SOURCE LIST"
            print(dash)
            print('{:<18s}{:>6s}{:>6s}{:>12s}{:>6s}{:>13s}{:>13s}'.format("IP_ADDRESS","PORT","ID","TYPE","STATE","CURRENT","ACTUAL_CURR"))
            print (dash)
        try:
            print ('{:<18s}{:>6s}{:>6s}{:>12s}{:>6d}{:>13f}{:>13f}'.format(local_source_list[i].ip_address,local_source_list[i].port,local_source_list[i].id,str(local_source_list[i].type),local_source_list[i].state,local_source_list[i].current_aval,local_source_list[i].actual_curr))
        except:
            pass

def feedback_list_append(Feedback_list):
    par_obj = par_var()
    for i in range(par_obj.ports):
        Feedback_list.append(fb_var())
        print Feedback_list


def sorting():
    
    print "SOURCE SECTION"                
    
    with open("source_list.txt",'r') as f:
        con=f.readlines()
    #print con[0]
    con4=[]
    t=0
    if con:
        for k in con:
            con3=[]
            con1=k.split(',')
            j=0
            for i in con1:
#                print i
                con2=i.split(': ')
            
                if j==(len(con1)-1):
            #        print con2
                    con2[1]=con2[1].split('}')
                    
                    con3.append(con2[1][0])
                else:
                    if con2[1]=="None":
                        con3.append(None)
                    else:
                        con3.append(con2[1])
                j=j+1
                
            for i in con3[t]:
#                print i
                if i==None:
                    pass
            #        print "YES"
                
            con3[0]=float(con3[0])
            con3[1]=float(con3[1])
            con3[2]=float(con3[2])
            con3[3]=float(con3[3])
            con3[7]=float(con3[7])
            con3[8]=int(con3[8])
            con3[9]=float(con3[9])
            con3[10]=float(con3[10])
            
#            for i in con3:
#                print type(i)
            t=t+1
            con4.append(con3)
            
            
    print "LOAD SECTION"            
    with open("load_list.txt",'r') as f:
        con=f.readlines()
    #print con[0]
    con5 = []
    t=0
    if con:
        for k in con:
            con3=[]
            con1=k.split(',')
            j=0
            for i in con1:
#                print i
                con2=i.split(': ')
            
                if j==(len(con1)-1):
            #        print con2
                    con2[1]=con2[1].split('}')
                    
                    con3.append(con2[1][0])
                else:
                    if con2[1]=="None":
                        con3.append(None)
                    else:
                        con3.append(con2[1])
                j=j+1
                
            for i in con3[t]:
                print i
                if i==None:
                    pass
            #        print "YES"
                
            con3[0]=float(con3[0])
            con3[1]=float(con3[1])
            con3[2]=float(con3[2])
            con3[3]=float(con3[3])
            con3[7]=float(con3[7])
            con3[8]=int(con3[8])
            con3[9]=float(con3[9])
            con3[10]=float(con3[10])
            
            for i in con3:
                print type(i)
            t=t+1
            con5.append(con3)

    return con4, con5
    
    
def source_mapping(con):
    
    source_param_obj = source_param()
    print con    
    
    source_param_obj.max_curr = con[0]
    source_param_obj.min_volt = con[1]
    source_param_obj.actual_curr = con[2]
    source_param_obj.max_volt = con[3]
    source_param_obj.ip_address = con[4]
    source_param_obj.value = con[5]
    source_param_obj.id = con[6]
    source_param_obj.curr_aval = con[7]
    source_param_obj.state = con[8]
    source_param_obj.min_curr = con[9]
    source_param_obj.voltage = con[10]
    source_param_obj.type = con[11]
    source_param_obj.port = con[12]
    
    print len(con[12])
    
    return source_param_obj
    
def load_mapping(con):
        
    load_param_obj = load_param()
    
    load_param_obj.ip_address=None
    load_param_obj.port=0 
    load_param_obj.id=0 
    load_param_obj.type=0 
    load_param_obj.value=0
    load_param_obj.voltage=0
    load_param_obj.min_volt=0 
    load_param_obj.max_volt=0
    load_param_obj.min_curr=0 
    load_param_obj.max_curr=0 
    load_param_obj.current_reqd=0
    load_param_obj.state=0
    load_param_obj.actual_curr=0
    
def master_main(list_change_event,Source_list,Load_list,Feedback_list):
    
    global local_load_list
    global local_source_list
    ls=[]
    ld=[]
    feedback_list_append(Feedback_list)    
    
    bus=serial.Serial(port='/dev/ttyAMA0',baudrate = 115200, timeout = 2)
    if bus.closed:
        bus.open()      
    
    batt_thread = Thread(target = batt_voltage_f,args=(bus,))
    batt_thread.daemon=True     
    
    slave_poll_thread = Thread(target = poll_slave_f,args=(bus,Feedback_list))
    slave_poll_thread.daemon = True
    
#    batt_thread.start()    
    #~ print "\nBattery_thread_started"
    slave_poll_thread.start()
    print "\nslave_poll_thread_started"
    
    send_rs485_block_event.set()
    state_switch_event.set()
#    obj= parameters.load_param()
#    obj.port="2"
#    obj.state=1
#    obj.min_volt=14.2
#    obj.current_reqd=0.2
#    Load_list.append(obj) 
#    list_change_event.set()

    while True:
        list_change_event.wait()
        if list_change_event.is_set():
            list_change_event.clear()

#            local_source_list = []
#            local_load_list =[]
#            local_source_data, local_load_data=sorting()
#            if local_source_data:
#                con1=[]
#                for con_rows in local_source_data:
#                        local_source_list.append(source_mapping(con_rows))
#                        print "PRINTING CON1"
#                print con1
#                for rows in con1:
#                    print vars(rows)
#
#            if local_load_data:
#                con1=[]
#                for con_rows in local_load_data:
#                        local_load_list.append(load_mapping(con_rows))
#                        print "PRINTING CON1"
#                print con1
#                for rows in con1:
#                    print vars(rows)

#            print con

            """
            print "*************************************************"
            print "______________ ____Before LOOP_______________________"
            print "LOAD"
            print local_load_list"""  
            ld=local_load_list
            ls=local_source_list
            #~ if local_load_list:
                #~ for i in local_load_list:
                    #~ print (i)
                    #~ print vars(i)
            #~ print "SOURCE"
            #~ if local_source_list:    
                #~ for i in local_source_list:
                    #~ print (i)
                    #~ print vars(i)

            list_check_f(bus,Source_list, Load_list)
            """
            print "*************************************"
            print "LOAD"
            for i in local_load_list:
                print i
                print vars(i)
            print "SOURCE"
            for i in local_source_list:
                print i
                print vars(i)
            print "*************************************"
            """
            local_load_list = deepcopy(Load_list)
            local_source_list = deepcopy(Source_list)
            state_switch_event.clear()
            print "state_switch -> State switch event clear"
            state_switch(bus,0,local_source_list,local_load_list,Feedback_list)
            print "state_switch -> State switch event set"
            state_switch_event.set()

        
            del ld
            del ls
            
            print "___________________After LOOP________________________"
            print "LOAD"
            for i in local_load_list:
                print i
                print vars(i)
            print "SOURCE"
            for i in local_source_list:
                print i
                print vars(i)
            print "*************************************************"
            
#            f=open("source_list.txt",'w')
#            f.writelines(["%s\n"  % vars(item) for item in Source_list])
#            f.close()   
#            
#            f = open("load_list.txt", 'w')
#            f.writelines(["%s\n"  % vars(item) for item in Load_list])
#            f.close()
                
            #table(local_load_list,local_source_list)
                                    

if __name__ == "__main__":
    
    
#    Source_list= []
#    Load_list = []
#    comm_to_power_change_event = Event()
#    
#    
##    main_loop_th = Thread(target=master_main,args=(comm_to_power_change_event,Source_list,Load_list))
#    debug_thread = Thread(target=debug_code,args=())
#    debug_thread.daemon = True
#    debug_thread.start()
#
##    main_loop_th.daemon = True
##    main_loop_th.start()
#    pass
    pass
#    state_switch(0,0,0)
