# -*- coding: utf-8 -*-

#import socket
#import select
import sys
import string
from main_codes.comm import main
from main_codes.gui import table_gui
from main_codes.gui import gui_try2 as gui
#sys.path.append('/home/pi/Desktop/i2c_pi/Energy_Router/')
from global_var import setting
from Tkinter import *
from apscheduler.schedulers.background import BackgroundScheduler
import broadcast
import pandas as pd
import csv
process = main.subprocess.Popen("ifconfig | grep eth0 | awk '{print $1}'", shell =True, stdout =main.subprocess.PIPE)
try:
    outs, errs = process.communicate()
    print (outs)
except:
    process.kill()
    outs, errs = process.communicate()
    print(errs)
    main.sys.exit()
main.ni.ifaddresses('eth0') 

"""For poll debuging """
if sys.argv[1] == "debug":
    poll_debug =False
else:
    poll_debug =True
    


initial_config_a= 'send_initial_config'
k= str(main.random.randint(1,1000))   
csv='.csv'
initial_config= initial_config_a+k+csv


poll_period_a= 'poll_period'
k= str(main.random.randint(1,1000))   
csv='.csv'
poll_period= poll_period_a+k+csv



initial_config_poll= 'send_initial_config_poll'
k= str(main.random.randint(1,1000))   
csv='.csv'
initial_config_period=initial_config_poll+k+csv

broadcast_time = "broadcast_time"
k= str(main.random.randint(1,1000))
csv='.csv'
broadcast_time_file = broadcast_time+k+csv

t_broadcast_send     = main.time.time()
t_broadcast_receive  = main.time.time()

while True:
    try:
        IPAddr = main.ni.ifaddresses('eth0')[main.ni.AF_INET][0]['addr']
        ip  =IPAddr
        setting.common.ip_address =ip
        setting.network_var.self_ip = IPAddr
        break
    except:
        print("Interface doesnot have a  ip address")
    

print("Your Computer IP Address is:" + IPAddr) 
   


#sock_poll = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
poll_portno =8050       # port number for which it will sending poll request to load


while True:
	try:
		pollread_portno =8010  # port number for which poll file will be received by the server
		poll_read = main.socket.socket(main.socket.AF_INET,main.socket.SOCK_STREAM)
		poll_read.setsockopt(main.socket.SOL_SOCKET, main.socket.SO_REUSEADDR, 1)
		poll_read.bind((ip,int(pollread_portno)))
		poll_read.listen(1)
		print("Binding  completed port number 8010")
		break
	except main.socket_error as serr:
		print("Socket server not created port number 8010")
		print (serr)


while True:
	try:
		pollsend_portno =8050  # port number for which poll file will be received by the server
		poll_read_portno = main.socket.socket(main.socket.AF_INET,main.socket.SOCK_STREAM)
		poll_read_portno.setsockopt(main.socket.SOL_SOCKET, main.socket.SO_REUSEADDR, 1)
		poll_read_portno.bind((ip,int(pollsend_portno)))
		poll_read_portno.listen(100)
		print("Binding  completed port number 8050")
		break
	except main.socket_error as serr:
		print("Socket server not created port number 8010")
		print (serr)

list_of_clients=[]
list_of_external_power_conn=[]

""" ******************* this is for port forwading and communication with external router************************** """
"""while True:
        try:
            power_conn_port_no = 8050
            power_conn        = main.socket.socket(main.socket.AF_INET,main.socket.SOCK_STREAM)
            power_conn.setsockopt(main.socket.SOL_SOCKET,main.socket.SO_REUSEADDR,1)
            power_conn.bind((ip,int(power_conn_port_no)))
            power_conn.listen(1)
            break
        except main.socket_error as serr:
            print("Socket server not created port number 9050")
"""            


#print (serr)

"""def power_conn():
    while True:
            conn,addr= power_conn()
            list_of_power_conn.append((conn,addr))


    
def queue_power_conn():
    while True:
        main.time.sleep(0.5)    
        if not list_of_power_conn:
                var =list_of_power_conn.pop()
                t   =  threading.Thread()## write a function over here"""

"""**************************************************************************************************************** """


def id_generator(size =6 ,chars =string.ascii_uppercase +string.digits):
    return  ''.join(main.random.choice(chars) for _ in range(size))
    
        


""" ******************* The port number at which the router is receiving message form the power devices  **************************  """
 
    
while True:
        try:
            port_no = 8000
            server = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
            server.setsockopt(main.socket.SOL_SOCKET, main.socket.SO_REUSEADDR, 1)
            server.bind((ip,int(port_no)))
            print("Binding  completed port number 8000")
            server.listen(100)
            break
        except main.socket_error as serr:
            print("Socket server not created port number 8000")
            print (serr)    




def start_poll():
    while True:
        conn, addr = poll_read_portno.accept()
        message = conn.recv(4096)   



        
def start_conn():
#  global list_of_ip
  print ("We are in start conn function")
  while True:
 
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()
    
    print ("WHILE__________strart_conn")
 
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    #if addr[0] in setting.network_var.list_of_ip:
            # prints the address of the user that just connected
            
    print (addr[0] + " connected")
            #message = conn.recv(4096)
    list_of_clients.append((conn, addr))
    #else:
    #print("**************start_conn*****************")
    #print("************* {0} not in setting.network_var.list_of_ip ********".format(addr[0])) 
    #print("************* {0} not in setting.network_var.list_of_ip ********".format(addr[0])) 
            # creates and individual thread for every user 
            # that connects
#            t1=main.threading.Thread(target=clientthread,args=(conn,addr,)) 
#            t1.start()


        
            
def queue_func():
    
    print ('We are queue function')
    while True:
        #print ("WHILE_________queue function")
        main.time.sleep(0.5)
        if list_of_clients:
              print("We are in list of clients")
              client         = list_of_clients.pop()
              thread_id      = id_generator()
              #print("thread_id",thread_id)
              thread_id = main.threading.Thread(target=clientthread,args=(client[0],client[1],))
              thread_id.daemon = True
              thread_id.start()
              
"""  ***************************************************************************************  """                  
              
              
### Recieves the files from the devices and classifies them into different list according to the content in the file

