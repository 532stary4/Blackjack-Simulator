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
name_list = []

def processMessages(conn, addr):
    global conn_list
    global name_list
    while True:
        try:
            data = conn.recv(1024)
            if not data: 
                conn.close()
            incoming_data = data.decode("utf-8").split(';')
            #print(incoming_data)
            
            for actual_data in incoming_data:
                if actual_data == '':
                    pass
                elif actual_data[0] == '-':
                    name_list.insert(conn_list.index(conn), actual_data[2:])
                    player_and_dealer_list.append(BlackjackPlayer(actual_data[2:]))
                    conn.sendall(bytes('-' + str(len(name_list)), 'utf-8'))
                    #send_to_all_connections('4Dealer')
                    #send_to_all_connections('4' + actual_data[2:])
                    #print(name_list)
                    
                elif actual_data[0] == '0':
                    send_to_all_connections(actual_data)
                    
                elif actual_data[0] == '1':
                    hit_card(conn)
                
                elif actual_data[0] == '2':
                    hold_card()
                
                elif actual_data[0] == '3':
                    give_hint(conn)
        #conn.sendall(bytes('Thank you for connecting', 'utf-8'))

        except:
            name_list.pop(conn_list.index(conn))
            conn_list.remove(conn)
            conn.close()
            print("Connection closed by", addr)
            # Quit the thread.
            sys.exit()

def start_listening():
    global conn_list
    global name_list
    while True:
        # Wait for connections
        conn, addr = s.accept()
        print('Got connection from ', addr[0], '(', addr[1], ')')
        conn_list.append(conn)
        #print(conn_list)
        
        conn.sendall(bytes(socket.gethostbyname(socket.gethostname()) + ';', 'utf-8')) 
        # Listen for messages on this connection
        listener = threading.Thread(target=processMessages, args=(conn, addr))
        listener.start()

def send_to_all_connections(message):
    for connections in conn_list:
        connections.sendall(bytes(message + ';', 'utf-8'))

threading.Thread(target=start_listening).start()

from random import randint
import time
import copy
import pygal
from tkinter import *

# a player object which is used for easy storage
class BlackjackPlayer():
    # this is what is initialised when class called
    def __init__(self, name):
        
        self.cards_list = []
        self.cards_values = 0
        self.wins = 0
        self.wins_list = [0]
        self.name = name
    
    # calculates the value of all cards held in the players hand
    def calculate_value_return_lost(self):
        aces = 0
        self.cards_values = 0
        
        for items in self.cards_list:
            card_value = items
            
            if card_value == 'A':
                aces += 1
                continue
            elif card_value == 'J' or card_value == 'Q' or card_value == 'K':
                card_value = 10
            
            self.cards_values += card_value
        
        for ace in range(aces):
            if self.cards_values + 11 > 21:
                self.cards_values += 1
            else:
                self.cards_values += 11
    
    # adds the number of wins to the wins list, used for the graph
    def add_to_win_list(self):
        self.wins_list.append(self.wins)

# creates the master playing deck used
# the number is the number of decks used
def create_playing_deck(number):
    for j in range(1,14):
        playing_deck[j] = (number * 4)

# shuffles the discard pile back into the playing deck
def shuffle_new_deck():
    global discard_pile
    global playing_deck
    if not graphing_mode:
        print('')
        print('Shuffle')
        print('')
    playing_deck = copy.deepcopy(discard_pile)
    discard_pile = {}
    
    for keys in playing_deck.keys():
        left_in_deck.append(keys)

# gives a card to the player which number was put in
def deal_card_to_player(player_number):
    #global playing_deck
    if len(left_in_deck) == 0:
        shuffle_new_deck()
    
    card_number = left_in_deck[randint(0, len(left_in_deck) - 1)]
    playing_deck[card_number] -= 1
    
    if playing_deck[card_number] == 0:
        left_in_deck.remove(card_number)
    
    if card_number == 1:
        card_number = 'A'
    elif card_number == 11:
        card_number = 'J'
    elif card_number == 12:
        card_number = 'Q'
    elif card_number == 13:
        card_number = 'K'
    
    player_and_dealer_list[player_number].cards_list.append(card_number)
    player_and_dealer_list[player_number].calculate_value_return_lost()


# creates the dealer, which is just a blackjack player with special rules
def create_dealer():
    player_and_dealer_list.append(BlackjackPlayer('Dealer'))
    
# deals cards to each player at the start of each game
def start_game(number_of_player):
    for players in range(number_of_player + 1):
        deal_card_to_player(players)
    
    for players in range(1, number_of_player + 1):
        deal_card_to_player(players)
        
