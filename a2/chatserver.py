from socket import *
from threading import *

# RUN SERVER FIRST, THEN CLIENT
serverIP = 'localhost'
serverPort = 10000

serverS = socket(AF_INET, SOCK_STREAM)

# empty string means listen to all interfaces
serverS.bind((serverIP, serverPort))
serverS.listen()
# list of connected clients, it's how we send each client's message to everyone else.
clients = []

#send the message to all clients except the sender
def sendToAll(message, socket):
    # first send to server
    ip, port = socket.getpeername()
    # new message adding the port to the front.
    newmsg = f"{port}: {message}"
    print(newmsg)
    for client in clients:
        # make sure it's not the sender
        if client != socket:
            try:
                client.send(newmsg.encode())
            except:
                # if there's an issue with a client's ability to send, take them away.
                client.close()
                clients.remove(client)

# whenever a new client connects, add them to the list and run a loop to keep receiving what they send
# and forward that to all other clients (sendToAll).
# break the loop when theres an issue with except.
def newClient(client_socket, address):
    print(f"New connection from {address}")
    clients.append(client_socket)

    try:
        while True:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            sendToAll(msg, client_socket)
    except:
        # any issues will result in disconnecting the client and dropping it
        print(f"{address} disconnected.")
        clients.remove(client_socket)
        client_socket.close()

# locking in
print(f"Server listening on :{serverPort}")

# keep accepting new clients
while True:
    clientS, addr = serverS.accept()
    thread = Thread(target=newClient, args=(clientS, addr))
    thread.start()
