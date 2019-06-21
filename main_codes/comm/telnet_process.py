import os
import sys
import re


def process():
	 f = open("Net_Table.txt","r"):
	 msg =f.read()
	 f.close()
	 mac_table = re.findall("^.*Mac_Table.*$",msg,re.MULTILINE)
	 print(mac_table)
	 
