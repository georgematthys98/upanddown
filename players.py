from lib import Player


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
        asci_list = [i.split('\n') for i in asci_list]
        
        asci_str = ''
        for i in zip(*asci_list):
            asci_str += (''.join(i)) +'\n'

        choice = input(
            "Choice of cards to play: (input int)\n"
            + asci_str
        )
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