def clientthread(conn, addr):
#           global Load_list
#           global lock
           global gui_obj
           conn.settimeout(5)
           print("We are in client thread")
           global port_list
           try:
             message = conn.recv(4096)
             print(message)
           except:
             print("The connection exited for ip:"+addr[0])
             sys.exit()
           s= 'receive'
           i= str(main.random.randint(1,101))   
           xml_1='.xml'
           receive_xml = s+i+xml_1
           #print(receive_xml)
           if message:
               f =open(receive_xml,"w")
               message =message.decode('ASCII')
               f.write(message)
               f.close()
               print ("<" + addr[0] + "> " + message )
               ##if the file is not in correct format 
               try:
                   doc= main.xml.dom.minidom.parse(receive_xml)
               except:
                   print("The document file recived is not correct")
                   sys.exit()
               print(doc.nodeName)
               print(doc.firstChild.tagName)
               #get the list of html tag from document and print each one
               tag_name = doc.getElementsByTagName("Verb")
               tag_name =tag_name[0].firstChild.nodeValue.encode('utf-8')
               #print(type(tag_name))
               print(tag_name)
               #post information about the port
               if tag_name.strip() == 'post':
                   print("It is  a post response")
                   verb = doc.getElementsByTagName("Noun")
                   verb = verb[0].firstChild.nodeValue.encode('utf-8')
                   if verb.strip() == 'Load':
                       arr = main.xml_process.Load_parse(doc)
                       
                       print("||##################################||###############################||")
                       print("                                 New Load joined                       ")
                       print("  ipaddress                         || {}                             ".format(addr[0]))
                       print("  Load ID                            || {}                             ".format(arr[0]))
                       print("  Type                              || {}                             ".format(arr[1]))
                       print("  Load Value                        || {}                             ".format(arr[2]))
                       print("  Load Voltage                      || {}                             ".format(arr[3]))
                       print("  Load Current                      || {}                             ".format(arr[4]))
                       print("  Minimum Voltage                   || {}                             ".format(arr[5]))
                       print("  Maximum Voltage                   || {}                             ".format(arr[6]))
                       print("  Minimum Current                   || {}                             ".format(arr[7]))
                       print("  Maximum Current                   || {}                             ".format(arr[8]))
                       print("||##################################||###############################||")
                       #print ("switch table" , setting.network_var.switch_table)
                       print (addr[0].strip())
                       x =  main.Parameter_pass.Load_mapping(main.load_param(), arr ,addr[0],str(ip_to_port(addr[0].strip())))
                       print ("^^^^^^^^^^^^Load joined^^^^^^^^^^")
                       print vars(x)
                       setting.common.lock.acquire()
                       if poll_debug:
                           #param_check  = parameter_check(x)  #to check the line voltage and see if it is under controll
                           param_check =True
                           if param_check:
                               setting.common.Load_list.append(x)
                               #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                               print("The  source is appended by an element")
                           else:
                               print("i.ip_address ->{0} ,i.port -> {1} ".format(x.ip_address,int(x.port.strip())))
                               setting.network_var.switch_table.remove((x.ip_address,int(x.port.strip())))                               
                               del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(x.ip_address)]
                               setting.network_var.list_of_ip.remove(x.ip_address)
                               print("********clientthread -> newload -> iplist",setting.network_var.list_of_ip)
                       else:
                       		setting.common.Load_list.append(x)
                       
                       print("**********UDIT********ADD***************")
                       print("LOAD")
                       print vars(x)
                       print("**********UDIT********ADD***************")
                       
                       
                       print('Load list',setting.common.Load_list)
                       
                       setting.common.comm_to_power_change_event.set()
                       #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                       setting.common.lock.release()
                       
                       #print (x[0])
                       #t1 =main.Table(rows =x , names =('ipaddress' ,'Load ID','Type ','Load Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Required', 'Status'))
                       main.os.remove(receive_xml)
                       sys.exit()
                   else:
                       pass
                   if verb.strip() == 'Source':
                       arr= main.xml_process.Source_parse(doc)
                      
                       print("||##################################||###############################||")
                       print("                                 New Source joined                       ")
                       print("  ipaddress                         || {}                             ".format(addr[0]))
                       print("  Source ID                         || {}                             ".format(arr[0]))
                       print("  Type                              || {}                             ".format(arr[1]))
                       print("  Source Value                      || {}                             ".format(arr[2]))
                       print("  Source Voltage                    || {}                             ".format(arr[2]))
                       print("  Source Current                    || {}                             ".format(arr[3]))
                       print("  Minimum Voltage                   || {}                             ".format(arr[4]))
                       print("  Maximum Voltage                   || {}                             ".format(arr[5]))
                       print("  Minimum Current                   || {}                             ".format(arr[6]))
                       print("  Maximum Current                   || {}                             ".format(arr[7]))
                       print("||##################################||###############################||")
                       x =  main.Parameter_pass.Source_mapping(main.source_param(), arr ,addr[0],str(ip_to_port(addr[0].strip())))
                       #print "Source joined"
                       setting.common.lock.acquire()
                       if poll_debug:
                           #param_check  = parameter_check(x)  #to check the line voltage and see if it is under controll
                           param_check = True
                           if param_check:
                               setting.common.Source_list.append(x)
                               #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                               print("The  source is appended by an element")
                           else:
                               print("i.ip_address ->{0} ,i.port -> {1} ".format(x.ip_address,int(x.port.strip()) ))
                               setting.network_var.switch_table.remove((x.ip_address,int(x.port.strip())))
                               del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(x.ip_address)]
                               setting.network_var.list_of_ip.remove(x.ip_address)
                               print("********clientthread -> newload -> iplist",setting.network_var.list_of_ip)
                       else:
                           setting.common.Source_list.append(x)
                       
                       print("**********UDIT********ADD***************")
                       print("SOURCE")
                       print vars(x)
                       print("**********UDIT********ADD***************")
                       
                       setting.common.comm_to_power_change_event.set()
                       
                       #gui_source.update_load(setting.common.Source_list)
                       #t2 =main.Table(rows =x , names =('ipaddress' ,'Source ID','Type ','Source Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Available', 'Status'))
                       print("new source join source ,source list",len(setting.common.Source_list))
                       print(setting.common.Source_list)
                       #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                       setting.common.lock.release()
                       main.os.remove(receive_xml)
                       sys.exit()
                   else:
                       pass  
                   if verb.strip() == 'Connect':
                        print ("It is a outside connect file response")
                        ip = doc.getElementsByTagName("Router_ip")
                        ip = ip[0].firstChild.nodeValue.encode('utf-8')
                        if ip == IPAddr:
                            load_ip = doc.getElementsByTagName("ip_to")
                            load_ip = load_ip[0].firstChild.nodeValue.encode('utf-8')
                            source_ip   = doc.getElementsByTagName("ip_from")
                            source_ip = source_ip[0].firstChild.nodeValue.encode('utf-8')
                            load_port = doc.getElementsByTagName("port_to")
                            load_port = load_port[0].firstChild.nodeValue.encode('utf-8')
                            source_port = doc.getElementsByTagName("port_from")
                            source_port = source_port[0].firstChild.nodeValue.encode('utf-8')
                            load_current = doc.getElementsByTagName("current_to")
                            load_current = load_current[0].firstChild.nodeValue.encode('utf-8')
                            source_current = doc.getElementsByTagName("current_from")
                            source_current = source_current[0].firstChild.nodeValue.encode('utf-8')
                            load_voltage = doc.getElementsByTagName("voltage_to")
                            load_voltage = load_voltage[0].firstChild.nodeValue.encode('utf-8')
                            source_voltage = doc.getElementsByTagName("voltage_from")
                            source_voltage = source_voltage[0].firstChild.nodeValue.encode('utf-8')
                            if load_ip in setting.network_var.list_of_ip:
                                setting.common.current_avail = setting.common.current_avail + float(load_current)
                                print ("****load_ip*****",load_ip)
                                print ("****source_ip***",source_ip)
                                print ("****load_port****",load_port)
                                print ("****source_port***",source_port)
                                print ("****load_current***",load_current)
                                print ("*****source_current**",source_current)
                                print ("*****load_voltage****",load_voltage)
                                print ("*****source_voltage***",source_voltage)
                                source = main.source_param()
                                source.ip_address =source_ip
                                source.port =str(source_port)
                                source.current_aval =float(source_current)
                                source.voltage =float(source_voltage)
                                source.state =1
                                setting.common.lock.acquire()
                                setting.common.Source_list.append(source)
                                setting.common.extern_Source_list.append(source)
                                print setting.common.Source_list
                                setting.common.lock.release()
                                if setting.common.broadcast_flag ==1:
                                    setting.common.broadcast_flag =0
                                setting.common.comm_to_power_change_event.set()
                                t_broadcast_receive  = main.time.time()
                                t = t_broadcast_receive -t_broadcast_send
                                with open(broadcast_time_file,'a') as fd:
                                    fd.write(str(t))
                                    fd.write('\n')
                                    fd.close()
                            else:
                                #setting.common.current_avail = setting.common.current_avail + float(load_current)
                                print ("****load_ip*****",load_ip)
                                print ("****source_ip***",source_ip)
                                print ("****load_port****",load_port)
                                print ("****source_port***",source_port)
                                print ("****load_current***",load_current)
                                print ("*****source_current**",source_current)
                                print ("*****load_voltage****",load_voltage)
                                print ("*****source_voltage***",source_voltage)
                                source = main.source_param()
                                load   = main.source_param()
                                source.ip_address = source_ip
                                load.ip_address   = load_ip
                                source.port =str(source_port)
                                load.port   =str(load_port)
                                source.current_aval =float(source_current)
                                load.current_reqd   =float(load_current)
                                source.voltage =float(source_voltage)
                                load.voltage =float(load_voltage)
                                load.state =1
                                source.state =1
                                setting.common.lock.acquire()
                                setting.common.Source_list.append(source)
                                setting.common.Load_list.append(load)
                                setting.common.extern_Source_list.append(source)
                                setting.common.extern_Load_list.append(load)
                                print setting.common.Source_list
                                setting.common.lock.release()
                                if setting.common.broadcast_flag ==1:
                                    setting.common.broadcast_flag =0
                                setting.common.comm_to_power_change_event.set()
                                t_broadcast_receive  = main.time.time()
                                t = t_broadcast_receive -t_broadcast_send
                                with open(broadcast_time_file,'a') as fd:
                                    fd.write(str(t))
                                    fd.write('\n')
                                    fd.close()
                        main.os.remove(receive_xml)
                   if verb.strip() == 'Disconnect':
                        print ("It is a outside disconnect file response")
                        ip = doc.getElementsByTagName("Router_ip")
                        ip = ip[0].firstChild.nodeValue.encode('utf-8')
                        if ip == IPAddr:
                            load_ip = doc.getElementsByTagName("ip_to")
                            load_ip = load_ip[0].firstChild.nodeValue.encode('utf-8')
                            source_ip   = doc.getElementsByTagName("ip_from")
                            source_ip = source_ip[0].firstChild.nodeValue.encode('utf-8')
                            load_port = doc.getElementsByTagName("port_to")
                            load_port = load_port[0].firstChild.nodeValue.encode('utf-8')
                            source_port = doc.getElementsByTagName("port_from")
                            source_port = source_port[0].firstChild.nodeValue.encode('utf-8')
                            load_current = doc.getElementsByTagName("current_to")
                            load_current = load_current[0].firstChild.nodeValue.encode('utf-8')
                            source_current = doc.getElementsByTagName("current_from")
                            source_current = source_current[0].firstChild.nodeValue.encode('utf-8')
                            load_voltage = doc.getElementsByTagName("voltage_to")
                            load_voltage = load_voltage[0].firstChild.nodeValue.encode('utf-8')
                            source_voltage = doc.getElementsByTagName("voltage_from")
                            source_voltage = source_voltage[0].firstChild.nodeValue.encode('utf-8')
                            if load_ip in setting.network_var.list_of_ip:
                                setting.common.current_avail = setting.common.current_avail + float(load_current)
                                print ("****load_ip*****",load_ip)
                                print ("****source_ip***",source_ip)
                                print ("****load_port****",load_port)
                                print ("****source_port***",source_port)
                                print ("****load_current***",load_current)
                                print ("*****source_current**",source_current)
                                print ("*****load_voltage****",load_voltage)
                                print ("*****source_voltage***",source_voltage)
                                source = main.source_param()
                                load   = main.load_param()
                                source.ip_address =source_ip
                                source.port =str(source_port)
                                source.current_aval =float(source_current)
                                source.voltage =float(source_voltage)
                                load.ip_address =load_ip
                                load.port =str(load_port)
                                load.current_aval =float(load_current)
                                load.voltage =float(load_voltage)
                                setting.common.lock.acquire()
                                print "Load is local"
                                for i in setting.common.extern_Source_list:
                                    if i.ip_address == source.ip_address:
                                        if i.port == source.port:
                                            print ("external source removed")
                                            setting.common.Source_list.remove(i)
                                            setting.common.extern_Source_list.remove(i)
                                            break
                                print " External source list remove from clien thread"
                                print setting.common.Source_list
                                for i in setting.common.extern_Load_list:
                                    if i.ip_address == load.ip_address:
                                        if i.port == load.port:
                                            print ("external load removed")
                                            setting.common.Load_list.remove(i)
                                            setting.common.extern_Load_list.remove(i)
                                            break
                                print " External load list remove from clien thread"
                                print setting.common.Load_list
                                setting.common.lock.release()
                                setting.common.comm_to_power_change_event.set()
                            else:
                                #setting.common.current_avail = setting.common.current_avail + float(load_current)
                                print ("****load_ip*****",load_ip)
                                print ("****source_ip***",source_ip)
                                print ("****load_port****",load_port)
                                print ("****source_port***",source_port)
                                print ("****load_current***",load_current)
                                print ("*****source_current**",source_current)
                                print ("*****load_voltage****",load_voltage)
                                print ("*****source_voltage***",source_voltage)
                                source = main.source_param()
                                load   = main.source_param()
                                source.ip_address = source_ip
                                load.ip_address   = load_ip
                                source.port =str(source_port)
                                load.port   =str(load_port)
                                source.current_aval =float(source_current)
                                load.current_reqd   =float(load_current)
                                source.voltage =float(source_voltage)
                                load.voltage =float(load_voltage)
                                setting.common.lock.acquire()
                                for i in setting.common.Source_list:
                                    if i.ip_address == source.ip_address:
                                        print "***** source is in source_list ******"
                                        if i.current_aval == source.current_aval: 
                                            print "***** source is in current is equal ******"
                                            setting.common.Source_list.remove(i)
                                            setting.common.extern_Source_list.remove(i)
                                            break
                                print("setting.common.Source_list", setting.common.Source_list)
                                print("setting.common.extern_Source_list", setting.common.extern_Source_list)
                                #print("load -->",vars(load))
                                #print ("vars(setting.common.Load_list[0])",vars(setting.common.Load_list[0]))
                                for i in setting.common.Load_list:
                                    if i.ip_address == load.ip_address:
                                        print "***** load is in load_list ******"
                                        if i.current_reqd == load.current_reqd:
                                            print "***** source is in current is equal ******"
                                            setting.common.Load_list.remove(i)
                                            setting.common.extern_Load_list.remove(i)
                                            break
                                print ("setting.common.Load_list",setting.common.Load_list)
                                print ("setting.common.extern_Load_list" ,setting.common.extern_Load_list)
                                setting.common.lock.release()
                                setting.common.comm_to_power_change_event.set()
                        main.os.remove(receive_xml)
               ### to update a value of port
               elif tag_name.strip() == 'update':
                   print("It is update response")
                   verb = doc.getElementsByTagName("Noun")
                   verb = verb[0].firstChild.nodeValue.encode('utf-8')
                   if verb.strip() == 'Load':
                        arr = main.xml_process.Load_parse(doc)
                        for i in setting.common.Load_list:
                           if arr[0] == i.id:
                               setting.common.lock.acquire()
                               setting.common.comm_to_power_change_event.set()
                               setting.common.Load_list[setting.common.Load_list.index(i)] = main.Parameter_pass.Load_mapping(main.load_param(), arr ,addr[0])
                               setting.common.lock.release()
                               #t3 =main.Table(rows =setting.common.Load_list , names =('ipaddress' ,'Load ID','Type ','Load Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Required', 'Status'))
                               print("load list has been upated")
                               break
                           else:
                               pass
                        main.os.remove(receive_xml)
                        sys.exit()
                          
                   elif verb.strip() == 'Source':
                        arr = main.xml_process.Source_parse(doc)
                        for i in setting.common.Source_list:
                           if arr[0] == i.id:
                               setting.common.lock.acquire()
                               setting.common.Source_list[setting.common.Source_list.index(i)] = main.Parameter_pass.Source_mapping(main.source_param(), arr ,addr[0])
                               setting.common.lock.release()
                               #t4 =main.Table(rows =setting.common.Source_list , names =('ipaddress' ,'Source ID','Type ','Source Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Available', 'Status'))
                               print("load list has been upated")
                               break
                           else:
                               pass
                        main.os.remove(receive_xml)
                        sys.exit()
               else :
                    print("It is not a get response")
                    

           #main.os.remove(receive_xml)
           message = None
                          
 

