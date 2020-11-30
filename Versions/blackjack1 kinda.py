from random import randint

def create_playing_deck(number, in_dict):
    for j in range(1,14):
        in_dict[j] = (number * 4)

def deal_card_to_player(player_number, player_dict, playing_deck):
    
    if player_number not in player_dict.keys():
        player_dict[player_number] = []
    
    card_number = randint(1, 13)
    player_dict[player_number].append(card_number)
    playing_deck[card_number] -= 1
    
    if playing_deck[card_number] == 0:
        del playing_deck[card_number]
    
    
def start_game(deck_size, player_number):
    
    playing_deck = {}
    
    create_playing_deck(deck_size, playing_deck)
    
    player_and_dealer_dictionary = {}
    
    for i in range(2):
        for players in range(player_number + 1):
            deal_card_to_player(players, player_and_dealer_dictionary, playing_deck)
            
    return player_and_dealer_dictionary, playing_deck

def print_cards(player_and_dealer_dictionary, player_number, number):
    
    if number == 1:
        print(f'Dealer card: {player_and_dealer_dictionary[0][0]}')
    elif number == 2:
        print(f'Dealer cards: {player_and_dealer_dictionary[0]}')
    
    for i in range(player_number):
        print(f'Player {i + 1} cards: {player_and_dealer_dictionary[i + 1]}')

def ask_for_decision(player_and_dealer_dictionary, playing_deck, actual_players):

    for i in range(actual_players):
        decision = int(input(f'Player {i + 1}, hold (0) or hit (1)? '))
        
        if decision == 1:
            deal_card_to_player(actual_players, player_and_dealer_dictionary, playing_deck)
            print(f'Player {i + 1} cards: {player_and_dealer_dictionary[i + 1]}')

player_number = 2
player_and_dealer_dictionary, playing_deck = start_game(2, player_number)

actual_players = 1

while True:
    
    print_cards(player_and_dealer_dictionary, player_number, 1)
    ask_for_decision(player_and_dealer_dictionary, playing_deck, actual_players)
    
    break

