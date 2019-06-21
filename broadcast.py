# -*- coding: utf-8 -*-

 
import socket
import sys
import traceback
import threading
import struct
import errno
import os
from Queue import *
from packet_gen import Packet ,Energy_Packet
import pickle
from time import sleep ,time
from astropy.table import Table
from global_var import setting
from main_codes.comm.Network import net_tools as nt
from global_var import setting
import random
from socket import error as socket_error
from main_codes.comm import main
#import time
from multiprocessing.pool import ThreadPool
packet_queue = Queue()
broadcast_resp_queue =[]
ip_list =['10.0.0.3']
if sys.argv[1] == "debug":
    debug =False
else:
    debug =True
    
while True:
    try:
        IP_addr = main.ni.ifaddresses('eth0')[main.ni.AF_INET][0]['addr']
        ip  =IP_addr
        print("IP Address",IP_addr)
        setting.common.ip_address =ip
        setting.network_var.self_ip = IP_addr
        break
    except:
        print("Interface doesnot have a  ip address")
#IP_addr = '192.168.0.100'
sem =threading.Semaphore()

next_hop_list =[]
packet_send     = []   ### create a list of send packet
packet_receive  = []  ### create a list ofr received packet
packet_event    = {}   ## Dictionary for maintaining an list for event and packet id
packet_received = {}  ### A dictionary for maintaing a packet received datbase
broadcast_packet_list = []
broad_packet_send =[]
broad_packet_recv =[]
broad_dict_packet_recv={}
response_packet_recv = {}
confirm_packet_recv  = []
confirm_packet_received={}
external_load_list =[]
"""  Pakcet Timer wait for a packet for certain time and return the packet when received. When there is a the time out happens timeout is retuned back.
     Threshold gives the time period (seconds) for which we should wait for packet. flag_set is used to flag an event when the packet of a paritcular  id is received.
     id is the packet id .

"""
class packet_timer(object):
    global packet
    def __init__(self,flag_set,id):
        self.time =time()
        self.flag_set =flag_set
        self.threshold =5.0
        self.id  =id

    def check_packet(self):
        while True:
            # checks if the time elapsed is less than threshold
            if ( (time() - self.time) < self.threshold):
                if self.flag_set.isSet():
                    pack =packet_received.get(self.id)  ## get the packet value from dictionary by giving the key "sef.id"
                    try:
                        del packet_received[self.id]    ## delete the "self.id" from the dictionary of packet_received
                    except KeyError:
                        print("Key Errorcheck_packet in ",KeyError)  ## if not able to delete show an error
                    return pack  ## return the packet 
                    break
                else:
                    pass
            else:
                print("timeout") ## not able to detect the packet within the time period "timeout" is returned back
                return "timeout"
            sleep(0.1)
        sys.exit()
        
        
        
        
list_of_power_conn=[]
""" ******************* this is for port forwading and communication with external router************************** """
while True:
        try:
            power_conn_port_no = 9050
            power_conn        = main.socket.socket(main.socket.AF_INET,main.socket.SOCK_STREAM)
            power_conn.setsockopt(main.socket.SOL_SOCKET,main.socket.SO_REUSEADDR,1)
            power_conn.bind((IP_addr,power_conn_port_no))
            power_conn.listen(10)
            print"________________PORT NUMBER 9050 IS OPEN___________________________"
            break
        except socket_error as serr:
            print("Socket server not created port number 9050")
            print("line 89")
            print (serr)

def router_to_router_server():
    print("We are in power conn port number 9050")
    while True:
            conn,addr= power_conn.accept()
            list_of_power_conn.append((conn,addr))


    
def queue_power_conn():
    print("we are in queus power conn")
    while True:
        if  list_of_power_conn:
                sleep(0.4)
                var =list_of_power_conn.pop()
                print("we are inside queue of power conn")
                t   =  threading.Thread(target =conn_recv ,args = (var[0],var[1]))
                t.daemon =True
                t.start()                

""" It is the func. which process the packet received from the broadcast response """
def conn_recv(conn,addr):
    print("We are in conn receive function")
    conn.settimeout(5)
    try:
             message = conn.recv(4096)
             #print(message)
    except:
             print("The connection exited for ip:"+addr[0])
             sys.exit()
    packet = pickle.loads(message)
    print("-----------------------conn_recv ->  PACKET[0]-----------------------------------------------")
    print(packet[0])
    print("-----------------------conn_recv ->  PACKET[1]-----------------------------------------------")
    print(packet[1])
    if  (packet[0] == 3 )and (packet[1] ==4):
                print("It is  a broadcast response packet")
                #print(packet[9])
                print("-----------------------conn_recv ->  PACKET[3]-----------------------------------------------")
                print(packet[3])
                #print(broad_packet_send)
                """ In dictionary store the list  corresponding to a id."""
                if packet[3] in broad_packet_send:
                    print("We are inside broadcast packet send")
                    lst = broad_dict_packet_recv[packet[3]] 
                    lst.append(packet)
                    broad_dict_packet_recv[packet[3]] = lst
                    print("Broadcastlist packet received corresponding to the id ",packet[3])
                    print(broad_dict_packet_recv[packet[3]])
    if  (packet[0] == 5) and (packet[1] == 6) :
                print("It is a conformation pakcet")
                print(packet[9])
                if packet[3] in response_packet_recv:
                    confirm_packet_recv.append(packet[3])
                    confirm_packet_received[packet[3]] = packet
    sys.exit()
    

       
         



