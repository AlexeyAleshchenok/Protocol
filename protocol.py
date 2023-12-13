"""
author: Alexey Aleshchenok
date: 2023-12-05
Protocol that processes the information that the server sends to the client
"""
import struct

LEN_LEN = 4


def send(send_socket, cmd, data):
    """sends to server socket byte line containing name of the function and it's argument"""
    if data is not None:
        total_request = cmd.encode() + b' ' + data.encode()
    else:
        total_request = cmd.encode()
    send_socket.sendall(struct.pack('I', len(total_request)))
    send_socket.sendall(total_request)


def receive(receive_socket):
    """receives byte line sent by client socket"""
    net_len = receive_socket.recv(LEN_LEN)
    if not net_len:
        return b''
    packet_len = struct.unpack('I', net_len)[0]
    packet = b''
    while len(packet) < packet_len:
        packet += receive_socket.recv(packet_len - len(packet))
    return packet
