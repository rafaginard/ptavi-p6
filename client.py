#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor.
METHOD = ""
SIP_Data = []
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    METHOD = sys.argv[1]
    Message = sys.argv[2]
    SIP_Data = Message.replace(":", "@").split("@")
    User_Name = SIP_Data[0]
    Server_Ip = SIP_Data[1]
    Server_Port = SIP_Data[2]

    my_socket.connect((Server_Ip, int(Server_Port)))
    my_socket.send(bytes(METHOD + " sip:" + User_Name + "@" + Server_Ip +
                         " SIP/2.0", 'utf-8') + b'\r\n\r\n')
    data = my_socket.recv(1024)

#   Recibe el cliente 200 OK
    Recieve = data.decode('utf-8').split(" ")
    if Recieve[1] == "200":
        print(data.decode('utf-8'))
    elif Recieve[1] == "100":
        print(data.decode('utf-8'))
        my_socket.connect((Server_Ip, int(Server_Port)))
        my_socket.send(bytes("ACK sip:" + User_Name + "@" + Server_Ip +
                             " SIP/2.0", 'utf-8') + b'\r\n\r\n')
        data = my_socket.recv(1024)
    else:
        print(data.decode('utf-8'))
