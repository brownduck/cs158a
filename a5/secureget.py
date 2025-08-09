import socket
import ssl

domain = "www.google.com"
port = 443

tcpsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

context = ssl.create_default_context()
ssl_sock = context.wrap_socket(tcpsocket, server_hostname=domain)
ssl_sock.connect((domain, port))

# the format to set an HTTP GET
request = (
    f"GET / HTTP/1.1\r\n"
    f"Host: {domain}\r\n"
    f"Connection: close\r\n"
    f"User-Agent: Python-SSL-Client\r\n"
    f"\r\n"
)

# send through socket
ssl_sock.sendall(request.encode("utf-8"))

# receive and add the reponse
response = b""
while True:
    data = ssl_sock.recv(4096)
    if not data:
        break
    response += data

ssl_sock.close()

# separate the header and body
header, _, body = response.partition(b"\r\n\r\n")

# Save HTML body to file
with open("response.html", "wb") as file:
    file.write(body)

print("Success")

