import socket
import threading
import json
import time
import uuid
import sys
import os

# base class to forward and read json serialized messages
class Message:
    def __init__(self, uuid_str, flag):
        self.uuid = uuid_str
        self.flag = flag

    def makejson(self):
        return json.dumps({"uuid": self.uuid, "flag": self.flag}) + "\n"

    def unjson(data):
        obj = json.loads(data)
        return Message(obj["uuid"], obj["flag"])

# read the config file and grab the ip
def readconfig():
    f = open("config.txt")
    lines = f.readlines()
    f.close()
    line1 = lines[0].strip()
    line2 = lines[1].strip()
    serverparts = line1.split(',')
    serverip = serverparts[0]
    serverport = int(serverparts[1])
    clientparts = line2.split(',')
    clientip = clientparts[0]
    clientport = int(clientparts[1])
    return (serverip, serverport), (clientip, clientport)

# entire process class
class Process:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.state = 0
        self.leader_id = str(self.uuid) # assumed to be itself until finds out
        self.clientsocket = None
        self.finalsend = False
        self.done = False # terminates the loop when leader flag signalled

    # create and write its own log (I couldn't make it like log1.txt)
    def updatelog(self, msg):
        with open(f"log_{self.uuid}.txt", "a") as log:
            log.write(msg + "\n")
        print(msg)

    # reads the json message, decides what to do
    def processmessage(self, msg):
        relation = self.compare(msg.uuid)
        leader_known = self.state == 1
        log = f"Received: uuid={msg.uuid}, flag={msg.flag}, {relation}, {self.state}"
        # is the leader
        if leader_known:
            log += f", leader={self.leader_id}"
        self.updatelog(log)
        # means leader is declared, end the server thread
        if msg.flag == 1:
            self.state = 1
            self.leader_id = msg.uuid
            self.done = True  # <--- Add this so this node ends
            self.forwardmessage(msg)
            return
        # means your message has forwarded back to you (you are the leader)
        if msg.uuid == str(self.uuid):
            self.state = 1
            self.leader_id = str(self.uuid)
            self.finalsend = True
            self.updatelog(f"Leader is decided to {self.uuid}.")
        # means this is a possible leader
        elif msg.uuid > str(self.uuid):
            self.leader_id = msg.uuid
            self.forwardmessage(msg)
        else:
            # if it's less, then it can't be a leader and don't forward
            self.updatelog(f"Ignored message from {msg.uuid}")

    # send it away
    def forwardmessage(self, msg):
        if self.clientsocket:
            self.clientsocket.sendall(msg.makejson().encode())
            self.updatelog(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
    # the message that's sent for comparison
    def compare(self, other_uuid):
        if other_uuid == str(self.uuid): return "same"
        return "greater" if other_uuid > str(self.uuid) else "less"

# the thread that listens for a client (may take some time)
def serverside(server_ip, server_port, process):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(1)
    conn, _ = server.accept()
    # decode the message when received, using \n as the end
    bufferstr = ""
    while not process.done:
        data = conn.recv(1024).decode()
        if not data: # skip if nothing
            continue
        bufferstr += data
        while '\n' in bufferstr:
            messagestr, bufferstr = bufferstr.split('\n', 1)
            msg = Message.unjson(messagestr)
            process.processmessage(msg) # take away for processing
            if process.state == 1 and process.finalsend:
                return
    print(f"Leader is {process.leader_id}")
    sys.exit(0)

# in charge of sending its message, has a pause as well
def clientside(clientip, clientport, process):
    time.sleep(3)  # initial pause to get stuff rolling

    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((clientip, clientport))
            break
        except ConnectionRefusedError:
            time.sleep(2)

    process.clientsocket = client

    msg = Message(str(process.uuid), 0)
    client.sendall(msg.makejson().encode())
    process.updatelog(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
    # keep delaying
    while not process.state or not process.finalsend:
        time.sleep(1)
    # send away
    msg = Message(str(process.leader_id), 1)
    client.sendall(msg.makejson().encode())
    process.updatelog(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
    client.close()

# operate the script
def main():
    (my_ip, my_port), (neighbor_ip, neighbor_port) = readconfig()
    process = Process()
    t = threading.Thread(target=serverside, args=(my_ip, my_port, process), daemon=True)
    t.start()
    clientside(neighbor_ip, neighbor_port, process)
    t.join()
    process.updatelog(f"Leader is {process.leader_id}")


if __name__ == "__main__":
    main()