def Poll():

    print ("we are in poll ")
    tp_1 =main.time.time()
    tp_2 =main.time.time()
    #print ("Load list ",setting.common.Load_list)
    ### Poll  all the sources and loads connected to it and get there updated files ###
    """First check the load list get the all the updated files of the  load and then get the updated files of the sources."""
    while True:
        tp_1 =main.time.time()
        tp = tp_1- tp_2
        with open(poll_period,'a') as fd:
            fd.write(str(tp))
            fd.write('\n')
        fd.close()
        print ("XXXXXXXXXXXXXXXXXXXXXXXXXwe are in poll XXXXXXXXXXXXXXXXXXXXXXXXXX")        
        main.time.sleep(5)
        if  not setting.common.Load_list:
            pass
            print("We are in if not condition")
        else:
            for i in setting.common.Load_list:
              if (i in setting.common.Load_list) and (i not in setting.common.extern_Load_list):
                print("we are in poll common load list")
                sock_poll = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                #sock_poll.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_poll.settimeout(2)
                #print(vars(i))
                print("IP address",i.ip_address )
                print("POll port number", poll_portno)
                try:
                        sock_poll.connect((i.ip_address , poll_portno))
                except main.socket_error as serr:
                        #flag=1
                        print(serr)
                        print ("Load is no more connected to the poll file")
                        print "lock acquired___before  >> Polling"
                        setting.common.lock.acquire()
                        print "lock acquired___after  >> Polling"
                        if i in  setting.common.Load_list:
                                setting.common.Load_list.remove(i)
                                
                                print("**********UDIT********DELETE***************")
                                print("LOAD")
                                print (i)
                                print("**********UDIT********DELETE***************")
                               
                                setting.common.comm_to_power_change_event.set()
                                print("i.ip_address ->{0} ,i.port -> {1} ".format(i.ip_address,int(i.port.strip()) ))
                                setting.network_var.switch_table.remove((i.ip_address,int(i.port.strip())))
                                del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(i.ip_address)]
                                setting.network_var.list_of_ip.remove(i.ip_address)
                                setting.common.lock.release()
                                #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                                print("Below is load list")
                                print(setting.common.Load_list)
                                print("Below is ip_list")
                                print(setting.network_var.list_of_ip)
                                #gui_load.update_load(setting.common.Load_list)
                               
                        else:
                                pass
                        continue
                        
                
                main.xml_write.create_xml_file_poll(i.id,'poll.xml')
                    #print("sock_poll created")
                with open("poll.xml","r") as f:  ## to send poll file to the loads/source
                        data= f.read()
                        sock_poll.send(data.encode('ASCII'))
                        sock_poll.close()
                        #print("Load Poll file send")

                #print("we are in this part of code")
                conn , addr = poll_read.accept()
                main.time.sleep(3)
                message = conn.recv(4096)
                if message:
                    print("Load got a  poll response")
                    f =open("poll_response.xml","w")
                    message =message.decode('ASCII')
                    #print (message)
                    f.write(message)
                    f.close()
                    #print("Completed writing poll response")
                    #print ("<" + addr[0] + "> " + message )
                    ##if the file is not in correct format
                    try:
                        doc= main.xml.dom.minidom.parse("poll_response.xml")
                    except:
                        print("The document file recived is not correct")
                        sys.exit()
                    tag_name = doc.getElementsByTagName("Verb")
                    tag_name = tag_name[0].firstChild.nodeValue.encode('utf-8')
                    #print ("Before print doc",vars(doc))
                    if tag_name.strip() == 'poll':
                            #print("LOAD: It is update response")
                            noun = doc.getElementsByTagName("Noun")
                            noun = noun[0].firstChild.nodeValue.encode('utf-8')
                            if noun.strip() == 'Load':
                                arr = main.xml_process.Load_parse(doc)
                                print("||##################################||###############################||")
                                print("                                  Updated load                         ")
                                print("  ipaddress                         || {}                             ".format(addr[0]))
                                print("  Load ID                           || {}                             ".format(arr[0]))
                                print("  Type                              || {}                             ".format(arr[1]))
                                print("  Load Value                        || {}                             ".format(arr[2]))
                                print("  Minimum Voltage                   || {}                             ".format(arr[3]))
                                print("  Maximum Voltage                   || {}                             ".format(arr[4]))
                                print("  Minimum Current                   || {}                             ".format(arr[5]))
                                print("  Maximum Current                   || {}                             ".format(arr[6]))
                                print("||##################################||###############################||")
                                #x              = main.Parameter_pass.Source_mapping(main.source_param(), arr ,addr[0],"2")
                                x              = main.Parameter_pass.Load_mapping(main.load_param(), arr,addr[0],str(ip_to_port(addr[0])))
                                #print "lock acquired___before  >> Polling"
                                print ("_______AFTER LOAD MAPPING_____")
                                print vars(x)
                                setting.common.lock.acquire()
                                #print "lock acquired___after  >> Polling"
