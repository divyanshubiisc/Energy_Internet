# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 16:09:23 2018

@author: ud
"""

from xml.dom.minidom import getDOMImplementation

##module to create xml file. Input given are id number and file name
def create_xml_file_poll(number,file_name):
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "Message", None)
    top_element = newdoc.documentElement
    header =newdoc.createElement("Header")

    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('poll')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Load')
    noun.appendChild(noun_text)

    id_no = newdoc.createElement("id")
    id_no_text =newdoc.createTextNode(number)
    
    id_no.appendChild(id_no_text)

    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    top_element.appendChild(header)
    #text = newdoc.createTextNode('Some textual content.')
    #top_element.appendChild(text)
    #print("lala")
    newdoc.writexml( open(file_name, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
 
    newdoc.unlink()


def create_xml_ER_ER_connect(router_ip,ip_to,ip_from,port_to,port_from,current_to,current_from,voltage_to,voltage_from):
    impl = getDOMImplementation()
    
    newdoc= impl.createDocument(None,'Message',None)
    top_element =newdoc.documentElement
    header =newdoc.createElement("Header")
    body   =newdoc.createElement("Body")
    
    
    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('post')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Connect')
    noun.appendChild(noun_text)

    type_er = newdoc.createElement("type")
    type_text =newdoc.createTextNode('Energy_Router')
    type_er.appendChild(type_text)


    id_no = newdoc.createElement("Router_ip")
    id_no_text =newdoc.createTextNode(router_ip)
    id_no.appendChild(id_no_text)    
    
    ip_load = newdoc.createElement("ip_to")
    ip_load_text =newdoc.createTextNode(ip_to)
    ip_load.appendChild(ip_load_text)    

    ip_source = newdoc.createElement("ip_from")
    ip_source_text =newdoc.createTextNode(ip_from)
    ip_source.appendChild(ip_source_text)
    
    load_port = newdoc.createElement("port_to")
    load_port_text =newdoc.createTextNode(port_to)
    load_port.appendChild(load_port_text)    

    source_port = newdoc.createElement("port_from")
    source_port_text =newdoc.createTextNode(port_from)
    source_port.appendChild(source_port_text)    

    load_curr = newdoc.createElement("current_to")
    load_curr_text =newdoc.createTextNode(current_to)
    load_curr.appendChild(load_curr_text)    

    source_curr = newdoc.createElement("current_from")
    source_curr_text =newdoc.createTextNode(current_from)
    source_curr.appendChild(source_curr_text)
    
    load_volt = newdoc.createElement("voltage_to")
    load_volt_text =newdoc.createTextNode(voltage_to)
    load_volt.appendChild(load_volt_text)    

    source_volt = newdoc.createElement("voltage_from")
    source_volt_text =newdoc.createTextNode(voltage_from)
    source_volt.appendChild(source_volt_text)



    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    
    body.appendChild(ip_load)
    body.appendChild(ip_source)
    body.appendChild(load_port)
    body.appendChild(source_port)
    body.appendChild(load_curr)
    body.appendChild(source_curr)
    body.appendChild(load_volt)
    body.appendChild(source_volt)
    
    top_element.appendChild(header)
    top_element.appendChild(body)
    newdoc.writexml( open('er_er_connect.xml', 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    newdoc.unlink()
    f = open('er_er_connect.xml','r')
    data =f.read()
    f.close()
    #print data
    return data

def create_xml_ER_ER_disconnect(router_ip,ip_to,ip_from,port_to,port_from,current_to,current_from,voltage_to,voltage_from):
    impl = getDOMImplementation()
    
    newdoc= impl.createDocument(None,'Message',None)
    top_element =newdoc.documentElement
    header =newdoc.createElement("Header")
    body   =newdoc.createElement("Body")
    
    
    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('post')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Disconnect')
    noun.appendChild(noun_text)

    type_er = newdoc.createElement("type")
    type_text =newdoc.createTextNode('Energy_Router')
    type_er.appendChild(type_text)


    id_no = newdoc.createElement("Router_ip")
    id_no_text =newdoc.createTextNode(router_ip)
    id_no.appendChild(id_no_text)    
    
    ip_load = newdoc.createElement("ip_to")
    ip_load_text =newdoc.createTextNode(ip_to)
    ip_load.appendChild(ip_load_text)    

    ip_source = newdoc.createElement("ip_from")
    ip_source_text =newdoc.createTextNode(ip_from)
    ip_source.appendChild(ip_source_text)
    
    load_port = newdoc.createElement("port_to")
    load_port_text =newdoc.createTextNode(port_to)
    load_port.appendChild(load_port_text)    

    source_port = newdoc.createElement("port_from")
    source_port_text =newdoc.createTextNode(port_from)
    source_port.appendChild(source_port_text)    

    load_curr = newdoc.createElement("current_to")
    load_curr_text =newdoc.createTextNode(current_to)
    load_curr.appendChild(load_curr_text)    

    source_curr = newdoc.createElement("current_from")
    source_curr_text =newdoc.createTextNode(current_from)
    source_curr.appendChild(source_curr_text)
    
    load_volt = newdoc.createElement("voltage_to")
    load_volt_text =newdoc.createTextNode(voltage_to)
    load_volt.appendChild(load_volt_text)    

    source_volt = newdoc.createElement("voltage_from")
    source_volt_text =newdoc.createTextNode(voltage_from)
    source_volt.appendChild(source_volt_text)



    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    
    body.appendChild(ip_load)
    body.appendChild(ip_source)
    body.appendChild(load_port)
    body.appendChild(source_port)
    body.appendChild(load_curr)
    body.appendChild(source_curr)
    body.appendChild(load_volt)
    body.appendChild(source_volt)
    
    top_element.appendChild(header)
    top_element.appendChild(body)
    newdoc.writexml( open('er_er_connect.xml', 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    newdoc.unlink()
    f = open('er_er_connect.xml','r')
    data =f.read()
    f.close()
    #print data
    return data

def create_xml_source_poll(number,file_name):
    impl = getDOMImplementation()

    newdoc = impl.createDocument(None, "Message", None)
    top_element = newdoc.documentElement
    header =newdoc.createElement("Header")

    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('poll')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Source')
    noun.appendChild(noun_text)

    id_no = newdoc.createElement("id")
    id_no_text =newdoc.createTextNode(number)
    
    id_no.appendChild(id_no_text)

    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    top_element.appendChild(header)
    #text = newdoc.createTextNode('Some textual content.')
    #top_element.appendChild(text)
    #print("lala")
    newdoc.writexml( open(file_name, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
 
    newdoc.unlink()

def create_xml_file_connect(file_name,Mac_address,ip):
    impl = getDOMImplementation()
    
    newdoc= impl.createDocument(None,'Message',None)
    top_element =newdoc.documentElement
    header =newdoc.createElement("Header")
    body   =newdoc.createElement("Body")
    
    
    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('connect')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Master')
    noun.appendChild(noun_text)

    id_no = newdoc.createElement("Router_id")
    id_no_text =newdoc.createTextNode(Mac_address.strip())
    id_no.appendChild(id_no_text)    

    IP_addr = newdoc.createElement("IP_address")
    IP_addr_text =newdoc.createTextNode(ip)
    IP_addr.appendChild(IP_addr_text)

    #Port_no = newdoc.createElement("Port_no")
    #Port_no_text =newdoc.createTextNode(str(port_no).strip())
    #Port_no.appendChild(Port_no_text)
    
    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    
    body.appendChild(IP_addr)
    #body.appendChild(Port_no)
    
    top_element.appendChild(header)
    top_element.appendChild(body)
    
    newdoc.writexml( open(file_name, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
 
    newdoc.unlink()

def create_xml_broadcast_request(Mac_address,ip,ip_load,current,voltage):

    impl = getDOMImplementation()
    
    newdoc= impl.createDocument(None,'Message',None)
    top_element =newdoc.documentElement
    header =newdoc.createElement("Header")
    body   =newdoc.createElement("Body")
    
    
    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('Request')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Master')
    noun.appendChild(noun_text)

    type_er = newdoc.createElement("type")
    type_text =newdoc.createTextNode('Energy_Router')
    type_er.appendChild(type_text)

    """priority = newdoc.createElement("value")
    priority_text =newdoc.createTextNode(value)
    priority.appendChild(priority_text)"""
    
    
    id_no = newdoc.createElement("Router_id")
    id_no_text =newdoc.createTextNode(Mac_address.strip())
    id_no.appendChild(id_no_text)    
    
    IP_addr = newdoc.createElement("IP_address")
    IP_addr_text =newdoc.createTextNode(ip)
    IP_addr.appendChild(IP_addr_text)    
    
    IP_addr_load = newdoc.createElement("IP_address_load")
    IP_addr_load_text =newdoc.createTextNode(ip_load)
    IP_addr_load.appendChild(IP_addr_load_text)
    
    curr = newdoc.createElement("current")
    curr_text =newdoc.createTextNode(current)
    curr.appendChild(curr_text)    

    volt = newdoc.createElement("voltage")
    volt_text =newdoc.createTextNode(voltage)
    volt.appendChild(volt_text)    

    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    
    body.appendChild(IP_addr)
    body.appendChild(IP_addr_load)
    body.appendChild(curr)
    body.appendChild(volt)
    #body.appendChild(priority)
    
    top_element.appendChild(header)
    top_element.appendChild(body)
    newdoc.writexml( open('broadcast_req.xml', 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    newdoc.unlink()
    f = open('broadcast_req.xml','r')
    data =f.read()
    f.close()
    #print data
    return data
    

def create_xml_broadcast_confirm(Mac_address,ip,ip_load,current,current_enquire,voltage):

    impl = getDOMImplementation()
    
    newdoc= impl.createDocument(None,'Message',None)
    top_element =newdoc.documentElement
    header =newdoc.createElement("Header")
    body   =newdoc.createElement("Body")
    
    
    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('Acknowledgment')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Master')
    noun.appendChild(noun_text)

    type_er = newdoc.createElement("type")
    type_text =newdoc.createTextNode('Energy_Router')
    type_er.appendChild(type_text)


    id_no = newdoc.createElement("Router_id")
    id_no_text =newdoc.createTextNode(Mac_address.strip())
    id_no.appendChild(id_no_text)    
    
    IP_addr = newdoc.createElement("IP_address")
    IP_addr_text =newdoc.createTextNode(ip)
    IP_addr.appendChild(IP_addr_text)    

    IP_addr_load = newdoc.createElement("IP_address_load")
    IP_addr_load_text =newdoc.createTextNode(ip_load)
    IP_addr_load.appendChild(IP_addr_load_text)
    
    curr = newdoc.createElement("current")
    curr_text =newdoc.createTextNode(current)
    curr.appendChild(curr_text)    

    curr_enquire = newdoc.createElement("current_enquire")
    curr_enquire_text =newdoc.createTextNode(current_enquire)
    curr_enquire.appendChild(curr_enquire_text)

    volt = newdoc.createElement("voltage")
    volt_text =newdoc.createTextNode(voltage)
    volt.appendChild(volt_text)    

    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    
    body.appendChild(IP_addr)
    body.appendChild(IP_addr_load)
    body.appendChild(curr)
    body.appendChild(curr_enquire)
    body.appendChild(volt)
    
    top_element.appendChild(header)
    top_element.appendChild(body)
    newdoc.writexml( open('broadcast_req.xml', 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    newdoc.unlink()
    f = open('broadcast_req.xml','r')
    data =f.read()
    f.close()
    #print data
    return data



    
def create_xml_file_response(Mac_address,ip,current,voltage):

    impl = getDOMImplementation()
    
    newdoc= impl.createDocument(None,'Message',None)
    top_element =newdoc.documentElement
    header =newdoc.createElement("Header")
    body   =newdoc.createElement("Body")
    
    
    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('Response')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Master')
    noun.appendChild(noun_text)

    type_er = newdoc.createElement("type")
    type_text =newdoc.createTextNode('Energy_Router')
    type_er.appendChild(type_text)


    id_no = newdoc.createElement("Router_id")
    id_no_text =newdoc.createTextNode(Mac_address.strip())
    id_no.appendChild(id_no_text)    
    
    IP_addr = newdoc.createElement("IP_address")
    IP_addr_text =newdoc.createTextNode(ip)
    IP_addr.appendChild(IP_addr_text)    
    
    curr = newdoc.createElement("current")
    curr_text =newdoc.createTextNode(current)
    curr.appendChild(curr_text)    

    volt = newdoc.createElement("voltage")
    volt_text =newdoc.createTextNode(voltage)
    volt.appendChild(volt_text)    

    header.appendChild(value)
    header.appendChild(noun)
    header.appendChild(id_no)
    
    body.appendChild(IP_addr)
    body.appendChild(curr)
    body.appendChild(volt)
    
    top_element.appendChild(header)
    top_element.appendChild(body)
    newdoc.writexml( open('broadcast_req.xml', 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
    newdoc.unlink()
    f = open('broadcast_req.xml','r')
    data =f.read()
    f.close()
    #print data
    return data    
    
def create_xml_multicast_response(file_name,Mac_address,ip):

    impl = getDOMImplementation()
    
    newdoc= impl.createDocument(None,'Message',None)
    top_element =newdoc.documentElement
    header =newdoc.createElement("Header")
    body   =newdoc.createElement("Body")
    
    
    value  =newdoc.createElement("Verb")
    value_text = newdoc.createTextNode('Multicast_response')
    value.appendChild(value_text)

    noun = newdoc.createElement("Noun")
    noun_text =newdoc.createTextNode('Master')
    noun.appendChild(noun_text)

    id_no = newdoc.createElement("Router_id")
    id_no_text =newdoc.createTextNode(Mac_address.strip())
    id_no.appendChild(id_no_text)    
    
    IP_addr = newdoc.createElement("IP_address")
    IP_addr_text =newdoc.createTextNode(ip)
    IP_addr.appendChild(IP_addr_text)    

    header.appendChild(value)
    header.appendChild(noun)
    
    body.appendChild(id_no)
    body.appendChild(IP_addr)

    top_element.appendChild(header)
    top_element.appendChild(body)

    newdoc.writexml( open(file_name, 'w'),
               indent="  ",
               addindent="  ",
               newl='\n')
 
    newdoc.unlink()
 
     
    
if __name__ == '__main__':
        #create_xml_file_poll('1256','try_19.xml')
        #create_xml_file_connect('connect_2.xml',"10.156.02.0143.156","10.14.56.253",223)
         data = create_xml_broadcast_request('20:56:45:25:34:55','192.168.0.102','192.168.0.106','8.2' ,'12')
         try:
                   tag_name = data.getElementsByTagName("Verb")
         except:
                   print("The document file recived is not correct")
