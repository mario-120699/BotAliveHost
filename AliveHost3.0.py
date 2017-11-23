import pzgram
import json
import subprocess
from time import localtime, strftime
from subprocess import Popen
from threading import Thread, Lock
from re import findall, search

# bot creation
token = '437678547:AAGRK9W1eQgGVKawmg0C7MElfy6OFZsYZmc'
bot = pzgram.Bot(token)
bot.owner="@Mariob99"
# create Lock
log_lock = Lock()
port_lock = Lock()
# create global variables
host_list = list()
ping_thread_list = list()
port_thread_list = list()
port_thread_single = list()


class Port:  # classe per la gestione delle porte con tutte le caratteristiche necessarie
    def __init__(self, port_number, port_state, port_name):
        self.number = port_number
        self.state = port_state
        self.name = port_name

    def get_number(self):
        return self.number

    def get_state(self):
        return self.state

    def get_name(self):
        return self.name


class Host:  # class Host per la gestione delle variabili del host
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip

    def get_ip(self):
        return self.ip

    def get_name(self):
        return self.name


class ThreadPortSingle(Thread):  # classe derivata da threading.Thread fatta appositamente per il test nmap con le variabili chat e send per la communicazione tramite bot
    def __init__(self, name, ip, chat, message):
        Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port_list = list()
        self.chat = chat
        self.message = message

    def run(self):
        print("Start nmap for {}".format(self.ip))
        command = "nmap -p 22 -v {}".format(self.ip)
        out_string = Popen(command, stdout=subprocess.PIPE, shell=True).communicate()
        result = findall('([0-9]+)/[a-z]+[ ]+([a-z]+)[ ]+([a-z-]+)', str(out_string))
        for r_e in result:
            port = int(r_e[0])
            state = str(r_e[1])
            name = str(r_e[2])
            self.port_list.append(Port(port, state, name))
        if self.port_list:
            print('Done for ip {}, port 22 port is opened!'.format(self.ip))
            self.chat.send('Done for ip {}, port 22 port is opened!'.format(self.ip))
        else:
            print('Done for ip {}, port 22 port is closed!'.format(self.ip))
            self.chat.send('Done for ip {}, port 22 port is closed!'.format(self.ip))


class ThreadPortList(Thread):  # classe derivata da threading.Thread fatta appositamente per il test nmap con le variabili chat e send per la communicazione tramite bot
    def __init__(self, name, ip, chat, message):
        Thread.__init__(self)
        self.name = name
        self.ip = ip
        self.port_list = list()
        self.chat = chat
        self.message = message

    def run(self):
        print("Start nmap for {}".format(self.ip))
        command = "nmap -p 1-65535 -v {}".format(self.ip)
        out_string = Popen(command,stdout=subprocess.PIPE, shell=True).communicate()
        result = findall('([0-9]+)/[a-z]+[ ]+([a-z]+)[ ]+([a-z-]+)', str(out_string))
        for r_e in result:
            port = int(r_e[0])
            state = str(r_e[1])
            name = str(r_e[2])
            self.port_list.append(Port(port, state, name))
        self.write_result()

    def write_result(self):
        global port_lock
        with port_lock:
            with open('PortState.txt', 'a') as f:
                string_formatted = '\n'
                string_formatted += strftime("%Y-%m-%d %H:%M:%S", localtime())
                string_formatted += ' Port results for {}\n\n'.format(self.ip)
                for port in self.port_list:
                    string_formatted += str(port.get_number()) + ', '
                    string_formatted += port.get_name() + ', '
                    string_formatted += port.get_state() + ', '
                    string_formatted += '\n'
                f.write(string_formatted)
            print('Done for ip {}, detected {}  port opened/filtered!'.format(self.ip,str(len(self.port_list))))
            self.chat.send('Done for ip {}, detected {}  port opened/filtered!'.format(self.ip,str(len(self.port_list))))