"""**************************************************************************************************************** """


"""  ***************************** this function is for sending unicast response to a particular ip and email address"""
def unicast_message(ip , port_no ,msg):
                sock = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                #sock_poll.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.settimeout(1)
                try:
                        print ("________________ip_____________",ip)
                        print("________________port_no__________",port_no)
                        sock.connect((ip ,port_no))
                        print("________________sock_connect_______________")
                        sock.send(msg)
                        print("________________sock_send__________________")
                        sock.close()
                        print("________________sock_close_________________")
                        return True
                except socket_error as serr:
                        sock.close()
                        print("-->ERROR:",serr)
                        return False



"""Try to trace route the packet max. 3 time. If not able no able to get the path in 3 try declare it as not reachable
ip_req is ip of the load which wants to connect to some other source.
ip_req is ip of the source in detination energy router
ip_dst_mast is ip of the detination energy router
"""

def traceroute(ip_req,ip_dst,ip_dst_mast):
    i =0
    while i < 3:
        if debug:
                port_from , port_to = get_port_info(ip_req,ip_dst_mast)  #port_from where  the packet is coming  and port_to where packet is going
                output = traceroute_path(ip_dst,ip_dst_mast,port_to ,port_from)  # give traceroute command to the end destination point
        else:
                output = traceroute_path(ip_dst,ip_dst_mast,'6' ,'3')
        
        #print( port_from ,port_to)
        if output == "timeout":
            i =i+1
            pass
        else:
            return output
    return "No route to path"

 
def traceroute_path(ip_dst,ip_dst_mast,port_to,port_from):
    sock        = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ip_next         = next_hop_ip(port_to)
    pack            = Packet()
    print("We are in traceroute path")
    while True:
        packet_id       = random.randint(1,65792)
        if packet_id not in packet_send:
            break
        sleep(0.005)
    packet      = pack.packet_src(packet_id,IP_addr,ip_dst,ip_dst_mast,port_to,port_from)
    print(pickle.loads(packet))
    print ("ip_next",ip_next)
    sock.sendto(packet,(ip_next,9000))
    packet_send.append(packet_id)                                    ### to append packet id in packet send function
    flag_set ='flag_set'+str(packet_id)
    flag_set =threading.Event()  
    
    packet_event[packet_id] =flag_set
    p = packet_timer(flag_set,packet_id)
    poll   = ThreadPool(processes =1)
    result = poll.apply_async(p.check_packet,)
    #print("traceroute path op",result.get())
    return result.get()
 
"""
To receive any packet for the router
""" 
 
def traceroute_recive():
    sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((IP_addr,9000))
    while True:
            data ,addr = sock.recvfrom(1024)
            if data:
                sem.acquire()
                packet_queue.put(data)
                sem.release()
                
                
                
                
