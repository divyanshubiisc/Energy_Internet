import xml.dom.minidom   # used for file parsing


def Load_parse(doc):
                       arr         = []
                       id_load     = doc.getElementsByTagName("id")
                       id_load     = id_load[0].firstChild.nodeValue.encode('utf-8')
                       id_load     = id_load.strip()
                       type_load   = doc.getElementsByTagName("type")
                       type_load   = type_load[0].firstChild.nodeValue.encode('utf-8')
                       type_load   = type_load.strip()
                       value_load  = doc.getElementsByTagName("value")
                       value_load  = value_load[0].firstChild.nodeValue.encode('utf-8')
                       value_load  = value_load.strip()
                       voltage     = doc.getElementsByTagName("voltage")
                       voltage     = voltage[0].firstChild.nodeValue.encode('utf-8')
                       voltage     = voltage.strip()
                       current     = doc.getElementsByTagName("current")
                       current     = current[0].firstChild.nodeValue.encode('utf-8')
                       current     = current.strip()
                       try:
                           min_volt_load    = doc.getElementByTagName("Min_Voltage")
                           min_volt_load = min_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           min_volt_load = min_volt_load.strip()
                       except:
                           min_volt_load = None
                       try:
                           max_volt_load    = doc.getElementsByTagName("Max_Voltage")
                           max_volt_load = max_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           max_volt_load = max_volt_load.strip()
                       except:
                           max_volt_load = None
                       try:
                           min_current_load  = doc.getElementsByTagName("Min_Current")
                           min_current_load = min_current_load[0].firstChild.nodeValue.encode('utf-8')
                           min_current_load = min_current_load.strip()
                       except:
                           min_current_load = None
                       try:
                           max_current_load = doc.getElementsByTagName("Max_Current")
                           max_current_load = max_current_load[0].firstChild.nodeValue.encode('utf-8')
                           max_current_load = max_current_load.strip()
                       except:
                           max_current_load = None
#                       try:
#			   curr_req_load    = doc.getElementsByTagName("Current_req")
#			   curr_req_load    = curr_req_load[0].firstChild.nodeValue.encode('utf-8')
#			   curr_req_load    = curr_req_load.strip()
#		       except:
#			   curr_req_load    = 0.2
					   
                       arr.extend([id_load,type_load,value_load,voltage,current,min_volt_load,max_volt_load,min_current_load,max_current_load])
                       return arr
def Source_parse(doc):
                       arr           = []
                       id_source     = doc.getElementsByTagName("id")
                       id_source     = id_source[0].firstChild.nodeValue.encode('utf-8')
                       id_source     = id_source.strip()
                       type_source   = doc.getElementsByTagName("type")
                       type_source   = type_source[0].firstChild.nodeValue.encode('utf-8')
                       type_source   = type_source.strip()
                       voltage     = doc.getElementsByTagName("voltage")
                       voltage     = voltage[0].firstChild.nodeValue.encode('utf-8')
                       voltage     = voltage.strip()
                       current     = doc.getElementsByTagName("current")
                       current     = current[0].firstChild.nodeValue.encode('utf-8')
                       current     = current.strip()
                       try:
                           min_volt_source    = doc.getElementByTagName("Min_Voltage")
                           min_volt_source = min_volt_source[0].firstChild.nodeValue.encode('utf-8')
                           min_volt_source = min_volt_source.strip()
                       except:
                           min_volt_source = None
                       try:
                           max_volt_source    = doc.getElementsByTagName("Max_Voltage")
                           max_volt_source = max_volt_source[0].firstChild.nodeValue.encode('utf-8')
                           max_volt_source = max_volt_source.strip()
                       except:
                           max_volt_source = None
                       try:
                           min_current_source  = doc.getElementsByTagName("Min_Current")
                           min_current_source = min_current_source[0].firstChild.nodeValue.encode('utf-8')
                           min_current_source = min_current_source.strip()
                       except:
                           min_current_source = None
                       try:
                           max_current_source  =doc.getElementsByTagName("Max_Current")
                           max_current_source = max_current_source[0].firstChild.nodeValue.encode('utf-8')
                           max_current_source = max_current_source.strip()
                       except:
                           max_current_source = None
#                       try:
#                           current_aval  =doc.getElementsByTagName("Current_aval")
#                           current_aval = current_aval[0].firstChild.nodeValue.encode('utf-8')
#                           current_aval = current_aval.strip()
#                       except:
#                           current_aval = 0.4

                       arr.extend([id_source,type_source,voltage,current,min_volt_source,max_volt_source,min_current_source,max_current_source])
                       return arr


