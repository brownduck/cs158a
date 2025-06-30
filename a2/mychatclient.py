from socket import *
from threading import *

serverName = 'localhost'
serverPort = 10000

clientS = socket(AF_INET, SOCK_STREAM)
clientS.connect((serverName, serverPort))
# get client port info
ip, port = clientS.getsockname()

# this function will keep checking for packets from the socket and printing them, it's usually from
# other clients.
def messageHandler():
    while True:
        try:
            message = clientS.recv(1024).decode()
            if message:
                print(message)
        except:
            # if there is nothing to receive, server probably died.
            print("Server has disconnected.")
            break

# start the thread
thread = Thread(target=messageHandler, daemon=True)
thread.start()
# once connected, begin the loop that keeps grabbing user input until there is an exit.
print("You are connected to the server. Type 'exit' to escape")
while True:
    sentence = input()
    # check from break
    if sentence == "exit":
        print("Disconnected from server")
        break
    # send that input
    clientS.send(sentence.encode())