# calculates the percentage chance of having less than 22 after a hit
def calculate_win_percentage(current_value):
    return round(((count_up_to(21 - current_value) / count_cards_in_deck()) * 100), 2)

# looks at the players and returns the winners and tiers with the dealer
def count_biggest_return_winners():
    temp = {}
    
    for players in player_and_dealer_list:
        if player_and_dealer_list.index(players) != 0:
            if players not in busted:
                temp[player_and_dealer_list.index(players)] = players.cards_values
        
            else:
                player_and_dealer_list[0].wins += 1
                players.wins -= 1
    
    temp[0] = player_and_dealer_list[0].cards_values
    
    ordered = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1], reverse = True)}
    
    winners = []
    
    rest_lose = False
    
    for players_number, card_value in ordered.items():
        if rest_lose:
            player_and_dealer_list[players_number].wins -= 1
            player_and_dealer_list[0].wins += 1
            continue
            
        if players_number != 0:
            winners.append([players_number, card_value])
        else:
            if len(winners) != 0:
                if ordered[0] == winners[-1][1]:
                    winners.append([players_number, card_value])
            else:
                winners.append([players_number, card_value])
            rest_lose = True
    
    
    actual_winners = []
    tiers = []
    
    if winners[-1][0] == 0:
        
        if len(winners) != 1:
            for players in winners:
                if players[1] == winners[-1][1]:
                    tiers.append(players[0])
                else:
                    if players[0] != 0:
                        player_and_dealer_list[players[0]].wins += 1
                        player_and_dealer_list[0].wins -= 1
                        actual_winners.append(players[0])
            
            #if len(actual_winners) != 0:
            #    pass
                #print(f'Players {actual_winners} win.')
            #if len(tiers) != 0:
            #    pass
                #print(f'Players {tiers} tie.')
        else:
            change_all_label('Dealer wins')
            time.sleep(2)
            pass
            #print('Dealer wins.')
    else:
        for players in winners:
            player_and_dealer_list[players[0]].wins += 1
            player_and_dealer_list[0].wins -= 1
            actual_winners.append(players[0])
        #print(f'Players {actual_winners} win.')
    
    if not graphing_mode:
        if len(actual_winners) != 0:
            change_all_label(f'Players {actual_winners} win.')
            time.sleep(2)
            
        if len(tiers) != 0:
            change_all_label(f'Players {tiers} tie.')
            time.sleep(2)
        
    #return winners

# counts the number of cards left in the deck
def count_cards_in_deck():
    output = 0
    
    for value in playing_deck.values():
        output += value
    
    if output == 0:
        shuffle_new_deck()
        output = count_cards_in_deck()
    
    return output

# counts how many cards up to in_num
def count_up_to(in_num):
    output = 0
    
    for key, value in playing_deck.items():
        if key == 'A':
            key = 1
        elif key == 11 or key == 12 or key == 13 or key == 'K' or key == 'J' or key == 'Q':
            key = 10
            
        if key <= in_num:
            output += value
    
    return output

'''# creates a pygal graph from the win lists of each player
def make_graph():
    chart = pygal.Line()
        
    chart.title = 'Blackjack Total Wins'
    #chart.x_labels = map(str, range(0, total_goes + 1))
    
    for players in player_and_dealer_list:
        #print(players.wins_list)
        if player_and_dealer_list.index(players) == 0:
            chart.add('Dealer', players.wins_list)
        else:
            chart.add('Player ' + str(player_and_dealer_list.index(players)), players.wins_list)
    
    chart.render_to_file('Wins.svg')
    try:
        chart.render_in_browser()
    except:
        print('Install lxml for some magic!')'''

# creates the players at the start and puts them in their seats
def make_players_in_chairs():
    for players in name_list:
        player_and_dealer_list.append(BlackjackPlayer(players))

