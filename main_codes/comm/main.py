import socket
import select
import sys
sys.path.append('/home/pi/Desktop/PC_ER/ER/Energy_Router/')
import threading
import os
import netifaces as ni   # to get a interface ip address
import random            # to produce random number for a file
import xml.dom.minidom   # used for file parsing
from collections import namedtuple #used for making structure 
import time
import errno
import subprocess
from socket import error as socket_error
from astropy.table import Table
from global_var  import load_param, source_param
#from global_var import 
from XML import *
from Network import net_tools as network
from Network import *
