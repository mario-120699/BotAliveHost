import sys
import subprocess
from pprint import pprint
import json
from time import localtime, strftime
import os
import botogram
import threading

host_list = list()
ping_thread_list = list()
log_lock = threading.Lock()

# bot creation
bot = botogram.create('437678547:AAGRK9W1eQgGVKawmg0C7MElfy6OFZsYZmc')
bot.owner = "@Mariob99"
chatid = 139024889


class Host:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def get_ip(self):
        return self.ip

    def get_name(self):
        return self.name

def send_all_message(chat, message, string):
    print(string)
    chat.send(string)
    with log_lock:
        with open('aliveHosts.log', 'a') as log_file:
            log_file.write(string)


def create_log_string(chat, message, name, ip, is_dead = False, start_log = False, end_log = False):
    string_formatted = str()
    string_formatted += strftime("%Y-%m-%d %H:%M:%S", localtime())
    if start_log:
        string_formatted += '  startLog\n'
        send_all_message(chat, message, string_formatted)
        return
    elif end_log:
        string_formatted += '  endLog\n'
        send_all_message(chat, message, string_formatted)
        return
    string_formatted += ', ' + name + ', ' + ip
    if is_dead:
        string_formatted += 'DEAD\n'
    else:
        string_formatted += 'ALIVE\n'
    send_all_message(chat, message, string_formatted)
    return


def create_host_list():
    global host_list
    with open('hosts.json', 'r') as f:
        stringa = f.read()
        data = json.loads(stringa)
    for i in data.keys():
        host_list.append(Host(i, data[i]))


def ping_work(chat, message, name, ip):
    back = int()
    global log_lock
    subp = subprocess.call('ping -n 1'+ ip, stdout=open(os.devnull, 'wb'))  # primo ping per vedere se l'Host è attivo o no
    back = subp
    while 1:
        subp = subprocess.call('ping -n 1'+ ip, stdout=open(os.devnull, 'wb'))
        if back != subp:
            create_log_string(chat, message, name, ip, subp, False, False)
            back = subp


def create_thread_list(chat, message):
    global host_list
    global ping_thread_list
    for host in host_list:
        thread_list.append(threading.Thread(target = ping_work ,args = (chat, message, host.get_name(), host.get_ip(),)))


@bot.command("StartPingWork")
def start_ping_work(chat, message):
    global ping_thread_list
    global log_lock
    global host_list
    if len(thread_list) <= 0:
        create_thread_list(chat, message)
    create_log_string(chat, message, ' ',' ', False, True, False)
    for t in thread_list:
        t.start()
        t.join()


@bot.command("StopPingWork")
def stop_ping_work(chat, message):
    global ping_thread_list
    for t in thread_list:
        t._stop()
    create_log_string(chat, message, ' ',' ', False, False, True)


def main():
    create_host_list()

if __name__ == '__main__':
    main()