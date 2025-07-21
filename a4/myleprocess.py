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
    with open("config.txt") as f:
        lines = f.readlines()
    line1 = lines[0].strip()
    line2 = lines[1].strip()
    serverip, serverport = line1.split(',')
    clientip, clientport = line2.split(',')
    return (serverip, int(serverport)), (clientip, int(clientport))

# entire process class
class Process:
    def __init__(self):
        self.uuid = uuid.uuid4()
        self.state = 0
        self.leader_id = str(self.uuid)
        self.clientsocket = None
        self.finalsend = False
        self.done = False

    def updatelog(self, msg):
        with open(f"log_{self.uuid}.txt", "a") as log:
            log.write(msg + "\n")
        print(msg)

    def processmessage(self, msg):
        relation = self.compare(msg.uuid)
        leader_known = self.state == 1
        log = f"Received: uuid={msg.uuid}, flag={msg.flag}, {relation}, {self.state}"
        if leader_known:
            log += f", leader={self.leader_id}"
        self.updatelog(log)
        if msg.flag == 1:
            self.state = 1
            self.leader_id = msg.uuid
            self.done = True
            self.forwardmessage(msg)
            return

        if msg.uuid == str(self.uuid) and self.state == 0:
            self.state = 1
            self.leader_id = str(self.uuid)
            self.finalsend = True
            self.updatelog(f"Leader is decided to {self.uuid}.")
        elif msg.uuid > str(self.uuid):
            # print(f"{msg.uuid} is greater than {self.uuid}, maybe I send {msg.uuid}")
            self.leader_id = str(msg.uuid)
            self.forwardmessage(msg)
        else:
            self.updatelog(f"Ignored message from {msg.uuid}")

    def forwardmessage(self, msg):
        # my solution: stay waiting until clientsocket is not None
        # this is because the process might(always) receive a message faster than the process and connect the socket
        # to client.
        while self.clientsocket == None:
            time.sleep(.25)
        if self.clientsocket:
            # print(f"making sure the msg is still {msg.uuid}")
            self.clientsocket.sendall(msg.makejson().encode())
            self.updatelog(f"Sent: uuid={msg.uuid}, flag={msg.flag}")

    def compare(self, other_uuid):
        if other_uuid == str(self.uuid): return "same"
        return "greater" if other_uuid > str(self.uuid) else "less"

def serverside(server_ip, server_port, process):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(1)
    conn, _ = server.accept()
    bufferstr = ""
    while not process.done:
        data = conn.recv(1024).decode()
        if not data:
            continue
        bufferstr += data
        while '\n' in bufferstr:
            messagestr, bufferstr = bufferstr.split('\n', 1)
            msg = Message.unjson(messagestr)
            process.processmessage(msg)
            if process.state == 1 and process.finalsend:
                return
    print(f"Leader is {process.leader_id}")
    sys.exit(0)

def clientside(clientip, clientport, process):
    time.sleep(3)
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

    while process.state == 0:
        time.sleep(.5)
    # Leader sends final message
    if str(process.uuid) == process.leader_id:
        msg = Message(str(process.leader_id), 1)
        client.sendall(msg.makejson().encode())
        process.updatelog(f"Sent: uuid={msg.uuid}, flag={msg.flag}")
    client.close()

def main():
    (my_ip, my_port), (neighbor_ip, neighbor_port) = readconfig()
    process = Process()
    # process.updatelog(f"my id is {process.uuid}")
    t = threading.Thread(target=serverside, args=(my_ip, my_port, process), daemon=True)
    t.start()
    clientside(neighbor_ip, neighbor_port, process)
    t.join()
    # print("hello, this is the end")
    # because the non-leaders print it elsewhere
    if str(process.uuid) == str(process.leader_id):
        process.updatelog(f"Leader is {process.leader_id}")

if __name__ == "__main__":
    main()