#                                setting.common.Load_list[setting.common.Load_list.index(i)] =main.Parameter_pass.Load_mapping(main.load_param(), arr ,addr[0],str(ip_to_port(addr[0])))
                                if poll_debug:
                                    #param_check  = parameter_check(x)
                                    param_check  = True
                                    if not param_check:
                                        if x in setting.common.Load_list:
                                            del setting.common.Load_list[setting.common.Load_list.index(x)]
                                            del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(x.ip_address)]
                                            setting.network_var.list_of_ip.remove(x.ip_address)
                                            print("********clientthread -> newload -> iplist",setting.network_var.list_of_ip)
                                            print("Source has been removed from the source list")
                                    else:
                                        if x in setting.common.Load_list:
                                            setting.common.Load_list[setting.common.Load_list.index(i)] = x
                                else:
                                    setting.common.Load_list[setting.common.Load_list.index(i)] = x
                                print("**********UDIT********UPDATE***************")
                                print("LOAD")
                                print (i)
                                print("**********UDIT********UPDATE***************")
                               
                                setting.common.comm_to_power_change_event.set()
                                #print("common update feedback list", setting.common.Feedback_list[1].voltage_port1)
                                #print(setting.common.Feedback_list[0].voltage_port1)
                                #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                                setting.common.lock.release()
                                
                                #t3 =main.Table(rows =setting.common.Load_list , names =('ipaddress' ,'Load ID','Type ','Load Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Required', 'Status'))
                                main.os.remove("poll_response.xml")
        if  not setting.common.Source_list:
            pass
        else:
	    print("We are in source list")
            for i in setting.common.Source_list:
              if (i in setting.common.Source_list) and (i not in setting.common.extern_Source_list):
                try:
                    sock_poll = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                    sock_poll.connect((i.ip_address , poll_portno))
                    main.xml_write.create_xml_source_poll(i.id,'poll.xml')
                    #print("sock_poll created")
                    with open("poll.xml","r") as f:  ## to send poll file to the loads/source
                        data= f.read()
                        sock_poll.send(data.encode('ASCII'))
                        sock_poll.close()
                        print("Poll file send")
                except main.socket_error as serr:
                        print(serr)
                        print ("Source is no more connected to the poll file")
                        
                        setting.common.lock.acquire()
                        if i in setting.common.Source_list:
                            setting.common.Source_list.remove(i)
                            print ("Length of source list",)
                       
                            print("**********UDIT********DELETE***************")
                            print("SOURCE")
                            print (i)
                            print("**********UDIT********DELETE***************")
                       
                            setting.common.comm_to_power_change_event.set()
                            print("i.ip_address ->{0} ,i.port -> {1} ".format(i.ip_address,int(i.port.strip()) ))
                            setting.network_var.switch_table.remove((i.ip_address,int(i.port.strip())))
                            del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(i.ip_address)]
                            setting.network_var.list_of_ip.remove(i.ip_address)
                            setting.common.lock.release()
                            #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                            print("Below is Source list")
                            print(setting.common.Source_list)
                            print("Below is ip_list")
                            print(setting.network_var.list_of_ip)
                            #   gui_source.update_load(setting.common.Source_list)

                            continue

                            #del setting.common.Source_list[setting.common.Source_list.index(i)]
                            print ("Length of source list",)
                            #break
                conn , addr = poll_read.accept()
                main.time.sleep(3)
                message = conn.recv(4096)
                if message:
                    print("got a  poll response")
                    f =open("poll_response.xml","w")
                    message =message.decode('ASCII')
                    f.write(message)
                    f.close()
                    print("Completed writing poll response")
                    try:
                        doc= main.xml.dom.minidom.parse("poll_response.xml")
                    except:
                        print("The document file recived is not correct")
                        sys.exit()
                    tag_name = doc.getElementsByTagName("Verb")
                    tag_name = tag_name[0].firstChild.nodeValue.encode('utf-8')
                    if tag_name.strip() == 'poll':
                            print("It is source  update response")
                            noun = doc.getElementsByTagName("Noun")
                            noun = noun[0].firstChild.nodeValue.encode('utf-8')
                            if noun.strip() == 'Source':
                                arr = main.xml_process.Source_parse(doc)
                                print("||##################################||###############################||")
                                print("                                  Updated Source                        ")
                                print("  ipaddress                         || {}                             ".format(addr[0]))
                                print("  Source ID                         || {}                             ".format(arr[0]))
                                print("  Type                              || {}                             ".format(arr[1]))
                                print("  Source Value                      || {}                             ".format(arr[2]))
                                print("  Minimum Voltage                   || {}                             ".format(arr[3]))
                                print("  Maximum Voltage                   || {}                             ".format(arr[4]))
                                print("  Minimum Current                   || {}                             ".format(arr[5]))
                                print("  Maximum Current                   || {}                             ".format(arr[6]))
                                print("||##################################||###############################||")
                                #print("poll->source{0} addr[0]{1}".format(str(ip_to_port(addr[0])),addr[0]))
                                x              = main.Parameter_pass.Source_mapping(main.source_param(), arr,addr[0],str(ip_to_port(addr[0])))
                                setting.common.lock.acquire()
                                if poll_debug:
                                    param_check  = parameter_check(x)
                                    if not param_check:
                                        try:
                                            if x in setting.common.Source_list:
                                                del setting.common.Source_list[setting.common.Source_list.index(x)]
                                                del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(x.ip_address)]
                                                setting.network_var.list_of_ip.remove(x.ip_address)
                                                print("********clientthread -> newload -> iplist",setting.network_var.list_of_ip)
                                                print("Source has been removed from the source list")
                                        except:
                                                pass
                                    else:
                                        try:
                                            if x in setting.common.Source_list:
                                                setting.common.Source_list[setting.common.Source_list.index(i)] = x
                                        except:
                                            pass
                                else:
                                    if x in setting.common.Source_list:
                                        setting.common.Source_list[setting.common.Source_list.index(i)] = x
                                    
                                #setting.common.comm_to_power_change_event.set()
                               
                                print("**********UDIT********UPDATE***************")
                                print("SOUREC")
                                print (x)
                                print("**********UDIT********UPDATE***************")
                               
                                setting.common.comm_to_power_change_event.set()
                                #gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
                                setting.common.lock.release()
                                
                                #t4 =main.Table(rows =setting.common.Source_list , names =('ipaddress' ,'Source ID','Type ','Source Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Available', 'Status'))
                                main.os.remove("poll_response.xml")
                else:
                    print("Nothing in message")
        curr_ava =current_available()
        print("********curr_ava********",curr_ava)
        tp_2 =main.time.time()
        if broadcast_req():
          print("++++++++++setting.common.broadcast_flag++++++++++",setting.common.broadcast_flag)
          if setting.common.broadcast_flag == 0:
                    print "______BEFORE broadcast is sent_______"
                    setting.common.lock.acquire()
                    current = current_available()
                    print("______current_______",current)
                    setting.common.lock.release()
                    if current < 0.0:
                        curr_i =0.0
                        l1 =[]
                        for i in setting.common.Load_list:
                            if (curr_i+current) < 0.0:
                                  curr_i = i.current_reqd + curr_i
                                  l1.append(i)
                                  
                        setting.common.broadcast_flag =1
                        for i in l1:
                            data    = main.xml_write.create_xml_broadcast_request(main.network.Self_Mac(),IPAddr,i.ip_address,str(abs(current)),str(i.voltage))
                            #data    = main.xml_write.create_xml_broadcast_request(main.network.Self_Mac(),IPAddr,setting.common.Load_list[0].ip_address,str(abs(current)),'12')
                            #data    = main.xml_write.create_xml_broadcast_request(main.network.Self_Mac(),IPAddr,'10.02','12')
                            broadcast.broadcast_energy_request(data)
                            t_broadcast_send =main.time.time()
                        print "***************************** broadcast request send**************************************"  

	