def packet_fwd():
    while True:
        sleep(0.4)
        if not packet_queue.empty():
              print("We are in packet queue")
              sem.acquire()
              packet = packet_queue.get()         
              sem.release()
              packet =pickle.loads(packet)
              print(packet)
              if packet[0] ==30:
                  if packet[7].strip() == setting.network_var.self_ip:
                          print("Broadcast IP Address is matched")
                          if packet[6].strip() in setting.network_var.list_of_ip:
                              print("we are in if of packet(6)")
                              pack        = Packet()
                              end_port    = port_no(packet[6].strip())## to get the port number to which the end load is connected
                              print ("End port port number ",end_port)
                              """prev_hop_port variable gives the port number from which the traceroute packet is coming from"""
                              if len(packet)>10:
                                  length =len(packet)
                                  prev_hop_data =packet[length -1]
                                  prev_hop_ip   =prev_hop_data[0]
                                  prev_hop_port =next_hop_port(prev_hop_ip)
                                  print("pakcet len greater than 10")
                                  setting.common.traceroute_recived[packet[5]]=packet
                              else:
                                  prev_hop_port= next_hop_port(packet[5])
                                  print("packet len less than 10")
                              packet_resp = pack.packet_response(packet,end_port,prev_hop_port)##to create the response of the requested packet
                              Udp_message(str(packet[5]),packet_resp,9000)
                          else:
                              pack        = Packet()
                              packet_resp = pack.packet_end_error(packet)
                              Udp_message(str(packet[5]),packet_resp,9000)
                  else :
                      
                      """  This part of the code for sending hop count expired packet . 
                      When the packet reaches the router and it's value is 1 then the hop couunt expired packet is send back to the source router .   """
                      if  packet[3] == 1:      ### to give a response message that the hop count has expired
                          pack        = Packet()
                          packet_resp = pack.packet_hop_exp(packet)
                          Udp_message(str(packet[5]),packet_resp,9000)
                          
                      #""" this part of the code is for packet forwarding.
                      #The packet is forwarded to the next router and a packket is send to source router indicating the packet has crossed the current router """    
                      else :
                           port_from ,port_to = get_port_info(packet[5],packet[7])  #port_from where  the packet is coming  and port_to where packet is going
                           if port_from is  None:  ## if the destination is not available in the routertable
                               print("Out ip not avaiable")
                               pack   = Packet()
                               pack   = pack.packet_no_route(packet)
                               Udp_message(str(packet[5]),packet_resp,9000)
                               continue
                           next_ip            = next_hop_ip(port_to)
                           pack               = Packet()
                           packet_resp        = pack.packet_fwd(packet,IP_addr,port_to,port_from)
                           
                           print("packet_resp",pickle.loads(packet_resp))
                           print("next hop ip address is:",next_ip)
                           
                           packet_feedback    = pack.packet_intermediate_response(packet,IP_addr)
                           
                           Udp_message(next_ip,packet_resp,9000)
                           Udp_message(str(packet[5]),packet_feedback,9000)
              elif packet[0] ==0 :
                  if packet[1] == 10:
                        print("hop count exceded",packet[6])
                  if packet[1] == 1:
                        print("Destination unreachable",packet[6])
              elif packet[0] ==4:
                  print("Load or source is no more present")
              elif packet[0] ==20:
                  print (" reached router --> {}  ................... hop count -->{} ".format(packet[6],packet [4]))
              elif packet[0]  ==3:
                  flag_set  = packet_event.get(packet[2])
                  try :
                      del packet_event[packet[2]]
                  except KeyError:
                      print('This is an key error in packet_fwd',KeyError)
                  packet_received[int(packet[2])] = packet
                  flag_set.set()
                  """
                  dst_port_from =packet[10]
                  dst_port_to   =packet[11]
                  hop_count     =packet[4]
                  hop_max       =packet[3]
                  temp_table    =[]
                  i             =0
                  while i <packet[4]:
                      temp_table.append(packet[12+i])
                      i =i+1
                  temp_table.append([packet[6],packet[10],packet[11]])
                  t1 = Table(rows =temp_table , names =('ip' ,'port_to','port_from'))
                  print(t1)
                  """
        else:
            pass
        
        
"""to get about information of input and output ip connected to which of the ports"""
def get_port_info(ip_in,ip_out):
    print("we are in get port info")
    i=0
    in_port=None
    out_port =None
    for net in next_hop_list:
	#print("net[0]",net[0].strip())
        if  ip_in.strip() == net[1].strip():
            in_port =net[0]
        else:
            pass
        if  ip_out.strip() == net[1].strip():
            out_port =net[0]
        else:
            pass
        
    if setting.common.Load_list:   ### to check wether the ip list is populated
        for net in setting.common.Load_list:
            if  ip_in.strip() == net.ip_address:
                in_port =net.port
            else:
                pass 

    if setting.common.Source_list:   ### to check wether the ip list is populated
        for net in setting.common.Source_list:
            if  ip_in.strip() == net.ip_address:
                in_port =net.port
            else:
                pass 
    if out_port is None:
        while i<4:
            port = nt.Mac(ip_out)
            if port is  not None:
                out_port =port
                break
            else:
                i=i+1
                if i ==4:
                    out_port=None
                sleep(0.05)
                
                        
    print("in_port {}  out_port   {}".format(in_port,out_port))
    #print ("in_port {}",type(in_port))   
    return in_port , '1'



"""It give next hop ip address corresponding to a port number"""
def next_hop_ip(port):##make a file for the next_hop_list and access ip and port from there

    for net in next_hop_list:
        if port.strip()== net[0].strip():
            ip_addr =net[1].strip()
            break
    return ip_addr




"""Gives port number corresponding to an ip addresss"""
def next_hop_port(ip):

    for net in next_hop_list:
        if ip.strip() == net[1].strip():
            port =net[0]
            break
    return port




"""It is for end port .It gives the port of the load or source which is connected to the switch/ER"""
def port_no(ip):
    Local_load               = setting.common.Load_list
    Local_source             = setting.common.Source_list
    Switch_table             = setting.network_var.switch_table
    i=0
    j=0
    #print("We are in port__no")
    if Local_load:
        #print("We are in common load list",len(Local_load))
        while i < len(Local_load):
            if ip == Local_load[i].ip_address:
                  print("we are in for loop",Local_load[i].id)
                  print Switch_table
                  for net in Switch_table:
                      if net[0].strip() == ip.strip():
                          return net[1]
                  break
            i=i+1
    if Local_source:
        while j < len(Local_source):
            if ip == Local_source[i].ip_address:
                  print("we are in for loop",Local_source[i].id)
                  #print Switch_table
                  for net in Switch_table:
                      if net[0].strip() == ip.strip():
                          return net[1]
                  break
            j=j+1
            
    return 3

