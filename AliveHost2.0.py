import telepot, json, sys, subprocess
from time import localtime, strftime
from subprocess import Popen
from threading import Thread, Lock
from re import search

# create bot
token = '437678547:AAGRK9W1eQgGVKawmg0C7MElfy6OFZsYZmc'
MyBot = telepot.Bot(token)
chat_id_mario = 139024889
# create Lock
log_lock = Lock()
# create global variables
host_list = list()
ping_thread_list = list()

class Host:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def get_ip(self):
        return self.ip

    def get_name(self):
        return self.name

class ThreadPing(Thread):
    def __init__(self, name, chId, addr):
        Thread.__init__(self)
        self.chat_id = chId # chat di destinazione (telegram)
        self.ip = addr # ip server
        self.name = name # nome server
        self.back_state = True # 0 se non riceve nessun pachetto, viceversa 1
        self.alive_thread = True

    def run(self):
        while self.alive_thread: #finchè è true il thread rimane attivo
            ping_command = 'ping -n 1 ' + self.ip
            out_string = Popen(ping_command,stdout=subprocess.PIPE, shell=True).communicate()
            if search('Ricevuti = 0', str(out_string)) and self.back_state: # ping non andato a buon fine
                log_string = self.create_log_string(True)
                self.send_all_msg(log_string)
                self.back_state = 0
            elif search('Ricevuti = 1', str(out_string))and not self.back_state:
                log_string = self.create_log_string(False)
                self.send_all_msg(log_string)
                self.back_state = 1

    def create_log_string(self, is_dead=False):
        string_formatted = str()
        string_formatted += strftime("%Y-%m-%d %H:%M:%S", localtime())
        string_formatted += ', ' + self.name + ', ' + self.ip
        if is_dead:
            string_formatted += ' DEAD\n'
        else:
            string_formatted += ' ALIVE\n'
        return string_formatted


    def send_all_msg(self, string):
            global log_lock
            global MyBot
            MyBot.sendMessage(self.chat_id, string)
            with log_lock:
                with open('aliveHosts.log', 'a') as log_file:
                    log_file.write(string)
            print(string)

    def change_alive_thread(self):
        self.alive_thread = False

def create_log_string_init_and_end(start):
    string_formatted = str()
    string_formatted += strftime("%Y-%m-%d %H:%M:%S", localtime())
    if start:
        string_formatted += '  startLog\n'
    else:
        string_formatted += '  endLog\n'
    return string_formatted

def create_host_list():
    global host_list
    with open('hosts.json', 'r') as f:
        stringa = f.read()
        data = json.loads(stringa)
    for i in data.keys():
        host_list.append(Host(i, data[i]))

def create_thread_list():
    global host_list
    global ping_thread_list
    global chat_id_mario
    for host in host_list:
        thread_list.append(ThreadPing(host.get_name(), chat_id_mario, host.get_ip()))

def start_all_thread():
    log_string = create_log_string_init_and_end(True)
    global log_lock
    global MyBot
    global chat_id_mario
    MyBot.sendMessage(chat_id_mario, log_string)
    with log_lock:
        with open('aliveHosts.log', 'a') as log_file:
            log_file.write(log_string)
    print(log_string)
    global ping_thread_list
    for thread in thread_list:
        thread.start()

def stop_all_thread():
    log_string = create_log_string_init_and_end(False)
    global log_lock
    global MyBot
    global chat_id_mario
    MyBot.sendMessage(chat_id_mario, log_string)
    with log_lock:
        with open('aliveHosts.log', 'a') as log_file:
            log_file.write(log_string)
    print(log_string)
    global ping_thread_list
    for thread in thread_list:
        thread.change_alive_thread()
        thread.join()

def init(): # create host_list and thread_list
    create_host_list()
    create_thread_list()
    start_all_thread()

def main():
    init()
    try:
        ki = sys.stdin.read(1) # aspetta che venga inserito un carattere, fino ad allora il progamma sta fermo( con i thread che lavorano)
    except KeyboardInterruptc:
        pass
    finally:
        stop_all_thread()

if __name__ == '__main__':
    main()