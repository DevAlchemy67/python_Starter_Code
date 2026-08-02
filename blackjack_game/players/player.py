"""
Player module - Player and Dealer classes for blackjack
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum, auto
from ..core.hand import BlackjackHand
from ..core.card import Card


class Action(Enum):
    """Possible player actions in blackjack"""
    HIT = auto()
    STAND = auto()
    DOUBLE = auto()
    SPLIT = auto()
    SURRENDER = auto()
    INSURANCE = auto()
    EVEN_MONEY = auto()
    
    def __str__(self) -> str:
        return self.name.capitalize()


class PlayerType(Enum):
    """Types of players"""
    HUMAN = auto()
    AI_BASIC = auto()
    AI_ADVANCED = auto()
    DEALER = auto()


@dataclass
class Bet:
    """Represents a bet placed by a player"""
    amount: float
    hand_index: int = 0  # For split hands
    is_insurance: bool = False
    is_double: bool = False
    
    @property
    def payout(self) -> float:
        """Standard payout for blackjack (3:2)"""
        return self.amount * 1.5
    
    @property
    def even_payout(self) -> float:
        """Even money payout (1:1)"""
        return self.amount
    
    @property
    def insurance_payout(self) -> float:
        """Insurance payout (2:1)"""
        return self.amount * 2


@dataclass
class Player:
    """
    Represents a blackjack player with bankroll and hands.
    """
    name: str
    bankroll: float = 1000.0
    player_type: PlayerType = PlayerType.HUMAN
    current_bet: float = 0.0
    hands: List[BlackjackHand] = field(default_factory=list)
    active_hand_index: int = 0
    
    # Statistics
    wins: int = 0
    losses: int = 0
    pushes: int = 0
    blackjacks: int = 0
    
    def __post_init__(self):
        if not self.hands:
            self.hands = [BlackjackHand()]
    
    @property
    def current_hand(self) -> BlackjackHand:
        """Get the currently active hand"""
        return self.hands[self.active_hand_index]
    
    @property
    def has_active_hands(self) -> bool:
        """Check if player has any active (non-busted, non-standing) hands"""
        return any(not hand.is_bust for hand in self.hands)
    
    @property
    def all_hands_bust(self) -> bool:
        """Check if all hands have busted"""
        return all(hand.is_bust for hand in self.hands)
    
    @property
    def total_bet(self) -> float:
        """Get total bet across all hands"""
        return self.current_bet
    
    def place_bet(self, amount: float) -> bool:
        """
        Place a bet for the next hand.
        
        Args:
            amount: Amount to bet
            
        Returns:
            True if bet was successful, False if not enough bankroll
        """
        if amount > self.bankroll:
            return False
        
        self.current_bet = amount
        self.bankroll -= amount
        return True
    
    def add_hand(self, hand: Optional[BlackjackHand] = None) -> None:
        """Add a new hand (used for splitting)"""
        if hand is None:
            hand = BlackjackHand()
        self.hands.append(hand)
    
    def clear_hands(self) -> None:
        """Clear all hands for a new round"""
        self.hands = [BlackjackHand()]
        self.active_hand_index = 0
        self.current_bet = 0.0
    
    def receive_card(self, card: Card, hand_index: int = 0) -> None:
        """Receive a card into a specific hand"""
        if hand_index < len(self.hands):
            self.hands[hand_index].add_card(card)
    
    def hit(self) -> Action:
        """Player chooses to hit"""
        return Action.HIT
    
    def stand(self) -> Action:
        """Player chooses to stand"""
        return Action.STAND
    
    def double_down(self) -> Action:
        """Player chooses to double down"""
        return Action.DOUBLE
    
    def split(self) -> Action:
        """Player chooses to split"""
        return Action.SPLIT
    
    def surrender(self) -> Action:
        """Player chooses to surrender"""
        return Action.SURRENDER
    
    def take_insurance(self) -> Action:
        """Player chooses to take insurance"""
        return Action.INSURANCE
    
    def win(self, amount: float, hand_index: int = 0) -> None:
        """Player wins a hand"""
        self.bankroll += amount
        self.wins += 1
    
    def lose(self, hand_index: int = 0) -> None:
        """Player loses a hand"""
        self.losses += 1
    
    def push(self, hand_index: int = 0) -> None:
        """Player pushes (ties) a hand"""
        self.bankroll += self.current_bet  # Return original bet
        self.pushes += 1
    
    def blackjack_payout(self, hand_index: int = 0) -> None:
        """Player gets blackjack payout (3:2)"""
        payout = self.current_bet * 1.5
        self.bankroll += payout
        self.wins += 1
        self.blackjacks += 1
    
    def win_payout(self, amount: float, hand_index: int = 0) -> None:
        """Player wins with standard payout"""
        self.bankroll += amount
        self.wins += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get player statistics"""
        total_hands = self.wins + self.losses + self.pushes
        win_rate = (self.wins / total_hands * 100) if total_hands > 0 else 0
        
        return {
            'name': self.name,
            'bankroll': self.bankroll,
            'wins': self.wins,
            'losses': self.losses,
            'pushes': self.pushes,
            'blackjacks': self.blackjacks,
            'win_rate': win_rate,
            'total_hands': total_hands,
        }
    
    def __str__(self) -> str:
        return f"{self.name} (${self.bankroll:.2f})"
    
    def __repr__(self) -> str:
        return f"Player(name='{self.name}', bankroll={self.bankroll}, type={self.player_type})"