class ThreadPing(Thread):  # classe derivata da threading.Thread fatta appositamente per il test del ping con le variabili chat e send per la communicazione tramite bot
    def __init__(self, name, addr, chat, message):
        Thread.__init__(self)
        self.ip = addr  # ip server
        self.name = name  # nome server
        self.back_state = True  # 0 se non riceve nessun pachetto, viceversa 1
        self.alive_thread = True  # variabile per arrestare il thread
        self.chat = chat
        self.message = message

    def run(self):
        while self.alive_thread:  # finchè è true il thread rimane attivo
            ping_command = 'ping -n 1 -w 2000 {}'.format(self.ip)
            out_string = Popen(ping_command,stdout=subprocess.PIPE, shell=True).communicate()
            if search('Ricevuti = 0', str(out_string)) and self.back_state:  # ping non andato a buon fine
                log_string = self.create_log_string(True)
                self.send_all_msg(log_string)
                self.back_state = 0
            elif search('Ricevuti = 1', str(out_string))and not self.back_state:  # ping andato a buon fine
                log_string = self.create_log_string(False)
                self.send_all_msg(log_string)
                self.back_state = 1

    def create_log_string(self, is_dead=False):
        string_formatted = str()
        string_formatted += strftime("%Y-%m-%d %H:%M:%S", localtime())
        string_formatted += ', {}, {} '.format(self.name, self.ip)
        if is_dead:
            string_formatted += ' DEAD\n'
        else:
            string_formatted += ' ALIVE\n'
        return string_formatted

    def send_all_msg(self, string):
            global log_lock
            self.chat.send(string)
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


def create_thread_port_single_list(chat, message):
    global host_list
    global port_thread_single
    for host in host_list:
        port_thread_single.append(ThreadPortSingle(host.get_name(), host.get_ip(), chat, message))


def create_thread_list(chat, message):
    global host_list
    global ping_thread_list
    for host in host_list:
        ping_thread_list.append(ThreadPing(host.get_name(), host.get_ip(), chat, message))


def create_thread_port_list(chat, message):
    global host_list
    global port_thread_list
    for host in host_list:
        port_thread_list.append(ThreadPortList(host.get_name(), host.get_ip(), chat, message))


def start_all_thread(chat, message):
    log_string = create_log_string_init_and_end(True)
    global Log_lock
    chat.send(log_string)
    with log_lock:
        with open('aliveHosts.log', 'a') as log_file:
            log_file.write(log_string)
    print(log_string)
    global ping_thread_list
    for thread in ping_thread_list:
        thread.start()


def start_port_thread(chat, message):
    global port_thread_list
    for thread in port_thread_list:
        thread.start()


def start_single_port_thread(chat, message):
    global port_thread_single
    for thread in port_thread_single:
        thread.start()


def stop_all_thread(chat, message):
    log_string = create_log_string_init_and_end(False)
    global log_lock
    chat.send(log_string)
    with log_lock:
        with open('aliveHosts.log', 'a') as log_file:
            log_file.write(log_string)
    print(log_string)
    global ping_thread_list
    for thread in ping_thread_list:
        thread.change_alive_thread()
        thread.join()


def start_command(chat, message):  # funzione di prova
    chat.send("Ciao sono PyAliveHost, il bot multifunzione che ti permette di avere informazioni " +
              "dettagliate sulle reti\nPer vedere i singoli comandi digitale /help")


def StartPingCommand(chat, message):  # "interfaccia" di communicazione tra il bot e i vari threads,
    global host_list                  # con questo stoppa tutti thread inerenti al ping
    if len(host_list) == 0:
        create_host_list()
    create_thread_list(chat, message)
    start_all_thread(chat, message)


def StopPingCommand(chat, message):  # "interfaccia" di communicazione tra il bot e i vari threads, con questo stoppa tutti thread inerenti al ping
    stop_all_thread(chat, message)


def SearchPortList(chat, message):  # "interfaccia" di communicazione tra il bot e i vari threads, con questo fa partire tutti i thread per cercare i servizi disponibili per ogni host
    global host_list
    if len(host_list) == 0:
        create_host_list()
    create_thread_port_list(chat, message)
    start_port_thread(chat, message)


def RenewHostList(chat, message):  # Rinnova la lista degli Host e se è vuota tenta di farla
    global host_list
    if len(host_list) == 0:
        create_host_list()
    else:
        host_list.clear()
        create_host_list()
    chat.send('Done')


def SearchPort22(chat, message):
    global host_list
    if len(host_list) == 0:
        create_host_list()
    create_thread_port_single_list(chat, message)
    start_single_port_thread(chat, message)


if __name__== "__main__":
    bot.set_commands({'/start': start_command, '/StartPingWork': StartPingCommand, '/StopPingWork': StopPingCommand, '/SearchPortList': SearchPortList, '/RenewHostList': RenewHostList, '/SearchPort22': SearchPort22})
    bot.run()