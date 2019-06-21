import socket
import sys
sys.path.append('/home/pi/Documents/udit/Energy_Router/main_codes/comm')
import os
import struct
import pickle
import xml.dom.minidom
from threading import Timer ,Event
import threading
from socket import error as socket_error
from time import sleep
try:
    from  XML import xml_process ,xml_write
except:
    print("Not able to import xml file")



multicast_port  = 10000
multicast_group = '230.50.10.7' 
ip_address=[]
mac=[]
udp_port_receive = 9000
IPAddr = '192.168.0.200'


def udp_send(packet,IP,port):
    sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(packet,(IP,port))
    
def udp_listen_port():
    sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((IPAddr, udp_port_receive))
    print("we are in listen port")
    while True:
        data, addr =sock.recvfrom(1024)
        if data:
            data = pickle.loads(data)
            data_process(data)
            
def data_process(data):
    data_proc =[]
    data_proc =list(data)
    #my_list   =[]
    if data[0] == 0:
                udp_send('not reachable',data[1],9000)
    else:
                data_proc[0] =data_proc[0]-1
                print data_proc[0]
                data_proc.append('10')
                print data_proc



def multicast_listen():
    global event
    multicast_server=('',multicast_port)
    sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(multicast_server)
    group =socket.inet_aton(multicast_group)
    mreq  = struct.pack('4sL',group,socket.INADDR_ANY)
    #sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP)
    sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,mreq)
    while True:
		data , address = sock.recvfrom(1024)
		if data:
                 try:
                     master_query ='master_query'+address[0]+'.xml'
                     f = open(master_query,"w")
                     data =data.decode('ASCII')
                     f.write(data)
                     f.close()
                 except:
                        print("Master queret file is not created")
                 try:
                     doc= xml.dom.minidom.parse(master_query)
                     tag_name = doc.getElementsByTagName("Verb")
                     tag_name =tag_name[0].firstChild.nodeValue.encode('utf-8')
                     if tag_name.strip() == 'query':
                         noun = doc.getElementsByTagName("Noun")
                         noun = noun[0].firstChild.nodeValue.encode('utf-8')
                         if noun.strip() == 'Master':
                             try:
                                 arr = xml_process.master_query_parse(doc)
                                 try:
                                     event.set()
                                     ip_address.append(arr[1])
                                     mac.append(arr[0])
#                                     print(ip_address)
#                                     print(mac)
                                 except:
                                      print("this is an event error")

                             except:
                                print('This is xml error')
                 except:
                     print("The document file recived is not correct")
#                os.remove(master_query)
def multicast_send(message):
    multicast_send = (multicast_group, multicast_port)
    sock_send      = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    ttl            = struct.pack('b',1)
    sock_send.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,ttl)
    sock_send.sendto(message,multicast_send)
    sock_send.close()



def multicast_reponse():
    while True:
#       event.wait()
#        while event.is_set():
            if ip_address:
                for i in ip_address:
                     xml_write.create_xml_multicast_response('multicast_response.xml','10:16:56:23:15:48:45',i)
                     sock_response          = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                     with open("multicast_response.xml","r") as f:
                         message=f.read()
                         print(message)
                     print(i)
                     sock_response.sendto(message,('192.168.0.100',udp_port_receive))
                     sock_response.close()
                     os.remove("multicast_response.xml")
                     ip_address.remove(i)
#            event.clear()

def traceroute_path(packet,ip):
    sock =socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(packet,(ip,5000))


def trace_receive():
    sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((IPAddr,5000))    
    while True:
        data ,address = sock.recvfrom()
        if data:
            data 
        
def multicast_test():
        sock =socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = 'hello'
        try:
            sock.sendto(message.encode('ASCII'),('192.168.0.102',9000))
        except socket_error as err:
            print(err)
            
        
def multicast_start():
      global event
      event = Event()
      t1 = Timer(0.2,multicast_listen,args=[])
      t2 = threading.Thread(target = multicast_reponse,args=[])
      t3 = Timer(0.2,udp_listen_port,args=[])
      t1.daemon =True
      t2.daemon =True
      t3.daemon =True
      t1.start()
      t2.start()
      t3.start()
      
if __name__ =='__main__':
       ip_address.append('192.168.0.102')
       multicast_start()
       #multicast_reponse()
       while True:
           pass
           sleep(10)