### try to make this function mutex
def broadcast_req():
    print "WE entered the broadcast req function"
    if (current_available() < 0.0):
            return True
    else:
        return False

def current_available():
    curr_ava = 0.0
    curr_req = 0.0
    curr_ext = 0.0
    for i in setting.common.Source_list:
        curr_ava = float(i.current_aval)+curr_ava
    for j in setting.common.Load_list:
        curr_req = float(j.current_reqd)+curr_req
    curr_ext = curr_ava - curr_req
    setting.common.current_avail    = curr_ext
    setting.common.current_required = curr_ext*(-1.0)
    return curr_ext

def local_current_available():
    curr_ava = 0.0
    curr_req = 0.0
    curr_ext = 0.0
    extern_curr_ava =0.0
    extern_curr_req = 0.0
    for i in setting.common.Source_list:
        curr_ava = float(i.current_aval)+curr_ava
    for i in setting.common.extern_Source_list:
        extern_curr_ava =float(i.current_aval) + extern_curr_ava
    for j in setting.common.Load_list:
        curr_req = float(j.current_reqd)+curr_req
    for j in setting.common.extern_Load_list:
        extern_curr_req = float(j.current_reqd)+ extern_curr_req
    local_curr_ava = curr_ava - extern_curr_ava
    local_curr_req = curr_req - extern_curr_req
    print("*********local_curr_ava***************",local_curr_ava)
    print("*********local_curr_req***************",local_curr_req)
    local_curr_ext = local_curr_ava - local_curr_req
    """if curr_req > curr_ava:
        curr_ext = curr_req - curr_ava
        setting.common.current_required = curr_ext
    else:
        curr_ext=0.0
        setting.common.current_required = curr_ext"""
    return local_curr_ext
    
