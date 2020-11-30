import socket                           # Import socket module

host = socket.gethostname()          # Get local machine name
port = 12345                        # Reserve a port for your   service.
conn = socket.socket()                   # Create a socket object

conn.connect((host, port))

conn.sendall(b'Connected. Wait for data...') 

intosend = input("message to send:")
conn.sendall(bytes(intosend, 'utf-8')) 

data = conn.recv(1024)
intosend= "no"

while intosend != "quit":
    intosend = input("message to send:")
    conn.sendall(bytes(intosend, 'utf-8'))



conn.close()                                    # Close the socket when done


print(data.decode("utf-8"))