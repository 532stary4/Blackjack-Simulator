from random import randint

def create_deck():
    for i in range(1,5):
        for j in range(1,14):
            standard_deck_of_cards.append((i,j))

def create_playing_deck(number):
    out_deck = []
    
    for i in range(number):
        for items in standard_deck_of_cards:
            out_deck.insert(randint(0, len(out_deck)), items)
    
    return out_deck




standard_deck_of_cards = []
create_deck()
playing_deck = create_playing_deck(2)