"""
To get the path information from the source port to the destination port.

"""

def path_info(packet):
    dst_port_from =packet[10]
    dst_port_to   =packet[11]
    hop_count     =packet[4]
    hop_max          =packet[3]
    temp_table    =[]
    i             =0
    while i <packet[4]:
        temp_table.append(packet[12+i])
        i =i+1
    temp_table.append([packet[6],packet[10],packet[11]])
    t1 = Table(rows =temp_table , names =('ip' ,'port_to','port_from'))
    return t1
    
 
    
""" To get the ip address of the previous hop from the pakcet. """
def packet_prev_ip(packet):

    a = packet[len(packet)-1]
    port_from = next_hop_port(a[0])
    return port_from



""" To send the Udp packet outfrom here"""    
def Udp_message(ip,packet,port_no):
    #print(packet)
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(packet,(ip,port_no))


def broadcast_receive():
    port =10100
    while True:
        try :
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.bind(('<broadcast>',port))
            break
        except socket.error as error:
            print("the socket error is",error)
    print("We are in broadcast receive  loop")
    while True:
        (buf,address)=s.recvfrom(1000)
        if buf:
            #print("buff ",buf)
            if address[0].strip() != IP_addr:
               # print("address",address[0])
                broadcast_packet_list.append(buf)
            
            
def broadcast_packet_queue():
    print("We are in broadcast packet queue")
    while True:
        sleep(0.4)
        if broadcast_packet_list:
            packet =broadcast_packet_list.pop()
            packet =pickle.loads(packet)
            if (packet[0]==1) and (packet[1] ==2):
                print("It is  a energy request packet")
                print packet[9]
                data = request_parse(packet[9])
                res =power_check()
                if data:
                    #pack = Energy_Packet()
                    pack =broadcast_energy_response(packet[2],data)
                    print("port",packet[5])
                    print("ip", packet [3])
                    result =unicast_message(ip=packet[3].strip() ,port_no =int(packet[5]),msg =pack)
                    if result:
                        print("--------------------  broadcast_packet_queue ->broadcat packet queue result-------------")
                        print(result)
                        response_packet_recv[packet[2]] = packet
                        print("------------- broadcast_packet_queue -> response_packet_recv[packet[2]]---------------")
                        print(packet[2])
                        print("------------- broadcast_packet_queue -> response_packet_recv---------------")
                        print(response_packet_recv)
                    print(result)
            elif  (packet[0] == 3 )and (packet[1] ==4):
                print("It is  a energy response packet")
                if packet[3] in broad_packet_send:
                    lst = broad_dict_packet_recv[packet[3]] 
                    lst.append(packet[9])
                    broad_dict_packet_recv[packet[3]] = lst


def response_parse(data):
    if data:
        f =open("broadcast_response.xml","w")
        message =data.encode('ASCII')
        f.write(message)
        f.close()
        ##if the file is not in correct format 
        try:
            doc= main.xml.dom.minidom.parse("broadcast_response.xml")
        except:

            print("The document file recived is not correct")
        os.remove("broadcast_response.xml")
        print(doc.nodeName)
        print(doc.firstChild.tagName)
        #get the list of html tag from document and print each one
        tag_name = doc.getElementsByTagName("Verb")
        tag_name =tag_name[0].firstChild.nodeValue.encode('utf-8')
        #print(type(tag_name))
        print(tag_name)
        if tag_name.strip() == 'Response':
                   print("It is  a response message")
                   volt = doc.getElementsByTagName("voltage")
                   volt = volt[0].firstChild.nodeValue.encode('utf-8')
                   volt = float(volt)
                   curr = doc.getElementsByTagName("current")
                   curr = curr[0].firstChild.nodeValue.encode('utf-8')
                   curr = float(curr)
                   ip = doc.getElementsByTagName("IP_address")
                   ip = ip[0].firstChild.nodeValue.encode('utf-8')
                   return ip ,curr
        else:
                    print "broadcast.py --->  response_parse"
                    return None, None
                    

