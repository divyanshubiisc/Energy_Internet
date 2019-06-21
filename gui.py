from Tkinter import *
from threading import Timer
from main_codes.gui import table_gui
from global_var import setting
from time import sleep

def update_port():
	global router_table 

	while True:
           fb_list     =      setting.common.Feedback_list
           i=0
           l1 =[]
           while i <len(fb_list):
                     l1.append((fb_list[i].voltage_port1,fb_list[i].voltage_port2))
                     i= i+1
                   
           router_table.update(l1)

def start_gui():
	global router_table
	root =Tk()
	root.wm_title("Load List")
	router_table = table_gui.McListBox(['port_1','port_2'],[])
	t1 = Timer(5,update_port,args=[])
	t1.daemon   = True
	t1.start()
	root.mainloop()

def main():
    	t0 =Timer(5,start_gui,args=[])
	t0.daemon   = True
	t0.start()
        while True:
          pass
          sleep(5)
