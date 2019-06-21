import power_master
#import receive_xml
import broadcast
import receive_xml_copy
from time import sleep
import gui
if __name__ == '__main__':
    power_master.start_power_master()
    # sleep(5)
    #gui.main()
    receive_xml_copy.start_receive()
    #receive_xml.start_receive()
    broadcast.broadcast_conf()
