from lib import Player
from probBotFunctions import prob_of_winning_trick
from statistics import mean
from betabot import *


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
        print(self.name + " played " + played_card.display())
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

        print(f"{self.name} has made the prediction of {self.prediction}")
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
        print(self.name + " played " + played_card.display())
        return played_card

    def predict(self, allowed, gamestate):

        print(f"Possible guesses are {', '.join([str(x) for x in allowed])}")
        self.display_hand_ascii()
        prediction = int(input("Enter your guess: "))

        while prediction not in allowed:
            prediction = int(input("Enter an allowed prediction: "))

        self.prediction = prediction
        print(f"{self.name} has made the prediction of {self.prediction}")
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
        print(self.name + " played " + played_card.display())
        return played_card

    def predict(self, allowed, gamestate):
        trump_suit = gamestate.current_trump_card.suit
        n_cards = len(self.hand)
        excluded = self.hand
        played = []
        n_players = gamestate.n_players
        # p_leading = 1/n_players
        # p_not_leading = 1-p_leading
        print(self.name, "guessing")
        (self.display_hand_ascii())
        print("trump", trump_suit)
        prediction = 0
        for card in self.hand:
            prob_winning_list = []
            print(card.display())
            for leading_suit in ["Hearts", "Spades", "Clubs", "Diamonds"]:
                print()
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
                print("leading suit", leading_suit, prob_winning_trick)

            card_guess = mean(prob_winning_list)
            prediction += card_guess
            print(card_guess)
            print("\n")
        self.prediction = round(prediction)
        print(f"{self.name} has made the prediction of {self.prediction}")
        return self.prediction


class BetaBot(Player):
    def play(self, leading_suit, gamestate):
        pass

    def predict(self, allowed, gamestate):

        print("Predict starting")
        print(gamestate.current_round)
        hand_points = points_in_hand(
            self.hand, gamestate.n_players, gamestate.current_trump_card.suit
        )
        print(hand_points)
        hand_percentile = points_to_percentile(
            hand_points,
            gamestate.n_players,
            gamestate.current_round,
            gamestate.current_trump_card.suit,
        )
        print(hand_percentile)
        expected_tricks = percentile_to_expected(
            hand_percentile, gamestate.n_players, gamestate.current_round
        )

        return round(expected_tricks)
