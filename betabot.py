from typing import Dict, List
from lib import GameState, Card, Deck
from scipy.stats import beta, percentileofscore
import numpy as np
import matplotlib.pyplot as plt

CONST_DISTRIBUTION_ITERATION = 100000

CONST_ALPHA = 2.5
CONST_SCALING = 3.0


def points_in_hand(hand: List[Card], n_players: int, trump_suit) -> float:

    return sum(
        [
            (card.value * trump_scaling(n_players, len(hand)))
            if card.suit == trump_suit
            else card.value
            for card in hand
        ]
    )


def points_to_percentile(
    points: float, n_players: int, n_cards: int, trump_suit
) -> float:

    distribution = generate_points_distribution(
        points_in_hand, n_players, n_cards, trump_suit
    )
    percentile = percentileofscore(distribution, points)

    return percentile


def percentile_to_expected(
    percentile: float, n_players: int, n_cards: int
) -> float:

    alpha = beta_parameter_a()
    expected = beta.ppf(
        percentile / 100,
        alpha,
        beta_parameter_b(1 / n_players, alpha),
        scale=n_cards,
    )

    return expected


def get_expected_tricks(
    points: float, n_players: int, n_cards: int, trump_suit
) -> float:

    percentile = points_to_percentile(points, n_players, n_cards, trump_suit)
    expected = percentile_to_expected(percentile, _)
    return expected


def trump_scaling(n_players: int, n_cards: int) -> float:
    return CONST_SCALING


def beta_parameter_b(mean, alpha):
    return (alpha - mean * alpha) / mean


def beta_parameter_a() -> float:
    return CONST_ALPHA


def generate_points_distribution(
    points_in_hand_function, n_players, n_cards, trump_suit
) -> List[float]:
    deck = Deck()

    scores = []

    for _ in range(CONST_DISTRIBUTION_ITERATION):
        deck.shuffle()
        hand = deck.cards[:n_cards]
        scores.append(points_in_hand_function(hand, n_players, trump_suit))

    plt.hist(scores, bins=np.arange(0, 180, 1))
    plt.savefig("something.png")

    return scores
