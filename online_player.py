import uno_game
import socket
from sys import argv
import threading
from json import *

def receiver(clientsocket):
    while True:
        msg = clientsocket.recv(1024).decode()
        if msg == '':
            print("disconnected from host")
            break
        print(msg)
    clientsocket.close()

if "-ip" in argv: # read arguments
    ip = argv[argv.index("-ip")+1]
else:
    ip = input("What IP address do you want to connect to? ")

try:
    port = argv[argv.index("-p")+1]
except:
    port = 11111

address = (ip, port)
s = socket.create_connection(address)
try:
    print("Connected!")
    nickname = None
    while not nickname:
        tempname = input("Enter a unique nickname: ")
        s.send(str.encode(tempname))
        response = s.recv(1024).decode()
        print(response)
        if "accepted" in response:
            nickname = tempname
    threading.Thread(target=receiver, args=(s, ), daemon=True).start()
    while True:
        message = input("")
        s.send(str.encode(message))
except KeyboardInterrupt:
    s.close()
    print("Keyboard Interrupt")
