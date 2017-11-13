import re
import sys
import subprocess


port_list = list()

class Port:

    def __init__(self, port_number, port_state, port_name):
        self.number = port_number
        self.state = port_state
        self.name = port_name

    def __repr__(self):
        return self.name + ' ' + str(self.number) + ' ' + self.state

def nmap_work(ip):
    global port_list
    port = int()
    state = str()
    name = str()
    command = "nmap -p 1-65535 -v " + ip
    out = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True).communicate()
    print("end of nmap")
    result = re.findall("([0-9]+)/[a-z]+[ ]+([a-z]+)[ ]+([a-z-]+)", str(out))
    for r_e in result:
        port = int(r_e[0])
        state = str(r_e[1])
        name = str(r_e[2])
        port_list.append(Port(port,state, name))

nmap_work("188.209.80.62")
print(port_list)