### send_initial_conf is for creating network table and sending intial configuration file

def send_initial_conf():
      global Net_Table_present
      global Net_Table_previous
      global admin
      global Host
      global router_table
      global gui_obj
      global send_port_number 
      send_port_number =8050   ### it is same as poll port number
      port_check =False
      t3 = main.time.time()
      t4 = main.time.time()
      print("we are in send intial config")
      while True:
        main.time.sleep(0.3)
        t1 = main.time.time()
        t3 = main.time.time()
        tp_p = t3- t4
        with open(initial_config_period,'a') as fd:
            fd.write(str(tp_p))
            fd.write('\n')
        fd.close()
	dup_port                     = []
        print("||||||||||||||||||||||||______BEFORE NET_TABLE_PRESENT_________||||||||||||||||||||||||")
	Net_Table_present , dup_port = main.telnet.telnet_update(Host,admin,IPAddr)  #to get the mac addresses of all the loads connected to switch
	print("||||||||||||||||||||||||______AFTER NET_TABLE_PRESENT_________||||||||||||||||||||||||")
        if not Net_Table_present:
		continue    
	for net in Net_Table_present:
				if ((net.ip_address not in  setting.network_var.list_of_ip) and (net.mac not in setting.network_var.list_of_mac)) and (net.port_no not in dup_port):
                     		  #port_check  = device_connect(net.port_no)
                                  port_check  = True
				  if net.ip_address:
                      			print ("connect file  send for port number",net.port_no)
                                        print ("net entry",net)
					try:
                                                try:
                                                        #print("|||| we are before lock acquire-->try ||||")
                                                        setting.common.lock.acquire()
                                                        #print("|||| we are after lock acquire -->try||||")
                                                        setting.network_var.list_of_ip.append(net.ip_address)
                                                        setting.network_var.switch_table.append((net.ip_address,net.port_no))
                                                        setting.network_var.list_of_mac.append(net.mac)
                                                        #print("|||| we are before lock release -->try||||")
                                                        setting.common.lock.release()
                                                        #print("|||| we are after lock release -->try||||")
                                                        sock_initial = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                                                        sock_initial.settimeout(1)
                                                        sock_initial.connect((net.ip_address , send_port_number))
						        with open("connect.xml","r") as f:  ## to send poll file to the loads/source
							    data= f.read()
                                                            f.close()

                                                        sock_initial.send(data.encode('ASCII'))
                                                        sock_initial.close()
                                                except main.socket_error as serr:
                                                        print("***********send initial config send _initial_config***********")
                                                        #print("|||| we are before lock acquire-->except ||||")
                                                        setting.common.lock.acquire()
                                                        #print("|||| we are after lock acquire -->except||||")
                                                        setting.network_var.list_of_ip.remove(net.ip_address)
                                                        setting.network_var.switch_table.remove((net.ip_address,net.port_no))
                                                        setting.network_var.list_of_mac.remove(net.mac)
                                                        #print("|||| we are before lock release -->except||||")
                                                        setting.common.lock.release()
                                                        #print("|||| we are after lock release -->except||||")
                                                        print serr
                                                        continue

                               				#main.time.sleep(1)
					except main.socket_error as serr:
                                                        pass
        t2 = main.time.time()
        t= t1- t2
        print ("______________TIME send_initial_conf___________",t)
        with open(initial_config,'a') as fd:
            fd.write(str(t))
            fd.write('\n')
        fd.close()
        if  Net_Table_present :
                 print("--------------------------Net table Present----------------------------------------------------------")
                 gui_obj.update_iplist(Net_Table_present)
                 pass


