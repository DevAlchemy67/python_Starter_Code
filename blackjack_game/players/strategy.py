"""
Strategy module - Basic and advanced blackjack strategies
"""

from typing import Optional, Dict, Tuple
from enum import Enum
from ..core.hand import BlackjackHand
from ..core.card import Card, Rank
from .player import Action


class StrategyLevel(Enum):
    """Strategy difficulty levels"""
    BEGINNER = "beginner"
    BASIC = "basic"
    ADVANCED = "advanced"
    EXPERT = "expert"


class BasicStrategy:
    """
    Implements basic blackjack strategy.
    This is the mathematically optimal strategy for most situations.
    """
    
    # Strategy tables for different scenarios
    # Format: (player_total, dealer_upcard, is_soft) -> Action
    
    @staticmethod
    def get_hard_total_action(player_total: int, dealer_upcard: Card) -> Action:
        """
        Get action for hard totals (no Ace or Ace counted as 1).
        
        Basic Strategy for Hard Totals:
        - 8 or less: Always Hit
        - 9: Double vs 3-6, else Hit
        - 10: Double vs 2-9, else Hit
        - 11: Double vs 2-10, Hit vs Ace
        - 12: Stand vs 4-6, Hit otherwise
        - 13-16: Stand vs 2-6, Hit vs 7-Ace
        - 17+: Always Stand
        """
        dealer_value = dealer_upcard.value
        
        if player_total <= 8:
            return Action.HIT
        elif player_total == 9:
            return Action.DOUBLE if 3 <= dealer_value <= 6 else Action.HIT
        elif player_total == 10:
            return Action.DOUBLE if 2 <= dealer_value <= 9 else Action.HIT
        elif player_total == 11:
            return Action.DOUBLE if 2 <= dealer_value <= 10 else Action.HIT
        elif player_total == 12:
            return Action.STAND if 4 <= dealer_value <= 6 else Action.HIT
        elif 13 <= player_total <= 16:
            return Action.STAND if 2 <= dealer_value <= 6 else Action.HIT
        else:  # 17+
            return Action.STAND
    
    @staticmethod
    def get_soft_total_action(player_total: int, dealer_upcard: Card) -> Action:
        """
        Get action for soft totals (Ace counted as 11).
        
        Basic Strategy for Soft Totals:
        - A2-A3: Double vs 5-6, Hit otherwise
        - A4-A5: Double vs 4-6, Hit otherwise
        - A6: Double vs 2-6, Hit otherwise
        - A7: Double vs 2-6, Stand vs 7-8, Hit vs 9-Ace
        - A8+: Always Stand
        """
        dealer_value = dealer_upcard.value
        
        # player_total includes Ace as 11, so A2=13, A3=14, etc.
        if player_total <= 13:  # A2
            return Action.DOUBLE if 5 <= dealer_value <= 6 else Action.HIT
        elif player_total == 14:  # A3
            return Action.DOUBLE if 5 <= dealer_value <= 6 else Action.HIT
        elif player_total == 15:  # A4
            return Action.DOUBLE if 4 <= dealer_value <= 6 else Action.HIT
        elif player_total == 16:  # A5
            return Action.DOUBLE if 4 <= dealer_value <= 6 else Action.HIT
        elif player_total == 17:  # A6
            return Action.DOUBLE if 2 <= dealer_value <= 6 else Action.HIT
        elif player_total == 18:  # A7
            return Action.DOUBLE if 2 <= dealer_value <= 6 else (
                Action.STAND if 7 <= dealer_value <= 8 else Action.HIT
            )
        else:  # A8+ (19+)
            return Action.STAND
    
    @staticmethod
    def get_pair_action(pair_rank: Rank, dealer_upcard: Card) -> Action:
        """
        Get action for pairs.
        
        Basic Strategy for Pairs:
        - Aces, 8s: Always Split
        - 2s, 3s: Split vs 4-7
        - 4s: Split vs 5-6
        - 5s: Never Split (treat as 10)
        - 6s: Split vs 2-6
        - 7s: Split vs 2-7
        - 9s: Split vs 2-6, 8-9
        - 10s: Never Split
        """
        dealer_value = dealer_upcard.value
        
        if pair_rank == Rank.ACE:
            return Action.SPLIT
        elif pair_rank == Rank.TWO:
            return Action.SPLIT if 4 <= dealer_value <= 7 else Action.HIT
        elif pair_rank == Rank.THREE:
            return Action.SPLIT if 4 <= dealer_value <= 7 else Action.HIT
        elif pair_rank == Rank.FOUR:
            return Action.SPLIT if 5 <= dealer_value <= 6 else Action.HIT
        elif pair_rank == Rank.FIVE:
            return Action.HIT  # Never split 5s
        elif pair_rank == Rank.SIX:
            return Action.SPLIT if 2 <= dealer_value <= 6 else Action.HIT
        elif pair_rank == Rank.SEVEN:
            return Action.SPLIT if 2 <= dealer_value <= 7 else Action.HIT
        elif pair_rank == Rank.EIGHT:
            return Action.SPLIT
        elif pair_rank == Rank.NINE:
            return Action.SPLIT if dealer_value in [2, 3, 4, 5, 6, 8, 9] else Action.STAND
        else:  # 10, J, Q, K
            return Action.STAND  # Never split 10s
    
    @staticmethod
    def should_take_insurance(dealer_upcard: Card) -> bool:
        """
        Determine if player should take insurance.
        Basic strategy: Only take insurance if you have a blackjack.
        """
        return False  # Basic strategy says no to insurance
    
    @staticmethod
    def should_surrender(hand: BlackjackHand, dealer_upcard: Card) -> bool:
        """
        Determine if player should surrender.
        Basic strategy: Surrender 16 vs 9, 10, Ace and 15 vs 10.
        """
        dealer_value = dealer_upcard.value
        total = hand.total
        
        # Late surrender (most common)
        if total == 16 and dealer_value >= 9:
            return True
        if total == 15 and dealer_value == 10:
            return True
        
        return False
    
    @classmethod
    def get_action(cls, hand: BlackjackHand, dealer_upcard: Card, 
                   can_split: bool = True, can_double: bool = True,
                   can_surrender: bool = True) -> Tuple[Action, str]:
        """
        Get the recommended action for a hand using basic strategy.
        
        Args:
            hand: Player's current hand
            dealer_upcard: Dealer's visible card
            can_split: Whether splitting is allowed
            can_double: Whether doubling is allowed
            can_surrender: Whether surrendering is allowed
            
        Returns:
            Tuple of (recommended action, explanation)
        """
        # Check for surrender first
        if can_surrender and cls.should_surrender(hand, dealer_upcard):
            return Action.SURRENDER, "Basic strategy: Surrender"
        
        # Check for split
        if can_split and hand.is_pair:
            action = cls.get_pair_action(hand.pair_rank, dealer_upcard)
            if action == Action.SPLIT:
                return Action.SPLIT, f"Basic strategy: Split {hand.pair_rank}s"
        
        # Check for double down
        if can_double and hand.size == 2:
            if hand.is_soft:
                action = cls.get_soft_total_action(hand.total, dealer_upcard)
                if action == Action.DOUBLE:
                    return Action.DOUBLE, f"Basic strategy: Double on soft {hand.total}"
            else:
                action = cls.get_hard_total_action(hand.total, dealer_upcard)
                if action == Action.DOUBLE:
                    return Action.DOUBLE, f"Basic strategy: Double on hard {hand.total}"
        
        # Default to hit or stand
        if hand.is_soft:
            action = cls.get_soft_total_action(hand.total, dealer_upcard)
        else:
            action = cls.get_hard_total_action(hand.total, dealer_upcard)
        
        explanation = f"Basic strategy: {action.name} on {'soft' if hand.is_soft else 'hard'} {hand.total}"
        return action, explanation


