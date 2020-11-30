from random import randint
import time

class BlackjackPlayer():
    def __init__(self, cpu_controller, cpu_strength=1):
        
        self.cards_list = []
        self.cards_values = 0
        self.cpu_controller = cpu_controller
        
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

def create_playing_deck(number):
    for j in range(1,14):
        playing_deck[j] = (number * 4)

def deal_card_to_player(player_number):
    
    card_number = left_in_deck[randint(0, len(left_in_deck) - 1)]
    playing_deck[card_number] -= 1
    
    if playing_deck[card_number] == 0:
        left_in_deck.pop(card_number)
    
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
        player_and_dealer_list.append(BlackjackPlayer(True))

def create_dealer():
    player_and_dealer_list.append(BlackjackPlayer(False))
    
def start_game(deck_size, number_of_players):
    create_playing_deck(deck_size)
    
    create_dealer()
    
    for players in range(number_of_players):
        create_player()
    
    for players in range(number_of_players + 1):
        deal_card_to_player(players)
    
    for players in range(1, number_of_players + 1):
        deal_card_to_player(players)

def print_cards(player_number):
    print(f'Player {player_number} cards: {player_and_dealer_list[player_number].cards_list} {player_and_dealer_list[player_number].cards_values}')
    time.sleep(0.1)

def ask_for_decision(player_number):
    global busted
    while True:
        if player_and_dealer_list[player_number].cpu_controller:
            decision = calculate_next_move(player_number)
        else:
            decision = int(input(f'Player {player_number}, hold (0) or hit (1)? '))
        
        if decision == 1:
            deal_card_to_player(player_number)
            print_cards(player_number)
            
            if player_and_dealer_list[player_number].cards_values > 21:
                print(f'Player {player_number} busted.')
                busted.append(player_and_dealer_list[player_number])
                break
        
        elif decision == 0:
            print_cards(player_number)
            break

def calculate_next_move(player_number):
    strength = player_and_dealer_list[player_number].cpu_strength
    
    decision = 0
    
    if strength == 1:
        if player_and_dealer_list[player_number].cards_values < 15:
            decision = 1
            
    elif strength == 2:
        pass
    elif strength == 3:
        pass
    
    return decision

def count_biggest_return_winners():
    temp = {}
    
    for players in player_and_dealer_list:
        if players not in busted:
            if player_and_dealer_list.index(players) != 0:
                temp[player_and_dealer_list.index(players)] = players.cards_values
    
    temp[0] = player_and_dealer_list[0].cards_values
    
    ordered = {k: v for k, v in sorted(temp.items(), key=lambda item: item[1], reverse = True)}
    
    #for k, v in ordered.items():
    #    print(k, v)
    
    winners = []
    for players_number, card_value in ordered.items():
        if players_number != 0:
            winners.append([players_number, card_value])
        else:
            if len(winners) != 0:
                if ordered[0] == winners[-1][1]:
                    winners.append([players_number, card_value])
            else:
                winners.append([players_number, card_value])
            break
    
    
    print('')
    if winners[-1][0] == 0:
        actual_winners = []
        tiers = []
        
        if len(winners) != 1:
            for players in winners:
                if players[1] == winners[-1][1]:
                    tiers.append(players[0])
                else:
                    actual_winners.append(players[0])
            
            if len(actual_winners) != 0:
                print(f'Players {actual_winners} win.')
            if len(tiers) != 0:
                print(f'Players {tiers} tie.')
        else:
            print('Dealer wins.')
    else:
        actual_winners = []
        for players in winners:
            actual_winners.append(players[0])
        print(f'Players {actual_winners} win.')
    #return winners


while True:
    number_of_players = 4

    playing_deck = {}
    player_and_dealer_list = []
    left_in_deck = [1,2,3,4,5,6,7,8,9,10,11,12,13]

    actual_players = 1
    busted = []

    start_game(2, number_of_players)
    
    for i in range(number_of_players + 1):
        print_cards(i)
    
    for i in range(1, number_of_players + 1):
        print('')
        print_cards(i)
        ask_for_decision(i)
    
    print('')
    
    if len(busted) != number_of_players:
        while True:
            deal_card_to_player(0)
            print_cards(0)
        
            if player_and_dealer_list[0].cards_values > 21:
                print('')
                print('Dealer busted.')
                print('')
                busted.append(player_and_dealer_list[0])
                
                winners = []
    
                for players in player_and_dealer_list:
                    if players not in busted:
                        winners.append(player_and_dealer_list.index(players))
                
                print(f'Players {winners} win.')
                break
            
            elif player_and_dealer_list[0].cards_values == 21:
                count_biggest_return_winners()
                break
            
            else:
                win = True
                for i in range(1, len(player_and_dealer_list)):
                    if player_and_dealer_list[0].cards_values <= player_and_dealer_list[i].cards_values:
                        win = False
                
                if win:
                    print('')
                    print('Dealer wins.')
                    print('')
                    break
                
                else:
                    if player_and_dealer_list[0].cards_values > 16:
                        count_biggest_return_winners()
                        break
        
        
    #for i in range(number_of_players + 1):
    #    print_cards(i)
    
    #break
    print('')
    time.sleep(5)
