"""Sample tests for assignment 2
CSSE1001
Semester 2, 2018
"""

__author__ = 'Brae Webb and Benjamin Martin'
__version__ = '1.0.0'

#!/usr/bin/env python3
from testrunner import OrderedTestCase, TestMaster
from testrunner import skipIfFailed

import a2
import a2_support

CARD_CLASS = {
    '__init__': 3,
    'get_number': 1,
    'set_number': 2,
    'get_colour': 1,
    'set_colour': 2,
    'get_pickup_amount': 1,
    'matches': 2,
    'play': 3,
    '__str__': 1,
    '__repr__': 1
}

CARD_SUBCLASSES = [
    'SkipCard',
    'ReverseCard',
    'Pickup2Card',
    'Pickup4Card'
]

CARD_PICKUP_AMOUNTS = {
    a2.Card: 0,
    a2.SkipCard: 0,
    a2.ReverseCard: 0,
    a2.Pickup2Card: 2,
    a2.Pickup4Card: 4
}

DECK_CLASS = {
    # TODO: check keyword argument
    '__init__': 2,
    'get_cards': 1,
    'get_amount': 1,
    'shuffle': 1,
    # TODO: check keyword argument
    'pick': 2,
    'add_cards': 2,
    'add_card': 2,
    'top': 1,
}

PLAYER_CLASS = {
    '__init__': 2,
    'get_name': 1,
    'get_deck': 1,
    'is_playable': 1,
    'has_won': 1,
    'pick_card': 2
}

PLAYER_SUBCLASSES = [
    'HumanPlayer',
    'ComputerPlayer'
]


class TestDesign(OrderedTestCase):
    def test_card_defined(self):
        """Card class is defined"""
        self.assertClassDefined(a2, 'Card')

    @skipIfFailed(test_name='test_card_defined')
    def test_card_methods(self):
        """Card class has required methods"""
        for name, arg_count in CARD_CLASS.items():
            self.assertFunctionDefined(a2.Card, name, arg_count)

    @skipIfFailed(test_name='test_card_methods')
    def test_card_docstring(self):
        """All Card class methods have docstrings"""
        for name in CARD_CLASS:
            self.assertDocString(a2.Card, name)

    @skipIfFailed(test_name='test_card_methods')
    def test_card_subclasses(self):
        """All card subclasses are defined"""
        for class_name in CARD_SUBCLASSES:
            self.assertClassDefined(a2, class_name)

    @skipIfFailed(test_name='test_card_subclasses')
    def test_card_are_subclasses(self):
        """All card subclasses are actually subclasses of Card"""
        for class_name in CARD_SUBCLASSES:
            self.assertIsSubclass(getattr(a2, class_name), a2.Card)

    def test_deck_defined(self):
        """Deck class is defined"""
        self.assertClassDefined(a2, 'Deck')

    @skipIfFailed(test_name='test_deck_defined')
    def test_deck_methods(self):
        """Deck class has required methods"""
        for name, arg_count in DECK_CLASS.items():
            self.assertFunctionDefined(a2.Deck, name, arg_count)

    @skipIfFailed(test_name='test_deck_methods')
    def test_deck_docstring(self):
        """All Deck class methods have docstrings"""
        for name in DECK_CLASS:
            self.assertDocString(a2.Deck, name)

    def test_player_defined(self):
        """Player class is defined"""
        self.assertClassDefined(a2, 'Player')

    @skipIfFailed(test_name='test_player_defined')
    def test_player_methods(self):
        """Player class has required methods"""
        for name, arg_count in PLAYER_CLASS.items():
            self.assertFunctionDefined(a2.Player, name, arg_count)

    @skipIfFailed(test_name='test_player_methods')
    def test_player_docstring(self):
        """All player class methods have docstrings"""
        for name in PLAYER_CLASS:
            self.assertDocString(a2.Player, name)

    @skipIfFailed(test_name='test_player_methods')
    def test_player_subclasses(self):
        """All player subclasses are defined"""
        for class_name in PLAYER_SUBCLASSES:
            self.assertClassDefined(a2, class_name)

    @skipIfFailed(test_name='test_player_subclasses')
    def test_player_are_subclasses(self):
        """All player subclasses are actually subclasses of Player"""
        for class_name in PLAYER_SUBCLASSES:
            self.assertIsSubclass(getattr(a2, class_name), a2.Player)