def request_parse(data):
        f =open("broadcast_receive.xml","w")
        message =data.encode('ASCII')
        f.write(message)
        f.close()
        ##if the file is not in correct format 
        try:
            doc= main.xml.dom.minidom.parse("broadcast_receive.xml")
        except:
            print("The document file recived is not correct")
        os.remove("broadcast_receive.xml")
        print(doc.nodeName)
        print(doc.firstChild.tagName)
        #get the list of html tag from document and print each one
        tag_name = doc.getElementsByTagName("Verb")
        tag_name =tag_name[0].firstChild.nodeValue.encode('utf-8')
        #print(type(tag_name))
        print(tag_name)
        if tag_name.strip() == 'Request':
                   print("It is  a broadcast request")
                   verb = doc.getElementsByTagName("Noun")
                   verb = verb[0].firstChild.nodeValue.encode('utf-8')
                   if verb.strip() == 'Master':
                       arr = main.xml_process.Broadcast_req_parse(doc)
                       print("request_parse--->setting.common.current_avail",setting.common.current_avail)
                       print (" arr[3] {0} {1}".format(arr[3], type(arr[3])))
                       print("+++++++arr++++++++",arr)
                       print ("************setting.common.temp_current***********",setting.common.temp_current)
                       print ("************setting.common.current_avail***********",setting.common.current_avail)
                       if float(arr[3]) < (setting.common.current_avail -setting.common.temp_current):
                            broadcast_resp_queue.append(arr)
                            print arr
                            setting.common.temp_current = setting.common.temp_current + float(arr[3])
                            print ("************setting.common.temp_current***********",setting.common.temp_current)
                            #setting.common.current_avail =setting.common.current_avail - float(arr[3])
                            data = main.xml_write.create_xml_file_response(main.network.Self_Mac(),IP_addr,str(setting.common.current_avail),'12')
                            return data
                       else:
                            return False
                   else:
                           return None

def ack_parse(data):
        f =open("acknowledgment.xml","w")
        message =data.encode('ASCII')
        f.write(message)
        f.close()
        ##if the file is not in correct format 
        try:
            doc= main.xml.dom.minidom.parse("acknowledgment.xml")
        except:
            print("The document file recived is not correct")
        os.remove("acknowledgment.xml")
        print(doc.nodeName)
        print(doc.firstChild.tagName)
        #get the list of html tag from document and print each one
        tag_name = doc.getElementsByTagName("Verb")
        tag_name =tag_name[0].firstChild.nodeValue.encode('utf-8')
        #print(type(tag_name))
        print(tag_name)
        if tag_name.strip() == 'Acknowledgment':
                   print("It is  a acknowledgment message")
                   volt = doc.getElementsByTagName("voltage")
                   volt = volt[0].firstChild.nodeValue.encode('utf-8')
                   volt = float(volt)
                   curr = doc.getElementsByTagName("current")
                   curr = curr[0].firstChild.nodeValue.encode('utf-8')
                   curr = float(curr)
                   ip = doc.getElementsByTagName("IP_address")
                   ip = ip[0].firstChild.nodeValue.encode('utf-8')
                   ip_load =doc.getElementsByTagName("IP_address_load")
                   ip_load =ip_load[0].firstChild.nodeValue.encode('utf-8')
                   curr_req = doc.getElementsByTagName("current_enquire")
                   curr_req =curr_req[0].firstChild.nodeValue.encode('utf-8')
                   return ip,ip_load,volt,curr,curr_req
        else:
                    print "broadcast.py --->  response_parse"
                    return None, None,None,None
                    
"""def response_parse(data):
    if data:
        f =open("broadcast_response.xml","w")
        message =data.encode('ASCII')
        f.write(message)
        f.close()
        ##if the file is not in correct format 
        try:
            doc= main.xml.dom.minidom.parse("broadcast_response.xml")
        except:

            print("The document file recived is not correct")
        os.remove("broadcast_response.xml")
        print(doc.nodeName)
        print(doc.firstChild.tagName)
        #get the list of html tag from document and print each one
        tag_name = doc.getElementsByTagName("Verb")
        tag_name =tag_name[0].firstChild.nodeValue.encode('utf-8')
        #print(type(tag_name))
        print(tag_name)
        if tag_name.strip() == 'Response':
                   print("It is  a response message")
                   volt = doc.getElementsByTagName("voltage")
                   volt = volt[0].firstChild.nodeValue.encode('utf-8')
                   volt = float(volt)
                   curr = doc.getElementsByTagName("current")
                   curr = curr[0].firstChild.nodeValue.encode('utf-8')
                   curr = float(curr)
                   ip = doc.getElementsByTagName("IP_address")
                   ip = ip[0].firstChild.nodeValue.encode('utf-8')
                   return ip ,curr
        else:
                    print "broadcast.py --->  response_parse"
                    return None, None"""
            
    
    
    
    
    
    
def power_check():
    return True

def broadcast_send(msg):
    dest = ('<broadcast>',10100)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(msg, dest)
    print ("Looking for replies; press Ctrl-C to stop.")


""" Function for intializing broadcast request """    
def broadcast_energy_request(data):
    packet = Energy_Packet()
    curr_time = time()
    while True:
        packet_id       = random.randint(1,65792)
        if packet_id not in packet_send:
            break
        sleep(0.025)
    pack  = packet.energy_request_packet(packet_id =packet_id,port_no =9050 ,time = curr_time ,data =data)
    broadcast_send(pack)
    broad_packet_send.append(packet_id)
    print data
    print("------ broadcast_energy_request ->packet_id -----------")
    print(packet_id)
    flag_set ='flag_set'+str(packet_id)
    flag_set =threading.Thread(target =broadcast_timer ,args =(packet_id,data))
    flag_set.daemon =True
    flag_set.start()
    return pack


