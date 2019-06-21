#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 19:28:24 2019

@author: div
"""
import sys
import serial
sys.path.append('/home/pi//Documents/Energy_Router/')
#from global_var import par_var
import struct
import time
import smbus
from crccheck.crc import CrcModbus
import RPi.GPIO as GPIO
from global_var import par_var, fb_var, source_param, load_param
import threading


uart_event =threading.Event()

class message_send:
    def crc_checksum(self,string):
        return CrcModbus.calc(bytearray(string))
        
    def send_rs485(self,ser,message):
        return ser.write(message)
            
#        return True
    def receive_rs485(self,ser,slave_id):
        flag =0
        data = []
        while True:
            try:
                incoming = ser.read(1)
                incoming1 = ord(incoming)
    #            incoming1 = (list(incoming))[0]
                print incoming
                if flag ==1:
                    if i== 0:
                        data.append(incoming1)
                    if i== 1:
                        data_len =int(incoming.encode('hex'),24)
                        data.append(incoming1)
                    if i>1:
                        data.append(incoming1)
                        if i== (data_len-2):
#                            print ("crc_message",crc_message)
                            string_d = ""
                            for i in data:
                                string_d = string_d + chr(i)
#                                print ("string_d",string_d)
                            print ("string_d",string_d)
                            string_d = string_d
                            crc_message_result = msg_c_obj.crc_checksum(string_d)
                            print  crc_message_result
                            if crc_message_result != 0:
                                return None
                            break
                    i=i+1
                if incoming1 == slave_id:
                    data.append(incoming1)
                    flag =1
                    i=0  # to check for slave condition
            except:
                return None

        return data[3:19]
    def send_i2c(self,bus,slave_addr,command,data):
#    try:
#        print str(len(data))
    #    for rows in range(len(data)):
#        print len(data)
    #    print rows
        #print data
        #print command
        #print ("Sending message in message_send function")
        i=0
        while True:
            try:
                #print("slave",slave_addr)
#                print("data",data)
                bus.write_block_data(slave_addr,command,data)
                break
            except:
                if i == 5:
                    print("ERROR -> message_slave -> send_i2c")
                    print("slave address",slave_addr)
                    break
                i = i+1
                pass
            
        
    def receive_i2c(self,bus,slave_addr,command,byte_s):
        #print ("Receiving message")
#        try:
        i=0
        while True:
            try:
                return bus.read_i2c_block_data(slave_addr,command,byte_s)
                break
            except:
                if i == 5:
                    print("ERROR -> message_slave -> receive_i2c")
                    print("slave address",slave_addr)
                    break
                i = i+1
                pass
        
#        except:
#            pass
    """        
    def msg_pack(self,data,order):
        par_obj=par_var()
        total_number=len(order)
        list_msg=[]
        total_msg_size=0
        data = ""
        for param in range(len(data)):
            if(order[param]==par_obj.VOLTAGE):
                for param_char in range(par_obj.VOLTAGE_TYPE_SIZE):
                    list_msg.append(ord(data[param][param_char]))
                list_msg.append(ord(','))
            elif(order[param]==par_obj.CURRENT):
                for param_char in range(par_obj.CURRENT_TYPE_SIZE):
                    list_msg.append(ord(data[param][param_char]))
                list_msg.append(ord(','))
                total_msg_size=total_msg_size+1
            elif(order[param]==par_obj.SLAVEID):
        #            msg=msg+chr(data[param])
                list_msg.append((data[param]))
                list_msg.append(ord(','))
            elif(order[param]==par_obj.DIRECTION):
                list_msg.append(data[param])
                list_msg.append(ord(','))
        total_msg_size=total_msg_size+2
        #print list_msg
        return list_msg
    """
    def msg_pack(self,data,order):
        par_obj=par_var()
        total_number=len(order)
        list_msg=[]
        total_msg_size=0
        data = ""
        for param in range(len(data)):
            if(order[param]==par_obj.VOLTAGE):
                for param_char in range(par_obj.VOLTAGE_TYPE_SIZE):
                    list_msg.append(ord(data[param][param_char]))
                list_msg.append(ord(','))
            elif(order[param]==par_obj.CURRENT):
                for param_char in range(par_obj.CURRENT_TYPE_SIZE):
                    list_msg.append(ord(data[param][param_char]))
                list_msg.append(ord(','))
                total_msg_size=total_msg_size+1
            elif(order[param]==par_obj.SLAVEID):
        #            msg=msg+chr(data[param])
                list_msg.append((data[param]))
                list_msg.append(ord(','))
            elif(order[param]==par_obj.DIRECTION):
                list_msg.append(data[param])
                list_msg.append(ord(','))
        total_msg_size=total_msg_size+2
        print list_msg
        return list_msg
        
        
        
    def msg_unpack(self,data,param_count):
        par_obj=par_var()
        parameter_list=[]
#        total_number=len(param_count)
        if data:
            for count in range(param_count):
                x=""
                for i in reversed(range(count*4,(count+1)*4)):
                    y=format(data[i],'x').zfill(2)
    #            y.format(':2s')
                    x=x+y
                print x
                print (struct.unpack('!f',x.decode('hex'))[0])
                parameter_list.append(struct.unpack('!f',x.decode('hex'))[0])
        
            return parameter_list
        else:
            print("Connection timeout")
            return parameter_list
    def voltage_float_hex(self,v_f):
        return str(struct.pack('<f',v_f))    
    
    def current_float_hex(self,c_f):
        return str(struct.pack('<f',c_f))    
    
    def voltage_hex_float(self,v_hex_l):
#        return struct.unpack('<B', v_hex_l)
        pass

    def current_hex_float(self,c_hex_l):
        pass
    def send_before(ser,slaveid,command,data):
        pass
        

if __name__ =='__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)

    '''
    
    #   FOR SMBUS CODING
    
        bus=smbus.SMBus(1) 
        msg_c_obj = message_send()
        time.sleep(4)
        msg_c_obj.send_i2c(bus,0x32,0x80,[8])
        time.sleep(3)
        x=msg_c_obj.receive_i2c(bus,0x32,0x23,8)
        print x
        param=msg_c_obj.msg_unpack(x,2)
    '''
    
    
    msg_c_obj = message_send()
    par_obj = par_var()
    ser=serial.Serial(port='/dev/ttyAMA0',baudrate = 115200)
    slave_addr = 0x34  
    function = 0x12
#
#
##    *****************************************
##    PARAMETER UPDATE COMMAND TEST
##    *****************************************
#
    voltage = 12.3
    current = 0.78
    data=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.LOAD_DIRECTION]
    data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]
    message=msg_c_obj.msg_pack(data,data_type_order)
    
#    data = ""


#    data = data + msg_c_obj.voltage_float_hex(voltage)
#    data = data + msg_c_obj.voltage_float_hex(current)
#    data = data + chr(par_obj.LOAD_DIRECTION)
#
##    data_c=[msg_c_obj.voltage_float_hex(voltage),msg_c_obj.current_float_hex(current),par_obj.LOAD_DIRECTION]
##    data_type_order=[par_obj.VOLTAGE,par_obj.CURRENT,par_obj.DIRECTION]    
##    data=msg_c_obj.msg_pack(data_c,data_type_order)
#


#    data_size=len(data)
#    print ("Before data_size:" + str(len(data)))
#    if ((1+len(data))%4 !=0):
#        for i in range (4-(1+len(data))%4):        
#            data = data + chr(0x00)
#    else:
#        pass


#    print ("After data_size:" + str(len(data)))

#    message = chr(slave_addr) + chr(function) + chr(data_size) + (data)
#    print ("Message"+str(len(message)))
#    print message
#    check_data = msg_c_obj.crc_checksum(message)
#    check_high = chr(check_data>>8)
#    check_low = chr(check_data & 0xFF)
#    
#    
#    print "*******"
#    message = message + check_low + check_high
#    print (message)
#    GPIO.output(4,GPIO.HIGH)
#    msg_c_obj.send_rs485(ser,message)
    
    

#    *****************************************
#    POLL SLAVE RECEIVE COMMAND TEST
#    *****************************************print ser.inWaiting()
    
    msg_c_obj = message_send()
    par_obj = par_var()

    ser=serial.Serial(port='/dev/ttyAMA0',baudrate = 115200, timeout = 2)
    if ser.closed:
        ser.open()
    msg_recv =message_send()
    
#    time.sleep(0.5)
    while True:
        time.sleep(0.05)
        uart_event.clear()
        slave_addr = 0x34  
        function = 0x80
        data = "2"   
        #receive_thread.start()
        '''
        
        #   FOR SMBUS CODING
        
            bus=smbus.SMBus(1) 
            msg_c_obj = message_send()
            time.sleep(4)
            msg_c_obj.send_i2c(bus,0x32,0x80,[8])
            time.sleep(3)
            x=msg_c_obj.receive_i2c(bus,0x32,0x23,8)
            print x
            param=msg_c_obj.msg_unpack(x,2)
        '''
        data_size = len(data)
        #print ("Before data_size:" + str(len(data)))
        if ((1+len(data))%4 !=0):
            for i in range (4-(1+len(data))%4):        
                data = data + chr(0x00)
        else:
            pass
        #print ("After data_size:" + str(len(data)))
        #print data_size
        message = chr(slave_addr) + chr(function) + chr(data_size) + (data)
        #print ("Message"+str(len(message)))
        #print message
        check_data = msg_c_obj.crc_checksum(message)
        check_high = chr(check_data>>8)
        check_low = chr(check_data & 0xFF)
        
        
        #print "*******"
        message = message + check_low + check_high
        #print (message)
        GPIO.output(18,GPIO.HIGH)
    #    time.sleep(0.03)
        bytes_transmit_return = msg_c_obj.send_rs485(ser,message)
        #time.sleep(0.00005 *len(message))
        
        time_p = (float (len(message)))/10000
        time.sleep(time_p)
        
        GPIO.output(18,GPIO.LOW)
    #    print ser.out_waiting(3242) 
        
        
        
        
        ser.reset_input_buffer()
        #print(bytes_transmit_return)
        time.sleep(0.0006)  # FIND how to remove this timeout: since gpio get low before data is fully sent out    
        GPIO.output(18,GPIO.LOW)
        #uart_event.set()
        data =[]
        i=0
        t =time.time()
        flag =0
        data = []
        ser.reset_input_buffer()
        ser.reset_output_buffer()
    
        data=msg_c_obj.receive_rs485(ser,0x34)
        
        if data is not None:
            print data
        #    print ord(data[1])
            param=msg_c_obj.msg_unpack(data,4)
            print param
        else:
            print "Timeout occured"
    ser.close()
    #             except serial.serialutil.SerialException:
    #                print("No data this time")
     #   print(data)
    #    while True:
    #            if ser.inWaiting() > 0:
    #                data = ser.read()
    #            #print ser.inWaiting()
    #                print data.encode('hex')
    #    time.sleep(0.03)
    #    while True:
    #        pass
    #    print ser.inWaiting()
        #   rcd_message = msg_c_obj.receive_rs485(ser)
        #print rcd_message
       
