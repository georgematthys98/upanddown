from players import *
from lib import * 

def better_worse_in_suit(card,suit,played,excluded):
    suit_deck = Deck(suit=suit)
    # suit_deck.remove(card) exclude in excluded
    for i in played+excluded:
        suit_deck.remove(i)
    suit_deck = suit_deck.cards
    better_cards = [i for i in suit_deck if i.value > card.value]
    worse_cards = [i for i in suit_deck if i.value < card.value]
    n_better, n_worse = len(better_cards), len(worse_cards)
    return n_better,n_worse

def prob_player_having_leading_suit(leading_suit,n_cards,played,excluded):
    n_leading_suit = 13
    played_leading_suit = [i for i in played if i.suit == leading_suit]
    n_played_leading_suit = len(played_leading_suit)
    excluded_leading_suit = [i for i in excluded if i.suit == leading_suit]
    n_excluded_leading_suit = len(excluded_leading_suit)
    n_leading_suit = 13 - n_excluded_leading_suit - n_played_leading_suit
    total_cards = 52 - len(excluded) - len(played)
    prob_card_is_leading_suit = n_leading_suit / total_cards
    prob_having_no_leading_suit = (1 - prob_card_is_leading_suit)**n_cards
    prob_having_leading_suit = 1 - prob_having_no_leading_suit
    print('n cards:', n_cards)
    print('# leading suit cards available:', n_leading_suit)
    print('# cards availabel:', total_cards)
    print('prob player having leading suit:', prob_having_leading_suit)
    return prob_having_leading_suit


def prob_of_beating_their_leading(card,trump_suit,leading_suit,played,excluded):
    if card.suit == leading_suit:
        better_leading,worse_leading = better_worse_in_suit(card,leading_suit,played,excluded)
        print('n better leading cards:', better_leading, 'n worse leading cards', worse_leading)
        print('prob your card better than their leading:', 1- better_leading / (better_leading+worse_leading))
        return 1 - better_leading / (better_leading+worse_leading)
    elif card.suit == trump_suit:
        print('You have trump, you beat the leading suit')
        return(1)

    else:
        #print('Not leading suit or Trump - you will lose trick')
        return 0


def prob_of_you_beat_their_non_leading_card_than_yours(card,trump_suit,leading_suit,played,excluded):
    if card.suit == leading_suit and card.suit != trump_suit:
        #return prob that their card is a trump
        possibilities = Deck()
        possibilities.cards = [i for i in possibilities.cards if i.suit != leading_suit]
        for i in played+excluded:
            possibilities.remove(i)
        possibilities.remove(card)
        #since we are assuming that they are not following the leading suit, remove all leading suit cards
        #unless leading = trump
        print(len(possibilities.cards))
        print(len(possibilities.cards))
        trumps = [i for i in possibilities.cards if i.suit == trump_suit]
        print(len(possibilities.cards))
        n_trumps = len(trumps)
        n_possibilities = len(possibilities.cards)
        print('# available trumps', n_trumps)
        print('available cards:', n_possibilities)
        print('prob they dont have a trump:', 1 - n_trumps/n_possibilities)
        return 1 - n_trumps/n_possibilities

    elif card.suit == trump_suit:
        #return prob that their card is a trump suit better than yours
        better_trumps,_ = better_worse_in_suit(card,trump_suit,played,excluded)
        possibilities = Deck()
        possibilities.cards = [i for i in possibilities.cards if i.suit != leading_suit]
        for i in played+excluded:
            possibilities.remove(i)
        possibilities.remove(card)
        #since we are assuming that they are not following the leading suit, remove all leading suit cards
        possibilities.cards = [i for i in possibilities.cards if i.suit!= leading_suit]
        worse_not_leading_cards = len(possibilities.cards)
        print('prob your trump better than theirs:',1 - better_trumps / (better_trumps+worse_not_leading_cards))
        return 1 - better_trumps / (better_trumps+worse_not_leading_cards)
    else:
        print('Not a trump or leading you lose trick')
        return 0

def prob_of_beating_next_player(card,trump_suit,leading_suit,n_cards,played,excluded):
    p_player_having_leading_suit = prob_player_having_leading_suit(leading_suit,n_cards,played,excluded)
    p_player_not_having_leading_suit = 1 - p_player_having_leading_suit
    p_beating_their_leading_card = prob_of_beating_their_leading(card,trump_suit,leading_suit,played,excluded)
    p_of_you_have_better_not_leading_card = prob_of_you_beat_their_non_leading_card_than_yours(card,trump_suit,leading_suit,played,excluded)

    p_of_beating_player = p_player_having_leading_suit*p_beating_their_leading_card + p_player_not_having_leading_suit*p_of_you_have_better_not_leading_card
    print('prob beating one card', p_of_beating_player)
    return(p_of_beating_player) 

