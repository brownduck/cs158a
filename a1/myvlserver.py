from socket import *
#RUN SERVER FIRST, THEN CLIENT
serverPort = 11111

# the actual varlen function
def varlen(sentence):
    num = ""
    i = 0
    # default return string if numbers are missing
    str = "Missing Number"
    # find the first digits(no check if it's between 0 and 99)
    while i < len(sentence) and sentence[i].isdigit():
        num += sentence[i]
        i += 1
    # if there is an expected number
    if i != 0:
        print("Length of message: ",num)
        num = int(num)
        text = sentence[i:]  # the string without the leading digits
        print("processed: ", text[:num])
        str = text[:num].upper()  # the rest of the string stretching num times
        print("Length of message sent: ", num)
    else:
        # for the no digit case
        print("Returning error; no number found")
    return str

serverS = socket(AF_INET, SOCK_STREAM)

#empty string means listen to all interfaces
serverS.bind(('', serverPort))

#listen
serverS.listen(1) # num specifies how many you cna listen to

#accept
cnSocket, addr = serverS.accept()
print("Server has connected from: ", addr[0])
#receive
sentence = cnSocket.recv(64).decode()
#process(includes the varlen)
capSentence = varlen(sentence)
#send back
cnSocket.send(capSentence.encode())
#close
cnSocket.close()
