# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:25:29 2019

@author: divyanshu
"""

#!/usr/bin/python

#import smbus
import time
import signal
from threading import Thread, Timer, Event


from main_codes.power import master_main
from global_var import setting,parameters
from test_prog import main_th

from main_codes.gui import vp_start_gui

def start_power_master():
    main_loop_th = Thread(target=master_main,args=(setting.common.comm_to_power_change_event,setting.common.Source_list,setting.common.Load_list,setting.common.Feedback_list))
    main_loop_th.daemon = True
    main_loop_th.start()
    
    #gui_thread = Thread(target=gui_er,args=(setting.common.Feedback_list,))
    #gui_thread.daemon = True
    #gui_thread.start()


def debug_test_without_comm(list_change_event,Source_list,Load_list):
    time.sleep(2)
    
    print "Adding a Source"
    
    obj= parameters.source_param()
    obj.port="1"
    obj.state=1
    obj.voltage=14.2
    obj.current_aval=0.5
    obj.max_curr = 1
    Source_list.append(obj) 

#    obj= parameters.source_param()
#    obj.port="2"
#    obj.state=1
#    obj.min_volt=14.2
#    obj.current_aval=0.2
#    Source_list.append(obj) 
#    
    list_change_event.set()
    time.sleep(2)
    
    obj= parameters.load_param()
    obj.port="2"
    obj.state=1
    obj.voltage=14.2
    obj.current_reqd = 0.3
    obj.max_curr = 0.5
    Load_list.append(obj) 
    
    list_change_event.set()

    time.sleep(1)
#    
#    obj= parameters.load_param()
#    obj.port="5"
#    obj.state=1
#    obj.voltage=14.2
#    Load_list.append(obj) 
#
#    obj= parameters.load_param()
#    obj.port="6"
#    obj.state=1
#    obj.voltage=14.2
#    Load_list.append(obj) 
#    
#    list_change_event.set()
#    
    #~ time.sleep(5)
#~ #    print Load_list[1]
    #~ Load_list[0].current_reqd = 0.2
#~ #    Load_list[2].voltage=19.2
    #~ list_change_event.set()
    
    #~ time.sleep(5)

    #~ Load_list[0].current_reqd = 0.4
#~ #    Load_list[2].voltage=19.2
    #~ list_change_event.set()
        
    
    #~ time.sleep(2)
    #print "Deleting Elements"
    #time.sleep(1)
    #Load_list.pop(0)
    #list_change_event.set()
#    print ("Deleting the source")
    #~ Source_list[0].state=2
    #~ Source_list[1].state=2
#    obj= parameters.load_param()
#    obj.port="2"
#    obj.state=1
#    obj.voltage=14.2
#    obj.current_reqd=0.3
#    Load_list.append(obj) 
    #~ list_change_event.set()
#    time.sleep(5)
#    print "Deleting all the elements"
#    Load_list.pop(0)
#    Source_list.pop(0)
#    list_change_event.set()
    
#    time.sleep(5)
#    obj=parameters.load_param()
#    obj.port="2"
#    obj.stat
    print "Done"
    while True:
        time.sleep(1000)
        pass    
def gui_er(Feedback_list):
    vp_start_gui(Feedback_list)
    
if __name__ == "__main__":

    Source_list= []
    Load_list = []
    comm_to_power_change_event = Event()
    Feedback_list=[]
    
#    main_loop_th = Thread(target=master_main,args=(comm_to_power_change_event,Source_list,Load_list))
    debug_thread = Thread(target=debug_test_without_comm,args=(comm_to_power_change_event,Source_list,Load_list))
    debug_thread.daemon = True
   # debug_thread.start()
    
    start_thread = Thread(target=master_main,args=(comm_to_power_change_event,Source_list,Load_list,Feedback_list))
    start_thread.daemon = True
    start_thread.start()
    
    #gui_thread = Thread(target=gui_er,args=(Feedback_list,))
    #gui_thread.daemon = True
    #gui_thread.start()
    while True:
        time.sleep(10)
#    main_loop_th.daemon = True
#    main_loop_th.start()
    pass
#    comm_to_power_change_event = Event()
#    Load_list = []
#    
#    print "Main_state_thread STARTED"
#    main_loop_th = Thread(target=master_main,args=(comm_to_power_change_event,setting.common.Source_list,setting.common.Load_list))
#    main_loop_th.daemon = True
#    
#    print "Test_state_thread STARTED"
#    test_state_th = Thread(target=main_th,args=(comm_to_power_change_event,setting.common.Source_list,setting.common.Load_list))
#    test_state_th.daemon = True
##    
#    
#    main_loop_th.start()
#    test_state_th.start()
#    
#    while True:
#        time.sleep(5)
    
#    main_state_th.join()

#    print "Done"
#    state_th.join()
#    print "Joined"
    
#    to be updated by communication moodule
#
#    load = Load_struct(ip_address = "192.168.0.100", port=1, id = 12, type="real", value=10, min_volt=9.1, max_volt = 15, min_curr = 0.1, max_curr = 0.8, load_reqd=0.5, state=0, actual_curr=0)
#    load = load.param()

#    LOAD_DIRECTION = 2
#    SOURCE_DIRECTION =1
#
#    Load_list.append(load_param())
#    Load_list[0].current_reqd=0.26
#    Load_list[0].port = 2
#    Load_list[0].state = PARAM_UPDATE_STATE
#    
##    source = Source_struct(ip_address = "192.168.0.101", port=2, id = 12, type="real", value=10, min_volt=9.1, max_volt = 15, min_curr = 0.1, max_curr = 0.8, current_aval=0.7, state=0, actual_curr=0)
#    
#    Source_list.append(source_param())
#    Source_list[0].current_aval=0.5
#    Source_list[0].port = 1
#    Source_list[0].state = PARAM_UPDATE_STATE
#    
#    batt_voltage=13.5
#
#    total_sources = len(Source_list)  
#    
#    total_amp_av=0
#    total_load_rq=0
#    mul_factor=0
#    voltage =25
#    conv_max_current=0.8
#    conv_min_current=0.1
##    
##
#    exit_sig=0
#    data=[]
#    bytes_s=8
#
#    slaveid=[0x32,0x33]
#    
##    data=[voltage_float_hex(voltage),current_float_hex(current)]
##    data_type_order=[VOLTAGE,CURRENT]    
##    message=msg_pack(command,data,data_type_order)
##    print message
#    
#    s=struct.pack('<f',voltage)
#    print ord(s[0])
##    print ord(message[2])
##    print struct.pack('<B',message[0])
##    try:
#    i=0
#    
##    while True:
#        # CALCULATING THE CURRENT AVAILABILITY AND REQUIRED: Equal priority and sourcing based on the multiplicative factor
#    for rows in range(len(Source_list)):
#        total_amp_av += Source_list[rows].current_aval
#    
#    for rows in range(len(Load_list)):
#        if(Load_list[rows].current_reqd <= conv_max_current):                
#            total_load_rq += Load_list[rows].current_reqd
#            Load_list[rows].actual_curr = Load_list[rows].current_reqd
#        else:
#            total_load_rq += conv_max_current
#            Load_list[rows].actual_curr = conv_max_current
#    print "loop"
#    print i
#    while(i<=0):
#        if(total_amp_av>=total_load_rq):
#            mul_factor=total_load_rq/total_amp_av
#            print "if complete"
#            for rows in range(len(Load_list)):
#                if(Load_list[rows].state == START_UPDATE_STATE):
#                # STARTING CONVERTER BASED ON THE PORTS GIVEN AND WITH NO DUTY OUT
#                    if(Load_list[rows].port==1):
#                        print "Sending start port 1"
#                        send_i2c(slaveid[0],START_COMMAND,[ord("0")])
#                        Load_list[rows].state = PARAM_UPDATE_STATE
#                        
#                    elif(Load_list[rows].port==2):
#                        print "Sending start port 1"
#                        send_i2c(slaveid[1],START_COMMAND,[ord("0")])
#                        Load_list[rows].state = PARAM_UPDATE_STATE
#                        
#                elif(Load_list[rows].state == PARAM_UPDATE_STATE):
#        
#                    if(Load_list[rows].port == 1):
#                        current = Load_list[rows].actual_curr
#                        print current
#                        data=[voltage_float_hex(voltage),current_float_hex(current),LOAD_DIRECTION]
#                        data_type_order=[VOLTAGE,CURRENT,DIRECTION]    
#                        message=msg_pack(data,data_type_order)
#                        
#                        print "slave id"  + str(slaveid[0])
#                        
#                        send_i2c(slaveid[0],PARAM_COMMAND,message)    
#                    elif(Load_list[rows].port == 2):
#        #                    voltage = 13.2
#                        current = Load_list[rows].actual_curr
#                        print current
#                        data=[voltage_float_hex(voltage),current_float_hex(current),LOAD_DIRECTION]
#                        data_type_order=[VOLTAGE,CURRENT,DIRECTION]    
#                        message=msg_pack(data,data_type_order)
#                        
#                        print "slave id"  + str(slaveid[1])
#                        print message
#                        send_i2c(slaveid[1],0x12,message)
#                elif(Load_list[rows].state == STOP_UPDATE_STATE):
#                    if(Load_list[rows].port==1):
#                        print "Sending start port 1"
#                        send_i2c(slaveid[0],STOP_COMMAND,[ord("0")])
#                        Load_list[rows].state = START_UPDATE_STATE
#                        
#                    elif(Load_list[rows].port==2):
#                        print "Sending start port 1"
#                        send_i2c(slaveid[1],STOP_COMMAND,[ord("0")])
#                        Load_list[rows].state = START_UPDATE_STATE
#
#        
#        
#            for rows in range(len(Source_list)):
#                if(Source_list[rows].state == START_UPDATE_STATE):
#                # STARTING CONVERTER BASED ON THE PORTS GIVEN AND WITH NO DUTY OUT
#                    if(Source_list[rows].port==1):
#        
#                        send_i2c(slaveid[0],START_COMMAND,[ord("0")])
#                        Source_list[rows].state = PARAM_UPDATE_STATE
#                        
#                    elif(Source_list[rows].port==2):
#                        
#                        send_i2c(slaveid[1],START_COMMAND,[ord("0")])
#                        Source_list[rows].state = PARAM_UPDATE_STATE
#                        
#                elif(Source_list[rows].state == PARAM_UPDATE_STATE):
#        
#                    if(Source_list[rows].port == 1):
#                        print mul_factor
#                        Source_list[rows].actual_curr = Source_list[rows].current_aval * mul_factor
#                        current = Source_list[rows].actual_curr
#                        
#                        data=[voltage_float_hex(voltage),current_float_hex(current),SOURCE_DIRECTION]
#                        data_type_order=[VOLTAGE,CURRENT,DIRECTION]    
#                        message=msg_pack(data,data_type_order)
#                        
#                        print "slave id"  + str(slaveid[0])
#                        
#                        send_i2c(slaveid[0],PARAM_COMMAND,message)    
#                    elif(Source_list[rows].port == 2):
#                        print mul_factor
#                        Source_list[rows].actual_curr = Source_list[rows].current_aval * mul_factor
#                        current = Source_list[rows].actual_curr
#                        
#                        data=[voltage_float_hex(voltage),current_float_hex(current),SOURCE_DIRECTION]
#                        data_type_order=[VOLTAGE,CURRENT,DIRECTION]    
#                        message=msg_pack(data,data_type_order)
#                        
#                        print "slave id"  + str(slaveid[1])
#                        
#                        send_i2c(slaveid[1],PARAM_COMMAND,message)
#                        
#                elif(Source_list[rows].state == STOP_UPDATE_STATE):
#                    if(Source_list[rows].port==1):
#                        print "Sending start port 1"
#                        send_i2c(slaveid[0],STOP_COMMAND,[ord("0")])
#                        Source_list[rows].state = START_UPDATE_STATE
#                        
#                    elif(Source_list[rows].port==2):
#                        print "Sending start port 1"
#                        send_i2c(slaveid[1],STOP_COMMAND,[ord("0")])
#                        Source_list[rows].state = START_UPDATE_STATE
#            time.sleep(0.01)
#        if(i==1):
#            time.sleep(5)
#            Load_list[0].state=STOP_UPDATE_STATE
#            Source_list[0].state=STOP_UPDATE_STATE
#        elif(i==0):
#            time.sleep(1)
#        i=i+1     
#
#i=0
    
    
    
    
    
#        for rows in range(len(Source_list)):
#            if(Source_list[rows].port == 1):
##                    voltage = 13.2
#                current = (Source_list[rows].current_aval)*mul_factor
#                data=[voltage_float_hex(voltage),current_float_hex(current)]
#                data_type_order=[VOLTAGE,CURRENT]    
#                message=msg_pack(data,data_type_order)
#                print "slave id"  + str(slaveid[0])
#                send_i2c(slaveid[1],PARAM_COMMAND,message)    
#            elif(Source_list[rows].port == 2):
##                    voltage = 13.2
#                current = (Source_list[rows].current_aval)*mul_factor
#                data=[voltage_float_hex(voltage),current_float_hex(current)]
#                data_type_order=[VOLTAGE,CURRENT]    
#                message=msg_pack(data,data_type_order)
#                print "slave id"  + str(slaveid[1])
#                send_i2c(slaveid[1],PARAM_COMMAND,message)                
#            
        
#        time.sleep(0.01)        
    
    
#    while True:


#    if( (batt_voltage>9.8) & (batt_voltage<12.2) ):
#        pass
#    elif((batt_voltage>=12.2) & (batt_voltage<14.6) ):
#        for rows in range(len(Source_list)):
#            total_amp_av += Source_list[rows].current_aval
#        
#        for rows in range(len(Load_list)):
#            total_load_rq += Load_list[rows].load_reqd
#        
#        if(total_amp_av>=total_load_rq):
#            mul_factor=total_load_rq/total_amp_av
#            
#            for rows in range(len(Load_list)):
#                if(Load_list[rows].port == 1):
##                    voltage = 13.2
#                    current = Load_list[rows].load_reqd
#                    voltage = Load_list[rows].                    
#                    data=[voltage_float_hex(voltage),current_float_hex(current)]
#                    data_type_order=[VOLTAGE,CURRENT]    
#                    message=msg_pack(command,data,data_type_order)
#                    print "slave id"  + str(slaveid[0])
#                    send_i2c(slaveid[0],0x01,message)    
#                elif(Load_list[rows].port == 2):
##                    voltage = 13.2
#                    current = Load_list[rows].load_reqd
#                    data=[voltage_float_hex(voltage),current_float_hex(current)]
#                    data_type_order=[VOLTAGE,CURRENT]    
#                    message=msg_pack(command,data,data_type_order)
#                    print "slave id"  + str(slaveid[0])
#                    send_i2c(slaveid[0],0x01,message)
#            for rows in range(len(Source_list)):
#                if(Source_list[rows].port == 1):
##                    voltage = 13.2
#                    current = (Source_list[rows].current_aval)*mul_factor
#                    data=[voltage_float_hex(voltage),current_float_hex(current)]
#                    data_type_order=[VOLTAGE,CURRENT]    
#                    message=msg_pack(command,data,data_type_order)
#                    print "slave id"  + str(slaveid[1])
#                    send_i2c(slaveid[1],0x01,message)    
#                elif(Source_list[rows].port == 2):
##                    voltage = 13.2
#                    current = (Source_list[rows].current_aval)*mul_factor
#                    data=[voltage_float_hex(voltage),current_float_hex(current)]
#                    data_type_order=[VOLTAGE,CURRENT]    
#                    message=msg_pack(command,data,data_type_order)
#                    print "slave id"  + str(slaveid[1])
#                    send_i2c(slaveid[1],0x01,message)                
        
#        print total_amp_av
#        print total_load_rq
#    send_i2c(0x22,0x01,message)    
#    send_i2c(0x22,0x80,[bytes_s])    
#    print ("Okay")
#    x=bus.read_i2c_block_data(0x22,0x23,bytes_s)
#    except:
#        print x
    
#    print x
#    send_i2c(0x22,message)    
#    data=[0x23,0x34,0x45,0x56]
#    msg_pack(0x81,data)
#    data=[0x34,0x45,0x45]
#    msg_pack(0x81,data)

#def handler(a,b):
#    print("Signal Number:", a, " Frame: ", b)  
#    
#def timer():
#    global timer_value
#    time_start=time.time()
##    print time_start
#    while True:
#        if (time.time()-time_start) >0.001:
#            timer_value=time.time()-time_start
#            time_start=time.time()
##            time.sleep(0.0005)
##            print timer_value
##            time.sleep(0.1)
#    
#
#def send_data(slave_addr,data):
#    try:    
#        bus.write_byte_data(slave_addr,1,data)
#        print "This slave " +str(slave_addr) + " responded"
#    except:
#        pass
#
#def print_timer():
#    global timer_value
#    while True:
#        time.sleep(0.1)
#        print timer_value
#
#def i2c_check():
#    for device_id in range(128):
#        send_data(device_id,0x01)
#
#def pack_param():
#    
#def print_d():
#    
#    global timer_value
#    print"inside" + str(time.time() - timer_value)
#    pass
#
#if __name__ == "__main__":
##    while(1):
#    th=threading.Timer(0.001,print_d)
#    timer_value= time.time()
#    print time.time()
#    th.start()
##    th.join()
##    print time.time() - timer_value
##    thread_timer=threading.Thread(target=timer,args=())
##    thread_timer_print=threading.Thread(target=print_timer,args=())
##    thread_timer.start()
##    thread_timer_print.start()
##    thread_timer.join()
##    thread_timer_print.join()
#
##    signal.signal(signal.SIGINT, handler)
##    while(1):
##        time.sleep(10)
##    while True:
##        pass
