from random import randint
import time
import copy
import pygal

class BlackjackPlayer():
    def __init__(self, cpu_controller, cpu_strength=1):
        
        self.cards_list = []
        self.cards_values = 0
        self.cpu_controller = cpu_controller
        self.wins = 0
        self.wins_list = [0]
        
        if cpu_controller:
            self.cpu_strength = cpu_strength
        
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
            if self.cards_values + 10 > 21:
                self.cards_values += 1
            else:
                self.cards_values += 10
    
    def add_to_win_list(self):
        self.wins_list.append(self.wins)

def create_playing_deck(number):
    for j in range(1,14):
        playing_deck[j] = (number * 4)

def shuffle_new_deck():
    global leftover_pile
    global playing_deck
    if not graphing_mode:
        print('')
        print('Shuffle')
        print('')
    playing_deck = copy.deepcopy(leftover_pile)
    leftover_pile = {}
    
    for keys in playing_deck.keys():
        left_in_deck.append(keys)

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

def create_player():
    global actual_players
    if actual_players != 0:
        player_and_dealer_list.append(BlackjackPlayer(False))
        actual_players -= 1
    else:
        player_and_dealer_list.append(BlackjackPlayer(True, randint(1,3)))#1))#randint(1,3)))

def create_dealer():
    player_and_dealer_list.append(BlackjackPlayer(False))
    
def start_game(number_of_player):
    
    for players in range(number_of_player + 1):
        deal_card_to_player(players)
    
    for players in range(1, number_of_player + 1):
        deal_card_to_player(players)

def print_cards(player_number):
    if not graphing_mode:
        if player_number != 0:
            print(f'Player {player_number} cards: {player_and_dealer_list[player_number].cards_list} {player_and_dealer_list[player_number].cards_values}')
        else:
            print(f'Dealer cards: {player_and_dealer_list[player_number].cards_list} {player_and_dealer_list[player_number].cards_values}')
        time.sleep(sleeping_time)

def ask_for_decision(player_number):
    while True:
        if player_and_dealer_list[player_number].cpu_controller:
            decision = calculate_next_move(player_number)
        else:
            #print(f'Player {player_number} cards: {player_and_dealer_list[player_number].cards_list} {player_and_dealer_list[player_number].cards_values}')
            decision = int(input(f'Player {player_number}, hold (0), hit (1) or hint (2)? '))
        
        if decision == 1:
            deal_card_to_player(player_number)
            print_cards(player_number)
            
            if player_and_dealer_list[player_number].cards_values > 21:
                #print(f'Player {player_number} busted.')
                busted.append(player_and_dealer_list[player_number])
                break
        
        elif decision == 0:
            print_cards(player_number)
            break
        
        elif decision == 2:
            print(calculate_win_percentage(player_and_dealer_list[player_number].cards_values))

def calculate_win_percentage(current_value):
    return round(((count_up_to(21 - current_value) / count_cards_in_deck()) * 100), 2)

def calculate_next_move(player_number):
    strength = player_and_dealer_list[player_number].cpu_strength
    
    decision = 0
    
    if strength == 1:
        if player_and_dealer_list[player_number].cards_values < 15:
            decision = 1
            
    elif strength == 2:
        #cards = player_and_dealer_list[player_number].cards_list
        value = player_and_dealer_list[player_number].cards_values
        dealer = player_and_dealer_list[0].cards_values
        
        if value > 16:
            decision = 0
        
        elif value > 12:
            if dealer < 7:
                decision = 0
                
            else:
                decision = 1
                
        else:
            decision = 1
            
    elif strength == 3:
        percentage = calculate_win_percentage(player_and_dealer_list[player_number].cards_values)
        
        if percentage > 60:
            decision = 1
        else:
            decision = 0
    
    return decision

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
    
    #for k, v in ordered.items():
    #    #print(k, v)
    
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
    
    #print('')
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
            
            if len(actual_winners) != 0:
                pass
                #print(f'Players {actual_winners} win.')
            if len(tiers) != 0:
                pass
                #print(f'Players {tiers} tie.')
        else:
            pass
            #print('Dealer wins.')
    else:
        for players in winners:
            player_and_dealer_list[players[0]].wins += 1
            player_and_dealer_list[0].wins -= 1
            actual_winners.append(players[0])
        #print(f'Players {actual_winners} win.')
    
    if not graphing_mode:
        print(f'Players {actual_winners} win.')
        print(f'Players {tiers} tie.')
        
    #return winners

def count_cards_in_deck():
    output = 0
    
    for value in playing_deck.values():
        output += value
    
    if output == 0:
        shuffle_new_deck()
        output = count_cards_in_deck()
    
    return output

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
        print('Install lxml for some magic!')


playing_deck = {}
left_in_deck = [1,2,3,4,5,6,7,8,9,10,11,12,13]
leftover_pile = {}
player_and_dealer_list = []

sleeping_time = 0

number_of_decks = 4

create_playing_deck(number_of_decks)

total_goes = 1000
times = total_goes
start_time = time.time()


number_of_players = 2
actual_players = 1

graphing_mode = False

if graphing_mode:
    actual_players = 0
    print('Total goes:',total_goes)
elif actual_players == 0:
    actual_players = 1

create_dealer()

for players in range(number_of_players):
    create_player()


while True:
    
    if not graphing_mode:
        print('')
        print('New game')
        print('')
    
    busted = []

    start_game(number_of_players)
    
    for i in range(number_of_players + 1):
        print_cards(i)
    
    for i in range(1, number_of_players + 1):
        #print('')
        print_cards(i)
        ask_for_decision(i)
    
    #print('')
    
    if len(busted) != number_of_players:
        while True:
            deal_card_to_player(0)
            print_cards(0)
        
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
                    print(f'Players {winners} win.')
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
                
                
            if cards not in leftover_pile:
                leftover_pile[cards] = 0
            leftover_pile[cards] += 1
        
        players.cards_list = []
    
    #print(playing_deck)
    #print(left_in_deck)
    #print(leftover_pile)
        
    #for players in player_and_dealer_list:
    #    print(players.wins)
    if graphing_mode:
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
        
        if times % (total_goes / 10) == 0:
            print(str(int(100 - (times / (total_goes / 100)))) + '%')
            
            for players in player_and_dealer_list:
                players.add_to_win_list()
    
    
    #time.sleep(5)
