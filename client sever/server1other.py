import socket
import threading
import sys

s = socket.socket()                      # Create a socket object
host = socket.gethostname()              # Get local machine name
print('Hostname is: ' + host)
port = 12345                             # Reserve a port for your service.
s = socket.socket()
s.bind((host, port))                     # Bind to the port

s.listen(5)                              # Now wait for client connection.

conn_list = []

def processMessages(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data: 
                conn.close()
            print(data.decode("utf-8"))
            #conn.sendall(bytes('Thank you for connecting', 'utf-8'))
            for connections in conn_list:
                connections.send(data)
            
        except:
            conn_list.remove(conn)
            conn.close()
            print("Connection closed by", addr)
            # Quit the thread.
            sys.exit()


while True:
    # Wait for connections
    conn, addr = s.accept()
    print('Got connection from ', addr[0], '(', addr[1], ')')
    conn_list.append(conn)
    
    conn.send(bytes(socket.gethostbyname(socket.gethostname()), 'utf-8')) 
    # Listen for messages on this connection
    listener = threading.Thread(target=processMessages, args=(conn, addr))
    listener.start()