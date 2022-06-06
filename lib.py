import random
suits = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
values = list(range(2, 15))

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def display(self):
        if self.value in [11, 12, 13, 14]:
            display_value = {14: "Ace", 11: "Jack", 12: "Queen", 13: "King"}[self.value]
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
        for card in (self.cards):
            card.display()

class Player:
    def __init__(self, name):
        self.hand = []
        self.score = 0
        self.name = name
    
    def get_allowed_cards(self,leading_suit):
        if leading_suit:
            suit_list = [card.suit for card in self.hand]
            req_to_play_leading = leading_suit in suit_list
            if req_to_play_leading:
                allowed_list = [card for card in self.hand if card.suit == leading_suit]
            else:
                allowed_list = self.hand
        else:
            allowed_list = self.hand
        
        return allowed_list
        
        
    def draw(self, card):
        self.hand.append(card)
    
    def play(self, leading_suit):
        allowed_to_play = self.get_allowed_cards(leading_suit)
        display_value = {14: "Ace", 11: "Jack", 12: "Queen", 13: "King"}
        display_value.update({i:str(i) for i in range(2,11)})
        allowed_to_play_display = [display_value[i.value] +' of ' + i.suit for i in allowed_to_play]
        choice = input('Choice cards to play: (input int)\n' +', '.join(allowed_to_play_display))
        choice = int(choice)
        played_card = allowed_to_play[choice]
        self.hand.remove(played_card) #remove
        return(played_card)
    
    
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
        self.leading_suit = None
        self.winning_card = None
        self.winning_card_score = None
        self.winning_player = None
        
    def deal(self, cards):
        self.deck.shuffle()
        for _ in range(cards):
            for player in self.players:
                player.draw(self.deck.draw())
        
        self.trump_card = self.deck.draw()
        self.trump_suit = self.trump_card.suit
    
    def add_to_table(self,card):
        self.table.append(card)

    def display(self):  
        if self.trump_suit:
            print('Trump suit: '+ self.trump_suit)
        if self.winning_card:
            print('Best card played')
            self.winning_card.display()
        else:
            print('No best card yet')
            
        if self.leading_suit:
            print('Leading suit: '+ self.leading_suit)
        else:
            print('No leading suit yet')
        
        if len(self.table)>=1:
            print('Cards on board:')
            for card in self.table:
                card.display()
        else:
            print('No cards on board yet')
    
    def calc_card_score(self,card):
        score = 0
        if card.suit == self.trump_suit:
            score += 2
        elif card.suit == self.leading_suit:
            score += 1
        score += card.value
        return score
    # def deal_to_table(self):
    #     card = self.deck.draw()
    #     self.table.insert(0, card)

    def reset(self):
        self.deck = Deck()
        for player in self.players:
            player.reset_hand()
            
    def rotate_players(self):
        self.players = self.players[1:] + self.players[:1]
    
    def get_predictions(self, n):
        predictions = []
        for i, player in enumerate(self.players):
            print('Your position this trick',i)
            print('Trump suit'+self.trump_suit)
            player.display_hand()
            if i != len(self.players) - 1:
                allowed_predictions = list(range(0, n+1))
            else:
                disallowed_predict = n - sum(predictions)
                allowed_predictions = [p for p in range(0, n+1) if p != disallowed_predict]
            predictions.append(player.predict(allowed_predictions))
            
    def play_trick(self):
        for count,player in enumerate(board.players):  
            played_card = player.play(self.leading_suit)
            board.add_to_table(played_card)
            
            if count == 0:
                self.leading_suit = played_card.suit
                self.winning_card = played_card
                self.winning_card_score = self.calc_card_score(played_card)
                self.winning_player = player
                print('You are leading the trick')
            else:
                if self.calc_card_score(played_card) > self.winning_card_score:
                    self.winning_card = played_card
                    self.winning_card_score = self.calc_card_score(played_card)
                    self.winning_player = player
                    print('You are leading the trick')
                else:
                    print('You are not leading the trick')
            print()
            
            
if __name__ == '__main__':
    board = Board(['Player1', 'Player2'])
    board.reset()
    board.deal(7)
    board.get_predictions(7)
    print()
    board.play_trick()