from dataclasses import dataclass
from typing import Dict, Type
import random

from players import *

suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
values = list(range(2, 15))


class Card:
    def __init__(self, suit, value):

        # for creating cards in short hand
        if suit in ["h", "s", "d", "c"]:
            suit = {
                "h": "Hearts",
                "s": "Spades",
                "d": "Diamonds",
                "c": "Clubs",
            }[suit]

        self.suit = suit
        self.value = value

    def display(self):
        if self.value in [11, 12, 13, 14]:
            display_value = {14: "Ace", 11: "Jack", 12: "Queen", 13: "King"}[
                self.value
            ]
            return f"{display_value} of {self.suit}"
        else:
            return f"{self.value} of {self.suit}"

    def get_ascii(self):
        display_value_dic = {14: "A ", 11: "J ", 12: "Q ", 13: "K "}
        display_value_dic.update({i: str(i) + " " for i in range(2, 11)})
        display_value_dic.update({10: "10"})
        display_suit_dic = {
            "Spades": "\u2660",
            "Hearts": "\u2665",
            "Diamonds": "\u2666",
            "Clubs": "\u2663",
        }
        card_template = """
 ┌─────────┐
 │{}       │
 │         │
 │         │
 │    {}    │
 │         │
 │         │
 │       {}│
 └─────────┘"""
        display_value = display_value_dic[self.value]
        display_suit = display_suit_dic[self.suit]
        return card_template.format(display_value, display_suit, display_value)


class Deck:
    def __init__(self, suit=None):
        if not suit:
            self.cards = [
                Card(suit, value) for suit in suits for value in values
            ]
        else:
            self.cards = [
                Card(suit, value) for suit in [suit] for value in values
            ]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            print("You cannot draw from an empty deck")
        else:
            draw_card = self.cards[0]
            self.cards = self.cards[1:]
            return draw_card

    def display(self):
        for card in self.cards:
            print(card.display())

    def remove(self, card):
        cards = self.cards
        remove_suit = card.suit
        remove_value = card.value
        new_cards = [
            card
            for card in cards
            if not (card.suit == remove_suit and card.value == remove_value)
        ]
        self.cards = new_cards


class Board:
    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.gamestate = GameState(players)
        self.table = []
        self.trump_suit = None
        self.leading_suit = None
        self.winning_card = None
        self.winning_card_score = None
        self.winning_player = None

    def deal(self, cards):
        self.deck.shuffle()
        for _ in range(cards):
            for player in self.players:
                player.draw(self.deck.draw())

        self.gamestate.reset()
        self.gamestate.set_round(cards)
        self.gamestate.current_trump_card = self.deck.draw()
        self.trump_suit = self.gamestate.current_trump_card.suit

    def train(self, n_tricks: int, iterations: int):
        self.reset()

        self.gamestate.training = True

        for _ in range(iterations):
            self.reset()
            self.deal(n_tricks)
            self.get_predictions(n_tricks)
            self.play_round(n_tricks)

        print({k: v for k, v in self.gamestate.game_score.items()})

    def add_to_table(self, card):
        self.table.append(card)

    def display(self):
        if self.trump_suit:
            print("Trump suit: " + self.trump_suit)
        if self.winning_card:
            print("Best card played")
            self.winning_card.display()
        else:
            print("No best card yet")

        if self.leading_suit:
            print("Leading suit: " + self.leading_suit)
        else:
            print("No leading suit yet")

        if len(self.table) >= 1:
            print("Cards on board:")
            for card in self.table:
                card.display()
        else:
            print("No cards on board yet")

    def calc_card_score(self, card):
        score = 0
        if card.suit == self.gamestate.current_trump_card.suit:
            score += 20
        elif card.suit == self.leading_suit:
            score += 10
        score += card.value / 10
        return score

    def reset(self):
        self.deck = Deck()
        for player in self.players:
            player.reset_hand()
        self.gamestate.reset()

    def rotate_players(self):
        self.players = self.players[1:] + self.players[:1]

    def get_predictions(self, n):
        predictions = {}
        for i, player in enumerate(self.players):

            if i != len(self.players) - 1:
                allowed_predictions = list(range(0, n + 1))
            else:
                disallowed_predict = n - sum(predictions.values())
                allowed_predictions = [
                    p for p in range(0, n + 1) if p != disallowed_predict
                ]
            predictions[player] = player.predict(
                allowed_predictions, self.gamestate
            )

        self.gamestate.current_predictions = predictions

    def play_trick(self):
        for count, player in enumerate(self.players):
            played_card = player.play(self.leading_suit, self.gamestate)
            self.add_to_table(played_card)

            if count == 0:
                self.leading_suit = played_card.suit
                self.winning_card = played_card
                self.winning_card_score = self.calc_card_score(played_card)
                self.winning_player = player

            else:
                if self.calc_card_score(played_card) > self.winning_card_score:
                    self.winning_card = played_card
                    self.winning_card_score = self.calc_card_score(played_card)
                    self.winning_player = player
        winning_player = self.winning_player
        self.gamestate.current_tricks[self.winning_player] += 1
        self.leading_suit = None
        self.winning_card = None
        self.winning_card_score = None
        self.winning_player = None
        return winning_player

    def play_round(self, n_tricks):
        for trick_n in range(n_tricks):
            winner = self.play_trick()
            winning_player_pos = self.players.index(winner)
            self.players = (
                self.players[winning_player_pos:]
                + self.players[:winning_player_pos]
            )

        print(f"Total tricks: {n_tricks}")
        for player in self.players:
            won_tricks = self.gamestate.current_tricks[player]
            guessed_tricks = player.prediction
            print(
                f"{player.name} guessed {guessed_tricks} and won {won_tricks}"
            )
            if won_tricks == guessed_tricks:
                self.gamestate.game_score[player.name] += 10 + 2 * won_tricks
            else:
                self.gamestate.game_score[player.name] -= 2 * abs(
                    won_tricks - guessed_tricks
                )

    def go_up_and_down(self):

        for i in range(1, 8):
            self.reset()
            self.deal(i)
            self.get_predictions(i)
            self.play_round(i)

        for i in reversed(range(1, 7)):
            self.reset()
            self.deal(i)
            self.get_predictions(i)
            self.play_round(i)

        print({k: v for k, v in self.gamestate.game_score.items()})


@dataclass
class GameState:
    current_trump_card: Card
    current_predictions: dict
    current_tricks: dict
    game_score: Dict[str, int]
    n_players: int
    current_round: int
    training: bool

    def __init__(self, players):
        self.current_trump_card = None
        self.current_predictions = {}
        self.current_tricks = {player: 0 for player in players}
        self.game_score = {player.name: 0 for player in players}
        self.n_players = len(players)
        self.training = False

    def reset(self):
        self.current_predictions = {}
        self.current_tricks = {k: 0 for k in self.current_tricks.keys()}
        self.current_trump_card = None

    def set_round(self, round: int):
        self.current_round = round


if __name__ == "__main__":
    board = Board(
        [*[ShitBot(f"shitbot{i}") for i in range(1, 5)], BetaBot("betabot")]
    )
    board.reset()
    board.train(7, 1000)
    pass
