import telnetlib
import re
import sys	
Host ="192.168.0.20"
admin ="admin"
#y =None
f =open("telnet.txt","w+")
f.write("")
f.close


def address(mac):   
    with open("telnet.txt","r") as openfile:
        for line in openfile:
            if mac in line:
                part =line.split()
                #print(part[0])
                return part[0]
            
    return None




print("This is telnet update file")
try:
            tn= telnetlib.Telnet(Host,23,5)
	    #tn.open(Host)
            tn.write(admin+"\n")

except:
            print("Not able to login into telnet host")
            sys.exit()
try:
            tn.read_until("Password:")
            tn.write("admin"+"\n")
            x = tn.read_until("DGS-1210-10P> ")
            #print(x)
            #print("password printed"
except:
            print("Login or password error")

try:
                tn.write("debug info" + "\n")
                while True:
                    r = tn.read_until("DGS-1210-10P> ",timeout =.2)
                    #print(r.strip())
                    if r.strip() =='':
                      break
                    f =open("telnet.txt","a")
                    f.write(r)
                    f.close
                    tn.write(" ")

# 	    tn.write("debug info"+"\n")
	    #print(x)
	    #while 	
	    	#tn.write("t"+"\n")
            	#x = tn.read_until("--More-- ",timeout =.2)
	    	#print(x)		
except:
                try:
                    x = tn.read_until("DGS-1210-10P> ")
                except:
                    print("Not able to get debug info")
 	        print(x)
#print(r)
f = open ("telnet.txt","r")  #open file with f only other wise it qill not work properly
data     =f.read()



#for line in openfile:
#        print(line)
#        if "Learnt" in line:
#                        print("Learnt",line)
#                        for part in line.split():
#                            if "Gi0/" in part:
#                                        part =part.split('/')
#                                        a =part[1]
#                                        print(a)
#                            if  ":" in part:
#                                        b= part
#                                        print(b)
msg = re.findall("^.*Learnt.*$",data,re.MULTILINE)
#print(msg)
print("Mac Table getting updated ........")
for p in msg:
            p=str(p)
            for part in p.split():
                if "Gi0/" in part:
                    part = part.split('/')
                    b    = part[1]
                if  ":"  in part:
                    a    = part
            if a[1].strip() == network.Self_Mac(): # to get the self mac address and ip address as it is not avialable in arp table
               mac_entry = Mac(mac =a[1].strip() ,port_no =int(b[1].strip()),ip_address=ip_addr.strip())
               if int(b[1].strip()) in port:
                   if int(b[1].strip()) not in dup_port:
				   dup_port.append(int(b[1].strip()))
               port.append(int(b[1].strip()))
            
            
            
            