class Dealer(Player):
    """
    Represents the dealer in blackjack.
    Follows standard casino rules: hit on 16 or less, stand on 17 or more.
    """
    
    def __init__(self):
        super().__init__(
            name="Dealer",
            bankroll=0,  # Dealer doesn't have a bankroll
            player_type=PlayerType.DEALER
        )
        self.upcard: Optional[Card] = None
        self.hole_card: Optional[Card] = None
    
    def deal_initial_cards(self, card1: Card, card2: Card) -> None:
        """Deal initial two cards to dealer"""
        self.clear_hands()
        self.upcard = card1
        self.hole_card = card2
        self.current_hand = BlackjackHand([card1, card2])
    
    def reveal_hole_card(self) -> Card:
        """Reveal the dealer's hole card"""
        if self.hole_card:
            self.current_hand.add_card(self.hole_card)
            card = self.hole_card
            self.hole_card = None
            return card
        return None
    
    def get_action(self, visible_hand: Optional[BlackjackHand] = None) -> Action:
        """
        Get the dealer's action based on their hand.
        Dealer hits on 16 or less, stands on 17 or more.
        
        Args:
            visible_hand: The dealer's visible hand (upcard only initially)
            
        Returns:
            Action.HIT or Action.STAND
        """
        # If we have the full hand, use its total
        if self.current_hand.size >= 2:
            total = self.current_hand.total
        else:
            # Shouldn't happen in normal gameplay
            return Action.HIT
        
        # Standard dealer rules
        if total <= 16:
            return Action.HIT
        elif total >= 17:
            return Action.STAND
        
        # Soft 17 - some casinos hit, some stand
        # We'll stand on all 17s (most common rule)
        return Action.STAND
    
    @property
    def has_blackjack(self) -> bool:
        """Check if dealer has blackjack"""
        if self.current_hand.size == 2:
            return self.current_hand.is_blackjack
        return False
    
    @property
    def can_peek(self) -> bool:
        """Check if dealer can peek for blackjack (has Ace or 10 as upcard)"""
        if not self.upcard:
            return False
        return self.upcard.is_ace or self.upcard.is_ten_value
    
    def peek_for_blackjack(self) -> bool:
        """
        Peek at hole card to check for blackjack.
        
        Returns:
            True if dealer has blackjack
        """
        if not self.hole_card:
            return self.current_hand.is_blackjack
        
        # Check if upcard + hole card = blackjack
        temp_hand = BlackjackHand([self.upcard, self.hole_card])
        return temp_hand.is_blackjack
    
    def __str__(self) -> str:
        if self.hole_card:
            return f"Dealer: {self.upcard}, ?"
        return f"Dealer: {self.current_hand}"
    
    def __repr__(self) -> str:
        return f"Dealer(upcard={self.upcard}, hole_card={'?' if self.hole_card else None})"
