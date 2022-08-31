import numpy as np
import matplotlib.pyplot as plt
import itertools
class deck:
    def __init__(self):
        suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
        face_vals = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6":6,
                 "7": 7, "8": 8, "9": 9, "10": 10, "J":10, "Q":10, "K": 10} # Card name and the value associated


        self.cards = [(suit, item[0], item[1]) for suit in suits for item in face_vals.items()] # list of all cards, suit, number, and value

    def choose_card(self):




x = deck()
