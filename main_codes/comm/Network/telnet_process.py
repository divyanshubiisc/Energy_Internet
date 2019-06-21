import sys
import telnetlib
import re
from collections import namedtuple #used for making structure 
from astropy.table import Table
import threading
import net_tools as network
import time
import os
import fcntl

def process():
	Host ='192.168.0.40'
	admin ='admin'
        f =open("/home/pi/Desktop/PC_ER/ER/Energy_Router/main_codes/comm/Network/telnet.txt","w+")
        f.write("")
        f.close()
	t1 = time.time()
	print("This is telnet update file")
        try:
            tn= telnetlib.Telnet(Host,23,3)
	    tn.open(Host)
            tn.write(admin+"\n")
	    #print"tn.admin"
	    try:
		tn.read_until("Password:")
		tn.write("admin"+"\n")
		tn.read_until("DGS-1210-10P> ")
		#print"tn.read_until"
		try:
		    t2 = time.time()
		    print ("Before debug info",t2-t1)
		    tn.write("debug info" + "\n")
		    #print"tn.write"
		    while True:
			try:
			    f =open("/home/pi/Desktop/PC_ER/ER/Energy_Router/main_codes/comm/Network/telnet.txt" ,"a")
			    fcntl.lockf(f,fcntl.LOCK_EX) ## lock  the file 
			    while True:
				r = tn.read_until("DGS-1210-10P> ",timeout =.2)
				#print(r.strip())
				if r.strip() =='':
				    break
				f.write(r)
				tn.write(" ")
			    fcntl.flock(f,fcntl.LOCK_UN) ##unlock the file 
			    f.close()
			    break
			except:
				time.sleep(0.02)
		    t3 = time.time()
		    print("After debug info",t3 -t2)
		except:
			try:
			    x = tn.read_until("DGS-1210-10P> ")
			except:
			    print("Not able to get debug info")
	    except:
		print("Login or password error")
        except:
            print("Not able to login into telnet host")

def start():
	while True:
	    process()
	    """while True:
		try:
		    network.ARP_scan()
		    print "ARP Scan done"
		    break
		except:
		    pass
		time.sleep(0.25)"""
	    time.sleep(3)

	 
if __name__== '__main__':
	start()
