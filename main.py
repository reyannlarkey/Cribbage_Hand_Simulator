import numpy as np
import matplotlib.pyplot as plt
import itertools
import random
from math import comb

class cribbage:
    def __init__(self):

        ### Set up the deck of cards
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        face_vals = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6":6,
                 "7": 7, "8": 8, "9": 9, "10": 10, "J":10, "Q":10, "K": 10} # Card name and the value associated

        self.deck = [(suit, item[0], item[1]) for suit in suits for item in face_vals.items()] # list of all cards,
                                                                                                # suit, number, and value

    def shuffle_cards(self):
        shuffled_deck = random.sample(self.deck, len(self.deck))
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


        shuffled_deck = self.shuffle_cards() # shuffle the deck
        self.deck_index = 0 #<- I'm just going to define this to keep track of where we are in the deck


        ### Deal the cards appropriately

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

        self.inital_player_hands = player_piles
        self.discard_pile = discard_pile
        self.updated_deck = shuffled_deck[self.deck_index:] # all the cards that are left


    def evaluate_points_in_hand(self, community_card = None):
        '''
        Count up all the points in the hand currently
        if community card is passed in, include it in the hand count.

        This could be used before discarding any cards to see what gives the most points so far,
        or after the game is played to count pegging points.

        # There are a lot of ways to score:
        #
        # 15              | 2 points
        # Pair            | 2 points
        #
        # Three of a kind |	6 points  **** THESE TWO ARE JUST SUBSETS OF THE PAIRS REALLY ****
        # Four of a kind  | 12 points ********************************************************
        #
        # Run             | 1 point/card

        # Four Card Flush | 4 points  **** THESE TWO ARE ALSO REALLY JUST THE SAME THING ****
        # Five Card Flush | 5 points  *******************************************************

        # Nobs            | 1 point	(Jack of the same suit as the starter)

        This function is going to call to other functions that evaluate these scoring ways and then will add up all the
        results
        '''

        if community_card!=None: # if we have a community card we want to include do that
            player_hands = self.inital_player_hands
            for i in player_hands:
                i.append(community_card)

        else: # otherwise just look at the hands
            player_hands = self.inital_player_hands



        ### BEGIN CHECKING POINTS ###
        n_fifteens = self.n_fifteens(player_hands)
        n_pairs = self.n_pairs(player_hands)

        

        total_points = (np.asarray(n_fifteens) * 2.0) + (np.asarray(n_pairs) * 2.0)
        for i, hand in enumerate(player_hands):
            print(hand)
            print(total_points[i])
            print()

        # print(player_hands)
        # print("TOTAL POINTS: ",total_points)
        pass

    def n_fifteens(self, player_hands):
        # count up the number of fifteens in a hand
        target = 15
        n_fifteens = []
        for hand in player_hands:
            hand = [list(x) for x in hand] # convert hands to lists
            numbers = [i[2] for i in hand]

            result = [seq for i in range(len(numbers), 0, -1)
                      for seq in itertools.combinations(numbers, i)
                      if sum(seq) == target]

            n_fifteens.append(len(result))
        return n_fifteens
    def n_pairs(self, player_hands):
        # Counts the numbers of pairs in a hand
        n_pairs = []
        for hand in player_hands:
            hand = [list(x) for x in hand] # convert hands to lists
            numbers = [i[2] for i in hand] # get just the numbers
            counts = {item: comb(numbers.count(item),2) for item in numbers} # get the # of combinations of pairs
            n_pairs.append(sum(counts.values())) # append the total number of pairs to the n_pairs list
        return n_pairs

x = cribbage() # get a deck of cards
x.deal_cards(n_players=3) # deal the cards to the players
x.evaluate_points_in_hand(community_card=x.discard_pile[0])


# for hand in x.inital_player_hands:
#     print(hand)
#
# print(x.discard_pile)
# print(x.updated_deck)
#
# print()
# print(sum([len(i) for i in x.inital_player_hands])+len(x.discard_pile)+len(x.updated_deck))