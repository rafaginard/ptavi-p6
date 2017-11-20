#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import os
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
            if not line:
                break
            else:
                Check_Data = False
                print(line.decode('utf-8'))
                DATA = line.decode('utf-8').split(" ")
                if len(DATA) == 3:
                    if DATA[1].split(":")[0] == ("sip") and DATA[2] == ("SIP/2.0\r\n\r\n"):
                        Check_Data = True
                if DATA[0] == "INVITE" and Check_Data:
                    self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                elif DATA[0] == "BYE" and Check_Data:
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                elif DATA[0] == "ACK" and Check_Data:
                    fichero_audio = sys.argv[3]
                    aEjecutar = "mp32rtp -i 127.0.0.1 -p 23032 < " + fichero_audio
                    os.system(aEjecutar)
                elif DATA[0] != ("INVITE" or "ACK" or "BYE") and Check_Data:
                    self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
                else:
                    self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                # Si no hay más líneas salimos del bucle infinito

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)
    try:
        if os.path.isfile(sys.argv[3]):
            fichero_audio = sys.argv[3]
            print("Listening...")
            serv.serve_forever()
    except:
        sys.exit("Usage: python3 server.py IP port audio_file")
