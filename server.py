"""
author: Alexey Aleshchenok
date: 2023-12-05
Server program that has six commands to perform::
'Dir' - dir_cmd,
'Delete' - delete_cmd,
'Copy' - copy_cmd,
'Execute' - execute_cmd,
'Take_screenshot' - take_screenshot_cmd,
'Exit' - exit_cmd
"""
import socket
from protocol import receive
from functions import dir_cmd, delete_cmd, copy_cmd, execute_cmd, take_screenshot_cmd, exit_cmd

IP = '0.0.0.0'
PORT = 49002
QUEUE_SIZE = 1
MAX_PACKET = 4


def main():
    """main function"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print('Waiting for connection....')
        while True:
            comm_socket, addr = server_socket.accept()
            print(f'Connection with {addr}')
            try:
                while True:
                    request = receive(comm_socket).decode()
                    request = request.split(' ')

                    if request[0] == 'Dir':
                        comm_socket.send(dir_cmd(request[1].encode()))
                    elif request[0] == 'Delete':
                        comm_socket.send(delete_cmd(request[1].encode()))
                    elif request[0] == 'Copy':
                        comm_socket.send(copy_cmd(request[1].encode()))
                    elif request[0] == 'Execute':
                        comm_socket.send(execute_cmd(request[1].encode()))
                    elif request[0] == 'Take_screenshot':
                        comm_socket.send(take_screenshot_cmd())
                    elif request[0] == 'Exit':
                        comm_socket.send(exit_cmd())

            except socket.error as msg:
                print('Failed to open client socket - ' + str(msg))
            finally:
                comm_socket.close()
            print('Waiting for connection....')
    except socket.error as msg:
        print('Failed to open server socket - ' + str(msg))
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