def prob_of_winning_trick(card,trump_suit,leading_suit,n_cards,played,excluded,n_players):
    p_of_beating_next_player = prob_of_beating_next_player(card,trump_suit,leading_suit,n_cards,played,excluded)
    #print('prob winning trick:', p_of_beating_next_player**n_players)
    return p_of_beating_next_player**n_players
#if __name__ == '__main__':
#print(prob_player_having_leading_suit('Diamonds', 7, [Card('h',7),Card('h','A')],[]))
#print(prob_of_better_not_leading_card(Card('h',5),'Hearts',[Card('h',10)],[]))
#print('prob beating next player:', prob_of_beating_next_player(Card('h',12),'Hearts','Hearts',2,[Card('h',12)],[]))
    #print('prob winning trick', prob_of_winning_trick(Card('h',12),'Hearts','Hearts',2,[Card('h',12)],[],1))

# def calc_card_score(card,leading_suit,trump_suit):
#     score = 0
#     if card.suit == trump_suit:
#         score += 20
#     elif card.suit == leading_suit:
#         score += 10
#     score += card.value / 10
#     return score

# def get_better_cards(card, leading_suit, trump_suit, theoretical_deck):
#     our_card_score = calc_card_score(card,leading_suit,trump_suit)
#     potential_cards = theoretical_deck.cards
#     better_cards = []
#     for potential_card in potential_cards:
#         if calc_card_score(potential_card,leading_suit,trump_suit)>our_card_score:
#             better_cards.append(potential_card)
#     return better_cards

# def prob_better_trump(card,leading_suit,trump_suit,played,excluded):
#     theoretical_deck = Deck()
#     for i in played + excluded:
#         theoretical_deck.remove(i)
#     theoretical_deck.remove(card)
#     if card.suit == trump_suit:
#         better_trumps = get_better_cards(card,leading_suit,trump_suit,theoretical_deck)
#         n_better_trumps = len(better_trumps)
#         return n_better_trumps
#     else:
#         return 0

# def prob_better_leading(card,leading_suit,trump_suit,played,excluded):
#     theoretical_deck = Deck()
#     for i in played + excluded:
#         theoretical_deck.remove(i)
#     theoretical_deck.remove(card)
#     if card.suit == leading_suit:
#         theoretical_deck.cards = [i for i in theoretical_deck.cards if i.suit == leading_suit]
#         better_leading = get_better_cards(card,leading_suit,trump_suit,theoretical_deck)
#         n_better_leading = len(better_leading)
#         return n_better_leading  
#     else:
#         return 0

# def win_trick_prob(card,used_cards,leading_suit,trump_suit,n_players):
#     if card.suit not in (leading_suit,trump_suit):
#         return 0


#     results_dic = {
#         'win_prob':0,'loss_prob':0
#         }
#     theoretical_deck = Deck()
#     theoretical_deck.remove(card)
#     for used_card in used_cards:
#         theoretical_deck.remove(used_card)

#     potential_cards = theoretical_deck.cards
#     for potential_card in potential_cards:
#         our_card_score = calc_card_score(card,leading_suit,trump_suit)
#         win = (our_card_score>calc_card_score(potential_card,leading_suit,trump_suit))
#         loss = not win
# #         win,loss = int(win),int(loss)
# #         results_dic['win_prob']+= win
# #         results_dic['loss_prob']+= loss
# #         #print(potential_card.display(), win)
# #     total = results_dic['win_prob'] + results_dic['loss_prob']
# #     # for key,value in results_dic.items():
# #     #     results_dic[key] = value/total
# #     return results_dic

# if __name__ == "__main__":
#     board = Board([Human("Player1")])
#     board.reset()
#     board.deal(7)
#     for player in board.players:
#         player.display_hand_ascii()
#         for card in player.hand:
#             print('----------')
#             print('trump',board.trump_suit)
#             print('Leading: Diamonds')
#             print(card.get_ascii())
#             played_card = Card(board.trump_suit,10)
#             print('played')
#             print(played_card.get_ascii())
#             better_trumps,worse_trumps = better_worse_in_suit(card,board.trump_suit,[played_card],[])
#             better_leading,worse_leading= better_worse_in_suit(card,'Diamonds',[played_card],[])
#             print(better_trumps,worse_trumps,better_leading,worse_leading)
#             # fakeplayer = Player('fake')
#             # fakeplayer.hand = better_trumps
#             # fakeplayer.display_hand()
#             print()


