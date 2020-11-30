import socket                           # Import socket module
import threading
import sys

#host = socket.gethostname()          # Get local machine name
host = input('Input hostname: ')

port = 12345                        # Reserve a port for your   service.
conn = socket.socket()                   # Create a socket object

conn.connect((host, port))

#conn.send(b'Connected. Wait for data...')

public_name = input('Your public name: ')
public_name = public_name + ': '

intosend = input()
conn.sendall(bytes(public_name + intosend, 'utf-8')) 

def processMessages(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data: 
                conn.close()
            actual_data = data.decode("utf-8")
            if actual_data.split(' ')[0] + ' ' != public_name:
                print(actual_data)
            #conn.sendall(bytes('Thank you for connecting', 'utf-8'))
        except:
            conn.close()
            print("Connection closed by", addr)
            # Quit the thread.
            sys.exit()

data = conn.recv(1024)
    
listener = threading.Thread(target=processMessages, args=(conn, data.decode("utf-8")))
listener.start()

while intosend != "quit":
    intosend = input()
    conn.sendall(bytes(public_name + intosend, 'utf-8'))


conn.close()                                    # Close the socket when done


print(data.decode("utf-8"))