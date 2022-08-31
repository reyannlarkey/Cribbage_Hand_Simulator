import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
class deck:
    def __init__(self):

        ### Set up the deck of cards
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        face_vals = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6":6,
                 "7": 7, "8": 8, "9": 9, "10": 10, "J":10, "Q":10, "K": 10} # Card name and the value associated

        self.cards = [(suit, item[0], item[1]) for suit in suits for item in face_vals.items()] # list of all cards,
                                                                                                # suit, number, and value

    def shuffle_cards(self):
        shuffled_deck = random.sample(self.cards, len(self.cards))

        return shuffled_deck

    def deal_cards(self, n_players=2):
        ''' provide the number of players, this will return the appropriate # of cards per person'''

        if n_players == 2:
            cards_per_player = 6
            discard_one = False
            player_piles = [[],[]] # two empty piles of cards

        elif n_players == 3:
            cards_per_player = 5
            discard_one = True
            player_piles = [[], [], []] # three empty piles of cards

        elif n_players == 4:
            cards_per_player = 5
            discard_one = False
            player_piles = [[], [], [], []] # four empty piles of cards

        else:
            print("only 2, 3, or 4 players are allowed")
            quit()


        shuffled_deck = self.shuffle_cards()
        self.deck_index = 0 #<- I'm just going to define this to keep track of where we are in the deck


        # n_players * cards per player = the total number of cards to draw from the deck
        drawn_cards = shuffled_deck[0: n_players*cards_per_player]    # randomly select that many cards from the deck without replacement
        for i in range(cards_per_player*n_players):
            # print(i%n_players)
            player_piles[i%n_players].append(drawn_cards[i]) # put the cards into player hands sequentially

        self.deck_index+=n_players*cards_per_player #update index


        discard_pile = []
        if discard_one: # if we need to discard one to the main pot, then we do so here
            discard_pile.append(shuffled_deck[self.deck_index])
            self.deck_index+=1

        print(self.deck_index)
        for i in player_piles:
            print(i)
        print(discard_pile)

        updated_deck = shuffled_deck[self.deck_index:]
        print(updated_deck)

        print(sum([len(i) for i in player_piles])+len(discard_pile)+len(updated_deck))
x = deck() # get a deck of cards
x.deal_cards(n_players=3) # deal the cards to the players
