import json
import socket
from sys import argv
import threading


def receiver(clientsocket):
    while True:
        msg = clientsocket.recv(1024).decode()
        if msg == '':
            print("disconnected from host")
            break
        elif msg[0] == "{":
            j = json.loads(msg.replace("'", "\""))
            for key in j.keys():
                if key == "hand":
                    hand = j["hand"]
                    print("Your hand is:", hand)
                elif key == "turn":
                    print("It is", j["turn"], "'s go.")
                elif key == "start":
                    started = True
                    print(j["start"], "has started the game.")
                elif key == "top":
                    topcard = j["top"]
                    print("The top card is a", topcard)
                elif key == "colour":
                    colour = j["colour"]
                    print("The current colour is "+j["colour"])
            #print(j["start"], "has started the game. Your hand is:", hand, "It is", j["turn"], "'s go. The top card is a", j["top"], ". The current colour is "+j["colour"])
        else:
            print(msg)
    clientsocket.close()

hand = []
topcard = ""
colour = ""
started = False

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