def Network_polling():
      global send_port_number
      global previous_curr_available
      global previous_curr_requ  
      while True:
        #print "Network Polling"
        main.time.sleep(1)
        if  not setting.common.Load_list:
            pass
            #print("We are in if not condition ->Network polling")
        else:
            for i in setting.common.Load_list:
                if (i in setting.common.Load_list) and (i not in setting.common.extern_Load_list):
                    try: 
                        sock_initial = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                        sock_initial.settimeout(0.5)
                        sock_initial.connect((i.ip_address,send_port_number))
                        print "Load -> sock initial ->Netwrok Polling"
                        sock_initial.close()
                    except main.socket_error as serr:
                        #print "lock acquired___before  >> Network_polling"
                        setting.common.lock.acquire()
                        # print "lock acquired___after   >>Network_polling"
                        if i in setting.common.Load_list:
                            print("**********Socket_polling  ********DELETE Load ***************")
                            print("*************serr*****************************************",serr)
                            setting.network_var.switch_table.remove((i.ip_address,int(i.port.strip())))
                            del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(i.ip_address)]
                            setting.network_var.list_of_ip.remove(i.ip_address)
                            setting.common.Load_list.remove(i)
                            setting.common.comm_to_power_change_event.set()
                        #print "lock release___before"
                        setting.common.lock.release()
                        #print "lock release___after"
            for i in setting.common.extern_Source_list:
                    if i in setting.common.extern_Source_list:
                            try: 
                                sock_initial = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                                sock_initial.settimeout(0.5)
                                sock_initial.connect((i.ip_address,send_port_number))
                                print "Load -> sock initial ->Netwrok Polling"
                                sock_initial.close()
                            except main.socket_error as serr:
                                #print "lock acquired___before  >> Network_polling"
                                setting.common.lock.acquire()
                                # print "lock acquired___after   >>Network_polling"
                                if i in setting.common.extern_Source_list:
                                    print("**********Socket_polling  ********DELETE Source ***************")
                                    print("*************serr*****************************************",serr)
                                    setting.common.Source_list.remove(i)
                                    setting.common.extern_Source_list.remove(i)
                                setting.common.lock.release()
                                setting.common.comm_to_power_change_event.set()
            
        if  not setting.common.Source_list:
                        pass
                        #print("We are in if not condition")
        else:
                    for i in setting.common.Source_list:
                      if ((i in setting.common.Source_list) and (i not in setting.common.extern_Source_list)):
                        try:
                            sock_initial = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                            sock_initial.settimeout(1)
                            sock_initial.connect((i.ip_address,send_port_number))
                            print "Load -> sock initial ->Netwrok Polling"
                            sock_initial.close()
                        except main.socket_error as serr:
                            #print "lock acquired___before  >> Network_polling"
                            setting.common.lock.acquire()
                            #print "lock acquired___after  >> Network_polling"
                            if i in setting.common.Source_list:
                                print("**********Socket_polling  ********DELETE Source  ***************")
                                print("*************serr*****************************************",serr)
                                setting.network_var.switch_table.remove((i.ip_address,int(i.port.strip())))
                                del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(i.ip_address)]
                                setting.network_var.list_of_ip.remove(i.ip_address)
                                setting.common.Source_list.remove(i)
                                setting.common.comm_to_power_change_event.set()
                            setting.common.lock.release()
                    """     
                    if not ip_to_port_check(i.ip_address,i.port):
                      if i in setting.common.Load_list:
                        setting.common.lock.acquire()
                        print(" ")
                        print("LOAD")
                        print (i)
                        print("**********Network_polling  ********DELETE Load  ***************")
                       
                        setting.common.comm_to_power_change_event.set()
                        print("i.ip_address ->{0} ,i.port -> {1} ".format(i.ip_address,int(i.port.strip()) ))
                        setting.network_var.switch_table.remove((i.ip_address,int(i.port.strip())))
                        del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(i.ip_address)]
                        setting.network_var.list_of_ip.remove(i.ip_address)
                        setting.common.Load_list.remove(i)
                        setting.common.lock.release()
                        print("Below is load list")
                        print(setting.common.Load_list)
                        print("Below is ip_list")
                        print(setting.network_var.list_of_ip)
                    else:
                        pass"""

                            
                    for i in setting.common.extern_Load_list:
                        if i in setting.common.extern_Load_list:
                            try: 
                                sock_initial = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                                sock_initial.settimeout(0.5)
                                sock_initial.connect((i.ip_address,send_port_number))
                                print "Load -> sock initial ->Netwrok Polling"
                                sock_initial.close()
                            except main.socket_error as serr:
                                #print "lock acquired___before  >> Network_polling"
                                setting.common.lock.acquire()
                                # print "lock acquired___after   >>Network_polling"
                                if i in setting.common.extern_Load_list:
                                    print("**********Socket_polling  ********DELETE Load ***************")
                                    print("*************serr*****************************************",serr)
                                    setting.common.Load_list.remove(i)
                                    setting.common.extern_Load_list.remove(i)
                                setting.common.lock.release()
                                setting.common.comm_to_power_change_event.set()
                        
                        
                                
                                
        present_curr = current_available()
        print ("**********present_curr************",present_curr)
        if present_curr != previous_curr_available:
            print("---------------previous_curr_available-----------------" ,previous_curr_available)
            print("---------------present_curr-----------------" ,present_curr)
            previous_curr_available = present_curr
            local_curr = local_current_available()
            if (local_curr >= 0.0) and (present_curr >= 0.0):
                #print ("---------------Network_polling ---> local_curr",local_curr)
                #print ("---------------Network_polling ---> setting.common.extern_Source_list",setting.common.extern_Source_list)
                #print ("---------------Network_polling ---> setting.common.ack_send",setting.common.ack_send)
                if setting.common.extern_Source_list:
                        for i in  setting.common.ack_send:
                            print ("---------------Network_polling ---> setting.common.traceroute_recived",setting.common.traceroute_recived)
                            route = setting.common.traceroute_recived.pop(i)
                            data  = setting.common.ack_send.pop(i)
                            #print "XXXX||||||| ROUTE||||||||xxxxxxx"
                            print route
                            broadcast.disconnect_path_source(route,data)
                            print "**********disconnect_path**********"                            
                            source_rm = route[12]
                            source_rm = source_rm[0]
                            for i in setting.common.Source_list:
                                if i.ip_address ==source_rm:
                                    print "______||||||||||SOURCE _REMOVED||||||||||||||_________"
                                    setting.common.lock.acquire()
                                    setting.common.Source_list.remove(i) 
                                    setting.common.extern_Source_list.remove(i) 
                                    setting.common.lock.release()
                                    setting.common.comm_to_power_change_event.set()
                            if not setting.common.ack_send:
                                break
                            
            elif  present_curr < 0.0:
                if setting.common.extern_Load_list:
                    print ("---------------Network_polling ---> setting.common.extern_Source_list",setting.common.extern_Load_list)
                    for i in setting.common.extern_Load_list:
                        print"-----------||||||(present_curr +i.current_reqd)-----------||||||"
                        print (present_curr +(i.current_reqd)*2)
                        if (present_curr +(i.current_reqd)*2) >= 0.0:
                             print("We are inside external load removal") 
                             route = setting.common.traceroute_send.pop(i.ip_address)
                             print"#############route####################"
                             print route
                             data =[]
                             data.append(i.ip_address)
                             data.append(i.voltage)
                             data.append(i.current_reqd)
                             broadcast.disconnect_path_load(route,data)     
                             setting.common.lock.acquire()
                             try:
                                 setting.common.Load_list.remove(i) 
                             except:
                                 pass
                             try:
                                setting.common.extern_Load_list.remove(i)
                             except:
                                pass
                             setting.common.lock.release()
                             setting.common.comm_to_power_change_event.set()
                             print "**********disconnect_path**********"
            else :
                    pass
            """ empty the external connection"""
        
            """                 
                    if not ip_to_port_check(i.ip_address,i.port) :
                      for i in setting.common.Source_list:
                        setting.common.lock.acquire()
                        
                        
                        print("**********Network_polling   ********DELETE SOURCE***************")
                        print("Source")
                        print (i)
                        print("**********Network_polling  ********DELETE SOURCE***************")
                       
                        setting.common.comm_to_power_change_event.set()
                        print("i.ip_address ->{0} ,i.port -> {1} ".format(i.ip_address,int(i.port.strip()) ))
                        setting.network_var.switch_table.remove((i.ip_address,int(i.port.strip())))
                        del setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(i.ip_address)]
                        setting.network_var.list_of_ip.remove(i.ip_address)
                        setting.common.Source_list.remove(i)
                        setting.common.lock.release()
                        
                        print("Below is Source list")
                        print(setting.common.Source_list)
                        print("Below is ip_list")
                        print(setting.network_var.list_of_ip)"""

