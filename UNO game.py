#!/usr/bin/env python3
"""
Assignment 2 - UNO++
CSSE1001/7030
Semester 2, 2018
"""

import random

__author__ = "Minh Anh Bui 45041899"

# Write your classes here

class Card(object):
    '''
    A class to manage the card being played in Uno
    '''
    def __init__(self, number, colour):
        '''
        Construct the card being played in Uno
        '''
        self._number = number
        self._colour = colour
        self._pickup_amount = 0
        
    def get_number(self):
        '''
        Return the number of the card being played
        '''
        return self._number

    def get_colour(self):
        '''
        Return the colour of the card being played
        '''
        return self._colour

    def set_number(self, number):
        '''
        Change the current number of the card to a new number

        Parameter:
            number(int):The new number
        '''
        self._number = int(number)

    def set_colour(self, colour):
        '''
        Change the current colour of the card to a new colour

        Parameter:
            colour(str):The new colour
        '''
        self._colour = colour
    
    def get_pickup_amount(self):
        '''
        Return the colour of the card being played
        '''
        return self._pickup_amount

    def matches(self, card):
        ''' Determine whether the card is a match for the card currently being played
            A match means it is legally placed on top.

            Parameter:
                card(Card): The new card to be check

            Return:
                True if legal, otherwise False
        '''
        if self._colour == card._colour:
            return True

        elif type(self) != SkipCard and type(self) != ReverseCard and type(self) != Pickup2Card:
            if self._number == card._number:
                return True
            elif type(self) == Pickup4Card:
                return True
            else:
                return False
        else:
            return False

    
    def play(self, player, game):
        '''
        Catergorize special cards, then apply special actions towards the game

        Parameter:
                player(Player): The player who played the special card
                game(UnoGame): The game being processed
                
        '''
        if type(self) == SkipCard:
            game.skip()
            
        elif type(self) == ReverseCard:
            game.reverse()
            
        elif type(self) == Pickup2Card:
            cards_adding=game.pickup_pile.pick(self.get_pickup_amount())
            game.get_turns().peak().get_deck().add_cards(cards_adding)
            
                        
        elif type(self) == Pickup4Card:
            cards_adding=game.pickup_pile.pick(self.get_pickup_amount())
            game.get_turns().peak().get_deck().add_cards(cards_adding)
            
    def __str__(self):
        '''
        Returns the string representation of this card
        '''
        return 'Card({0}, {1})'.format(self._number, self._colour)

    def __repr__(self):
        '''
        Returns the string representation of this card
        '''
        return self.__str__()
       
class SkipCard(Card):
    '''
        This is a sub-class of Cards.
        This special card skips the turn of the next player
    '''
    def __init__(self, number, colour):
        super().__init__(number, colour)

    def __str__(self):
        return 'SkipCard({0}, {1})'.format(self._number, self._colour)

    def __repr__(self):
        return self.__str__()
        
class Pickup2Card(Card):
    '''
        This is a sub-class of Cards.
        This special card obliges the next player to pick up 2 cards
    '''
    def __init__(self, number, colour):
        super().__init__(number, colour)
        self._pickup_amount=2

    def __str__(self):
        return 'Pickup2Card({0}, {1})'.format(self._number, self._colour)

    def __repr__(self):
        return self.__str__()
        
class ReverseCard(Card):
    '''
        This is a sub-class of Cards.
        This special card reverse the order of turns
    '''
    def __init__(self, number, colour):
        super().__init__(number, colour)

    def __str__(self):
        return 'ReverseCard({0}, {1})'.format(self._number, self._colour)

    def __repr__(self):
        return self.__str__()
        
class Pickup4Card(Card):
    '''
        This is a sub-class of Cards.
        This special card obliges the next player to pick up 4 cards
        This card matches every other cards.
    '''
    def __init__(self, number, colour):
        super().__init__(number, colour)
        self._pickup_amount=4

    def __str__(self):
        return 'Pickup4Card({0}, {1})'.format(self._number, self._colour)

    def __repr__(self):
        return self.__str__()

