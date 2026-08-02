"""
Card counting module - Various card counting systems for advanced players
"""

from typing import Dict, List, Optional
from enum import Enum
from ..core.card import Card, Rank, Suit
from ..core.deck import Shoe


class CountingSystem(Enum):
    """Available card counting systems"""
    HI_LO = "Hi-Lo"
    KO = "KO (Knock-Out)"
    OMEGA_II = "Omega II"
    ZEN = "Zen Count"


class CardCounter:
    """Base class for card counting systems"""
    
    def __init__(self, num_decks: int = 6):
        """
        Initialize the card counter.
        
        Args:
            num_decks: Number of decks in the shoe
        """
        self.num_decks = num_decks
        self.true_count = 0
        self.running_count = 0
        self.cards_seen = 0
        self.decks_remaining = num_decks
    
    def reset(self) -> None:
        """Reset the counter for a new shoe"""
        self.true_count = 0
        self.running_count = 0
        self.cards_seen = 0
        self.decks_remaining = self.num_decks
    
    def update(self, card: Card) -> None:
        """
        Update the count with a new card.
        
        Args:
            card: The card that was dealt
        """
        self.cards_seen += 1
        self.decks_remaining = max(0, self.num_decks - (self.cards_seen / 52))
        
        # Update running count (to be implemented by subclasses)
        self.running_count += self.get_card_value(card)
        
        # Update true count
        if self.decks_remaining > 0:
            self.true_count = round(self.running_count / self.decks_remaining)
        else:
            self.true_count = self.running_count
    
    def get_card_value(self, card: Card) -> int:
        """
        Get the count value for a card.
        To be implemented by subclasses.
        """
        raise NotImplementedError
    
    def get_betting_advice(self) -> str:
        """
        Get betting advice based on the current count.
        
        Returns:
            String with betting advice
        """
        if self.true_count >= 5:
            return "Very high count - bet maximum!"
        elif self.true_count >= 3:
            return "High count - increase bet significantly"
        elif self.true_count >= 1:
            return "Positive count - increase bet slightly"
        elif self.true_count >= -1:
            return "Neutral count - bet minimum"
        elif self.true_count >= -3:
            return "Negative count - decrease bet or leave table"
        else:
            return "Very negative count - leave table!"
    
    def get_deviation_advice(self, player_total: int, dealer_upcard: Card) -> str:
        """
        Get playing deviation advice based on count.
        
        Args:
            player_total: Player's current hand total
            dealer_upcard: Dealer's upcard
            
        Returns:
            String with deviation advice
        """
        return "Follow basic strategy"
    
    def __str__(self) -> str:
        return f"Count: {self.running_count:+d}, True: {self.true_count:+d}, Decks: {self.decks_remaining:.1f}"


class HiLoCounter(CardCounter):
    """
    Hi-Lo counting system (most popular).
    
    Card values:
    - 2-6: +1
    - 7-9: 0
    - 10-A: -1
    
    This is a balanced system (count starts and ends at 0).
    """
    
    def __init__(self, num_decks: int = 6):
        super().__init__(num_decks)
        self.name = CountingSystem.HI_LO.value
    
    def get_card_value(self, card: Card) -> int:
        """Get Hi-Lo value for a card"""
        if card.rank.value <= 6:
            return 1
        elif card.rank.value >= 10:
            return -1
        else:
            return 0
    
    def get_betting_advice(self) -> str:
        """Get betting advice for Hi-Lo"""
        if self.true_count >= 5:
            return "Very high count (+5+) - bet 10-12 units"
        elif self.true_count >= 3:
            return "High count (+3 to +4) - bet 6-8 units"
        elif self.true_count >= 1:
            return "Positive count (+1 to +2) - bet 2-4 units"
        elif self.true_count >= -1:
            return "Neutral count (-1 to 0) - bet 1 unit (minimum)"
        elif self.true_count >= -3:
            return "Negative count (-2 to -3) - bet 1 unit or leave"
        else:
            return "Very negative count (-4-) - leave table!"
    
    def get_deviation_advice(self, player_total: int, dealer_upcard: Card) -> str:
        """Get playing deviations for Hi-Lo"""
        tc = self.true_count
        
        # Common Hi-Lo deviations
        if tc >= 3:
            if player_total == 16 and dealer_upcard.value == 10:
                return "Stand on 16 vs 10 (instead of hit)"
            if player_total == 15 and dealer_upcard.value == 10:
                return "Stand on 15 vs 10 (instead of hit)"
            if player_total == 13 and dealer_upcard.value in [2, 3]:
                return "Stand on 13 vs 2-3 (instead of hit)"
        
        if tc >= 4:
            if player_total == 12 and dealer_upcard.value in [2, 3]:
                return "Stand on 12 vs 2-3 (instead of hit)"
            if player_total == 14 and dealer_upcard.value in [4, 5, 6]:
                return "Stand on 14 vs 4-6 (instead of hit)"
        
        if tc >= 5:
            if player_total == 10 and dealer_upcard.value == 10:
                return "Double on 10 vs 10 (instead of hit)"
            if player_total == 12 and dealer_upcard.value == 4:
                return "Stand on 12 vs 4 (instead of hit)"
        
        if tc <= -1:
            if player_total == 16 and dealer_upcard.value == 10:
                return "Surrender 16 vs 10 (if allowed)"
            if player_total == 15 and dealer_upcard.value == 10:
                return "Surrender 15 vs 10 (if allowed)"
        
        return "Follow basic strategy"


