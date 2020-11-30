import socket

s = socket.socket()                      # Create a socket object
host = socket.gethostname()              # Get local machine name

port = 12345                             # Reserve a port for your service.
s = socket.socket()
s.bind((host, port))                     # Bind to the port

s.listen(5)                              # Now wait for client connection.

conn, addr = s.accept()
print('Got connection from ', addr[0], '(', addr[1], ')')

while True:
    data = conn.recv(1024)
    print(data.decode("utf-8"))
    if not data: 
        break
    conn.sendall(data)

conn.close() 

print('Thank you for connecting')