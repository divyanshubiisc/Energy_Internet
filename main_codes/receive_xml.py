    # -*- coding: utf-8 -*-

#import socket
#import select
import sys
from comm import main
#sys.path.append('/home/pi/Desktop/i2c_pi/Energy_Router/')
from global_var import setting

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

while True:
    try:
        IPAddr = main.ni.ifaddresses('eth0')[main.ni.AF_INET][0]['addr']
        ip  =IPAddr
        break
    except:
        print("Interface doesnot have a  ip address")
    

print("Your Computer IP Address is:" + IPAddr) 
   
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




#sock_poll = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
poll_portno =8050       # port number for which it will sending poll request to load


while True:
	try:
		pollread_portno =8010  # port number for which poll file will be received by the server
		poll_read = main.socket.socket(main.socket.AF_INET,main.socket.SOCK_STREAM)
		poll_read.setsockopt(main.socket.SOL_SOCKET, main.socket.SO_REUSEADDR, 1)
		poll_read.bind((ip,int(pollread_portno)))
		poll_read.listen(1)
		print("Binding  completed port number 8050")
		break
	except main.socket_error as serr:
		print("Socket server not created port number 8050")
		print (serr)
		
list_of_clients=[]

def start_conn():
#  global list_of_ip
  
  while True:
 
    """Accepts a connection request and stores two parameters, 
    conn which is a socket object for that user, and addr 
    which contains the IP address of the client that just 
    connected"""
    conn, addr = server.accept()
    

 
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    if addr[0] in setting.network_var.list_of_ip:
            # prints the address of the user that just connected
            print (addr[0] + " connected")
            # creates and individual thread for every user 
            # that connects
            t1=main.threading.Thread(target=clientthread,args=(conn,addr,)) 
            t1.start()
    
### Recieves the files from the devices and classifies them into different list according to the content in the file
def clientthread(conn, addr):
#           global Load_list
#           global lock
           conn.settimeout(5)
           try:
             message = conn.recv(4096)
           except:
             print("The connection exited for ip:"+addr[0])
             main.sys.exit()
           s= 'receive'
           i= str(main.random.randint(1,101))   
           xml_1='.xml'
           receive_xml = s+i+xml_1
           print(receive_xml)
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
                   main.sys.exit()
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
                       print("  Load ID                           || {}                             ".format(arr[0]))
                       print("  Type                              || {}                             ".format(arr[1]))
                       print("  Load Value                        || {}                             ".format(arr[2]))
                       print("  Minimum Voltage                   || {}                             ".format(arr[3]))
                       print("  Maximum Voltage                   || {}                             ".format(arr[4]))
                       print("  Minimum Current                   || {}                             ".format(arr[5]))
                       print("  Maximum Current                   || {}                             ".format(arr[6]))
                       print("||##################################||###############################||")
                       x =  main.Parameter_pass.Load_mapping(main.load_param(), arr ,addr[0])
                       setting.common.lock.acquire()
                       setting.common.Load_list.append(x)
                       setting.common.lock.release()
                       #print (x[0])
                       #t1 =main.Table(rows =x , names =('ipaddress' ,'Load ID','Type ','Load Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Required', 'Status'))
                       main.sys.exit()
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
                       print("  Minimum Voltage                   || {}                             ".format(arr[3]))
                       print("  Maximum Voltage                   || {}                             ".format(arr[4]))
                       print("  Minimum Current                   || {}                             ".format(arr[5]))
                       print("  Maximum Current                   || {}                             ".format(arr[6]))
                       print("||##################################||###############################||")
                       x =  main.Parameter_pass.Source_mapping(main.source_param(), arr ,addr[0])
                       setting.common.lock.acquire()
                       setting.common.Source_list.append(x)
                       setting.common.lock.release()
                       #t2 =main.Table(rows =x , names =('ipaddress' ,'Source ID','Type ','Source Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Available', 'Status'))
                       print(setting.common.Load_list)
                       main.sys.exit()
                   else:
                       pass                   
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
                               setting.common.Load_list[setting.common.Load_list.index(i)] = main.Parameter_pass.Load_mapping(main.load_param(), arr ,addr[0])
                               setting.common.lock.release()
                               #t3 =main.Table(rows =setting.common.Load_list , names =('ipaddress' ,'Load ID','Type ','Load Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Required', 'Status'))
                               print("load list has been upated")
                               break
                           else:
                               pass
                        main.sys.exit()
                          
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
                        main.sys.exit()
               else :
                    print("It is not a get response")
                    
               main.os.remove(receive_xml)
               message = None
               
           else:
                pass
                          
 

