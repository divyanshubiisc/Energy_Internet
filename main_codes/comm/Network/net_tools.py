# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 15:59:05 2019

@author: ud
"""

import subprocess
import re
import os
import time
import fcntl
def netmask_value(netmask):
    if netmask == "255.255.255.255":
        return 32
    elif netmask =="255.255.255.0":
        return 24
    elif netmask =="255.255.0.0":
        return 16
    elif netmask == "255.0.0.0":
        return 8
    else:
        return 0

def initial_conf():
    process_ip_address = subprocess.Popen("ifconfig |grep \"inet\"|awk  'NR==1{print $2}' ", shell =True, stdout =subprocess.PIPE)
    try:
        outs, errs = process_ip_address.communicate()
        #ip_address,netmask =outs.split(':')
        ip_address=outs.strip()
        #netmask = netmask.strip()
        #print (ip_address.strip())
        #print(netmask.strip())
        #netmask =netmask_value(netmask.strip())
        #print (str(netmask)+"--netmask")
    except:
            process_ip_address.kill()
            outs, errs = process_ip_address.communicate()
            print(errs)
            
            
    process_net_mask = subprocess.Popen("ifconfig |grep \"inet\"|awk  'NR==1{print $4}' ", shell =True, stdout =subprocess.PIPE)
    try:
        outs, errs = process_net_mask.communicate()
        #ip_address,netmask =outs.split(':')
        netmask=outs.strip()
        #netmask = netmask.strip()
        #print (ip_address.strip())
        #print(netmask.strip())
        #netmask =netmask_value(netmask.strip())
        #print (str(netmask)+"--netmask")
    except:
            process_net_mask.kill()
            outs, errs = process_net_mask.communicate()
            print(errs)
    return ip_address,netmask
    
def nmap(ip_address,netmask):
    process_nmap = subprocess.Popen("nmap"+"\t"+ "-sP"+ "\t" +ip_address+"/"+str(netmask), shell =True, stdout =subprocess.PIPE)
    try:
        outs, errs = process_nmap.communicate()
        #print ("Nmap Process Completed")
    except:
            process_nmap.kill()
            outs, errs = process_nmap.communicate()
            print(errs)


""" to give ip address from mac address  """       
"""def Arp(mac_address):
    print "ip_address to mac address in ARP scan in net_tools.py time calc."
    t1 = time.time()
    process_arp_n = subprocess.Popen("cat localnet|grep " +mac_address+"|awk '{print $1}'", shell =True, stdout =subprocess.PIPE)
    print time.time() - t1
    try:

        outs,errs =process_arp_n.communicate()
        return outs.strip()
    except:
        process_arp_n.kill()
        outs, errs = process_arp_n.communicate()
        print(errs)"""
        
        
def Arp(mac_address):
    while True:
        try:
            with open("/home/pi/Desktop/PC_ER/ER/Energy_Router/main_codes/comm/Network/localnet_1.txt","r") as f:
                fcntl.flock(f,fcntl.LOCK_EX) ## lock  the file
                data =f.read()
                fcntl.flock(f,fcntl.LOCK_UN) ## unlock  the file
                f.close()
            if data:
                    break
        except:
            pass
        time.sleep(0.01)
    #print data
    msg = re.findall("^.*"+mac_address,data,re.MULTILINE)
    #print msg
    if msg:
        for p in msg:
            part = p.split('\t')
        return part[0]
        #print type(part[0])
    else:
        return None
        
"""to give mac address from a ip addresss"""
def Mac(ip):
    with open("/home/pi/Desktop/PC_ER/ER/Energy_Router/main_codes/comm/Network/localnet_1.txt","r") as f:
        fcntl.flock(f,fcntl.LOCK_EX) ## lock  the file
        data = f.read()
        fcntl.flock(f,fcntl.LOCK_UN) ## unlock  the file
        f.close()
    msg =re.findall(ip+'.*$',data,re.MULTILINE)
    if msg:
        return None
        a=[]
        a=msg[0]
        #print(a)
        a =a.split('\t')
        #print a
        #print(a[1])
        return None
    else:
        return None



def ARP_scan():
    file_exists = os.path.isfile('localnet')
    if file_exists:
        os.remove('localnet')
    else:
        pass
    #print("process_arp_scan enter")
    process_arp_scan =subprocess.Popen("sudo arp-scan --localnet >> localnet", shell =True, stdout =subprocess.PIPE)  
    #print("process_arp_scan exit")
    try:
        outs,errs =process_arp_scan.communicate()   
        print("outs process")
        with open("/home/pi/Desktop/PC_ER/ER/Energy_Router/main_codes/comm/Network/localnet","r") as f:
            data =f.read()
            f.close()
        #print(data)
        with open("/home/pi/Desktop/PC_ER/ER/Energy_Router/main_codes/comm/Network/localnet.txt","w") as f:
            fcntl.flock(f,fcntl.LOCK_EX) ## lock  the file
            f.write(data)
            fcntl.flock(f,fcntl.LOCK_UN) ## unlock  the file
            f.close()
        return outs.strip()
    except:
        process_arp_scan.kill()
        outs, errs = process_arp_scan.communicate()
        print(errs) 

def ip_to_mac(ip):
    process_ip_mac = subprocess.Popen("arping -I   eth0 -c 1 "+ip, shell =True, stdout =subprocess.PIPE)
    try:
        outs,errs =process_ip_mac.communicate()
        if "Unicast reply" in outs:
            out       = outs.split('[')
            outs      = out[1].split(']')
            outs      = outs[0]
            return outs.strip()
        else:
            return None
        
    except:
        process_ip_mac.kill()
        outs, errs = process_ip_mac.communicate()
        print(errs) 
        return None
            
def Self_Mac():
    process_self_mac =subprocess.Popen("ifconfig eth0 |grep ether | awk 'NR==1{print $2}'", shell =True, stdout =subprocess.PIPE)  
    try:
        outs,errs =process_self_mac.communicate()
        #print("Mac address obtained")
        outs=outs.strip()
        return outs
    except:
        process_self_mac.kill()
        outs, errs = process_self_mac.communicate()
        print(errs) 
        
        
        
if __name__ =="__main__":
    #p1,p2 = initial_conf()
    #print(p1)
    #print(p2)
    #mac = ip_to_mac('192.168.0.103')
    #print(mac)
    #ARP_scan()
    mac =Mac('192.168.0.151')
    print(mac)
    #a =Arp('b8:27:eb:0f:01:0e')
    #print a
    '''
    while True:
        ARP_scan()
        time.sleep(0.1)'''