class AdvancedStrategy(BasicStrategy):
    """
    Advanced blackjack strategy with more nuanced decisions.
    Includes count-based adjustments and rule variations.
    """
    
    def __init__(self, true_count: int = 0):
        """
        Initialize advanced strategy with current true count.
        
        Args:
            true_count: Current Hi-Lo count (positive = favorable)
        """
        self.true_count = true_count
    
    @classmethod
    def get_action(cls, hand: BlackjackHand, dealer_upcard: Card,
                   can_split: bool = True, can_double: bool = True,
                   can_surrender: bool = True, true_count: int = 0) -> Tuple[Action, str]:
        """
        Get action with advanced strategy considerations.
        
        Args:
            hand: Player's current hand
            dealer_upcard: Dealer's visible card
            can_split: Whether splitting is allowed
            can_double: Whether doubling is allowed
            can_surrender: Whether surrendering is allowed
            true_count: Current Hi-Lo count
            
        Returns:
            Tuple of (recommended action, explanation)
        """
        # Basic strategy first
        basic_action, basic_explanation = super().get_action(
            hand, dealer_upcard, can_split, can_double, can_surrender
        )
        
        # Adjust for count
        if true_count > 0:
            # Positive count - be more aggressive
            return cls._adjust_for_positive_count(
                hand, dealer_upcard, basic_action, basic_explanation, true_count
            )
        elif true_count < 0:
            # Negative count - be more conservative
            return cls._adjust_for_negative_count(
                hand, dealer_upcard, basic_action, basic_explanation, true_count
            )
        
        return basic_action, basic_explanation
    
    @staticmethod
    def _adjust_for_positive_count(hand: BlackjackHand, dealer_upcard: Card,
                                   basic_action: Action, basic_explanation: str,
                                   true_count: int) -> Tuple[Action, str]:
        """Adjust strategy for positive count"""
        dealer_value = dealer_upcard.value
        
        # More aggressive doubling
        if basic_action == Action.HIT and hand.size == 2:
            if hand.is_soft:
                # Double on more soft hands
                if hand.total in [13, 14] and dealer_value in [4, 5, 6]:
                    return Action.DOUBLE, f"Advanced: Double soft {hand.total} vs {dealer_value} (count={true_count})"
                if hand.total in [15, 16] and dealer_value in [4, 5, 6]:
                    return Action.DOUBLE, f"Advanced: Double soft {hand.total} vs {dealer_value} (count={true_count})"
            else:
                # Double on more hard hands
                if hand.total == 9 and dealer_value == 2:
                    return Action.DOUBLE, f"Advanced: Double hard 9 vs 2 (count={true_count})"
                if hand.total in [10, 11] and dealer_value == 10:
                    return Action.DOUBLE, f"Advanced: Double hard {hand.total} vs 10 (count={true_count})"
        
        # More aggressive splitting
        if basic_action == Action.HIT and hand.is_pair:
            pair_rank = hand.pair_rank
            if pair_rank == Rank.TWO and dealer_value in [2, 3, 7]:
                return Action.SPLIT, f"Advanced: Split {pair_rank}s vs {dealer_value} (count={true_count})"
            if pair_rank == Rank.THREE and dealer_value in [2, 3]:
                return Action.SPLIT, f"Advanced: Split {pair_rank}s vs {dealer_value} (count={true_count})"
            if pair_rank == Rank.SEVEN and dealer_value in [8, 9]:
                return Action.SPLIT, f"Advanced: Split {pair_rank}s vs {dealer_value} (count={true_count})"
        
        # Take insurance with high count
        if dealer_upcard.is_ace and true_count >= 3:
            return Action.INSURANCE, f"Advanced: Take insurance (count={true_count})"
        
        return basic_action, basic_explanation
    
    @staticmethod
    def _adjust_for_negative_count(hand: BlackjackHand, dealer_upcard: Card,
                                    basic_action: Action, basic_explanation: str,
                                    true_count: int) -> Tuple[Action, str]:
        """Adjust strategy for negative count"""
        dealer_value = dealer_upcard.value
        
        # Less aggressive doubling
        if basic_action == Action.DOUBLE and hand.size == 2:
            if hand.is_soft:
                if hand.total in [13, 14, 15] and dealer_value in [5, 6]:
                    return Action.HIT, f"Advanced: Hit soft {hand.total} vs {dealer_value} (count={true_count})"
            else:
                if hand.total == 10 and dealer_value in [9, 10]:
                    return Action.HIT, f"Advanced: Hit hard {hand.total} vs {dealer_value} (count={true_count})"
                if hand.total == 11 and dealer_value == 10:
                    return Action.HIT, f"Advanced: Hit hard 11 vs 10 (count={true_count})"
        
        # Less aggressive splitting
        if basic_action == Action.SPLIT and hand.is_pair:
            pair_rank = hand.pair_rank
            if pair_rank == Rank.TWO and dealer_value in [7, 8, 9, 10]:
                return Action.HIT, f"Advanced: Hit {pair_rank}s vs {dealer_value} (count={true_count})"
            if pair_rank == Rank.THREE and dealer_value in [7, 8, 9, 10]:
                return Action.HIT, f"Advanced: Hit {pair_rank}s vs {dealer_value} (count={true_count})"
            if pair_rank == Rank.SEVEN and dealer_value in [8, 9, 10]:
                return Action.HIT, f"Advanced: Hit {pair_rank}s vs {dealer_value} (count={true_count})"
        
        # More surrendering
        if basic_action == Action.HIT:
            if hand.total == 15 and dealer_value in [9, 10, 11]:
                return Action.SURRENDER, f"Advanced: Surrender 15 vs {dealer_value} (count={true_count})"
            if hand.total == 14 and dealer_value == 10:
                return Action.SURRENDER, f"Advanced: Surrender 14 vs 10 (count={true_count})"
        
        return basic_action, basic_explanation
    
    @staticmethod
    def should_take_insurance(dealer_upcard: Card, true_count: int) -> bool:
        """
        Advanced insurance decision based on count.
        Take insurance when count is high enough.
        """
        if not dealer_upcard.is_ace:
            return False
        
        # Take insurance at true count +3 or higher
        return true_count >= 3
    
    @classmethod
    def get_strategy_explanation(cls, hand: BlackjackHand, dealer_upcard: Card,
                                true_count: int = 0) -> str:
        """
        Get a detailed explanation of the strategy for a hand.
        Useful for teaching players.
        """
        action, explanation = cls.get_action(
            hand, dealer_upcard, True, True, True, true_count
        )
        
        # Add educational context
        context = []
        
        if hand.is_soft:
            context.append(f"You have a soft {hand.total} (Ace counted as 11)")
        else:
            context.append(f"You have a hard {hand.total}")
        
        context.append(f"Dealer shows {dealer_upcard}")
        
        if true_count != 0:
            context.append(f"Current count: {true_count:+d}")
        
        context.append(f"Recommended action: {action}")
        context.append(f"Reason: {explanation}")
        
        # Add strategy tips
        if hand.is_pair:
            context.append(f"Strategy tip: {cls._get_pair_tip(hand.pair_rank, dealer_upcard)}")
        elif hand.size == 2 and hand.total <= 11:
            context.append("Strategy tip: Always consider doubling with 2-card hands totaling 9-11")
        elif hand.total > 21:
            context.append("Strategy tip: You've busted! Try to avoid hitting on hard 17+")
        
        return "\n".join(context)
    
    @staticmethod
    def _get_pair_tip(pair_rank: Rank, dealer_upcard: Card) -> str:
        """Get a tip for playing pairs"""
        tips = {
            Rank.ACE: "Always split Aces - two chances for blackjack!",
            Rank.EIGHT: "Always split 8s - 16 is a terrible hand to hit",
            Rank.TEN: "Never split 10s - you already have a great hand (20)",
            Rank.FIVE: "Never split 5s - treat as a 10 and double down instead",
            Rank.FOUR: "Split 4s only vs 5-6, otherwise hit",
        }
        return tips.get(pair_rank, "Check basic strategy for this pair")


