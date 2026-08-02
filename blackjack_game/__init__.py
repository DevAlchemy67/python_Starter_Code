"""
Blackjack Game - A comprehensive Python implementation
Supports beginner to advanced gameplay with strategy hints
"""

from .core.card import Card, Rank, Suit
from .core.deck import Deck, Shoe
from .core.hand import Hand, BlackjackHand
from .players.player import Player, Dealer
from .players.strategy import BasicStrategy, AdvancedStrategy
from .ui.cli import CLIInterface
from .game import BlackjackGame

__version__ = "1.0.0"
__all__ = [
    'Card', 'Rank', 'Suit', 'Deck', 'Shoe', 'Hand', 'BlackjackHand',
    'Player', 'Dealer', 'BasicStrategy', 'AdvancedStrategy',
    'CLIInterface', 'BlackjackGame'
]