class TestCard(OrderedTestCase):
    def test_card_getters(self):
        card = a2.Card(23, a2_support.CardColour.red)
        self.assertEqual(card.get_number(), 23,
                         "Card.get_number returns incorrect value")
        self.assertEqual(card.get_colour(), a2_support.CardColour.red,
                         "Card.get_colour returns incorrect value")

    @skipIfFailed(test_name='test_card_getters')
    def test_card_setters(self):
        card = a2.Card(23, a2_support.CardColour.green)
        self.assertIsNone(card.set_number(42), "Card.set_number returns value")
        self.assertEqual(card.get_number(), 42,
                         "Card.set_number does not update value")

        self.assertIsNone(card.set_colour(a2_support.CardColour.yellow),
                          "Card.set_colour returns value")
        self.assertEqual(card.get_colour(), a2_support.CardColour.yellow,
                         "Card.set_colour does not update value")

    def test_card_pickup_amount(self):
        for card_class, amount in CARD_PICKUP_AMOUNTS.items():
            card = card_class(14, a2_support.CardColour.yellow)
            self.assertEqual(card.get_pickup_amount(), amount,
                             f"{card_class.__name__} should have a pickup amount of {amount}")

    def test_card_matches_number(self):
        for card_class in (a2.Card, ):
            card = card_class(23, a2_support.CardColour.green)
            same = card_class(23, a2_support.CardColour.red)
            different = card_class(342, a2_support.CardColour.red)

            self.assertIs(card.matches(same), True, f"Green 23 {card_class.__name__} should have same number as red 23")
            self.assertIs(same.matches(card), True, f"Red 23 {card_class.__name__} should have same number as green 23")

            self.assertIs(card.matches(different), False, f"Green 23 {card_class.__name__} should not have same number as red 342")
            self.assertIs(different.matches(card), False, f"Red 342 {card_class.__name__} should have same number as green 23")

    def test_card_matches_colour(self):
        for card_class in (a2.SkipCard, a2.ReverseCard, a2.Pickup2Card):
            card = card_class(23, a2_support.CardColour.green)
            other = card_class(354, a2_support.CardColour.green)
            red = card_class(234, a2_support.CardColour.red)
            yellow = card_class(234, a2_support.CardColour.yellow)
            blue = card_class(234, a2_support.CardColour.blue)

            self.assertIs(card.matches(other), True, f"Green {card_class.__name__} should match same colour (1)")
            self.assertIs(other.matches(card), True, f"Green {card_class.__name__} should match same colour (2)")

            self.assertIs(card.matches(red), False, f"Green {card_class.__name__} should not match red (1)")
            self.assertIs(red.matches(card), False, f"Green {card_class.__name__} should not match red (2)")

            self.assertIs(card.matches(yellow), False, f"Green {card_class.__name__} should not match yellow (1)")
            self.assertIs(yellow.matches(card), False, f"Green {card_class.__name__} should not match yellow (2)")

            self.assertIs(card.matches(blue), False, f"Green {card_class.__name__} should not match blue (1)")
            self.assertIs(blue.matches(card), False, f"Green {card_class.__name__} should not match blue (2)")

    def test_card_matches_any(self):
        for card_class in (a2.Pickup4Card, ):
            card = card_class(23, a2_support.CardColour.green)
            other = card_class(354, a2_support.CardColour.green)
            red = card_class(234, a2_support.CardColour.red)
            yellow = card_class(23244, a2_support.CardColour.yellow)
            blue = card_class(0, a2_support.CardColour.blue)

            self.assertIs(card.matches(other), True, f"Green {card_class.__name__} should match same colour (1)")
            self.assertIs(other.matches(card), True, f"Green {card_class.__name__} should match same colour (2)")

            self.assertIs(card.matches(red), True, f"Green {card_class.__name__} should match red (1)")
            self.assertIs(red.matches(card), True, f"Green {card_class.__name__} should match red (2)")

            self.assertIs(card.matches(yellow), True, f"Green {card_class.__name__} should match yellow (1)")
            self.assertIs(yellow.matches(card), True, f"Green {card_class.__name__} should match yellow (2)")

            self.assertIs(card.matches(blue), True, f"Green {card_class.__name__} should match blue (1)")
            self.assertIs(blue.matches(card), True, f"Green {card_class.__name__} should match blue (2)")

    def test_card_str(self):
        card = a2.Card(90, a2_support.CardColour.red)
        skip = a2.SkipCard(12, a2_support.CardColour.yellow)
        reverse = a2.ReverseCard(3, a2_support.CardColour.green)
        pickup2 = a2.Pickup2Card(45, a2_support.CardColour.blue)
        pickup4 = a2.Pickup4Card(56, a2_support.CardColour.black)

        self.assertEqual(str(card), 'Card(90, CardColour.red)', 'Card.__str__ does not return correctly')
        self.assertEqual(repr(card), 'Card(90, CardColour.red)', 'Card.__repr__ does not return correctly')

        self.assertEqual(str(skip), 'SkipCard(12, CardColour.yellow)', 'SkipCard.__str__ does not return correctly')
        self.assertEqual(repr(skip), 'SkipCard(12, CardColour.yellow)', 'SkipCard.__repr__ does not return correctly')

        self.assertEqual(str(reverse), 'ReverseCard(3, CardColour.green)', 'ReverseCard.__str__ does not return correctly')
        self.assertEqual(repr(reverse), 'ReverseCard(3, CardColour.green)', 'ReverseCard.__repr__ does not return correctly')

        self.assertEqual(str(pickup2), 'Pickup2Card(45, CardColour.blue)', 'Pickup2Card.__str__ does not return correctly')
        self.assertEqual(repr(pickup2), 'Pickup2Card(45, CardColour.blue)', 'Pickup2Card.__repr__ does not return correctly')

        self.assertEqual(str(pickup4), 'Pickup4Card(56, CardColour.black)', 'Pickup4Card.__str__ does not return correctly')
        self.assertEqual(repr(pickup4), 'Pickup4Card(56, CardColour.black)', 'Pickup4Card.__repr__ does not return correctly')

