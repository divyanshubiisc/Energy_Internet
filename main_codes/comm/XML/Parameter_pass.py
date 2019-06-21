#import xml_process
from global_var import load_param, source_param
#import xml.dom.minidom  
def Load_mapping(obj,arr,address,port):
	#ip_address = addr[0] , id = arr[0] , type =arr[1], value =arr[2] , min_volt=arr[3] , max_volt = arr[4] , min_curr = arr[5], max_curr =arr[6]
	obj.ip_address = address
	obj.id =arr[0]
	obj.type =arr[1]
	obj.value =arr[2]
	obj.voltage =float(arr[3])
        obj.current =arr[4]
	obj.min_volt = arr[5]
	obj.max_volt =arr[6]
	obj.min_curr =arr[7]
	obj.max_curr =arr[8]
	obj.current_reqd = float(arr[4])
	obj.state =1
	obj.port  =port
	return obj


def Source_mapping(obj,arr,address,port):
	#ip_address = addr[0] , id = arr[0] , type =arr[1], value =arr[2] , min_volt=arr[3] , max_volt = arr[4] , min_curr = arr[5], max_curr =arr[6]
	obj.ip_address = address
	obj.id =arr[0]
	obj.type =arr[1]
	obj.value =arr[2]
        obj.voltage = float(arr[2])
        obj.current = arr[3]
	obj.min_volt = arr[4]
	obj.max_volt =arr[5]
	obj.min_curr =arr[6]
	obj.max_curr =arr[7]
	obj.current_aval = float(arr[3])
	obj.state =1
        obj.port  =port
	return obj





if __name__ == '__main__':
     doc= xml.dom.minidom.parse('try1.xml')
     arr = xml_process.Load_parse(doc)
     x = Load_mapping(load_param() ,arr ,'10.114.56.102')
     print(vars(x))
