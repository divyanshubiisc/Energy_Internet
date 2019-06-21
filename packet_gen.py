# -*- coding: utf-8 -*-

import pickle
from global_var import setting

class Packet(object):
    def __init__(self):
        self.ip_src=None
        self.type =30
        self.code =10
        self.max_hop=10
        self.hop_count=0
        #self.identifier=110022
        
        
        
    """ Function for generating packet from the source router. As the packet get forwarded the routers the packet get appended by the additional information of router and its port number.
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
        | Type =30 |Code =10 | id | Allowed Hop =10 | Hop Count =0 |source IP | destination load IP | destination Master IP | source port connection to | source  port connection from |
        -----------------------------------------------------------------------------------------------------------------------------------------------------------------------                
        Type and code are usually for the type of packet and is used to decribed different secnario and there response . 
        Allowed Hop    -->   It is maixmum number of hop that a packet can travell from that point onwards.
        Hop counts -->   Tells the number of hop that the packet has taken
        Source IP  -->   It is the ip address which is generating the trace route packet
        destination Load IP --> It gives the ip address of destination end point till where it wants to make the connection
        destination IP Master      --> It is the ip address of destination end point Master unit.
        Source port connection to  --> It is port number to which the destination is connected in the local switch
        Source port connection from  --> It is the port number which requested for the traceroute
    """
    def packet_src(self,packet_id,ip_src,ip_dst,ip_dst_master,port_to,port_from):
        packet = [self.type,self.code,packet_id,self.max_hop,self.hop_count,ip_src,ip_dst,ip_dst_master,port_to,port_from]
        packet =pickle.dumps(packet)
        return packet
        
        
    """ This function is creating a forwading packet.
        --------------------------------------------
        | packet   |   IP  |port to  | port from   |
        --------------------------------------------
        The hop count and max hop are changed  in the packet recived from previous router . The value of hop count is increased by 1 and Max hop is decreased by 1. 
        IP --> It is the ip address of the master forwarding the packet
        port from --> It is the port number from where the packet is coming in the intermediate router.
        port to   --> It is the port number where the packet is going from the intermediate router.
        IP ,port to & port from are appended in the packet and send to the next router.
    """    
    def packet_fwd(self,packet,ip_src,port_to,port_from):
        self.packet =packet
        self.packet[3] = self.packet[3] -1
        self.packet[4] = self.packet[4] +1
        self.packet.append([ip_src,port_from,port_to])
        self.packet =pickle.dumps(packet)
        return self.packet
        
        
    """  Function for creating hop count expired packet.
         -----------------------------------------------------------------------
         |Type =0 |Code =10 | id |Allowed  Hop =0 |Source IP |Destination Master IP |
         -----------------------------------------------------------------------
          Type  =0 and code 10- It for the destination master is unreachable in 10 hop counts
          Max_hop  cout is 0
          id gives the packet id number.
          Destination Master IP - It is the ip address of the master of  destination ip address. It is there so that if is any destination ip address which is in same destination master . 
          It can be declared unroutable
    """  
    def packet_hop_exp(self,packet):
        packet =[0,packet[1],packet[2],packet[3],packet[5],packet[7]]
        packet =pickle.dumps(packet)
        return packet
        
        
    """ Function for creating no further route avialable packet 
        ------------------------------------------------------------------------
       | Type =0 | code = 1 | id |Allowed  Hop =0 |Source IP |Destination Master IP |
        ------------------------------------------------------------------------
        Type = 0 and code = 1 is used when destination master ip address is not avaialable in the intermedate router database.
        This packet is send back to the source address
    """
    def packet_no_route(self,packet):
        packet =[0,1,packet[2],packet[3],packet[5],packet[7]]
        packet =pickle.dumps(packet)
        return packet
        
    """  At the destination router this  a packet is created for the response of trace route packet. This packet is only created when the desired load or source is present
         -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        | Type =30 |Code =10 | id | Allowed Hop | Hop Count  |source IP | destination IP | destination Master IP | source port connection to | source  port connection from | dest port from | dest port to |
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------     
        |                                                                     Route path information along with the port numbers                                                                        |                                                               |        
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
      """
    def packet_response(self,packet,port_to,port_from):
        self.packet =packet
        self.packet[0] = 3
        self.packet.insert(10,port_from)
        self.packet.insert(11,port_to)
        self.packet =pickle.dumps(packet)
        return self.packet
        
        
    """  Function generates packet if the requested ip is no more present in the destination router 
         ---------------------------------------------------------------------------------------------------
        | Type =4 |Code =10 | id | Allowed Hop  | Hop Count |source IP | destination IP | destination Master IP | 
        ----------------------------------------------------------------------------------------------------
        Type 4 and code 10 tells that the destination ip is no more present in the destination Master.
    
    """     
    def packet_end_error(self,packet):
        self.packet =packet[0:7]
        self.packet[0] =4
        self.packet=pickle.dumps(self.packet)
        return self.packet
        
        
    """"  To send a response back to source router from intermediate router 
    ------------------------------------------------------------------------
    |0 | code | packet-id |Allowed hop | hop count | ip_src | current router ip|   
    ------------------------------------------------------------------------  
    """
    def packet_intermediate_response(self,packet,ip_src):
        print("packet_intermediate_response",packet)
        packet = [20, packet[1],packet[2],(int(packet[3])-1),(int(packet[4])),packet[5],ip_src]
        packet =pickle.dumps(packet)
        return packet


class  Energy_Packet(object):
    def __init__(self):
        self.ip_src=setting.common.ip_address
        self.type_request =1
        self.code_request =2
        self.id =None
        self.hw_addr =setting.common.ip_address
        self.router_id ="b8:27:eb:a4:40:00"
        self.switch_id ="b8:27:eb:a4:40:00"
        self.type_response =3
        self.code_response =4
        self.type_confirm  =5
        self.code_confirm  =6
    def energy_request_packet(self,packet_id,port_no, time, data):
        packet_len=10
        packet =[self.type_request,self.code_request,packet_id,self.hw_addr,self.router_id,port_no,self.switch_id,time,packet_len,data]
        packet=pickle.dumps(packet)
        return packet
    
    def energy_response_packet(self, packet_id ,packet_response_id ,port_no, time, data):
        packet_len=11
        packet =[self.type_response, self.code_response, packet_id, packet_response_id, self.hw_addr,self.router_id, port_no,self.switch_id,time,packet_len ,data]
        packet =pickle.dumps(packet)
        return packet
        
    def energy_confirm_packet(self,packet_id, packet_response_id ,port_no, time, data):
        packet_len=10
        packet =[self.type_confirm,self.code_confirm ,packet_id, packet_response_id, self.hw_addr,self.router_id , port_no,self.switch_id,time, packet_len, data]
        packet=pickle.dumps(packet)
        return packet
        
        
if __name__ =='__main__':
    pack =Energy_Packet()
    packet = pack.energy_confirm_packet(packet_id =1034,packet_response_id = 1022 ,port_no =1036 ,time=11 ,data ="hello")
    print(packet)
