"""
author: Alexey Aleshchenok
date: 2023-12-05
Client program that has four commands available
(to use command enter its name and after space the argument):
'Dir' - path to the file to read data from
'Delete' - path to the file to delete
'Copy' - two paths to files separated by comma to copy from one to another
'Execute' - name of the program to execute
'Take_screenshot' - doesn't need the argument
'Exit' - doesn't need the argument
"""
import socket
from protocol import send

SERVER_IP = '127.0.0.1'
SERVER_PORT = 49002
MAX_PACKET = 1024


def main():
    """main function"""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP, SERVER_PORT))
        print('You have connected to the server ')
        while True:
            request = input('Enter command: ')
            request = request.split(' ')
            if request[0] == 'Dir' or 'Delete' or 'Copy' or 'Execute' or 'Take_screenshot' or 'Exit':
                if len(request) == 2:
                    send(client_socket, request[0], request[1])
                    response = client_socket.recv(MAX_PACKET)
                    print(response.decode())
                elif len(request) == 1:
                    send(client_socket, request[0], None)
                    response = client_socket.recv(MAX_PACKET)
                    if request == ['Take_screenshot']:
                        try:
                            print(response.decode('utf-16'))
                        except Exception as err:
                            # here program will always give an error, because 'pyautogui' library from the tusk
                            # doesn't work on my PC, and I'm using another one, which saves screenshot the way
                            # I don't know how decode it
                            print(f'{err}')
                    else:
                        print(response.decode())
                else:
                    print('Invalid request! Try again...')
            else:
                print('Unknown command! Try again...')
            if request == ['Exit']:
                break
    except socket.error as msg:
        print('Failed to open server socket - ' + str(msg))
    finally:
        client_socket.close()


if __name__ == '__main__':
    main()