""" Function for intializing broadcast response """
def broadcast_energy_response(packet_resp_id,data):
    packet = Energy_Packet()
    curr_time = time()
    while True:
        packet_id       = random.randint(1,65792)
        if packet_id not in packet_send:
            break
        sleep(0.025)
    pack  = packet.energy_response_packet(packet_id =packet_id, packet_response_id =packet_resp_id , port_no =9050 ,time = curr_time ,data =data)
    packet_send.append(packet_id)
    flag_set ='flag_set'+str(packet_id)
    flag_set =threading.Thread(target =response_packet_timer ,args =(packet_resp_id,))
    flag_set.daemon =True
    flag_set.start()    
    return pack    

def broadcast_energy_confirm(packet_resp_id):
    packet = Energy_Packet()
    curr_time = time()
    data ="connect"
#    packet_id       = random.randint(1,65792)
    while True:
        packet_id       = random.randint(1,65792)
        if packet_id not in packet_send:
            break
        sleep(0.01)
    pack  = packet.energy_confirm_packet(packet_id =packet_id, packet_response_id =packet_resp_id , port_no =9050 ,time = curr_time ,data =data)
    return pack
  
def broadcast_request():
    data =main.xml_write.create_xml_broadcast_request('20:56:45:25:34:55','10.114.56.203','8.2' ,'12')
    broadcast_send(broadcast_energy_request(data))

def broadcast_response():
    broadcast_send(broadcast_energy_response())    

def unicast_confirm():
    broadcast_send(broadcast_energy_response())
    
def broadcast_timer(packet_id,data):
        print " BROADCAST TIMER THREAD STARTED"
        start_time                        = time()
        time_interval                     = 4
        recv_packet                       = []
        broad_dict_packet_recv[packet_id] = recv_packet 
        f =open("broadcast_timer.xml","w")
        message =data.encode('ASCII')
        f.write(message)
        f.close()
        ##if the file is not in correct format 
        try:
            doc= main.xml.dom.minidom.parse("broadcast_timer.xml")
        except:
            print("The document file recived is not correct")
        ip_load = doc.getElementsByTagName("IP_address_load")
        ip_load =ip_load[0].firstChild.nodeValue.encode('utf-8')
        current_enquire = doc.getElementsByTagName("current")
        current_enquire = current_enquire[0].firstChild.nodeValue.encode('utf-8')
        os.remove("broadcast_timer.xml")
        """ This is the waiting period of the timer"""
        """ ---------------------------------------"""
        while True:
            if (time()-start_time) < time_interval:
                    sleep(0.1)
            else:
                break
        """----------------------------------------"""
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ BROADCAST TIMEOUT  $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        broad_packet_send.remove(packet_id)
        received_packet = broad_dict_packet_recv.pop(packet_id)   # recv_packet is the list of recieved packet for the requested packet id
        print("-----------------------broadcast_timer->  broad_packet_send_list.-----------------------------------------------")
        print(broad_packet_send)
        print("-----------------------broadcast_timer->  recv_packet.-----------------------------------------------")
        print(received_packet)
        if received_packet :
            
          """ Do some electrical processing and select 1 address """
          while True:
            pack_id       = random.randint(1,65792)
            if pack_id not in packet_send:
                break
            sleep(0.01)
          pack = Energy_Packet()
          lst =[]
          current_avail =0.0
          if received_packet:
            for recv_packet in received_packet:
                data  =       recv_packet[10]
                entry =       response_parse(data)
                current_avail  = entry[1] + current_avail
                lst.append(entry)
          current_req   = float(current_enquire)/len(received_packet)
          print("********* broadcast_timer -- > current_req*********",current_req)
          #current_req   = 0.4/len(received_packet)
          for recv_packet in received_packet:  
            print("*********************This recv_packet**********************************************")
            print(recv_packet)
            print("*********************recv_packet[0][3]*********************************************")
            print(recv_packet[3])# this is the packet id 
            tm = time()
            msg =main.xml_write.create_xml_broadcast_confirm(main.network.Self_Mac(),IP_addr,ip_load,str(current_req),current_enquire ,'10')
            #packet = pack.energy_confirm_packet(packet_id = pack_id , packet_response_id =recv_packet[3] ,port_no =9050 ,data ='confirm',time =tm)
            packet = pack.energy_confirm_packet(packet_id = pack_id , packet_response_id =recv_packet[3] ,port_no =9050 ,data = msg,time =tm)
            print("********************recevied packet************************************************")
            print(recv_packet[4])
            print("Port No -> ",int(recv_packet[6]))
            ret = unicast_message(ip =recv_packet[4].strip() , port_no = int(recv_packet[6]) ,msg =packet)
            setting.common.ack_send[recv_packet[4].strip()]=msg
            if ret:
                print("confrimation packet is send to ip {0} port {1} ")
        else:
            print("NO response for broadcast")
            setting.common.broadcast_flag =0 
        sys.exit()
        
        
