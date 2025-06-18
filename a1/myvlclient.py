from socket import *

serverName = 'localhost'
serverPort = 11111

#tcp socket
clientS = socket(AF_INET, SOCK_STREAM)
#connect to server
clientS.connect((serverName, serverPort))

sentence = input('Input: ')
#send that input
clientS.send(sentence.encode())

#receive modified sentence
modifiedSentence = clientS.recv(64) # buffer size

print('server return: ' + modifiedSentence.decode())
