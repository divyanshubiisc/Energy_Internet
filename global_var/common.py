import threading

global lock
global Load_list
global Source_list
global Feedback_list
global comm_to_power_change_event
global ip_address
global current_avail
global current_req
global broadcast_flag 
current_avail =0.0
current_req =0.0
temp_current =0.0
comm_to_power_change_event = threading.Event()
lock = threading.Lock()
Load_list =[]
Source_list=[]
extern_Load_list=[]
extern_Source_list=[]
Feedback_list=[]
traceroute_recived = {}
traceroute_send = {}
ack_send ={}
broadcast_flag =0 