def response_packet_timer(packet_id):
    start_time =time()
    time_interval =10    
    while True:
        if (time () -start_time) <time_interval:
                
            if packet_id in confirm_packet_recv:
                pack = response_packet_recv.pop(packet_id)
                print(pack)
                p    = confirm_packet_recv.pop()
                packet = confirm_packet_received[packet_id]
                print "____________________received packet ______________________________________"
                print packet[10]
                dst_ip,ip_load,volt,curr,curr_req = ack_parse(packet[10])
                setting.common.temp_current = setting.common.temp_current - float(curr_req) + float(curr)
                print("-------------response packet timer -> setting.common.temp_current ---------------",setting.common.temp_current)
                print("_____dst_ip,ip_load,volt,curr____{0} {1} {2} {3}".format(dst_ip,ip_load,volt,curr))
                print("-------------response packet timer -> response_packet_recv ---------------")
                print(response_packet_recv)
                print("--------------response packet timer -> confirm_packet_recv ")
                if setting.common.Source_list:
                    ip_source =setting.common.Source_list[0].ip_address
                    op =traceroute(ip_source,ip_load,dst_ip)
                    if op != False:
                        setting.common.traceroute_send[ip_load]=op 
                        print("___op___",op)
                        #print("___op[12]___",op[12])
                        a = len(op)-12
                        #print ("-------a--------",a)
                        print (op[8])
                        port =int(op[8])
                        ip   =op[6]
                        #print("ip",op[6])
                        current= curr
                        voltage= volt
                        external_load_list.append([port,ip,current,voltage])
                        #print("external_load_list",external_load_list)
                        load = main.load_param()
                        load.port = str(port)
                        load.ip_address = ip
                        load.voltage =12.0
                        load.state = 1
                        load.current_reqd =float(current)
                        setting.common.lock.acquire()
                        print ("|||||||___load__||||||||",vars(load))
                        setting.common.Load_list.append(load)
                        setting.common.extern_Load_list.append(load)
                        setting.common.comm_to_power_change_event.set()
                        setting.common.temp_current = setting.common.temp_current - float(curr)
                        #print("-------------response packet timer -> setting.common.temp_current after load appending ---------------",setting.common.temp_current)
                        setting.common.lock.release()
                        i=0
                        while (i < a):
                            data = op[12+i]
                            print("data",data)
                            if i ==0:
                                ip_from =str(op[5])
                            else:   
                                ip_from = op[12+(i-1)]
                                ip_from = ip_from[0]
                            if (i+12) == (len(op)-1):
                                ip_to =str(op[7])
                            else:
                                ip_to =op[12+i+1]
                                ip_to =ip_to[0]
                            print ("port_to,port_from {0} {1}".format(str(data[2]),str(data[1])))
                            msg = main.xml_write.create_xml_ER_ER_connect(data[0],ip_to,ip_from,str(data[2]),str(data[1]),str(current),str(current),'10.0','10.0')
                            print msg
                            unicast_message(data[0],8000 ,msg)
                            i=i+1
                        print (" load port_to,port_from {0} {1}".format(str(op[11]),str(op[10])))
                        msg =main.xml_write.create_xml_ER_ER_connect(str(op[7]),str(op[6]),data[0],str(op[11]),str(op[10]),str(current),str(current),str(voltage),'10.0')
                        print msg
                        unicast_message(op[7],8000 ,msg)
                        break
            else:
                sleep(0.2)
            
        else:
             print"_______________________________TIMER EXPIRED __________________________________"
             print("packet_id",packet_id)
             pack = response_packet_recv.pop(packet_id)
             #packet_send.remove(packet_id)
             print("---------------------------response_packet_timer -> response_packet_recv--------------------------- ")
             print(response_packet_recv)
             break
   
    sys.exit()


"""def disconnect_path(path,data):
    print "**********path**********"
    print path
    op=path
    a = len(op)-12
    #print ("-------a--------",a)
    dst_ip,ip_load,voltage,current,curr_req = ack_parse(data)
    #print("_____dst_ip,ip_load,volt,curr____{0} {1} {2} {3}".format(dst_ip,ip_load,voltage,current))
    i=0
    while (i < a):
            data = op[len(op)-(i+1)]
            print("data",data)
            if i == 0:
                ip_to =op[7]
                ip_from = data[0]
            else:
                ip_to   = op[len(op)-(i)]
                ip_to   = ip_to[0]
            if (len(op) -13 ==i):
                ip_from = op[5]
            else:     
                    ip_from = op[len(op)-(i+2)]
                    ip_from = ip_from[0]
            msg = main.xml_write.create_xml_ER_ER_disconnect(data[0],ip_to,ip_from,str(data[2]),str(data[1]),str(current),str(current),'15.0','15.0')
            unicast_message(data[0],8000 ,msg)
            i=i+1
    ip_from = op[6]
    ip_to   = op[len(op)-(i)]
    ip_to   = ip_to[0]
    #print("ip_to" ,ip_to)
    #print("!!!!!!op[5]!!!!!!!!",op[5])
    #print("!!!!!!op[6]!!!!!!!!",op[6])
    msg = main.xml_write.create_xml_ER_ER_disconnect(op[5],op[6],ip_from,str(data[2]),str(data[1]),str(current),str(current),str(voltage),str(voltage))
    unicast_message(op[5],8000 ,msg)"""


