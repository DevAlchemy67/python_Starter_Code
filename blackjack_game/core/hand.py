"""
Hand module - Manages card hands and blackjack-specific logic
"""

from typing import List, Optional, Tuple
from dataclasses import dataclass, field
from .card import Card, Rank


@dataclass
class Hand:
    """Represents a hand of cards"""
    cards: List[Card] = field(default_factory=list)
    
    def add_card(self, card: Card) -> None:
        """Add a card to the hand"""
        self.cards.append(card)
    
    def add_cards(self, cards: List[Card]) -> None:
        """Add multiple cards to the hand"""
        self.cards.extend(cards)
    
    def clear(self) -> None:
        """Clear all cards from the hand"""
        self.cards = []
    
    @property
    def size(self) -> int:
        """Number of cards in the hand"""
        return len(self.cards)
    
    @property
    def is_empty(self) -> bool:
        """Check if hand is empty"""
        return len(self.cards) == 0
    
    def __len__(self) -> int:
        return len(self.cards)
    
    def __iter__(self):
        return iter(self.cards)
    
    def __getitem__(self, index: int) -> Card:
        return self.cards[index]
    
    def __str__(self) -> str:
        return ", ".join(str(card) for card in self.cards)
    
    def __repr__(self) -> str:
        return f"Hand({self.cards})"


class BlackjackHand(Hand):
    """
    Specialized hand for blackjack with value calculation and game logic.
    Handles Ace counting (1 or 11) automatically.
    """
    
    def __init__(self, cards: Optional[List[Card]] = None):
        super().__init__(cards or [])
    
    @property
    def total(self) -> int:
        """
        Calculate the optimal total value of the hand.
        Aces are counted as 11 unless that would cause a bust.
        """
        if not self.cards:
            return 0
        
        # Count aces and total value
        aces = 0
        total = 0
        
        for card in self.cards:
            if card.is_ace:
                aces += 1
                total += 11  # Count Ace as 11 initially
            else:
                total += card.value
        
        # Adjust for aces if total is over 21
        while total > 21 and aces > 0:
            total -= 10  # Change Ace from 11 to 1
            aces -= 1
        
        return total
    
    @property
    def all_possible_values(self) -> List[int]:
        """
        Get all possible values of the hand considering Ace flexibility.
        Used for advanced strategy calculations.
        """
        if not self.cards:
            return [0]
        
        # This is a more comprehensive calculation that considers all combinations
        # For most hands, we just need the optimal value, but this is useful
        # for understanding the hand's potential
        
        # Simple approach: calculate with all Aces as 1 and all as 11
        min_value = sum(card.alternate_value for card in self.cards)
        max_value = sum(card.value for card in self.cards)
        
        # If no aces, only one possible value
        if min_value == max_value:
            return [min_value]
        
        # Generate all possible values
        values = set()
        ace_count = sum(1 for card in self.cards if card.is_ace)
        
        for ace_as_11 in range(ace_count + 1):
            value = min_value + ace_as_11 * 10
            if value <= 21:
                values.add(value)
        
        return sorted(values)
    
    @property
    def is_soft(self) -> bool:
        """
        Check if the hand is soft (contains an Ace counted as 11).
        A soft hand cannot bust with one more card.
        """
        if not self.cards:
            return False
        
        # Hand is soft if it has an Ace and the total with Ace as 11 is <= 21
        has_ace = any(card.is_ace for card in self.cards)
        
        # Calculate total with all Aces as 11
        ace_count = sum(1 for card in self.cards if card.is_ace)
        total_with_11 = sum(card.value for card in self.cards)
        
        # If we have at least one Ace and total with Ace as 11 is <= 21
        return has_ace and total_with_11 <= 21
    
    @property
    def is_hard(self) -> bool:
        """Check if the hand is hard (not soft)"""
        return not self.is_soft
    
    @property
    def is_bust(self) -> bool:
        """Check if the hand has busted (total > 21)"""
        return self.total > 21
    
    @property
    def is_blackjack(self) -> bool:
        """
        Check if the hand is a blackjack (Ace + 10-value card, 2 cards total).
        """
        if len(self.cards) != 2:
            return False
        
        has_ace = any(card.is_ace for card in self.cards)
        has_ten = any(card.is_ten_value for card in self.cards)
        
        return has_ace and has_ten
    
    @property
    def is_pair(self) -> bool:
        """Check if the hand is a pair (two cards of same rank)"""
        if len(self.cards) != 2:
            return False
        return self.cards[0].rank == self.cards[1].rank
    
    @property
    def pair_rank(self) -> Optional[Rank]:
        """Get the rank of the pair, or None if not a pair"""
        if self.is_pair:
            return self.cards[0].rank
        return None
    
    @property
    def can_split(self) -> bool:
        """Check if the hand can be split (is a pair)"""
        return self.is_pair
    
    @property
    def can_double(self) -> bool:
        """Check if the hand can be doubled (typically 2 cards, total 9-11)"""
        if len(self.cards) != 2:
            return False
        return 9 <= self.total <= 11
    
    @property
    def upcard(self) -> Optional[Card]:
        """Get the first card (used for dealer's upcard)"""
        return self.cards[0] if self.cards else None
    
    def split(self) -> Tuple['BlackjackHand', 'BlackjackHand']:
        """
        Split the hand into two separate hands.
        Each hand gets one of the original cards.
        
        Returns:
            Tuple of two new hands
        
        Raises:
            ValueError: If hand cannot be split
        """
        if not self.can_split:
            raise ValueError("Cannot split: hand is not a pair")
        
        hand1 = BlackjackHand([self.cards[0]])
        hand2 = BlackjackHand([self.cards[1]])
        
        return hand1, hand2
    
    def __str__(self) -> str:
        """String representation with total value"""
        cards_str = ", ".join(str(card) for card in self.cards)
        if self.cards:
            return f"{cards_str} (Total: {self.total})"
        return "Empty hand"
    
    def __repr__(self) -> str:
        return f"BlackjackHand({self.cards}, total={self.total})"
