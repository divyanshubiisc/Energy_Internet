# -*- coding: utf-8 -*-


import socket
import select
import sys
import threading
import os
import subprocess
import netifaces as ni   # to get a interface ip address
import random            # to produce random number for a file
import xml.dom.minidom   # used for file parsing
from collections import namedtuple #used for making structure 
import time
import errno
from socket import error as socket_error

server =None
ip_addr_master=None
ip_addr=None
id_no = 1024


def ip_address():
    global ip_addr
    process = subprocess.Popen("ifconfig | grep eth0 | awk '{print $1}'", shell =True, stdout =subprocess.PIPE)
    try:
        outs, errs = process.communicate()
        print (outs)
    except:
        process.kill()
        outs, errs = process.communicate()
        print(errs)
        sys.exit()
    
    while True:
        try:
            ni.ifaddresses(str(outs.strip()))
            ip_addr = ni.ifaddresses(str(outs.strip()))[ni.AF_INET][0]['addr']
            break
        except:
            print("not connected to the lan")
        
def create_server():
    global server
    global ip_addr
    port_no_listen = 8050 
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    while True:
        try:
            server.bind((ip_addr,int(port_no_listen))) ## create a server for listening poll reqeust from the server
            server.listen(100)
            break
        except socket_error as serr:
            print("Error in create_server part of the code")
            print(serr) 
# Set the name of the XML file.
xml_file = "try1.xml"

headers = {'Content-Type':'text/xml'}



# Open the XML file.
#with open(xml_file) as xml:
    # Give the object representing the XML file to requests.post.
    #r = requests.post('172.18.0.8', data=xml)

#print (r.content);

def start_conn():
    global ip_addr_master
    global server
    global id_no
    while True:
        conn, addr = server.accept()
        print("conn recived{}".format(conn))
        message = conn.recv(4096)
        if message:
               f =open("recive_file.xml","w")      ### recive_file.xml to store the message of head node
               message =message.decode('ASCII')
               f.write(message)
               f.close()
               print(message)
               try:
                   doc = xml.dom.minidom.parse("recive_file.xml")
               except:
                   print("The document file recived is not correct")
               #tag_name = doc.getElementsByTagName("Verb")
               verb = doc.getElementsByTagName("Verb")
               verb = verb[0].firstChild.nodeValue.encode('utf-8')
               if verb.strip() == 'poll':
                   id = doc.getElementsByTagName("id")
                   id = id[0].firstChild.nodeValue.encode('utf-8')
                   print  ("we are inside poll")
                   if int(id.strip()) == id_no:
                       print("Load ID number is same")
                       try:
                               s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                               
                               print("socket is created")
                               if ip_addr_master is not None:
                                   s.connect((ip_addr_master,8010)) # this corresponds to poll_read socket in receive_xml.py file
                               else:
                                   print ("master ip address not present")
                               with open("get.xml","r") as f:  ##get.xml contains poll response
                                   data= f.read()
                                   s.send(data.encode('ASCII'))
                                   s.close()
                                   print("File transfer Completed")
                       except socket_error as serr:
                           print("There is a socket error {}".format(serr))
               elif verb.strip() == 'connect':
                     router_id =doc.getElementsByTagName("Router_id")
                     router_id =router_id[0].firstChild.nodeValue.encode('utf-8')
                     ip_addr_master   =doc.getElementsByTagName("IP_address")
                     ip_addr_master   =ip_addr_master[0].firstChild.nodeValue.encode('utf-8')
                     try:
                         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                         s.connect((ip_addr.strip(),8000))
                         #command = '<xml version="1.0" encoding="UTF-8"><header/><body><code><body/>'
                         #command1 = 'the day was good'
                         with open("try1.xml","r") as f:
                             data= f.read()
                             s.send(data.encode('ASCII'))
                             s.close()
                             print("file  transfer ends here")
                     except:
                             print ("Not able to send the initial file")
    server.close()                       
                   
if __name__ == "__main__":
    

    global ip_addr
    global server
    ip_address()
    create_server()
    t1 = threading.Thread(target =start_conn(), args=())
    t1.start()
    while True:
        try:
            process = subprocess.Popen("ifconfig | grep eth0 | awk '{print $1}'", shell =True, stdout =subprocess.PIPE)
        except:
            if ip_addr !=None:
                server.close()
                ip_addr =None
                ip_address()
                create_server()
