#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print(line.decode('utf-8'))
            DATA = line.decode('utf-8').split(" ")
            if DATA[0] == "INVITE":
                self.wfile.write(b"SIP/2.0 100 Trying\nSIP/2.0 180 Ringing\nSIP/2.0 200 OK")

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