class KOCount(CardCounter):
    """
    KO (Knock-Out) counting system.
    
    Card values:
    - 2-7: +1
    - 8-9: 0
    - 10-A: -1
    
    This is an unbalanced system (count doesn't start at 0).
    The key index is different based on number of decks.
    """
    
    # Key indices for different deck counts
    KEY_INDICES = {
        1: 4,
        2: 0,
        4: -4,
        6: -16,
        8: -28,
    }
    
    def __init__(self, num_decks: int = 6):
        super().__init__(num_decks)
        self.name = CountingSystem.KO.value
        self.key_index = self.KEY_INDICES.get(num_decks, -16)
    
    def reset(self) -> None:
        """Reset the counter"""
        super().reset()
        self.running_count = self.key_index  # KO starts at key index
    
    def get_card_value(self, card: Card) -> int:
        """Get KO value for a card"""
        if card.rank.value <= 7:
            return 1
        elif card.rank.value >= 10:
            return -1
        else:
            return 0
    
    def get_betting_advice(self) -> str:
        """Get betting advice for KO"""
        # For KO, we use the running count directly
        rc = self.running_count
        
        if rc >= self.key_index + 4:
            return "High count - bet maximum!"
        elif rc >= self.key_index + 2:
            return "Positive count - increase bet"
        elif rc >= self.key_index:
            return "Neutral count - bet minimum"
        else:
            return "Negative count - leave table"


class OmegaII(CardCounter):
    """
    Omega II counting system (advanced).
    
    Card values:
    - 2,3,7: +1
    - 4,5,6: +2
    - 8: 0
    - 9: -1
    - 10,A: -2
    
    This is a balanced, multi-level system.
    """
    
    def __init__(self, num_decks: int = 6):
        super().__init__(num_decks)
        self.name = CountingSystem.OMEGA_II.value
    
    def get_card_value(self, card: Card) -> int:
        """Get Omega II value for a card"""
        if card.rank in [Rank.TWO, Rank.THREE, Rank.SEVEN]:
            return 1
        elif card.rank in [Rank.FOUR, Rank.FIVE, Rank.SIX]:
            return 2
        elif card.rank == Rank.NINE:
            return -1
        elif card.rank.is_ten_value or card.rank == Rank.ACE:
            return -2
        else:  # 8
            return 0
    
    def get_betting_advice(self) -> str:
        """Get betting advice for Omega II"""
        if self.true_count >= 4:
            return "Very high count - bet maximum!"
        elif self.true_count >= 2:
            return "High count - increase bet significantly"
        elif self.true_count >= 0:
            return "Positive count - increase bet slightly"
        elif self.true_count >= -2:
            return "Neutral count - bet minimum"
        else:
            return "Negative count - leave table"


class ZenCount(CardCounter):
    """
    Zen Count (another advanced system).
    
    Card values:
    - 2,3,7: +1
    - 4,5,6: +2
    - 8,9: 0
    - 10,A: -2
    
    Similar to Omega II but with different values.
    """
    
    def __init__(self, num_decks: int = 6):
        super().__init__(num_decks)
        self.name = "Zen Count"
    
    def get_card_value(self, card: Card) -> int:
        """Get Zen Count value for a card"""
        if card.rank in [Rank.TWO, Rank.THREE, Rank.SEVEN]:
            return 1
        elif card.rank in [Rank.FOUR, Rank.FIVE, Rank.SIX]:
            return 2
        elif card.rank.is_ten_value or card.rank == Rank.ACE:
            return -2
        else:  # 8,9
            return 0


class ShoeTracker:
    """
    Tracks a shoe and provides counting information.
    """
    
    def __init__(self, shoe: Shoe, counter_type: CountingSystem = CountingSystem.HI_LO):
        """
        Initialize shoe tracker.
        
        Args:
            shoe: The shoe to track
            counter_type: Type of counting system to use
        """
        self.shoe = shoe
        self.counter: CardCounter
        
        if counter_type == CountingSystem.HI_LO:
            self.counter = HiLoCounter(shoe.num_decks)
        elif counter_type == CountingSystem.KO:
            self.counter = KOCount(shoe.num_decks)
        elif counter_type == CountingSystem.OMEGA_II:
            self.counter = OmegaII(shoe.num_decks)
        else:
            self.counter = HiLoCounter(shoe.num_decks)
        
        self.history: List[Dict] = []
    
    def deal_card(self, card: Card) -> Card:
        """
        Deal a card and update the count.
        
        Args:
            card: The card being dealt
            
        Returns:
            The same card
        """
        self.counter.update(card)
        
        # Record in history
        self.history.append({
            'card': card,
            'running_count': self.counter.running_count,
            'true_count': self.counter.true_count,
            'decks_remaining': self.counter.decks_remaining,
        })
        
        return card
    
    def get_stats(self) -> Dict:
        """Get tracking statistics"""
        return {
            'counter_type': self.counter.name,
            'running_count': self.counter.running_count,
            'true_count': self.counter.true_count,
            'decks_remaining': self.counter.decks_remaining,
            'cards_seen': self.counter.cards_seen,
            'betting_advice': self.counter.get_betting_advice(),
        }
    
    def reset(self) -> None:
        """Reset the tracker"""
        self.counter.reset()
        self.history = []