class Deck(object):
    '''
    A class to manage deck being played in Uno
    '''
    def __init__(self,starting_cards=None):
        '''
        Construct the deck being played in Uno
        '''
        self._starting_cards = starting_cards
        if self._starting_cards == None:
            self._starting_cards=[]

    def get_cards(self):
        '''
        Return the cards in the deck
        '''
        return self._starting_cards

    def get_amount(self):
        '''
        Return the number of the cards in the deck
        '''
        return len(self._starting_cards)

    def shuffle(self):
        '''
        Return the cards in the deck with a new order(shuffled)
        '''
        return random.shuffle(self._starting_cards)

    def pick(self, amount = 1):
        '''
        Pick the first amount of cards from the top offs the deck
        Return the cards picked
        '''
        temp_li=[]
        if len(self._starting_cards) != 0:
            for i in range(1, amount+1):
               temp=self._starting_cards[-1]
               temp_li.append(temp)
               self._starting_cards.pop()
               i+=1
            return temp_li
        else:
            raise NotImplementedError
        

    def add_card(self, card):
        '''
        Add a card in the deck 
        '''
        self._starting_cards.append(card)

    def add_cards(self, cards):
        '''
        Add a list of cards in the deck
        '''
        for card in cards:
           self._starting_cards.append(card)   

    def top(self):
        '''
        Return the card in the top of the deck
        '''
        return self._starting_cards[-1]
        
class Player(object):
    '''
    A class to manage player in Uno
    '''
    def __init__(self, name):
        '''
        Construct the player in Uno
        '''
        self._name = name
        self._deck = Deck()
        

    def get_name(self):
        '''
        Return the name of the player
        '''
        return self._name

    def get_deck(self):
        '''
        Return the deck of the current player
        '''
        return self._deck

    def is_playable(self):
        '''
        Determine whether the Player is 'playable'
        Return True for HumanPlayer, otherwise False
        '''
        raise NotImplementedError()
        

    def has_won(self):
        '''
        Determine whether the Player has won the game or not
        by checking the number of cards on hand
        
        Return True if the deck is empty, otherwise False
        '''
        if len(self._deck._starting_cards) == 0:
            return True
        else:
            return False

    def pick_card(self, putdown_pile):
        '''
        Select a card in the deck to be played next.
        The selected card would be taken off the deck.
        This only implies for Computer Player, otherwise return None
        '''
        raise NotImplementedError()
        
        
                
class HumanPlayer(Player):
    '''
        This is a sub-class of Player, specifies the non-automated player
    '''
    def __init__(self, name):
        super().__init__(name)

    def is_playable(self):
        '''
        Determine whether the Player is 'playable'
        Return True for HumanPlayer, otherwise False
        '''
        return True

    def pick_card(self, putdown_pile):
        '''
        Select a card in the deck to be played next.
        The selected card would be taken off the deck.
        This only implies for Computer Player, otherwise return None
        '''
        return None
    
class ComputerPlayer(Player):
    '''
        This is a sub-class of Player, specifies the automated player
    '''
    def __init__(self, name):
        super().__init__(name)

    def is_playable(self):
        '''
        Determine whether the Player is 'playable'
        Return True for HumanPlayer, otherwise False
        '''
        return False

    def pick_card(self, putdown_pile):
        '''
        Select a card in the deck to be played next.
        The selected card would be taken off the deck.
        This only implies for Computer Player, otherwise return None
        '''
        last_card=putdown_pile._starting_cards[-1]
        current_deck=self._deck.get_cards()
        for card in current_deck:
            if card.matches(last_card)== True:
                self._deck._starting_cards.remove(card)
                return card

   
def main():
    print("Please run gui.py instead")


if __name__ == "__main__":
    main()
