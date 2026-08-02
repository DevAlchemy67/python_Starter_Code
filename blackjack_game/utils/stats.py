"""
Stats module - Game statistics and hand analysis
"""

from typing import List, Dict, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass
from ..core.card import Card, Rank, Suit
from ..core.hand import BlackjackHand
from ..players.player import Player, Action


@dataclass
class HandStats:
    """Statistics for a single hand"""
    total: int
    is_soft: bool
    is_hard: bool
    is_pair: bool
    pair_rank: Optional[Rank]
    is_blackjack: bool
    can_split: bool
    can_double: bool
    bust_probability: float  # Probability of busting with one more card
    win_probability: float  # Estimated probability of winning


@dataclass
class PlayerStats:
    """Extended statistics for a player"""
    name: str
    bankroll: float
    initial_bankroll: float
    hands_played: int
    wins: int
    losses: int
    pushes: int
    blackjacks: int
    win_rate: float
    profit: float
    average_bet: float
    max_win_streak: int
    max_lose_streak: int
    current_streak: int
    streak_type: str  # 'win', 'lose', or 'push'


class HandAnalyzer:
    """
    Analyzes blackjack hands and provides statistics.
    """
    
    # Probability of dealer busting based on upcard
    DEALER_BUST_PROBABILITIES = {
        2: 0.35,
        3: 0.37,
        4: 0.40,
        5: 0.42,
        6: 0.42,
        7: 0.26,
        8: 0.24,
        9: 0.23,
        10: 0.22,
        11: 0.17,  # Ace
    }
    
    # Probability of improving hand with one more card
    IMPROVEMENT_PROBABILITIES = {
        # hard_total: probability of getting a card that doesn't bust
        4: 1.0, 5: 1.0, 6: 1.0, 7: 1.0, 8: 1.0, 9: 1.0, 10: 1.0, 11: 1.0,
        12: 0.31, 13: 0.39, 14: 0.56, 15: 0.58, 16: 0.62, 17: 0.69,
        18: 0.77, 19: 0.85, 20: 0.92, 21: 1.0
    }
    
    @staticmethod
    def analyze_hand(hand: BlackjackHand, dealer_upcard: Optional[Card] = None) -> HandStats:
        """
        Analyze a blackjack hand and return statistics.
        
        Args:
            hand: The hand to analyze
            dealer_upcard: Dealer's upcard (optional)
            
        Returns:
            HandStats object
        """
        total = hand.total
        is_soft = hand.is_soft
        is_hard = hand.is_hard
        is_pair = hand.is_pair
        pair_rank = hand.pair_rank
        is_blackjack = hand.is_blackjack
        can_split = hand.can_split
        can_double = hand.can_double
        
        # Calculate bust probability
        if total >= 21:
            bust_probability = 1.0 if total > 21 else 0.0
        else:
            # Probability of busting with one more card
            # This is based on the probability of drawing a card that makes total > 21
            # For hard hands: bust if card > (21 - total)
            # For soft hands: more complex calculation
            if is_hard:
                # Cards that cause bust: any card > (21 - total)
                bust_cards = [r for r in Rank if r.value > (21 - total)]
                bust_probability = len(bust_cards) / 13.0  # 13 ranks
            else:
                # For soft hands, Ace can be counted as 1
                # So we need to consider both possibilities
                # Simplified: use hard total calculation with Ace as 1
                hard_total = total - 10  # Convert soft to hard by making Ace = 1
                bust_cards = [r for r in Rank if r.value > (21 - hard_total)]
                bust_probability = len(bust_cards) / 13.0
        
        # Calculate win probability (simplified estimate)
        win_probability = 0.0
        if dealer_upcard:
            dealer_value = dealer_upcard.value
            dealer_bust_prob = HandAnalyzer.DEALER_BUST_PROBABILITIES.get(dealer_value, 0.25)
            
            # Estimate based on hand total vs dealer upcard
            if total > 21:
                win_probability = 0.0
            elif total == 21:
                win_probability = 1.0 - dealer_bust_prob
            else:
                # Rough estimate: higher hand = higher win probability
                # This is a simplification; actual probability depends on many factors
                if dealer_value <= 6:
                    # Dealer has weak upcard
                    win_probability = 0.6 if total >= 17 else 0.5
                elif dealer_value >= 10 or dealer_value == 1:  # Ace
                    # Dealer has strong upcard
                    win_probability = 0.4 if total >= 17 else 0.3
                else:
                    # Dealer has medium upcard
                    win_probability = 0.5 if total >= 17 else 0.4
        
        return HandStats(
            total=total,
            is_soft=is_soft,
            is_hard=is_hard,
            is_pair=is_pair,
            pair_rank=pair_rank,
            is_blackjack=is_blackjack,
            can_split=can_split,
            can_double=can_double,
            bust_probability=bust_probability,
            win_probability=win_probability
        )
    
    @staticmethod
    def get_hand_quality(hand: BlackjackHand) -> str:
        """
        Get a qualitative assessment of hand strength.
        
        Args:
            hand: The hand to assess
            
        Returns:
            String describing hand quality
        """
        if hand.is_blackjack:
            return "Excellent (Blackjack!)"
        elif hand.total > 21:
            return "Bust"
        elif hand.total >= 19:
            return "Very Strong"
        elif hand.total >= 17:
            return "Strong"
        elif hand.total >= 13:
            return "Moderate"
        elif hand.total >= 10:
            return "Weak"
        else:
            return "Very Weak"
    
    @staticmethod
    def get_dealer_strength(dealer_upcard: Card) -> str:
        """
        Assess dealer's strength based on upcard.
        
        Args:
            dealer_upcard: Dealer's visible card
            
        Returns:
            String describing dealer strength
        """
        value = dealer_upcard.value
        
        if value == 11:  # Ace
            return "Very Strong (Ace)"
        elif value >= 10:
            return "Strong (10-value)"
        elif value >= 7:
            return "Moderate"
        elif value >= 4:
            return "Weak"
        else:  # 2-3
            return "Very Weak"


