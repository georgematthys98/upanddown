from players import *
from lib import *
import mock


def test_get_allowed_cards():
    player = Player("test")
    cards = [
        ("h", 2),
        ("h", 10),
        ("d", 5),
    ]
    hand = [Card(*x) for x in cards]
    player.hand = hand

    assert player.get_allowed_cards("Diamonds") == [hand[2]]
    assert player.get_allowed_cards("Spades") == hand
    assert player.get_allowed_cards(None) == hand
    assert player.get_allowed_cards("Hearts") == hand[0:2]


def test_play():
    player = Human("test")
    cards = [
        ("h", 2),
        ("h", 10),
        ("d", 5),
    ]
    hand = [Card(*x) for x in cards]
    player.hand = hand.copy()
    gamestate = GameState([player])

    # make sure right card is played
    with mock.patch("builtins.input", return_value=0):
        assert player.play("Spades", gamestate) == hand[0]

    # make sure the card is removed
    assert player.hand == hand[1:]

    with mock.patch("builtins.input", return_value=0):
        assert player.play("Diamonds", gamestate) == hand[2]
    assert player.hand == [hand[1]]


def test_predict():
    player = Human("test")
    gamestate = GameState(players=[player])

    with mock.patch("builtins.input", return_value=3):
        assert player.predict([1, 2, 3, 5], gamestate) == 3
        assert player.prediction == 3
