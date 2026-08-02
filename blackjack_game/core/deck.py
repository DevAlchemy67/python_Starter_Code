"""
Deck module - Manages decks and shoes for blackjack
"""

import random
from typing import List, Optional, Iterator
from .card import Card, ALL_CARDS, Rank, Suit


class Deck:
    """
    Represents a single deck of 52 cards.
    Can be shuffled and dealt from.
    """
    
    def __init__(self, shuffle: bool = True):
        """
        Initialize a deck of 52 cards.
        
        Args:
            shuffle: Whether to shuffle the deck immediately
        """
        self._cards: List[Card] = ALL_CARDS.copy()
        self._shuffle = shuffle
        
        if shuffle:
            self.shuffle()
    
    def shuffle(self) -> None:
        """Shuffle the deck using Fisher-Yates algorithm"""
        random.shuffle(self._cards)
        self._shuffle = True
    
    def deal(self) -> Optional[Card]:
        """
        Deal the top card from the deck.
        
        Returns:
            The top card, or None if deck is empty
        """
        if not self._cards:
            return None
        return self._cards.pop(0)
    
    def deal_multiple(self, count: int) -> List[Card]:
        """
        Deal multiple cards from the deck.
        
        Args:
            count: Number of cards to deal
            
        Returns:
            List of dealt cards (may be shorter if deck runs out)
        """
        return [self.deal() for _ in range(count) if self._cards]
    
    def burn(self, count: int = 1) -> List[Card]:
        """
        Burn (discard) cards from the top of the deck.
        Used in casino procedures.
        
        Args:
            count: Number of cards to burn
            
        Returns:
            List of burned cards
        """
        return self.deal_multiple(count)
    
    @property
    def remaining(self) -> int:
        """Number of cards remaining in the deck"""
        return len(self._cards)
    
    @property
    def is_empty(self) -> bool:
        """Check if deck is empty"""
        return len(self._cards) == 0
    
    @property
    def is_shuffled(self) -> bool:
        """Check if deck has been shuffled"""
        return self._shuffle
    
    def reset(self, shuffle: bool = True) -> None:
        """Reset the deck to full and optionally shuffle"""
        self._cards = ALL_CARDS.copy()
        self._shuffle = shuffle
        if shuffle:
            self.shuffle()
    
    def __len__(self) -> int:
        return len(self._cards)
    
    def __iter__(self) -> Iterator[Card]:
        return iter(self._cards)
    
    def __repr__(self) -> str:
        return f"Deck(remaining={self.remaining}, shuffled={self._shuffle})"


class Shoe:
    """
    Represents a shoe (multiple decks) used in blackjack.
    Casinos typically use 6-8 decks in a shoe.
    """
    
    def __init__(self, num_decks: int = 6, shuffle: bool = True, 
                 reshuffle_threshold: float = 0.25):
        """
        Initialize a shoe with multiple decks.
        
        Args:
            num_decks: Number of decks in the shoe (typically 6-8)
            shuffle: Whether to shuffle immediately
            reshuffle_threshold: Fraction of cards remaining before reshuffling
                                (e.g., 0.25 = reshuffle when 25% of cards remain)
        """
        self.num_decks = num_decks
        self.reshuffle_threshold = reshuffle_threshold
        self._cards: List[Card] = []
        self._discarded: List[Card] = []
        
        self.reset(shuffle=shuffle)
    
    def reset(self, shuffle: bool = True) -> None:
        """Reset the shoe with fresh decks and optionally shuffle"""
        self._cards = ALL_CARDS * self.num_decks
        self._discarded = []
        
        if shuffle:
            self.shuffle()
    
    def shuffle(self) -> None:
        """Shuffle all cards in the shoe"""
        random.shuffle(self._cards)
    
    def deal(self) -> Optional[Card]:
        """
        Deal the top card from the shoe.
        
        Returns:
            The top card, or None if shoe is empty
        """
        if not self._cards:
            return None
        
        card = self._cards.pop(0)
        return card
    
    def deal_multiple(self, count: int) -> List[Card]:
        """
        Deal multiple cards from the shoe.
        
        Args:
            count: Number of cards to deal
            
        Returns:
            List of dealt cards
        """
        return [self.deal() for _ in range(count) if self._cards]
    
    def burn(self, count: int = 1) -> List[Card]:
        """
        Burn cards from the top of the shoe.
        
        Args:
            count: Number of cards to burn
            
        Returns:
            List of burned cards
        """
        burned = self.deal_multiple(count)
        self._discarded.extend(burned)
        return burned
    
    def collect_discards(self) -> None:
        """Collect all discarded cards back into the shoe"""
        self._cards.extend(self._discarded)
        self._discarded = []
    
    def needs_reshuffle(self) -> bool:
        """Check if shoe needs to be reshuffled based on threshold"""
        total_cards = len(ALL_CARDS) * self.num_decks
        return len(self._cards) <= total_cards * self.reshuffle_threshold
    
    def reshuffle(self) -> None:
        """Reshuffle the shoe when needed"""
        self.collect_discards()
        self.shuffle()
    
    @property
    def remaining(self) -> int:
        """Number of cards remaining in the shoe"""
        return len(self._cards)
    
    @property
    def discarded_count(self) -> int:
        """Number of cards in the discard pile"""
        return len(self._discarded)
    
    @property
    def total_cards(self) -> int:
        """Total number of cards (remaining + discarded)"""
        return len(self._cards) + len(self._discarded)
    
    @property
    def is_empty(self) -> bool:
        """Check if shoe is empty"""
        return len(self._cards) == 0
    
    def __len__(self) -> int:
        return len(self._cards)
    
    def __iter__(self) -> Iterator[Card]:
        return iter(self._cards)
    
    def __repr__(self) -> str:
        return f"Shoe(decks={self.num_decks}, remaining={self.remaining})"