""" To check if any device is actually connected to a given  port  """
def device_connect(port_no):
    try:
    	if  setting.common.Feedback_list[(port_no -1)].voltage_port1 > 3:
        	return True
    	else:
        	return False	                  
    except:
        return False
        

"""  To check the parameter given by the source or load is correct. """
def parameter_check(x):
     port = ip_to_port(x.ip_address)
     print ("-------------------------parameter_check-----------------------")
     if port is None:
         return False
     else:
         if (x.max_volt is not None) and (x.min_volt is not None) :
           print(1)
           print("port_no",int(x.port))
           print("Voltage at the port",setting.common.Feedback_list[(int(x.port)-1)].voltage_port1)
           if (float(x.max_volt) >  setting.common.Feedback_list[(int(x.port)-1)].voltage_port1) and (float(x.min_volt) < setting.common.Feedback_list[(int(x.port)-1)].voltage_port1 ):
               return True
               
           else: 
               return False
         elif (x.max_volt is None) and (x.min_volt is not None):
             print(2)
             print("port_no",int(x.port))
             print("Voltage at the port",setting.common.Feedback_list[(int(x.port)-1)].voltage_port1)
             if (float(x.min_volt) < setting.common.Feedback_list[(int(x.port)-1)].voltage_port1) and  (setting.common.Feedback_list[(int(x.port)-1)].voltage_port1 < (float(x.voltage)+0.5)):
                 return True
             else:
                 False
         elif  (x.max_volt is not None) and (x.min_volt is None):
             print(3)
             print("port_no",int(x.port))
             print("Voltage at the port",setting.common.Feedback_list[(int(x.port)-1)].voltage_port1)
             if ((float(x.voltage)-5) < setting.common.Feedback_list[(int(x.port)-1)].voltage_port1) and  (setting.common.Feedback_list[(int(x.port)-1)].voltage_port1 < float(x.max_volt)):
                 return True
             else:
                 print"False paramcheck"
                 return False
         elif (x.max_volt is None) and (x.min_volt is None):
             print(4)
             print("port_no",int(x.port))
             print("Voltage at the port",setting.common.Feedback_list[(int(x.port)-1)].voltage_port1)
             if ((float(x.voltage) -5) < setting.common.Feedback_list[(int(x.port)-1)].voltage_port1) and (setting.common.Feedback_list[(int(x.port)-1)].voltage_port1 < (float(x.voltage)+5)):
                 return True
             else:
                 print"False paramcheck"
                 return False
         else:
             return False
     


"""  It return port number for an ip address """

def ip_to_port(ip):
    while True:
        for net in setting.network_var.switch_table:
            if net[0]==ip:
                print ("net1 --  >>>",net[1])
                return net[1]
        #print "ip to port"
        main.time.sleep(0.01)





def ip_to_port_check(ip ,port):
    global Net_Table_present
    
    """ get the mac address of a ip address from mac list and ip list"""
    try:
        mac = setting.network_var.list_of_mac[setting.network_var.list_of_ip.index(ip)]
    except:
        return False
    """ check if the mac is in the Net_Table_present and if present  get the port number """
    try:
        for entry in Net_Table_present:
            if entry.mac.strip() == mac.strip():
                #print("entry.port_no",entry.port_no)
                if str(entry.port_no)  == port:
                    #print "True"
                    return True
    except:
            return False
    return False
    

def sys_exit():
  global schedular
  while True:
          message = sys.stdin.readline()
          if message.strip() == "exit":
              for rows in setting.common.Source_list:
                  rows.state=2
              for rows in setting.common.Load_list:
                  rows.state=2
              setting.common.comm_to_power_change_event.set()
              main.time.sleep(3)
              main.os._exit(0)
          else:
              pass

def gui_funcs():
    print("Gui is initialized")
    global gui_obj 
    root , gui_obj = gui.vp_start_gui()
    print ("gui_obj",gui_obj)
    root.mainloop()

def gui_electrical_param():
    global gui_obj
    while True:
        try:
            gui_obj.update_votage_current(setting.common.Feedback_list)
        except:
            pass
        main.time.sleep(0.5)
        

def gui_load_list(): 
    #root =Tk()
    #root.wm_title("Load source list")
    global gui_load
    while True:
            try:
                gui_obj.update_source_load(setting.common.Source_list,setting.common.Load_list)
            except:
                pass
            main.time.sleep(0.5)

def start_receive():
  global Host
  global Mac
  global ip_addr,netmask
  global Mac_Table
  global Net_Table_present
  global Net_Table_previous
  global admin
  global previous_curr_available
  global previous_curr_req
  global gui_obj
  previous_curr_available =0.0
  previous_curr_requ  =0.0
  t0=main.threading.Thread(target=sys_exit,args=[])
  t0.start()
  t1 = main.threading.Timer(20,Poll,args=[])
  t2 = main.threading.Timer(3,start_conn,args=[])
  t3 = main.threading.Timer(7,send_initial_conf, args=[])
  t4 = main.threading.Timer(2,gui_funcs,args=[])
  t5 = main.threading.Timer(2,queue_func,args=[])
  t6 = main.threading.Timer(10,Network_polling,args=[])
  t7 = main.threading.Timer(5,gui_electrical_param,args=[])
  #t8 = main.threading.Timer(5,main.network.ARP_scan,args=[])
  t9 = main.threading.Timer(5,gui_load_list,args=[])
  t10 = main.threading.Timer(1,start_poll,args=[])
  admin ="admin"  # user name of switch
  Host = "192.168.0.50" #ip address of the switch
  Mac   =  main.namedtuple("Mac_Table" , "mac port_no ip_address") # required attibute for the mac table of the switch
  Mac_Table=[]  #Mac table for storing the value of mac address and it's corresponding
  ip_addr,netmask = main.network.initial_conf() # get the ip address and the netmask for the system
  main.network.ARP_scan() #do arp ping to get the ip address and the mac address of all the system in the network
  Net_Table_present = []
  Net_Table_previous= []
  main.xml_write.create_xml_file_connect('connect.xml',main.network.Self_Mac(),ip_addr)
  t2.start()
  t3.start()
  t4.start()
  t5.start()
  t6.start()
  t7.start()
  #t8.start()
  t9.start()
  t10.start()
  t1.start()    
  
  
  
  
  
if __name__ == "__main__":
	
  start_receive()
  while True:
	  main.time.sleep(5)
	  pass
  