class TestGameplay(OrderedTestCase):
    def loadGame(self):
        deck = [
            a2.Card(1, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.green),
            a2.Card(4, a2_support.CardColour.yellow),
            a2.Card(5, a2_support.CardColour.red),
            a2.Card(6, a2_support.CardColour.blue),
            a2.Card(7, a2_support.CardColour.blue),
        ]
        self._deck = a2.Deck(starting_cards=deck)
        self._players = [
            a2.HumanPlayer("Anna Truffet"),
            a2.ComputerPlayer("Ashleigh Richardson"),
            a2.HumanPlayer("Benjamin Martin"),
            a2.ComputerPlayer("Brae Webb"),
            a2.HumanPlayer("Harry Keightly"),
            a2.ComputerPlayer("Henry O'Brien"),
            a2.HumanPlayer("Joshua Arnold"),
            a2.ComputerPlayer("Justin Luong"),
            a2.HumanPlayer("Luis Woodrow"),
            a2.ComputerPlayer("Mike Pham"),
            a2.HumanPlayer("Rudi Scarpa"),
            a2.ComputerPlayer("Sam Eadie"),
            a2.HumanPlayer("Steven Summers"),
            a2.ComputerPlayer("Wilson Kong"),
        ]
        self._game = a2_support.UnoGame(self._deck, self._players)

    def test_play_card(self):
        self.loadGame()
        self.assertEqual(self._players[0], self._game.get_turns().current(),
                         "Game should start with first player")

        skip_card = a2.Card(21, a2_support.CardColour.blue)
        skip_card.play(self._players[0], self._game)

        # play should have no effect
        self.assertEqual(self._players[0].get_name(),
                         self._game.get_turns().current().get_name(),
                         "Playing Card should change the player")

        self.assertEqual(self._game.get_turns().peak().get_deck().get_amount(), 0,
                         "Playing Card should change player's deck")

    def test_play_skip(self):
        self.loadGame()
        self.assertEqual(self._players[0], self._game.get_turns().current(),
                         "Game should start with first player")

        skip_card = a2.SkipCard(-1, a2_support.CardColour.blue)
        skip_card.play(self._players[0], self._game)

        self.assertEqual(self._players[1].get_name(),
                         self._game.get_turns().current().get_name(),
                         "Playing SkipCard should skip to next player")

        self._game.get_turns().skip(count=4)
        skip_card.play(self._players[6], self._game)

        self.assertEqual(self._players[7].get_name(),
                         self._game.get_turns().current().get_name(),
                         "Playing SkipCard should skip to next player")

    def test_play_reverse(self):
        self.loadGame()
        self.assertEqual(self._players[0], self._game.get_turns().current(),
                         "Game should start with first player")

        reverse_card = a2.ReverseCard(-1, a2_support.CardColour.blue)
        reverse_card.play(self._players[0], self._game)

        self.assertEqual(self._players[-1].get_name(),
                         self._game.get_turns().peak().get_name(),
                         "Playing ReverseCard should reverse order")

        self._game.get_turns().skip(count=4)

        self.assertEqual(self._players[-5].get_name(),
                         self._game.get_turns().current().get_name(),
                         "Playing ReverseCard should reverse order")

        reverse_card.play(self._players[-5], self._game)
        self._game.get_turns().skip(count=2)

        self.assertEqual(self._players[-2].get_name(),
                         self._game.get_turns().current().get_name(),
                         "Playing ReverseCard should reverse order")

    def test_play_pickup(self):
        self.loadGame()
        pickup2 = a2.Pickup2Card(13, a2_support.CardColour.blue)

        pickup2.play(self._players[0], self._game)

        self.assertEqual(self._game.get_turns().peak().get_deck().get_amount(), 2, "Playing a Pickup2Card should force the next player to pickup 2 cards")

        self._game.next_player()
        self._game.next_player()

        pickup4 = a2.Pickup4Card(10, a2_support.CardColour.red)

        pickup4.play(self._players[2], self._game)

        self.assertEqual(self._game.get_turns().peak().get_deck().get_amount(), 4, "Playing a Pickup4Card should force the next player to pickup 4 cards")


