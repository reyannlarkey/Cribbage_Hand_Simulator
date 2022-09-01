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
            print("Only 2, 3, or 4 players are allowed")
            quit()


        shuffled_deck = self.shuffle_cards() # shuffle the deck
        self.deck_index = 0 #<- I'm just going to define this to keep track of where we are in the deck


        ### Deal the cards appropriately
        ### n_players * cards per player = the total number of cards to draw from the deck
        drawn_cards = shuffled_deck[0: n_players*cards_per_player]    # randomly select that many cards from the deck without replacement
        for i in range(cards_per_player*n_players):
            player_piles[i%n_players].append(drawn_cards[i]) # put the cards into player hands sequentially

        self.deck_index+=n_players*cards_per_player #update index

        discard_pile = []
        if discard_one: # if we need to discard one to the main pot, then we do so here
            discard_pile.append(shuffled_deck[self.deck_index])
            self.deck_index+=1

        self.inital_player_hands = player_piles
        self.discard_pile = discard_pile
        self.updated_deck = shuffled_deck[self.deck_index:] # all the cards that are left

    def evaluate_points_in_hands(self, community_card = None):
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
        run_points = self.run_points(player_hands)
        flush_points = self.flush_points(player_hands)

        print("Fifteens: ", n_fifteens)
        print("Pairs: ", n_pairs)
        print("RUN POINTS: ", run_points)
        print("FLUSH POINTS: ", flush_points)

        total_points = (np.asarray(n_fifteens) * 2.0)\
                       + (np.asarray(n_pairs) * 2.0) \
                       + (np.asarray(run_points)) \
                       + (np.asarray(flush_points))

        for i, hand in enumerate(player_hands):
            for j in hand:
                print(j[0:2])
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

            # Have to update these cards so that Jacks don't get paired with Kings, etc.
            for i, card in enumerate(hand):
                if card[1] == "J":
                    hand[i][2] = 11
                if card[1] == "Q":
                    hand[i][2] = 12
                if card[1] == "K":
                    hand[i][2] = 13

            numbers = [i[2] for i in hand] # get just the numbers
            counts = {item: comb(numbers.count(item),2) for item in numbers} # get the # of combinations of pairs
            n_pairs.append(sum(counts.values())) # append the total number of pairs to the n_pairs list
        return n_pairs

    def run_points(self, player_hands):
        # This one's a little trickier, because we need to update:
        # J->11
        # Q->12
        # K->13
        # so we can just look at sequential #'s
        total_score = []
        for hand in player_hands:
            hand = [list(x) for x in hand] # convert hands to lists

            for i, card in enumerate(hand):
                if card[1] == "J":
                    hand[i][2]=11
                if card[1] == "Q":
                    hand[i][2]=12
                if card[1] == "K":
                    hand[i][2] = 13

            numbers = [i[2] for i in hand]  # get just the numbers

            ### This gets the consecutive #'s
            gb = itertools.groupby(enumerate(sorted(set(numbers))), key=lambda x: x[0] - x[1])

            # Repack elements from each group into list
            all_groups = ([i[1] for i in g] for _, g in gb)

            # Filter out one element lists
            run_cards = list(filter(lambda x: len(x) >=3 , all_groups))

            # For each run, count up the points (c), then add them together (total_score)
            hand_score= 0
            for i in run_cards:
                c = len(i)
                for num in i:
                    c*=numbers.count(num)
                hand_score+=c

            total_score.append(hand_score)
        return total_score

    def flush_points(self, player_hands):
        # count up number of cards with same suit, if more than 3, return that many points
        total_points = []
        for hand in player_hands:
            hand = [list(x) for x in hand]  # convert hands to lists
            suits = [hand[0] for hand in hand]

            suit_counts = [suits.count(x) for x in set(suits) if suits.count(x)>3]
            flush_points = sum(suit_counts)
            total_points.append(flush_points)

        return total_points

    def discard_cards(self):
        '''
        This is where things get tricky, and is really the crux of why I wanted to do this.

        There are different ways you could play this, depending on if it's your crib, if you want to
        gamble and try and maximize the potential points you get, if you want to play it safe based on
        the points in your hand, etc.

        Just to implement *something* I'm going to have it maximize the points in the hand currently.
        This can/will be changed later, but let's just start with this.
        '''

        player_hands = self.inital_player_hands

        for hand in player_hands:
            print(hand)


        pass


x = cribbage() # get a deck of cards
x.deal_cards(n_players=2) # deal the cards to the players
# x.evaluate_points_in_hands()#community_card=x.discard_pile[0])
x.discard_cards()

# for hand in x.inital_player_hands:
#     print(hand)
#
# print(x.discard_pile)
# print(x.updated_deck)
#
# print()
# print(sum([len(i) for i in x.inital_player_hands])+len(x.discard_pile)+len(x.updated_deck))