def Poll():

    print ("we are in poll ")
    ### Poll  all the sources and loads connected to it and get there updated files ###
    """
    First check the load list get the all the updated files of the  load and then get the updated files of the sources.
    
    
    """
    while True:
        if  not setting.common.Load_list:
            pass
        else:
            for i in setting.common.Load_list:
                sock_poll = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                #sock_poll.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock_poll.settimeout(2)
                print(vars(i))
                print("IP address",i.ip_address )
                print("POll port number", poll_portno)
                try:
                        sock_poll.connect((i.ip_address , poll_portno))
                except main.socket_error as serr:
                        flag=1
                        print(serr)
                        print ("Load is no more connected to the poll file")
                        setting.common.lock.acquire()
                        setting.common.Load_list.remove(i)
                        del setting.common.list_of_mac[setting.network_var.list_of_ip.index(i.ip_address)]
                        setting.network_var.list_of_ip.remove(i.ip_address)
                        setting.common.lock.release()
                        print("Below is load list")
                        print(setting.common.Load_list)
                        print("Below is ip_list")
                        print(setting.network_var.list_of_ip)
                        continue

                main.xml_write.create_xml_file_poll(i.id,'poll.xml')
                    #print("sock_poll created")
                with open("poll.xml","r") as f:  ## to send poll file to the loads/source
                        data= f.read()
                        sock_poll.send(data.encode('ASCII'))
                        sock_poll.close()
                        #print("Poll file send")

                #print("we are in this part of code")
                conn , addr = poll_read.accept()
                main.time.sleep(3)
                message = conn.recv(4096)
                if message:
                    #print("got a  poll response")
                    f =open("poll_response.xml","w")
                    message =message.decode('ASCII')
                    f.write(message)
                    f.close()
                    #print("Completed writing poll response")
                    #print ("<" + addr[0] + "> " + message )
                    ##if the file is not in correct format 
                    try:
                        doc= main.xml.dom.minidom.parse("poll_response.xml")
                    except:
                        print("The document file recived is not correct")
                        main.sys.exit()
                    tag_name = doc.getElementsByTagName("Verb")
                    tag_name = tag_name[0].firstChild.nodeValue.encode('utf-8')
                    if tag_name.strip() == 'poll':
                            #print("It is update response")
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
                                setting.common.lock.acquire()
                                setting.common.Load_list[setting.common.Load_list.index(i)] =main.Parameter_pass.Load_mapping(main.load_param(), arr ,addr[0])
                                setting.common.lock.release()
                                #t3 =main.Table(rows =setting.common.Load_list , names =('ipaddress' ,'Load ID','Type ','Load Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Required', 'Status'))
                                main.os.remove("poll_response.xml")
        if  not setting.common.Source_list:
            pass
        else:                  
            for i in setting.common.Source_list:
                try:
                    sock_poll = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
                    sock_poll.connect((i.ip_address , poll_portno))
                    main.xml_write.create_xml_file_poll(i.id,'poll.xml')
                    #print("sock_poll created")
                    with open("poll.xml","r") as f:  ## to send poll file to the loads/source
                        data= f.read()
                        sock_poll.send(data.encode('ASCII'))
                        sock_poll.close()
                        #print("Poll file send")
                except main.socket_error as serr:
                        print(serr)
                        print ("Load is no more connected to the poll file")
                        del setting.common.Load_list[setting.common.Load_list.index(i)]
                        break
                conn , addr = poll_read.accept()
                main.time.sleep(3)
                message = conn.recv(4096)
                if message:
                    print("got a  poll response")
                    f =open("poll_response.xml","w")
                    message =message.decode('ASCII')
                    f.write(message)
                    f.close()
                    #print("Completed writing poll response")
                    try:
                        doc= main.xml.dom.minidom.parse("poll_response.xml")
                    except:
                        print("The document file recived is not correct")
                        main.sys.exit()
                    tag_name = doc.getElementsByTagName("Verb")
                    tag_name = tag_name[0].firstChild.nodeValue.encode('utf-8')
                    if tag_name.strip() == 'poll':
                            #print("It is update response")
                            noun = doc.getElementsByTagName("Noun")
                            noun = noun[0].firstChild.nodeValue.encode('utf-8')
                            if noun.strip() == 'Source':
                                arr = main.xml_process.Source_parse(doc)
                                print("||##################################||###############################||")
                                print("                                 New Source joined                       ")
                                print("  ipaddress                         || {}                             ".format(addr[0]))
                                print("  Source ID                         || {}                             ".format(arr[0]))
                                print("  Type                              || {}                             ".format(arr[1]))
                                print("  Source Value                      || {}                             ".format(arr[2]))
                                print("  Minimum Voltage                   || {}                             ".format(arr[3]))
                                print("  Maximum Voltage                   || {}                             ".format(arr[4]))
                                print("  Minimum Current                   || {}                             ".format(arr[5]))
                                print("  Maximum Current                   || {}                             ".format(arr[6]))
                                print("||##################################||###############################||")
                                setting.common.lock.acquire()
                                setting.common.Source_list[setting.common.Source_list.index(i)] = main.Parameter_pass.Source_mapping(main.source_param(), arr ,addr[0])
                                setting.common.lock.release() 
                                #t4 =main.Table(rows =setting.common.Source_list , names =('ipaddress' ,'Source ID','Type ','Source Value ','Minimum Voltage','Maximum Voltage ','Minimum Current ','Maximum Current','Current Available', 'Status'))                               
                                main.os.remove("poll_response.xml")
                else:
                    print("Nothing in message")

