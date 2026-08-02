"""
Game module - Main blackjack game logic
"""

import random
from typing import List, Optional, Dict, Any, Tuple
from enum import Enum, auto
from dataclasses import dataclass, field
from .core.card import Card, Rank, Suit
from .core.deck import Shoe
from .core.hand import BlackjackHand
from .players.player import Player, Dealer, Action, Bet
from .players.strategy import BasicStrategy, AdvancedStrategy


class GamePhase(Enum):
    """Phases of a blackjack game"""
    WAITING_FOR_PLAYERS = auto()
    PLACING_BETS = auto()
    DEALING = auto()
    PLAYER_TURN = auto()
    DEALER_TURN = auto()
    SETTLING_BETS = auto()
    GAME_OVER = auto()


class GameResult(Enum):
    """Possible game outcomes"""
    PLAYER_WIN = auto()
    PLAYER_LOSE = auto()
    PUSH = auto()
    BLACKJACK = auto()
    SURRENDER = auto()


@dataclass
class GameSettings:
    """Settings for a blackjack game"""
    num_decks: int = 6
    min_bet: float = 10.0
    max_bet: float = 500.0
    allow_splitting: bool = True
    allow_doubling: bool = True
    allow_doubling_after_split: bool = False
    allow_surrender: bool = True
    allow_insurance: bool = True
    dealer_hits_soft_17: bool = False
    blackjack_payout: float = 1.5
    max_splits: int = 4
    reshuffle_threshold: float = 0.25
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary"""
        return {
            'num_decks': self.num_decks,
            'min_bet': self.min_bet,
            'max_bet': self.max_bet,
            'allow_splitting': self.allow_splitting,
            'allow_doubling': self.allow_doubling,
            'allow_doubling_after_split': self.allow_doubling_after_split,
            'allow_surrender': self.allow_surrender,
            'allow_insurance': self.allow_insurance,
            'dealer_hits_soft_17': self.dealer_hits_soft_17,
            'blackjack_payout': self.blackjack_payout,
            'max_splits': self.max_splits,
            'reshuffle_threshold': self.reshuffle_threshold,
        }


@dataclass
class HandResult:
    """Result of a single hand"""
    hand: BlackjackHand
    bet: float
    result: GameResult
    payout: float
    is_blackjack: bool = False
    is_surrendered: bool = False
    
    def __str__(self) -> str:
        result_str = {
            GameResult.PLAYER_WIN: "WIN",
            GameResult.PLAYER_LOSE: "LOSE",
            GameResult.PUSH: "PUSH",
            GameResult.BLACKJACK: "BLACKJACK",
            GameResult.SURRENDER: "SURRENDER",
        }[self.result]
        
        return f"{self.hand} - {result_str} (${self.payout:.2f})"


class BlackjackGame:
    """
    Main blackjack game class.
    Manages the game state, players, and game flow.
    """
    
    def __init__(self, settings: Optional[GameSettings] = None):
        """
        Initialize a new blackjack game.
        
        Args:
            settings: Game settings, or default settings if None
        """
        self.settings = settings or GameSettings()
        self.shoe = Shoe(
            num_decks=self.settings.num_decks,
            reshuffle_threshold=self.settings.reshuffle_threshold
        )
        
        self.players: List[Player] = []
        self.dealer = Dealer()
        self.phase = GamePhase.WAITING_FOR_PLAYERS
        self.current_player_index = 0
        self.round_number = 0
        
        # Game history
        self.history: List[Dict] = []
    
    def add_player(self, player: Player) -> None:
        """Add a player to the game"""
        self.players.append(player)
    
    def remove_player(self, player: Player) -> bool:
        """Remove a player from the game"""
        if player in self.players:
            self.players.remove(player)
            return True
        return False
    
    def start_game(self) -> None:
        """Start a new game"""
        if len(self.players) == 0:
            raise ValueError("Cannot start game with no players")
        
        self.phase = GamePhase.PLACING_BETS
        self.round_number += 1
        self.current_player_index = 0
        
        # Clear hands for new round
        for player in self.players:
            player.clear_hands()
        self.dealer.clear_hands()
        
        # Check if we need to reshuffle
        if self.shoe.needs_reshuffle():
            self.shoe.reshuffle()
    
    def place_bet(self, player: Player, amount: float) -> bool:
        """
        Place a bet for a player.
        
        Args:
            player: The player placing the bet
            amount: Amount to bet
            
        Returns:
            True if bet was successful
        """
        if self.phase != GamePhase.PLACING_BETS:
            return False
        
        if amount < self.settings.min_bet or amount > self.settings.max_bet:
            return False
        
        return player.place_bet(amount)
    
    def deal_initial_cards(self) -> None:
        """Deal initial cards to all players and dealer"""
        if self.phase != GamePhase.PLACING_BETS:
            raise ValueError("Cannot deal: not in betting phase")
        
        # Burn card (casino procedure)
        self.shoe.burn(1)
        
        # Deal to players and dealer
        for _ in range(2):
            for player in self.players:
                card = self.shoe.deal()
                if card:
                    player.receive_card(card)
            
            card = self.shoe.deal()
            if card:
                if len(self.dealer.current_hand.cards) == 0:
                    self.dealer.upcard = card
                else:
                    self.dealer.hole_card = card
        
        self.phase = GamePhase.PLAYER_TURN
    
    def get_current_player(self) -> Optional[Player]:
        """Get the current player whose turn it is"""
        if self.current_player_index < len(self.players):
            return self.players[self.current_player_index]
        return None
    
    def next_player(self) -> None:
        """Move to the next player"""
        self.current_player_index += 1
        
        # Check if all players have had their turn
        if self.current_player_index >= len(self.players):
            self.phase = GamePhase.DEALER_TURN
            self.current_player_index = 0
    
    def player_action(self, player: Player, action: Action, 
                     hand_index: int = 0) -> bool:
        """
        Process a player's action.
        
        Args:
            player: The player taking action
            action: The action to take
            hand_index: Which hand to act on (for split hands)
            
        Returns:
            True if action was successful
        """
        if self.phase != GamePhase.PLAYER_TURN:
            return False
        
        if self.get_current_player() != player:
            return False
        
        current_hand = player.hands[hand_index]
        
        if action == Action.HIT:
            card = self.shoe.deal()
            if card:
                player.receive_card(card, hand_index)
                # Check if hand busted
                if current_hand.is_bust:
                    # Move to next hand or player
                    if hand_index + 1 < len(player.hands):
                        # Still has other hands to play
                        return True
                    else:
                        # All hands done, move to next player
                        self.next_player()
            return True
        
        elif action == Action.STAND:
            # Move to next hand or player
            if hand_index + 1 < len(player.hands):
                # Play next hand
                return True
            else:
                # All hands done, move to next player
                self.next_player()
            return True
        
        elif action == Action.DOUBLE:
            if not self.settings.allow_doubling:
                return False
            
            if len(current_hand.cards) != 2:
                return False
            
            # Double the bet
            additional_bet = player.current_bet
            if additional_bet > player.bankroll:
                return False
            
            player.bankroll -= additional_bet
            player.current_bet += additional_bet
            
            # Deal one card
            card = self.shoe.deal()
            if card:
                player.receive_card(card, hand_index)
                # After doubling, must stand
                if hand_index + 1 < len(player.hands):
                    return True
                else:
                    self.next_player()
            return True
        
        elif action == Action.SPLIT:
            if not self.settings.allow_splitting:
                return False
            
            if not current_hand.can_split:
                return False
            
            if len(player.hands) >= self.settings.max_splits:
                return False
            
            # Split the hand
            hand1, hand2 = current_hand.split()
            player.hands[hand_index] = hand1
            player.hands.insert(hand_index + 1, hand2)
            
            # Place additional bet for second hand
            additional_bet = player.current_bet
            if additional_bet > player.bankroll:
                # Can't afford to split, revert
                player.hands.pop(hand_index + 1)
                return False
            
            player.bankroll -= additional_bet
            player.current_bet += additional_bet
            
            # Deal cards to both hands
            card1 = self.shoe.deal()
            card2 = self.shoe.deal()
            if card1 and card2:
                player.receive_card(card1, hand_index)
                player.receive_card(card2, hand_index + 1)
            
            # Continue with first hand
            return True
        
        elif action == Action.SURRENDER:
            if not self.settings.allow_surrender:
                return False
            
            # Surrender - lose half the bet
            player.bankroll += player.current_bet * 0.5
            player.lose()
            
            # Remove this hand
            player.hands.pop(hand_index)
            
            # Move to next hand or player
            if hand_index < len(player.hands):
                return True
            else:
                self.next_player()
            return True
        
        elif action == Action.INSURANCE:
            if not self.settings.allow_insurance:
                return False
            
            if not self.dealer.can_peek or not self.dealer.peek_for_blackjack():
                return False
            
            # Offer insurance
            insurance_bet = player.current_bet * 0.5
            if insurance_bet > player.bankroll:
                return False
            
            player.bankroll -= insurance_bet
            
            # Check if dealer has blackjack
            if self.dealer.has_blackjack:
                # Player gets insurance payout
                player.bankroll += insurance_bet * 2
            
            return True
        
        return False
    
    def play_dealer_turn(self) -> None:
        """Play the dealer's turn according to house rules"""
        if self.phase != GamePhase.DEALER_TURN:
            return
        
        # Reveal dealer's hole card
        self.dealer.reveal_hole_card()
        
        # Dealer plays according to rules
        while True:
            action = self.dealer.get_action()
            
            if action == Action.HIT:
                card = self.shoe.deal()
                if card:
                    self.dealer.receive_card(card)
                    if self.dealer.current_hand.is_bust:
                        break
            elif action == Action.STAND:
                break
        
        self.phase = GamePhase.SETTLING_BETS
    
    def settle_bets(self) -> List[HandResult]:
        """
        Settle all bets based on hand results.
        
        Returns:
            List of HandResult for each player hand
        """
        if self.phase != GamePhase.SETTLING_BETS:
            return []
        
        results = []
        dealer_total = self.dealer.current_hand.total
        dealer_has_blackjack = self.dealer.current_hand.is_blackjack
        
        for player in self.players:
            for hand_index, hand in enumerate(player.hands):
                bet_amount = player.current_bet / len(player.hands) if len(player.hands) > 1 else player.current_bet
                
                # Check for player blackjack
                if hand.is_blackjack:
                    if dealer_has_blackjack:
                        # Push
                        result = HandResult(
                            hand=hand,
                            bet=bet_amount,
                            result=GameResult.PUSH,
                            payout=bet_amount,
                            is_blackjack=True
                        )
                        player.push(hand_index)
                    else:
                        # Player wins with blackjack payout
                        payout = bet_amount * self.settings.blackjack_payout
                        result = HandResult(
                            hand=hand,
                            bet=bet_amount,
                            result=GameResult.BLACKJACK,
                            payout=payout,
                            is_blackjack=True
                        )
                        player.blackjack_payout(hand_index)
                    
                    results.append(result)
                    continue
                
                # Check if player busted
                if hand.is_bust:
                    result = HandResult(
                        hand=hand,
                        bet=bet_amount,
                        result=GameResult.PLAYER_LOSE,
                        payout=0
                    )
                    player.lose(hand_index)
                    results.append(result)
                    continue
                
                # Check if dealer busted
                if self.dealer.current_hand.is_bust:
                    payout = bet_amount * 2
                    result = HandResult(
                        hand=hand,
                        bet=bet_amount,
                        result=GameResult.PLAYER_WIN,
                        payout=payout
                    )
                    player.win_payout(payout, hand_index)
                    results.append(result)
                    continue
                
                # Compare totals
                if hand.total > dealer_total:
                    payout = bet_amount * 2
                    result = HandResult(
                        hand=hand,
                        bet=bet_amount,
                        result=GameResult.PLAYER_WIN,
                        payout=payout
                    )
                    player.win_payout(payout, hand_index)
                elif hand.total < dealer_total:
                    result = HandResult(
                        hand=hand,
                        bet=bet_amount,
                        result=GameResult.PLAYER_LOSE,
                        payout=0
                    )
                    player.lose(hand_index)
                else:  # Push
                    result = HandResult(
                        hand=hand,
                        bet=bet_amount,
                        result=GameResult.PUSH,
                        payout=bet_amount
                    )
                    player.push(hand_index)
                
                results.append(result)
        
        # Record round in history
        round_history = {
            'round': self.round_number,
            'dealer_total': dealer_total,
            'dealer_busted': self.dealer.current_hand.is_bust,
            'dealer_blackjack': dealer_has_blackjack,
            'results': [
                {
                    'player': player.name,
                    'hand': str(hand),
                    'result': result.result.name,
                    'payout': result.payout
                }
                for player in self.players
                for result in results
                if result.hand == hand  # This logic needs fixing
            ]
        }
        self.history.append(round_history)
        
        self.phase = GamePhase.GAME_OVER
        return results
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get the current game state"""
        return {
            'phase': self.phase.name,
            'round': self.round_number,
            'players': [
                {
                    'name': p.name,
                    'bankroll': p.bankroll,
                    'current_bet': p.current_bet,
                    'hands': [str(h) for h in p.hands],
                    'active_hand_index': p.active_hand_index,
                }
                for p in self.players
            ],
            'dealer': {
                'upcard': str(self.dealer.upcard) if self.dealer.upcard else None,
                'hand': str(self.dealer.current_hand) if self.phase != GamePhase.PLAYER_TURN else None,
                'has_blackjack': self.dealer.has_blackjack if self.phase != GamePhase.PLAYER_TURN else None,
            },
            'shoe': {
                'remaining': self.shoe.remaining,
                'total': self.shoe.total_cards,
            },
            'settings': self.settings.to_dict(),
        }
    
    def get_strategy_hint(self, player: Player, hand_index: int = 0) -> str:
        """
        Get a strategy hint for the current player and hand.
        
        Args:
            player: The player to get hint for
            hand_index: Which hand to analyze
            
        Returns:
            Strategy hint string
        """
        if self.phase != GamePhase.PLAYER_TURN:
            return ""
        
        if self.get_current_player() != player:
            return ""
        
        hand = player.hands[hand_index]
        dealer_upcard = self.dealer.upcard
        
        if not dealer_upcard:
            return ""
        
        # Use basic strategy for hints
        action, explanation = BasicStrategy.get_action(
            hand, dealer_upcard,
            can_split=self.settings.allow_splitting,
            can_double=self.settings.allow_doubling,
            can_surrender=self.settings.allow_surrender
        )
        
        return f"Strategy hint: {action} - {explanation}"
    
    def get_advanced_strategy_hint(self, player: Player, hand_index: int = 0,
                                    true_count: int = 0) -> str:
        """
        Get an advanced strategy hint with count consideration.
        
        Args:
            player: The player to get hint for
            hand_index: Which hand to analyze
            true_count: Current Hi-Lo count
            
        Returns:
            Advanced strategy hint string
        """
        if self.phase != GamePhase.PLAYER_TURN:
            return ""
        
        if self.get_current_player() != player:
            return ""
        
        hand = player.hands[hand_index]
        dealer_upcard = self.dealer.upcard
        
        if not dealer_upcard:
            return ""
        
        # Use advanced strategy for hints
        action, explanation = AdvancedStrategy.get_action(
            hand, dealer_upcard,
            can_split=self.settings.allow_splitting,
            can_double=self.settings.allow_doubling,
            can_surrender=self.settings.allow_surrender,
            true_count=true_count
        )
        
        return f"Advanced hint (count={true_count:+d}): {action} - {explanation}"
    
    def new_round(self) -> None:
        """Start a new round"""
        self.start_game()
    
    def __str__(self) -> str:
        return f"BlackjackGame(round={self.round_number}, phase={self.phase.name}, players={len(self.players)})"
    
    def __repr__(self) -> str:
        return f"BlackjackGame(settings={self.settings}, round={self.round_number})"