class GameStats:
    """
    Tracks and analyzes game statistics.
    """
    
    def __init__(self):
        self.players: Dict[str, PlayerStats] = {}
        self.rounds_played = 0
        self.total_hands = 0
        self.total_bets = 0.0
        self.total_winnings = 0.0
        
        # Hand type statistics
        self.hand_types: Dict[str, int] = defaultdict(int)
        self.outcomes: Dict[str, int] = defaultdict(int)
        
        # Dealer statistics
        self.dealer_upcards: Dict[int, int] = defaultdict(int)
        self.dealer_final_totals: Dict[int, int] = defaultdict(int)
        self.dealer_busts = 0
        self.dealer_blackjacks = 0
    
    def add_player(self, player: Player) -> None:
        """Add a player to track"""
        if player.name not in self.players:
            self.players[player.name] = PlayerStats(
                name=player.name,
                bankroll=player.bankroll,
                initial_bankroll=player.bankroll,
                hands_played=0,
                wins=0,
                losses=0,
                pushes=0,
                blackjacks=0,
                win_rate=0.0,
                profit=0.0,
                average_bet=0.0,
                max_win_streak=0,
                max_lose_streak=0,
                current_streak=0,
                streak_type=""
            )
    
    def record_hand(self, player: Player, hand: BlackjackHand, 
                   bet: float, result: str, payout: float) -> None:
        """
        Record a hand result.
        
        Args:
            player: The player
            hand: The hand played
            bet: Amount bet
            result: Result ('win', 'lose', 'push', 'blackjack')
            payout: Amount won
        """
        if player.name not in self.players:
            self.add_player(player)
        
        stats = self.players[player.name]
        
        # Update player stats
        stats.hands_played += 1
        stats.total_bets += bet
        stats.total_winnings += payout
        stats.profit = stats.bankroll - stats.initial_bankroll
        
        if result == 'win':
            stats.wins += 1
            self.outcomes['win'] += 1
            # Update streak
            if stats.streak_type == 'win':
                stats.current_streak += 1
            else:
                stats.current_streak = 1
                stats.streak_type = 'win'
            stats.max_win_streak = max(stats.max_win_streak, stats.current_streak)
        elif result == 'lose':
            stats.losses += 1
            self.outcomes['lose'] += 1
            # Update streak
            if stats.streak_type == 'lose':
                stats.current_streak += 1
            else:
                stats.current_streak = 1
                stats.streak_type = 'lose'
            stats.max_lose_streak = max(stats.max_lose_streak, stats.current_streak)
        elif result == 'push':
            stats.pushes += 1
            self.outcomes['push'] += 1
            # Reset streak
            stats.current_streak = 0
            stats.streak_type = ''
        elif result == 'blackjack':
            stats.blackjacks += 1
            stats.wins += 1
            self.outcomes['blackjack'] += 1
            # Update streak
            if stats.streak_type == 'win':
                stats.current_streak += 1
            else:
                stats.current_streak = 1
                stats.streak_type = 'win'
            stats.max_win_streak = max(stats.max_win_streak, stats.current_streak)
        
        # Update win rate
        total = stats.wins + stats.losses + stats.pushes
        if total > 0:
            stats.win_rate = (stats.wins + stats.blackjacks) / total * 100
        
        # Update hand types
        if hand.is_blackjack:
            self.hand_types['blackjack'] += 1
        elif hand.is_pair:
            self.hand_types[f'pair_{hand.pair_rank.name}'] += 1
        elif hand.is_soft:
            self.hand_types[f'soft_{hand.total}'] += 1
        else:
            self.hand_types[f'hard_{hand.total}'] += 1
        
        self.total_hands += 1
        self.total_bets += bet
    
    def record_dealer_round(self, upcard: Card, final_total: int, 
                           busted: bool, has_blackjack: bool) -> None:
        """Record dealer information for a round"""
        self.rounds_played += 1
        self.dealer_upcards[upcard.value] += 1
        self.dealer_final_totals[final_total] += 1
        
        if busted:
            self.dealer_busts += 1
        if has_blackjack:
            self.dealer_blackjacks += 1
    
    def get_summary(self) -> Dict:
        """Get a summary of all statistics"""
        return {
            'rounds_played': self.rounds_played,
            'total_hands': self.total_hands,
            'total_bets': self.total_bets,
            'total_winnings': self.total_winnings,
            'outcomes': dict(self.outcomes),
            'hand_types': dict(self.hand_types),
            'dealer_stats': {
                'upcards': dict(self.dealer_upcards),
                'final_totals': dict(self.dealer_final_totals),
                'busts': self.dealer_busts,
                'blackjacks': self.dealer_blackjacks,
                'bust_rate': (self.dealer_busts / self.rounds_played * 100) if self.rounds_played > 0 else 0,
            },
            'players': {name: self._player_stats_to_dict(stats) 
                       for name, stats in self.players.items()}
        }
    
    def _player_stats_to_dict(self, stats: PlayerStats) -> Dict:
        """Convert player stats to dictionary"""
        return {
            'bankroll': stats.bankroll,
            'initial_bankroll': stats.initial_bankroll,
            'hands_played': stats.hands_played,
            'wins': stats.wins,
            'losses': stats.losses,
            'pushes': stats.pushes,
            'blackjacks': stats.blackjacks,
            'win_rate': stats.win_rate,
            'profit': stats.profit,
            'average_bet': (stats.total_bets / stats.hands_played) if stats.hands_played > 0 else 0,
            'max_win_streak': stats.max_win_streak,
            'max_lose_streak': stats.max_lose_streak,
            'current_streak': stats.current_streak,
            'streak_type': stats.streak_type,
        }
    
    def get_player_summary(self, player_name: str) -> Optional[Dict]:
        """Get summary for a specific player"""
        if player_name in self.players:
            return self._player_stats_to_dict(self.players[player_name])
        return None
    
    def __str__(self) -> str:
        return f"GameStats(rounds={self.rounds_played}, hands={self.total_hands}, players={len(self.players)})"