# the whole program runs in this function
def go_do_it():
    global busted
    while True:
        '''if not graphing_mode:
            print('')
            print('New game')
            print('')'''
        
        busted = []

        start_game(number_of_players)
        
        #for i in range(number_of_players + 1):
        #    print_cards(i)
        refresh_list_box()
        
        global waiting_for_user
        
        for i in range(1, number_of_players + 1):
            #print('')
            #print_cards(i)
            refresh_list_box()
            change_all_label(f'{name_list[i - 1]}\'s turn')
            
            waiting_for_user = True
            
            global current_user
            current_user = i
            
            conn_list[i - 1].sendall(bytes('2;', 'utf-8'))
            
            while waiting_for_user:
                time.sleep(1)
            
            time.sleep(1)
        
        #print('')
        
        if len(busted) != number_of_players:
            change_all_label(f'Dealer\'s turn')
            while True:
                time.sleep(1)
                deal_card_to_player(0)
                #print_cards(0)
                
                refresh_list_box()
            
                if player_and_dealer_list[0].cards_values > 21:
                    #print('')
                    #print('Dealer busted.')
                    busted.append(player_and_dealer_list[0])
                    
                    winners = []
        
                    for players in player_and_dealer_list:
                        if player_and_dealer_list.index(players) != 0:
                            if players not in busted:
                                players.wins += 1
                                player_and_dealer_list[0].wins -= 1
                                winners.append(player_and_dealer_list.index(players))
                            else:
                                player_and_dealer_list[0].wins += 1
                                players.wins -= 1
                    
                    if not graphing_mode:
                        change_all_label(f'Players {winners} win.')
                        time.sleep(1)
                    break
                
                elif player_and_dealer_list[0].cards_values == 21:
                    count_biggest_return_winners()
                    break
                
                else:
                    '''win = True
                    for i in range(1, len(player_and_dealer_list)):
                        if player_and_dealer_list[0].cards_values <= player_and_dealer_list[i].cards_values:
                            win = False
                    
                    if win:
                        #print('')
                        #print('Dealer wins.')
                        break
                    
                    else:'''
                    if player_and_dealer_list[0].cards_values > 16:
                        count_biggest_return_winners()
                        break
            
            
        #for i in range(number_of_players + 1):
        #    print_cards(i)
        
        #break
        
        for players in player_and_dealer_list:
            for cards in players.cards_list:
                if cards == 'A':
                    cards = 1
                elif cards == 'J':
                    cards = 11
                elif cards == 'Q':
                    cards = 12
                elif cards == 'K':
                    cards = 13
                    
                    
                if cards not in discard_pile:
                    discard_pile[cards] = 0
                discard_pile[cards] += 1
            
            players.cards_list = []
        
        #print(playing_deck)
        #print(left_in_deck)
        #print(discard_pile)
            
        #for players in player_and_dealer_list:
        #    print(players.wins)
        if graphing_mode:
            global times
            times -= 1
            #print(times)
            
            if times == 0:
                print('100%')
                print('Time taken:',time.time() - start_time)
                
                for players in player_and_dealer_list:
                    players.add_to_win_list()
                
                if graphing_mode:
                    make_graph()
                break
            
            if times % (total_goes / 100) == 0:
                print(str(int(100 - (times / (total_goes / 100)))) + '%')
                
                for players in player_and_dealer_list:
                    players.add_to_win_list()
        
        
        time.sleep(3)
                    
# asks for an input and only accepts the correct type
def get_a_valid_input(type_of, message):
    try:
        output = type_of(input(message))
        return output
    except:
        print('Could not read')
        return get_a_valid_input(type_of, message)

def change_all_label(message):
    send_to_all_connections('3' + message)

# gives the hint
def give_hint(connect):
    if waiting_for_user:
        refresh_list_box()
        connect.sendall(bytes(f'3Percentage of getting less than 21\n{calculate_win_percentage(player_and_dealer_list[current_user].cards_values)}%;', 'utf-8'))

# holds cards
def hold_card():
    global waiting_for_user
    if waiting_for_user:
        refresh_list_box()
        waiting_for_user = False
    
# hits card
def hit_card(connect):
    global waiting_for_user
    if waiting_for_user:
        deal_card_to_player(current_user)
        refresh_list_box()
        
        if player_and_dealer_list[current_user].cards_values > 21:
            #print(f'Player {player_number} busted.')
            connect.sendall(bytes('3Busted;', 'utf-8'))
            
            busted.append(player_and_dealer_list[current_user])
            waiting_for_user = False
        else:
            connect.sendall(bytes('3Hit, Pick Again;2;', 'utf-8'))

# refreshes cards in listbox
def refresh_list_box():
    for players in player_and_dealer_list:
        for connections in conn_list:
            connections.sendall(bytes(f'1-{len(name_list)}-{players.name} cards: {players.cards_list} {players.cards_values};', 'utf-8'))
    

# declaring variables
playing_deck = {}
left_in_deck = [1,2,3,4,5,6,7,8,9,10,11,12,13]
discard_pile = {}
player_and_dealer_list = []
busted = []
current_user = 0

#sleeping_time = get_a_valid_input(int, 'sleeping')

create_dealer()

number_of_decks = get_a_valid_input(int, 'Number of decks: ')
create_playing_deck(number_of_decks)

number_of_players = len(name_list)
print(number_of_players)

graphing_mode = False

actual_players = number_of_players
total_goes = 1000000
    

times = total_goes
start_time = time.time()


#make_players_in_chairs()

waiting_for_user = False

threading.Thread(target=go_do_it).start()