class TestDeck(OrderedTestCase):
    def test_deck_constructor(self):
        deck = a2.Deck()
        self.assertEqual(deck.get_cards(), [],
                         "A Deck with no starting cards should be empty")

        deck = a2.Deck(starting_cards=None)
        self.assertEqual(deck.get_cards(), [],
                         "A Deck with no starting cards should be empty")

        deck1 = a2.Deck()
        deck2 = a2.Deck()
        card = a2.Card(1, a2_support.CardColour.blue)
        deck1.add_card(card)
        self.assertEqual(deck2.get_cards(), [], "List should not be used for default value for starting_cards (should be None)")

    def test_deck_cards_amount(self):
        cards = [
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green)
        ]
        deck = a2.Deck(starting_cards=cards)
        self.assertListEqual(deck.get_cards(), cards,
                             "starting_cards parameter should be used to populate deck")
        self.assertEqual(deck.get_amount(), 3)

    def test_deck_shuffle(self):
        cards = [
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green)
        ]
        deck = a2.Deck(starting_cards=cards.copy())

        found_different = False
        for _ in range(30):
            deck.shuffle()
            if deck.get_cards() != cards:
                found_different = True
                break

        self.assertIs(found_different, True, "Deck.shuffle should randomise order")

    def test_deck_pick(self):
        cards = [
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green),
            a2.Card(4, a2_support.CardColour.yellow),
            a2.Card(6, a2_support.CardColour.yellow),
            a2.Card(10, a2_support.CardColour.blue)
        ]
        deck = a2.Deck(starting_cards=cards)

        expected_cards = cards[-4:-1]

        self.assertListEqual(cards[-1:], deck.pick())

        actual_cards = deck.pick(amount=3)
        self.assertEqual(len(expected_cards), len(actual_cards),
                         "Deck.pick returns incorrect amount of cards")
        for card in actual_cards:
            self.assertIn(card, expected_cards,
                          "Deck.pick returns unexpected card")

    def test_deck_add_cards(self):
        cards1 = [
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red)
        ]
        deck = a2.Deck()
        deck.add_cards(cards1)

        self.assertListEqual(deck.get_cards(), cards1, "Deck's cards are invalid after adding a list of cards")

        cards2 = [
            a2.Card(4, a2_support.CardColour.yellow),
            a2.Card(6, a2_support.CardColour.yellow)
        ]
        deck.add_cards(cards2)

        self.assertListEqual(deck.get_cards(), cards1 + cards2, "Deck's cards are invalid after adding a second list of cards")

    def test_deck_add_card(self):
        cards = [
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green),
            a2.Card(4, a2_support.CardColour.yellow),
            a2.Card(6, a2_support.CardColour.yellow),
            a2.Card(10, a2_support.CardColour.blue)
        ]
        deck = a2.Deck()
        deck.add_card(cards[0])
        deck.add_card(cards[1])
        deck.add_card(cards[2])
        deck.add_card(cards[3])
        deck.add_card(cards[4])
        deck.add_card(cards[5])

        self.assertListEqual(deck.get_cards(), cards, "Deck.get_cards returns incorrectly")

    @skipIfFailed(test_name='test_deck_pick')
    def test_deck_top(self):
        cards = [
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green),
            a2.Card(4, a2_support.CardColour.yellow),
            a2.Card(6, a2_support.CardColour.yellow),
            a2.Card(10, a2_support.CardColour.blue)
        ]
        deck = a2.Deck(starting_cards=cards.copy())

        self.assertEqual(cards[-1], deck.top(), "Deck.top returns wrong card")
        deck.pick()


