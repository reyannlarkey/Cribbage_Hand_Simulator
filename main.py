import numpy as np
import matplotlib.pyplot as plt
import itertools

import random
from math import comb

class cribbage:
    def __init__(self,n_players):

        ### Set up the deck of cards
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        face_vals = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6":6,
                 "7": 7, "8": 8, "9": 9, "10": 10, "J":10, "Q":10, "K": 10} # Card name and the value associated

        self.deck = [(suit, item[0], item[1]) for suit in suits for item in face_vals.items()] # list of all cards,
                                                                                                # suit, number, and value
        self.n_players= n_players
    def shuffle_cards(self):
        shuffled_deck = random.sample(self.deck, len(self.deck))
        return shuffled_deck

    def deal_cards(self):
        ''' provide the number of players, this will return the appropriate # of cards per person'''

        if self.n_players == 2:
            cards_per_player = 6
            discard_one = False
            player_piles = [[],[]] # two empty piles of cards

        elif self.n_players == 3:
            cards_per_player = 5
            discard_one = True
            player_piles = [[], [], []] # three empty piles of cards

        elif self.n_players == 4:
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
        drawn_cards = shuffled_deck[0: self.n_players*cards_per_player]    # randomly select that many cards from the deck without replacement
        for i in range(cards_per_player*self.n_players):
            player_piles[i%self.n_players].append(drawn_cards[i]) # put the cards into player hands sequentially

        self.deck_index+=self.n_players*cards_per_player #update index

        discard_pile = []
        if discard_one: # if we need to discard one to the main pot, then we do so here
            discard_pile.append(shuffled_deck[self.deck_index])
            self.deck_index+=1

        self.inital_player_hands = player_piles
        self.discard_pile = discard_pile
        self.updated_deck = shuffled_deck[self.deck_index:] # all the cards that are left

    def evaluate_points_in_hand(self, hand_to_evaluate, community_card = None, flip_card = None):
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
            # player_hands = #self.inital_player_hands
            hand_to_evaluate.append(community_card)


        ### BEGIN CHECKING POINTS ###
        n_fifteens = self.n_fifteens(hand_to_evaluate)
        n_pairs = self.n_pairs(hand_to_evaluate)
        run_points = self.run_points(hand_to_evaluate)
        flush_points = self.flush_points(hand_to_evaluate)
        if flip_card!=None:
            nobs_points = self.nobs_points(hand_to_evaluate, flip_card)
        else:
            nobs_points = 0


        # print("Fifteens: ", n_fifteens[0]*2.0)
        # print("Pairs: ", n_pairs[0]*2.0)
        # print("Runs :" ,run_points[0])
        # print("Flushes :", flush_points[0])

        ### add up all the returned points
        total_points = (np.asarray(n_fifteens) * 2.0)\
                       + (np.asarray(n_pairs) * 2.0) \
                       + (np.asarray(run_points)) \
                       + (np.asarray(flush_points))\
                       + (np.asarray(nobs_points))

        # print("Fifteens: ", n_fifteens[0]*2.0)
        # print("Pairs: ", n_pairs[0]*2.0)
        # print("Runs :" ,run_points[0])
        # print("Flushes :", flush_points[0])
        # print("Nobs :", nobs_points)
        return total_points

    def n_fifteens(self, hand_to_evaluate):
        # count up the number of fifteens in a hand
        target = 15
        n_fifteens = []
        hand = [list(x) for x in hand_to_evaluate] # convert hand to lists
        numbers = [i[2] for i in hand]

        result = [seq for i in range(len(numbers), 0, -1)
                  for seq in itertools.combinations(numbers, i)
                  if sum(seq) == target]

        n_fifteens.append(len(result))
        return n_fifteens

    def n_pairs(self, hand_to_evaluate):
        # Counts the numbers of pairs in a hand
        n_pairs = []

        hand = [list(x) for x in hand_to_evaluate] # convert hands to lists

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

    def run_points(self, hand_to_evaluate):
        # This one's a little trickier, because we need to update:
        # J->11
        # Q->12
        # K->13
        # so we can just look at sequential #'s
        total_score = []
        hand = [list(x) for x in hand_to_evaluate] # convert hands to lists

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

    def flush_points(self, hand_to_evaluate):
        # count up number of cards with same suit, if more than 3, return that many points
        total_points = []
        hand = [list(x) for x in hand_to_evaluate]  # convert hand to lists
        suits = [hand[0] for hand in hand]

        suit_counts = [suits.count(x) for x in set(suits) if suits.count(x)>3]
        flush_points = sum(suit_counts)
        total_points.append(flush_points)

        return total_points

    def nobs_points(self, hand_to_evaluate, flip_card):
        nobs_points = 0
        if flip_card[1] != "J": # make sure flip card isn't a jack already
            flip_card_suit = flip_card[0] # if not, check if we have a Jack of same suit in our hand (1 point)
            for card in hand_to_evaluate:
                if card[1]=='J' and card[0] == flip_card_suit:
                    nobs_points = 1
                    break


        return nobs_points

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

        if self.n_players ==2:
            n_discard = 2
        else:
            n_discard = 1

        self.player_hands_after_discard = []
        for hand in player_hands: # check through all the hands
            top_hand, _, discards = self.optimal_discard(hand, n_discard=n_discard)
            self.player_hands_after_discard.append(top_hand)
            self.discard_pile.extend(discards)

        print(self.player_hands_after_discard)
        print(self.discard_pile)

    def optimal_discard(self, hand, n_discard):
        top_score = 0
        top_hand = None
        for combo in itertools.combinations(hand, len(hand)-n_discard): # check all possible combinations of cards
                                                                       # to find the optimal one at the moment.
            possible_hand = list(combo)
            hand_score = self.evaluate_points_in_hand(possible_hand)
            if hand_score > top_score: # if this score is better than zero (or the previous), keep track
                top_score = hand_score
                top_hand = possible_hand

        discarded = list(set(hand) - set(top_hand)) # cards that are discarded in this case
        return top_hand, top_score[0], discarded

    def play_round(self, hands, discard_pile):
        ''' the real meat of the game here...the round'''

        pass




x = cribbage(n_players = 3)# get a deck of cards
x.deal_cards() # deal the cards to the players
x.discard_cards()

# x.evaluate_points_in_hand(hand_to_evaluate=[('Hearts', 'J', 10), ('Clubs', '8', 8), ('Hearts', '8', 8), ('Spades', '4', 4)]),
#                           flip_card=('Hearts', '10', 10))#community_card=x.discard_pile[0])
# print (points)
# x.discard_cards()
# for hand in x.inital_player_hands:
#     print(hand)
#
# print(x.discard_pile)
# print(x.updated_deck)
#
# print()
# print(sum([len(i) for i in x.inital_player_hands])+len(x.discard_pile)+len(x.updated_deck))