def Broadcast_req_parse(doc):
                       arr         = []
                       #print("Entered the query ")
                       Router_id   = doc.getElementsByTagName("Router_id")
                       Router_id   = Router_id[0].firstChild.nodeValue.encode('utf-8')
                       Router_id.strip()
                       IP_address  = doc.getElementsByTagName("IP_address")
                       IP_address  =  IP_address[0].firstChild.nodeValue.encode('utf-8')
                       IP_address.strip()
                       voltage     = doc.getElementsByTagName("voltage")
                       voltage     = voltage[0].firstChild.nodeValue.encode('utf-8')
                       voltage     = voltage.strip()
                       current     = doc.getElementsByTagName("current")
                       current     = current[0].firstChild.nodeValue.encode('utf-8')
                       current     = current.strip()
                       """value     = doc.getElementsByTagName("value")
                       value     = value[0].firstChild.nodeValue.encode('utf-8')
                       value     = value.strip() """ 
                       try:
                           min_volt_load    = doc.getElementByTagName("Min_Voltage")
                           min_volt_load = min_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           min_volt_load = min_volt_load.strip()
                       except:
                           min_volt_load = None
                       try:
                           max_volt_load    = doc.getElementsByTagName("Max_Voltage")
                           max_volt_load = max_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           max_volt_load = max_volt_load.strip()
                       except:
                           max_volt_load = None
                       try:
                           min_current_load  = doc.getElementsByTagName("Min_Current")
                           min_current_load = min_current_load[0].firstChild.nodeValue.encode('utf-8')
                           min_current_load = min_current_load.strip()
                       except:
                           min_current_load = None
                       try:
                           max_current_load = doc.getElementsByTagName("Max_Current")
                           max_current_load = max_current_load[0].firstChild.nodeValue.encode('utf-8')
                           max_current_load = max_current_load.strip()
                       except:
                           max_current_load = None
                       #print("The arr master extension")
                       arr.extend([Router_id,IP_address,voltage,current,min_volt_load,max_volt_load,min_current_load,max_current_load])
                       #print (arr)
                       return arr  

                      
def update_parse(doc):
                       arr         = []
                       id_load     = doc.getElementsByTagName("id")
                       id_load     = id_load[0].firstChild.nodeValue.encode('utf-8')
                       id_load     = id_load.strip()
                       type_load   = doc.getElementsByTagName("type")
                       type_load   = type_load[0].firstChild.nodeValue.encode('utf-8')
                       type_load   = type_load.strip()
                       value_load  = doc.getElementsByTagName("value")
                       value_load  = value_load[0].firstChild.nodeValue.encode('utf-8')
                       value_load  = value_load.strip()
                       try:
                           min_volt_load    = doc.getElementByTagName("Min_Voltage")
                           min_volt_load = min_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           min_volt_load = min_volt_load.strip()
                       except:
                           min_volt_load = None
                       try:
                           max_volt_load    = doc.getElementsByTagName("Max_Voltage")
                           max_volt_load = max_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           max_volt_load = max_volt_load.strip()
                       except:
                           max_volt_load = None
                       try:
                           min_current_load  = doc.getElementsByTagName("Min_Current")
                           min_current_load = min_current_load[0].firstChild.nodeValue.encode('utf-8')
                           min_current_load = min_current_load.strip()
                       except:
                           min_current_load = None
                       try:  
                           max_current_load  =doc.getElementsByTagName("Max_Current")
                           max_current_load = max_current_load[0].firstChild.nodeValue.encode('utf-8')
                           max_current_load = max_current_load.strip()
                       except:
                           max_current_load = None
                       arr.extend([id_load,type_load,value_load,min_volt_load,max_volt_load,min_volt_load,min_current_load,max_current_load])
                       return arr
def master_query_parse(doc):
                       arr         = []
                       #print("Entered the query ")
                       Router_id   = doc.getElementsByTagName("Router_id")
                       Router_id   = Router_id[0].firstChild.nodeValue.encode('utf-8')
                       Router_id.strip()
                       IP_address  = doc.getElementsByTagName("IP_address")
                       IP_address  =  IP_address[0].firstChild.nodeValue.encode('utf-8')
                       IP_address.strip()
                       #print("The arr master extension")
                       arr.extend([Router_id,IP_address])
                       #print (arr)
                       return arr

"""
def Broadcast_req_parse(doc):
                       arr         = []
                       #print("Entered the query ")
                       Router_id   = doc.getElementsByTagName("Router_id")
                       Router_id   = Router_id[0].firstChild.nodeValue.encode('utf-8')
                       Router_id.strip()
                       IP_address  = doc.getElementsByTagName("IP_address")
                       IP_address  =  IP_address[0].firstChild.nodeValue.encode('utf-8')
                       IP_address.strip()
                       voltage     = doc.getElementsByTagName("voltage")
                       voltage     = voltage[0].firstChild.nodeValue.encode('utf-8')
                       voltage     = voltage.strip()
                       current     = doc.getElementsByTagName("current")
                       current     = current[0].firstChild.nodeValue.encode('utf-8')
                       current     = current.strip() 
                       try:
                           min_volt_load    = doc.getElementByTagName("Min_Voltage")
                           min_volt_load = min_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           min_volt_load = min_volt_load.strip()
                       except:
                           min_volt_load = None
                       try:
                           max_volt_load    = doc.getElementsByTagName("Max_Voltage")
                           max_volt_load = max_volt_load[0].firstChild.nodeValue.encode('utf-8')
                           max_volt_load = max_volt_load.strip()
                       except:
                           max_volt_load = None
                       try:
                           min_current_load  = doc.getElementsByTagName("Min_Current")
                           min_current_load = min_current_load[0].firstChild.nodeValue.encode('utf-8')
                           min_current_load = min_current_load.strip()
                       except:
                           min_current_load = None
                       try:
                           max_current_load = doc.getElementsByTagName("Max_Current")
                           max_current_load = max_current_load[0].firstChild.nodeValue.encode('utf-8')
                           max_current_load = max_current_load.strip()
                       except:
                           max_current_load = None
                       #print("The arr master extension")
                       arr.extend([Router_id,IP_address,voltage,current,min_volt_load,max_volt_load,min_current_load,max_current_load])
                       #print (arr)
                       return arr

"""
if __name__ == '__main__':
        doc= xml.dom.minidom.parse('try1.xml')
        arr = Load_parse(doc)
        print(arr)                     