class TestPlayer(OrderedTestCase):
    def test_player_constructor(self):
        player = a2.Player("Test Player")

        self.assertEqual(player.get_name(), "Test Player")
        self.assertListEqual(player.get_deck().get_cards(), [], "Player should have no cards initially")

    def test_player_playable(self):
        with self.assertRaises(NotImplementedError):
            a2.Player("Test Player").is_playable()

        self.assertIs(a2.HumanPlayer("Test Player").is_playable(), True, "HumanPlayer.is_playable should return True")
        self.assertIs(a2.ComputerPlayer("Test Player").is_playable(), False, "ComputerPlayer.is_playable should return False")

    def test_player_has_won(self):
        player = a2.Player("Test Player")

        self.assertIs(player.has_won(), True)

        player.get_deck().add_card(a2.Card(9, a2_support.CardColour.blue))
        player.get_deck().add_card(a2.Card(8, a2_support.CardColour.red))
        player.get_deck().add_card(a2.Card(7, a2_support.CardColour.black))

        self.assertIs(player.has_won(), False, "Player.has_won should return False if the Player has cards")

    def test_player_pick_card(self):
        deck = a2.Deck()
        deck.add_cards([
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green),
            a2.Card(4, a2_support.CardColour.yellow),
            a2.Card(6, a2_support.CardColour.yellow),
            a2.Card(10, a2_support.CardColour.blue)
        ])

        with self.assertRaises(NotImplementedError):
            a2.Player("Test Player").pick_card(deck)

        player = a2.HumanPlayer("Test Player")
        player.get_deck().add_cards(deck.get_cards().copy())

        self.assertIsNone(player.pick_card(deck), 'HumanPlayer.pick_card should return None')

    def test_player_pick_card_auto(self):
        deck = a2.Deck()
        deck.add_cards([
            a2.Card(1, a2_support.CardColour.blue),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green),
            a2.Card(4, a2_support.CardColour.yellow),
            a2.Card(6, a2_support.CardColour.yellow),
            a2.Card(10, a2_support.CardColour.blue)
        ])

        player = a2.ComputerPlayer("Test Player")

        player.get_deck().add_card(a2.Card(6, a2_support.CardColour.yellow))
        picked = player.pick_card(deck)
        self.assertIsNone(picked, "ComputerPlayer.pick_card should return None if no card can be played")

        cards = [
            a2.Card(10, a2_support.CardColour.yellow),
            a2.Card(3, a2_support.CardColour.red),
            a2.Card(2, a2_support.CardColour.green),
            a2.Card(4, a2_support.CardColour.blue),
            a2.Card(5, a2_support.CardColour.yellow),
        ]
        player.get_deck().add_cards(cards)
        picked = player.pick_card(deck)
        self.assertIsInstance(picked, a2.Card, "ComputerPlayer.pick_card should return an instance of Card (or a subclass) if it is possible to play a card")


def main():
    test_cases = [
        TestDesign,
        TestCard,
        TestDeck,
        TestPlayer,
        TestGameplay,
    ]

    master = TestMaster()
    master.run(test_cases)


if __name__ == '__main__':
    main()