class StrategyTrainer:
    """
    Helper class for training players on blackjack strategy.
    """
    
    @staticmethod
    def get_quiz_question() -> Dict:
        """Generate a strategy quiz question"""
        import random
        from ..core.card import Rank, Suit
        from ..core.hand import BlackjackHand
        
        # Random hand scenarios
        scenarios = [
            {
                'type': 'hard_total',
                'hand_total': random.choice([8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]),
                'dealer_upcard': random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            },
            {
                'type': 'soft_total',
                'hand_total': random.choice([13, 14, 15, 16, 17, 18, 19]),
                'dealer_upcard': random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            },
            {
                'type': 'pair',
                'pair_rank': random.choice(list(Rank)),
                'dealer_upcard': random.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
            },
        ]
        
        scenario = random.choice(scenarios)
        
        if scenario['type'] == 'pair':
            rank = scenario['pair_rank']
            dealer_card = Card(Rank(scenario['dealer_upcard']), Suit.HEARTS)
            
            question = f"You have a pair of {rank}s. Dealer shows {dealer_card}. What should you do?"
            correct_action, _ = BasicStrategy.get_pair_action(rank, dealer_card)
            
            return {
                'question': question,
                'type': 'pair',
                'correct_action': correct_action,
                'explanation': f"Basic strategy: {correct_action.name} on {rank}s vs {dealer_card}",
                'options': [Action.HIT, Action.STAND, Action.SPLIT, Action.DOUBLE],
            }
        
        # For hard/soft totals
        hand_total = scenario['hand_total']
        dealer_card = Card(Rank(scenario['dealer_upcard']), Suit.HEARTS)
        
        if scenario['type'] == 'hard_total':
            question = f"You have a hard {hand_total}. Dealer shows {dealer_card}. What should you do?"
            correct_action, _ = BasicStrategy.get_hard_total_action(hand_total, dealer_card)
        else:
            question = f"You have a soft {hand_total}. Dealer shows {dealer_card}. What should you do?"
            correct_action, _ = BasicStrategy.get_soft_total_action(hand_total, dealer_card)
        
        return {
            'question': question,
            'type': scenario['type'],
            'correct_action': correct_action,
            'explanation': f"Basic strategy: {correct_action.name} on {scenario['type'].replace('_', ' ')} {hand_total} vs {dealer_card}",
            'options': [Action.HIT, Action.STAND, Action.DOUBLE],
        }
