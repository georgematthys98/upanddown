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
    player = Player("test")
    cards = [
        ("h", 2),
        ("h", 10),
        ("d", 5),
    ]
    hand = [Card(*x) for x in cards]
    player.hand = hand.copy()

    with mock.patch("builtins.input", return_value=0):
        assert player.play("Spades") == hand[0]