### send_initial_conf is for creating network table and sending intial configuration file
                    
def send_initial_conf():
      global Net_Table_present
      global Net_Table_previous
      global admin
      global Host
      send_port_number =8050   ### it is same as poll port number
      
      while True:
		dup_port                     = []
		Net_Table_present , dup_port = main.telnet.telnet_update(Host,admin,IPAddr)  #to get the mac addresses of all the loads connected to switch
		for net in Net_Table_present:
				if ((net.ip_address not in  setting.network_var.list_of_ip) or (net.mac not in setting.network_var.list_of_mac)) and (net.port_no not in dup_port): 
					try:
						sock_initial = main.socket.socket(main.socket.AF_INET, main.socket.SOCK_STREAM)
						sock_initial.connect((net.ip_address , send_port_number))
						with open("connect.xml","r") as f:  ## to send poll file to the loads/source
							data= f.read()
							sock_initial.send(data.encode('ASCII'))
							sock_initial.close()
							setting.common.lock.acquire()
							setting.network_var.list_of_ip.append(net.ip_address)
							setting.network_var.list_of_mac.append(net.mac)
							setting.common.lock.release()
					except main.socket_error as serr:
							#print(serr)
							#print ("Error in file:receive_xml  function:send_initial_conf  line:342")
                                         if net.mac not in setting.network_var.mac_address_not_reacable:
                                            setting.network_var.mac_address_not_reacable.append(net.mac)
                                         continue
                        
			#Net_Table_previous =Net_Table_present
			## include uart function to send data
		Net_Table_previous= Net_Table_present
		#print(Net_Table_present)
		if  Net_Table_present :
			t1 =main.Table(rows =Net_Table_present , names =('mac' ,'port no','ip address'))
			print(t1)
		main.time.sleep(.10)





               
def sys_exit():
  while True:
          message = main.sys.stdin.readline()
          if message.strip() == "exit":
              main.os._exit(0)
          else:
              pass



def start_receive():
  global Host 	
  global Mac
  global ip_addr,netmask
  global Mac_Table
  global Net_Table_present
  global Net_Table_previous
  global admin
  t0=main.threading.Thread(target=sys_exit,args=[])
  t0.start()
  t1=main.threading.Timer(20,Poll,args=[]) 
  t2 = main.threading.Timer(3,start_conn,args=[]) 
  t3 = main.threading.Timer(3,send_initial_conf, args=[]) 
  admin ="admin"  # user name of switch
  Host = "192.168.0.10" #ip address of the switch
  Mac   =  main.namedtuple("Mac_Table" , "mac port_no ip_address") # required attibute for the mac table of the switch 
  Mac_Table=[]  #Mac table for storing the value of mac address and it's corresponding
  ip_addr,netmask = main.network.initial_conf() # get the ip address and the netmask for the system
  main.network.ARP_scan() #do arp ping to get the ip address and the mac address of all the system in the network
  Net_Table_present = []
  Net_Table_previous= []
  main.xml_write.create_xml_file_connect('connect.xml',main.network.Self_Mac(),ip_addr)
  t1.start()
  t2.start()
  t3.start()
              
if __name__ == "__main__":
	
  start_receive()
  while True:
	  main.time.sleep(5)
	  pass
  
