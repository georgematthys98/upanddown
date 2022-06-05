import random

suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
values = list(range(2, 15))


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def display(self):
        if self.value in [11, 12, 13, 14]:
            display_value = {14: "Ace", 11: "Jack", 12: "Queen", 13: "King"}[
                self.value
            ]
            print(f"{display_value} of {self.suit}")
        else:
            print(f"{self.value} of {self.suit}")


class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in suits for value in values]

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
            card.display()


class Player:
    def __init__(self, name):
        self.hand = []
        self.score = 0
        self.name = name

    def draw(self, card):
        self.hand.append(card)

    def display_hand(self):
        if len(self.hand) == 0:
            print(f"{self.name} has no cards")
        else:
            print(f"{self.name} has {len(self.hand)} cards:")
            for card in self.hand:
                card.display()

    def reset_hand(self):
        self.hand = []

    def predict(self, allowed):
        print(f"Possible guesses are {', '.join([str(x) for x in allowed])}")
        prediction = int(input("Enter your guess: "))

        while prediction not in allowed:
            prediction = int(input("Enter an allowed prediction: "))

        self.prediction = prediction
        print(f"{self.name} has made the prediction of {self.prediction}")
        return self.prediction


class Board:
    def __init__(self, players):
        self.deck = Deck()
        self.players = [Player(name) for name in players]
        self.table = []
        self.trump_card = None
        self.trump_suit = None

    def deal(self, cards):
        self.deck.shuffle()
        for _ in range(cards):
            for player in self.players:
                player.draw(self.deck.draw())

        self.trump_card = self.deck.draw()
        self.trump_suit = self.trump_card.suit

    def deal_to_table(self):
        card = self.deck.draw()
        self.table.insert(0, card)

    def reset(self):
        self.deck = Deck()
        for player in self.players:
            player.reset_hand()

    def rotate_players(self):
        self.players = self.players[1:] + self.players[:1]

    def get_predictions(self, n):
        predictions = []
        for i, player in enumerate(self.players):
            if i != len(self.players) - 1:
                allowed_predictions = list(range(0, n + 1))
            else:
                disallowed_predict = n - sum(predictions)
                allowed_predictions = [
                    p for p in range(0, n + 1) if p != disallowed_predict
                ]
            predictions.append(player.predict(allowed_predictions))
