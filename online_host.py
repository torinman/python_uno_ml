import uno_game
import socket               # Import socket module
import threading
import time
from sys import argv


def on_new_client(clientsocket, addr):
    global clients, names, started
    while True:
        name = clientsocket.recv(1024).decode()
        if name in names:
            clientsocket.send("declined".encode())
        else:
            names += [name]
            clientsocket.send("accepted".encode())
            break
    print('Got connection from', addr, " aka: ", name)
    for client in clients:
        if client != (clientsocket, addr):
            client[0].send(("New connection from: "+name).encode())
    clientsocket.send(("Current online users: "+", ".join(names)).encode())
    while True:
        msg = clientsocket.recv(1024).decode()
        if msg == '':
            print("Disconnected from "+str(addr)+" aka: "+name)
            names.remove(name)
            break
        elif msg == 'start game' and not started and len(clients) > 1:
            started = True
            uno_game.no_of_players = len(clients)
            uno_game.deal(7, len(clients))
            uno_game.play_card(uno_game.current_player, uno_game.deck[0], check=False)
            for i in range(len(clients)):
                clients[i][0].send(str.encode("{'start': "+name+"\n'turn': "+names[uno_game.current_player]+"\n'hand': "+str(uno_game.hands[i])+"}"))
        print(addr, " aka: ", name, " sent: ", msg)
        for client in clients:
            client[0].send(str.encode(name+": "+msg))
    clients.remove((clientsocket, addr))
    for client in clients:
        client[0].send((name+" has disconnected").encode())
    clientsocket.close()

started = False
uno_game.create_deck()
host = socket.gethostbyname(socket.gethostname()) # G et local machine name

s = socket.socket()         # Create a socket object
try:
    port = int(argv[argv.index("-p")])
except:
    port = 11111# Reserve a port for your service.
print(f'Server started on {host}:{port}')
print('Waiting for clients...')
clients = []
names = []

s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.

while True:
   c, addr = s.accept()     # Establish connection with client.
   threading.Thread(target=on_new_client,args=(c,addr),daemon=True).start()
   clients += [(c, addr)]
   # Note it's (addr,) not (addr) because second parameter is a tuple
   # Edit: (c,addr)
   # that's how you pass arguments to functions when creating new threads using thread module.
s.close()