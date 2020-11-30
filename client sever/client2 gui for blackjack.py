import socket                           # Import socket module
import threading
import sys
from tkinter import *

def change_label(text_in):
    text_label.config(text=text_in)

# gives the hint
def give_hint():
    send_message_over('3')
    
# holds cards
def hold_card():
    send_message_over('2')
    deactivate()
    
# hits card
def hit_card():
    send_message_over('1')
    deactivate()

def deactivate():
    hold_btn['state'] = DISABLED
    hit_btn['state'] = DISABLED
    hint_btn['state'] = DISABLED

def on_closing_main():
    conn.close()
    sys.exit()

def send_message_over(message):
    #print('sending ' + message)
    conn.sendall(bytes(message + ';', 'utf-8'))
    
    
root = Tk()
root.geometry("300x600")

listbox_frame = Frame(root)
listbox_frame.pack(padx=10, pady=10)

scrollbar = Scrollbar(listbox_frame)
scrollbar.pack(side=RIGHT, fill=BOTH)

player_card_box = Listbox(listbox_frame, height=30, width=50, yscrollcommand=scrollbar.set)
player_card_box.pack(side=LEFT, fill=BOTH)

scrollbar.config(command = player_card_box.yview)

text_label = Label(root, text='Starting...')
text_label.pack(padx=20, pady=20)

btn_frame = Frame(root)
btn_frame.pack()

hold_btn = Button(btn_frame, text='Hold', command=hold_card)
hit_btn = Button(btn_frame, text='Hit', command=hit_card)
hint_btn = Button(btn_frame, text='Hint', command=give_hint)

hold_btn['state'] = DISABLED
hit_btn['state'] = DISABLED
hint_btn['state'] = DISABLED

hold_btn.grid(row=0, column=0, padx=10, pady=10)
hit_btn.grid(row=0, column=1, padx=10, pady=10)
hint_btn.grid(row=0, column=2, padx=10, pady=10)




#host = socket.gethostname()          # Get local machine name
host = input('Input hostname: ')

port = 12345                        # Reserve a port for your   service.
conn = socket.socket()                   # Create a socket object

conn.connect((host, port))

#conn.send(b'Connected. Wait for data...')

public_name = input('Your public name: ')
root.title(public_name)
public_name = public_name + ': '

send_message_over('-1' + public_name.split(':')[0])

#intosend = input()
#conn.sendall(bytes(public_name + intosend, 'utf-8')) 

def processMessages(conn, addr):
    global player_card_box
    while True:
        try:
            data = conn.recv(1024)
            if not data: 
                conn.close()
            incoming_data = data.decode("utf-8").split(';')
            print(incoming_data)
            
            for actual_data in incoming_data:
                if actual_data == '':
                    pass
                elif actual_data[0] == '-':
                    root.title(public_name.split(':')[0] + ' ' + actual_data[1:])
                    
                elif actual_data[0] == '0' and actual_data.split(':')[0][1:] != public_name.split(':')[0]:
                    print(actual_data[1:])
                    
                elif actual_data[0] == '1':
                    actual_data = actual_data.split('-')
                    if player_card_box.size() > int(actual_data[1]):
                        player_card_box.delete(0)
                    player_card_box.insert(END, actual_data[2])
                
                elif actual_data[0] == '2':
                    hold_btn['state'] = NORMAL
                    hit_btn['state'] = NORMAL
                    hint_btn['state'] = NORMAL
                
                elif actual_data[0] == '3':
                    change_label(actual_data[1:])
                
                elif actual_data[0] == '4':
                    player_card_box.insert(END, actual_data[1:])
                        
            #conn.sendall(bytes('Thank you for connecting', 'utf-8'))
        except:
            conn.close()
            print("Connection closed by", addr)
            # Quit the thread.
            sys.exit()

def send_message():
    intosend = 0
    while intosend != "quit":
        intosend = input()
        send_message_over('0' + public_name + intosend)
    
data = conn.recv(1024)
    
listener = threading.Thread(target=processMessages, args=(conn, data.decode('utf-8')))
listener.start()

threading.Thread(target=send_message).start()

root.protocol("WM_DELETE_WINDOW", on_closing_main)
root.mainloop()
