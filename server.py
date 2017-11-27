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

    def Comprobar_Peticion(self, DATA):
        print(DATA)
        if len(DATA) == 3:
            condition_sip = DATA[1].split(":")[0] == ("sip")
            condition_final = DATA[2] == ("SIP/2.0\r\n\r\n")
            condition_arroba = False
            if DATA[1].find("@") != -1:
                condition_arroba = True
            if condition_sip and condition_arroba and condition_final:
                self.check = True

    def handle(self):
        self.check = False

        # Escribe dirección y puerto del cliente (de tupla client_address)
        #while 1:
            # Leyendo línea a línea lo que nos envía el cliente
        self.line = self.rfile.read()
        print(self.line.decode('utf-8'))

        if self.line:

            DATA = self.line.decode('utf-8').split(" ")
            print(self.Comprobar_Peticion(DATA))
            if self.Comprobar_Peticion(DATA):
                if DATA[0] == "INVITE":
                    self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                elif DATA[0] == "BYE":
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                elif DATA[0] == "ACK":
                    fichero_audio = sys.argv[3]
                    aEjecutar = "mp32rtp -i 127.0.0.1 -p 23032 < " + fichero_audio
                    os.system(aEjecutar)
                elif DATA[0] != ("INVITE" or "ACK" or "BYE"):
                    self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((sys.argv[1], int(sys.argv[2])), EchoHandler)
    try:
        if os.path.isfile(sys.argv[3]):
            fichero_audio = sys.argv[3]
            print("Listening...")
            serv.serve_forever()
        else:
            print("Usage: python3 server.py IP port audio_file")
    except:
        sys.exit("Usage: python3 server.py IP port audio_file")
