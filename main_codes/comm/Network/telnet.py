# -*- coding: utf-8 -*-
"""		
Created on Fri Jan 11 15:32:30 2019

@author: ud
"""

# -*- coding: utf-8 -*-


import sys
import telnetlib
import re
from collections import namedtuple #used for making structure 
#from astropy.table import Table
import threading
import net_tools as network
import time
import os
import fcntl                          # to loack the file while writing

"""
Get the mac addresses of all the hosts connected to the switch and match with the mac table present in the main server. 
1) Get the mac address and ip address of the system 
2) Do the arp pingg in order to fill the mac table with all the ip addresses connected to the router
3) Match the ip addresses with the MAC address presented in the switch  and table of table of it .This is done so that ip address can be mapped to a physical port of a switch.
4) Keep updating the table of mac addresses and ip table so that if any port is removed or connected can be captured.
net_tools python file is created to use some of the network tools in the code
"""
def telnet_update(Host,admin,ip_addr):  # ip_addr is for getting the own ip address, admin is the user_name password ,initial_msg to check with the message with the previous one
        Mac_Table=  []  #Mac table for storing the value of mac address and it's corresponding
        Mac      =  namedtuple("Mac_Table" , "mac port_no ip_address") # required attibute for the mac table of the switch
        port     =  []
        dup_port =  []
	t1 = time.time()
	while True:
	    try:
		with open ("telnet.txt","r") as f: #open file with f only other wise it qill not work properly
		    fcntl.flock(f,fcntl.LOCK_EX) ## lock  the file
		    data     =f.read()
		    fcntl.flock(f,fcntl.LOCK_UN) ##unlock the file 
		    f.close()
		    if data == "":
			continue
		    else:
			break
	    except:
		time.sleep(0.01)
	t2 = time.time()
	#print ("open telnet.txt",t2-t1)
	#print data
        msg = re.findall("^.*Learnt.*$",data,re.MULTILINE)
        #print(msg)
        #print("Mac Table getting updated ........")
        #network.ARP_scan()
	print("Network arp scan done")
        for p in msg:
            #p=str(p)
            p=str(p)
            for part in p.split():
                if "Gi0/" in part:
                    part = part.split('/')
                    b    = part[1]
                    print('b',b)
                print ("part",part)
                if  ":"  in part:
                    a    = part
                    print ("part a",a)
            if a.strip() == network.Self_Mac(): # to get the self mac address and ip address as it is not avialable in arp table
               mac_entry = Mac(mac =a.strip() ,port_no =int(b.strip()),ip_address=ip_addr.strip())
               if int(b.strip()) in port:
                   if int(b.strip()) not in dup_port:
				   dup_port.append(int(b.strip()))
               port.append(int(b.strip()))
            elif a.strip() == 'ac:84:c6:1f:3e:0d':
               continue
            else:   
               try:
		  #print "Arp loop"
		  #t1=time.time()
                  ip_entry =network.Arp(a.strip())
		  if ip_entry:
		      ip_entry =ip_entry.strip()
		  #print "After ARP LOOP"
		  #print time.time() - t1
		  """if '\n' in ip_entry:
		      ip = ip_entry.split('\n')
		      ip_entry =ip[0]"""
               except:
                  ip_entry = None
                  print("IP not avialable")
	       #print a.strip()
	       #print int(b.strip())
	       #print ip_entry
               mac_entry = Mac(mac =a.strip() ,port_no =int(b.strip()),ip_address=ip_entry)
               if int(b.strip()) in port:
                           if int(b.strip()) not in dup_port:
                               dup_port.append(int(b.strip()))
               port.append(int(b.strip()))
            Mac_Table.append(mac_entry)
	print("Mac Table is updated-----------------")
        
	""" try to write in the file every 10 msec and when writing is done it comes out of loop ."""
	while True:
		try:
		    #print "Inside while True statement for telnet.py file"
		    t1 = time.time()
		    with open("Net_Table.txt","w") as f:
			fcntl.flock(f,fcntl.LOCK_EX) ## lock  the file
			for items in Mac_Table:
			    items =str(items)
			    f.write(items)
			    f.write('\n')
			f.writelines(["dup_port %s\n" %item for item in dup_port])
			fcntl.flock(f,fcntl.LOCK_UN) ##unlock the file 
			f.close()
			break
		    print time.time() - t1
		except:
		    time.sleep(0.01)
	    #print "After while loop after file writing"
	#print("Mac Table is updated")  
        return Mac_Table,dup_port

if __name__ == '__main__':   
    admin ="admin"  # user name of switch
    Host = "192.168.0.50" #ip address of the switch 
    ip_addr="192.168.0.106"
    t1= threading.Thread(target = network.ARP_scan ,args =[])
    t1.daemon =True
    t1.start()
    while True:
    	mac_table , port = telnet_update(Host,admin,ip_addr)  #to get the mac addresses of all the loads connected to switch
	print(mac_table)
	if mac_table: 
    		#t1 = Table(rows = mac_table,names=('port' ,'mac','ip'))
   		print(t1)
    	#print(mac_table)
    	print(port)
	time.sleep(1)
