from probBotFunctions import prob_of_winning_trick
from statistics import mean
from betabot import *
import abc


class Player:
    def __init__(self, name):
        self.hand = []
        self.score = 0
        self.name = name

    def display_hand_ascii(self):
        if len(self.hand) == 0:
            print(f"{self.name} has no cards")
        else:
            asci_list = [card.get_ascii() for card in self.hand]
            asci_list = [i.split("\n") for i in asci_list]
            for i in zip(*asci_list):
                print("".join(i))

    def get_allowed_cards(self, leading_suit):
        if leading_suit:
            suit_list = [card.suit for card in self.hand]
            req_to_play_leading = leading_suit in suit_list
            if req_to_play_leading:
                allowed_list = [
                    card for card in self.hand if card.suit == leading_suit
                ]
            else:
                allowed_list = self.hand
        else:
            allowed_list = self.hand

        return allowed_list

    def draw(self, card):
        self.hand.append(card)

    @abc.abstractclassmethod
    def play(self, leading_suit, gamestate):
        ...

    def display_hand(self):
        if len(self.hand) == 0:
            print(f"{self.name} has no cards")
        else:
            print(f"{self.name} has {len(self.hand)} cards:")
            print(", ".join([card.display() for card in self.hand]))

    def reset_hand(self):
        self.hand = []

    @abc.abstractclassmethod
    def predict(self, allowed, gamestate):
        ...


class ShitBot(Player):
    def play(self, leading_suit, gamestate):
        allowed_to_play = self.get_allowed_cards(leading_suit)
        display_value = {14: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        display_value.update({i: str(i) for i in range(2, 11)})
        allowed_to_play_display = [
            display_value[i.value] + " of " + i.suit for i in allowed_to_play
        ]
        choice = 0
        played_card = allowed_to_play[choice]
        self.hand.remove(played_card)  # remove
        return played_card

    def predict(self, allowed, gamestate):
        n_trumps = len(
            [
                card
                for card in self.hand
                if card.suit == gamestate.current_trump_card.suit
            ]
        )
        self.prediction = n_trumps
        return self.prediction


class Human(Player):
    def play(self, leading_suit, gamestate):
        allowed_to_play = self.get_allowed_cards(leading_suit)
        asci_list = [card.get_ascii() for card in allowed_to_play]
        asci_list = [i.split("\n") for i in asci_list]

        asci_str = ""
        for i in zip(*asci_list):
            asci_str += ("".join(i)) + "\n"

        choice = input("Choice of cards to play: (input int)\n" + asci_str)
        choice = int(choice)
        played_card = allowed_to_play[choice]
        self.hand.remove(played_card)  # remove
        return played_card

    def predict(self, allowed, gamestate):

        print(f"Possible guesses are {', '.join([str(x) for x in allowed])}")
        self.display_hand_ascii()
        prediction = int(input("Enter your guess: "))

        while prediction not in allowed:
            prediction = int(input("Enter an allowed prediction: "))

        self.prediction = prediction
        return self.prediction


class ProbBot(Player):
    def play(self, leading_suit, gamestate):
        allowed_to_play = self.get_allowed_cards(leading_suit)
        display_value = {14: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        display_value.update({i: str(i) for i in range(2, 11)})
        allowed_to_play_display = [
            display_value[i.value] + " of " + i.suit for i in allowed_to_play
        ]
        choice = 0
        played_card = allowed_to_play[choice]
        self.hand.remove(played_card)  # remove
        return played_card

    def predict(self, allowed, gamestate):
        trump_suit = gamestate.current_trump_card.suit
        n_cards = len(self.hand)
        excluded = self.hand
        played = []
        n_players = gamestate.n_players
        prediction = 0
        for card in self.hand:
            prob_winning_list = []
            print(card.display())
            for leading_suit in ["Hearts", "Spades", "Clubs", "Diamonds"]:
                prob_winning_trick = prob_of_winning_trick(
                    card,
                    trump_suit,
                    leading_suit,
                    n_cards,
                    played,
                    excluded,
                    n_players,
                )
                prob_winning_list.append(prob_winning_trick)

            card_guess = mean(prob_winning_list)
            prediction += card_guess
        self.prediction = round(prediction)
        return self.prediction


class BetaBot(Player):
    def play(self, leading_suit, gamestate):
        allowed_to_play = self.get_allowed_cards(leading_suit)
        played_card = allowed_to_play[0]
        self.hand.remove(played_card)  # remove
        return played_card

    def predict(self, allowed, gamestate):

        hand_points = points_in_hand(
            self.hand, gamestate.n_players, gamestate.current_trump_card.suit
        )

        hand_percentile = points_to_percentile(
            hand_points,
            gamestate.n_players,
            gamestate.current_round,
            gamestate.current_trump_card.suit,
            gamestate.training,
        )
        expected_tricks = percentile_to_expected(
            hand_percentile, gamestate.n_players, gamestate.current_round
        )

        prediction = round(expected_tricks)
        self.prediction = prediction

        return prediction
