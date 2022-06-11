from typing import Dict, List
from lib import Deck
from scipy.stats import beta, percentileofscore
import numpy as np
import matplotlib.pyplot as plt

import constants
import pyperclip

DISTRIBUTION_ITERATIONS = 100000
PARAMETER_ALPHA = 2.5
TRUMP_SCALING = 3.0
TRUMP_CONST = 0.0


def points_in_hand(hand: list, n_players: int, trump_suit) -> float:

    return sum(
        [
            (
                card.value * trump_scaling(n_players, len(hand))
                + trump_const(n_players, len(hand))
            )
            if card.suit == trump_suit
            else card.value
            for card in hand
        ]
    )


def points_to_percentile(
    points: float, n_players: int, n_cards: int, trump_suit, training
) -> float:

    distribution = generate_points_distribution(
        points_in_hand, n_players, n_cards, trump_suit, training
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


def trump_scaling(n_players: int, n_cards: int) -> float:
    return TRUMP_SCALING


def trump_const(n_players: int, n_cards: int) -> float:
    return TRUMP_CONST


def beta_parameter_b(mean, alpha):
    return (alpha - mean * alpha) / mean


def beta_parameter_a() -> float:
    return PARAMETER_ALPHA


def generate_points_distribution(
    points_in_hand_function, n_players, n_cards, trump_suit, training
) -> List[float]:
    deck = Deck()

    if training:
        scores = constants.scores_7_cards
    else:
        scores = []

        for _ in range(DISTRIBUTION_ITERATIONS):
            deck.shuffle()
            hand = deck.cards[:n_cards]
            scores.append(points_in_hand_function(hand, n_players, trump_suit))

        # plt.hist(scores, bins=np.arange(0, 180, 1))
        # plt.savefig("something.png")

    return scores
