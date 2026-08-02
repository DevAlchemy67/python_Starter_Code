"""
Card module - Represents playing cards with ranks and suits
"""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, Tuple


class Rank(Enum):
    """Card ranks with their blackjack values"""
    ACE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    JACK = auto()
    QUEEN = auto()
    KING = auto()
    
    @property
    def value(self) -> int:
        """Get the primary value of the rank"""
        return {
            Rank.ACE: 11,
            Rank.TWO: 2,
            Rank.THREE: 3,
            Rank.FOUR: 4,
            Rank.FIVE: 5,
            Rank.SIX: 6,
            Rank.SEVEN: 7,
            Rank.EIGHT: 8,
            Rank.NINE: 9,
            Rank.TEN: 10,
            Rank.JACK: 10,
            Rank.QUEEN: 10,
            Rank.KING: 10,
        }[self]
    
    @property
    def alternate_value(self) -> int:
        """Get alternate value for Ace (1 instead of 11)"""
        return 1 if self == Rank.ACE else self.value
    
    @property
    def is_ace(self) -> bool:
        """Check if rank is Ace"""
        return self == Rank.ACE
    
    @property
    def is_face_card(self) -> bool:
        """Check if rank is a face card (J, Q, K)"""
        return self in {Rank.JACK, Rank.QUEEN, Rank.KING}
    
    @property
    def is_ten_value(self) -> bool:
        """Check if rank is worth 10 points"""
        return self.value == 10
    
    def __str__(self) -> str:
        return self.name.capitalize()
    
    def __repr__(self) -> str:
        return f"Rank.{self.name}"


class Suit(Enum):
    """Card suits"""
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()
    
    @property
    def symbol(self) -> str:
        """Get Unicode symbol for the suit"""
        return {
            Suit.HEARTS: "♥",
            Suit.DIAMONDS: "♦", 
            Suit.CLUBS: "♣",
            Suit.SPADES: "♠",
        }[self]
    
    @property
    def color(self) -> str:
        """Get color of the suit"""
        return "red" if self in {Suit.HEARTS, Suit.DIAMONDS} else "black"
    
    def __str__(self) -> str:
        return self.name.capitalize()
    
    def __repr__(self) -> str:
        return f"Suit.{self.name}"


@dataclass(frozen=True, order=True)
class Card:
    """
    Represents a playing card with rank and suit.
    Cards are immutable and can be compared.
    """
    rank: Rank
    suit: Suit
    
    def __str__(self) -> str:
        """String representation of the card (e.g., 'Ace of Hearts' or 'A♥')"""
        rank_str = {
            Rank.ACE: "A",
            Rank.JACK: "J", 
            Rank.QUEEN: "Q",
            Rank.KING: "K",
        }.get(self.rank, str(self.rank.value))
        
        # Short representation: "A♥", "10♦", "K♠"
        return f"{rank_str}{self.suit.symbol}"
    
    def long_str(self) -> str:
        """Long string representation (e.g., 'Ace of Hearts')"""
        return f"{self.rank} of {self.suit}"
    
    @property
    def value(self) -> int:
        """Get the primary value of the card"""
        return self.rank.value
    
    @property
    def alternate_value(self) -> int:
        """Get alternate value (for Ace)"""
        return self.rank.alternate_value
    
    @property
    def is_ace(self) -> bool:
        """Check if card is an Ace"""
        return self.rank.is_ace
    
    @property
    def is_face_card(self) -> bool:
        """Check if card is a face card"""
        return self.rank.is_face_card
    
    @property
    def is_ten_value(self) -> bool:
        """Check if card is worth 10 points"""
        return self.rank.is_ten_value
    
    def __repr__(self) -> str:
        return f"Card({self.rank}, {self.suit})"


# Pre-compute all 52 cards for efficiency
ALL_CARDS = [Card(rank, suit) for suit in Suit for rank in Rank]


def get_card(rank: Rank, suit: Suit) -> Card:
    """Get a specific card by rank and suit"""
    return Card(rank, suit)