def disconnect_path_source(path,data):
    print "**********path**********"
    print path
    op=path
    a = len(op)-12
    print ("-------a--------",a)
    dst_ip,ip_load,voltage,current,curr_req = ack_parse(data)
    print("_____ip_load,volt,curr____{0} {1} {2}".format(ip_load,voltage,current))
    i=0
    while (i < a):
            data = op[len(op)-(i+1)]
            print("data",data)
            if i == 0:
                ip_to =op[7]
                ip_from = data[0]
            else:
                ip_to   = op[len(op)-(i)]
                ip_to   = ip_to[0]
            if (len(op) -13 ==i):
                ip_from = op[5]
            else:     
                    ip_from = op[len(op)-(i+2)]
                    ip_from = ip_from[0]
            msg = main.xml_write.create_xml_ER_ER_disconnect(data[0],ip_to,ip_from,str(data[2]),str(data[1]),str(current),str(current),str(voltage),str(voltage))
            unicast_message(data[0],8000 ,msg)
            i=i+1
    ip_from = op[6]
    ip_to   = op[len(op)-(i)]
    ip_to   = ip_to[0]
    print("ip_to" ,ip_to) 
    msg = main.xml_write.create_xml_ER_ER_disconnect(op[5],ip_from,ip_to,str(data[2]),str(data[1]),str(current),str(current),str(voltage),str(voltage))
    print msg
    unicast_message(op[5],8000 ,msg)

def disconnect_path_load(path,data):
    print "**********path**********"
    print path
    op=path
    print "**********data**********"
    print data
    ip_load =data[0]
    voltage =data[1]
    current =data[2]
    a = len(op)-12
    i=0
    while (i < a):
            data = op[12+i]
            print("data",data)
            if i ==0:
                ip_from =str(op[5])
            else:
                ip_from = op[12+(i-1)]
                ip_from = ip_from[0]
            if (i+12) == (len(op)-1):
                ip_to =str(op[7])
            else:
                ip_to =op[12+i+1]
                ip_to =ip_to[0]
            msg = main.xml_write.create_xml_ER_ER_disconnect(data[0],ip_to,ip_from,str(data[2]),str(data[1]),str(current),str(current),str(voltage),str(voltage))
            print msg
            unicast_message(data[0],8000 ,msg)
            i=i+1
    msg =main.xml_write.create_xml_ER_ER_disconnect(str(op[7]),str(op[6]),data[0],str(op[11]),str(op[10]),str(current),str(current),str(voltage),str(voltage))
    unicast_message(op[7],8000 ,msg)

def broadcast_conf():
        t1 = threading.Timer(0.5,traceroute_recive)
        t2 =threading.Timer(0.5,packet_fwd)
	t3 =threading.Timer(0.5,traceroute_file_update)
        t4 = threading.Timer(0.5,broadcast_receive)
        t5 = threading.Timer(0.5,broadcast_packet_queue)
        t6 = threading.Timer(0.5,router_to_router_server)
        t7 = threading.Timer(0.5,queue_power_conn)
        t1.daemon= True
        t2.daemon= True
	t3.daemon= True
        t4.daemon =True
        t5.daemon=True
        t6.daemon=True
        t7.daemon=True
        t1.start()
        t2.start()
	t3.start()
        t4.start()
        t5.start()
        t6.start()
        t7.start()
        print("We are in braodcast file")
        while True:
                pass
                sleep(10)

""" Upadtes the net hop list from traceroute_log """
def traceroute_file_update():
	file = open('traceroute_log.txt','r')
	port_number =[]
	while True:
		for line in file :
			fields= line.strip().split()
			next_hop_list.append((fields[0],fields[1]))
		#print (next_hop_list)
		sleep(30)

if __name__=='__main__':
    #traceroute_file_update()
    t1 =threading.Timer(0.5,traceroute_recive)
    t2 =threading.Timer(0.5,packet_fwd)
    t3 =threading.Timer(0.5,traceroute_file_update)	
    t4 = threading.Timer(0.5,broadcast_receive)
    t5 = threading.Timer(0.5,broadcast_packet_queue)
    t6 = threading.Timer(0.5,router_to_router_server)
    t7 = threading.Timer(0.5,queue_power_conn)
    t1.daemon= True
    t2.daemon= True
    t3.daemon= True
    t4.daemon= True
    t5.daemon= True
    t6.daemon= True
    t7.daemon= True
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    while True:
            message = sys.stdin.readline()
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            if message.strip() =="traceroute_path":
                print("traceroute_path")
                traceroute('192.168.0.103','192.168.0.103','192.168.0.103')
            if message.strip() =="broadcast":
                print("Broadcast send")
                broadcast_request()
            sys.stdout.flush()

