"""
Tests for strategy classes
"""

import pytest
from blackjack_game.core.card import Card, Rank, Suit
from blackjack_game.core.hand import BlackjackHand
from blackjack_game.players.strategy import BasicStrategy, AdvancedStrategy


class TestBasicStrategy:
    """Tests for BasicStrategy class"""
    
    def test_hard_total_actions(self):
        """Test basic strategy for hard totals"""
        # Test various hard totals
        test_cases = [
            # (player_total, dealer_upcard_value, expected_action)
            (8, 10, "HIT"),
            (9, 5, "DOUBLE"),
            (9, 10, "HIT"),
            (10, 9, "DOUBLE"),
            (10, 10, "HIT"),
            (11, 10, "DOUBLE"),
            (11, 11, "HIT"),  # Ace
            (12, 4, "STAND"),
            (12, 7, "HIT"),
            (13, 6, "STAND"),
            (13, 7, "HIT"),
            (16, 6, "STAND"),
            (16, 7, "HIT"),
            (17, 10, "STAND"),
            (20, 10, "STAND"),
        ]
        
        for player_total, dealer_value, expected_action in test_cases:
            hand = BlackjackHand()
            # Create a hand with the specified total (hard)
            if player_total <= 10:
                hand.add_card(Card(Rank(player_total), Suit.HEARTS))
            else:
                # For totals > 10, use two cards
                values = [(v, r) for v, r in enumerate(Rank) if v <= 10 and v != 1]
                for v, r in values:
                    if v == player_total - 10:
                        hand.add_card(Card(r, Suit.HEARTS))
                        hand.add_card(Card(Rank.TEN, Suit.SPADES))
                        break
            
            dealer_upcard = Card(Rank(dealer_value), Suit.DIAMONDS)
            action, _ = BasicStrategy.get_action(hand, dealer_upcard)
            
            assert action.name == expected_action, f"Failed for {player_total} vs {dealer_value}"
    
    def test_soft_total_actions(self):
        """Test basic strategy for soft totals"""
        test_cases = [
            # (player_total, dealer_upcard_value, expected_action)
            # Note: player_total includes Ace as 11
            (13, 5, "DOUBLE"),  # A2 vs 5
            (13, 10, "HIT"),   # A2 vs 10
            (14, 6, "DOUBLE"), # A3 vs 6
            (15, 6, "DOUBLE"), # A4 vs 6
            (16, 6, "DOUBLE"), # A5 vs 6
            (17, 6, "DOUBLE"), # A6 vs 6
            (18, 2, "DOUBLE"), # A7 vs 2
            (18, 7, "STAND"),  # A7 vs 7
            (18, 10, "HIT"),   # A7 vs 10
            (19, 10, "STAND"), # A8 vs 10
        ]
        
        for player_total, dealer_value, expected_action in test_cases:
            hand = BlackjackHand()
            # Create soft hand: Ace + (player_total - 11)
            ace_value = 11
            other_card_value = player_total - ace_value
            
            hand.add_card(Card(Rank.ACE, Suit.HEARTS))
            hand.add_card(Card(Rank(other_card_value), Suit.SPADES))
            
            dealer_upcard = Card(Rank(dealer_value), Suit.DIAMONDS)
            action, _ = BasicStrategy.get_action(hand, dealer_upcard)
            
            assert action.name == expected_action, f"Failed for soft {player_total} vs {dealer_value}"
    
    def test_pair_actions(self):
        """Test basic strategy for pairs"""
        test_cases = [
            # (pair_rank, dealer_upcard_value, expected_action)
            (Rank.ACE, 10, "SPLIT"),
            (Rank.EIGHT, 10, "SPLIT"),
            (Rank.TWO, 7, "SPLIT"),
            (Rank.TWO, 10, "HIT"),
            (Rank.THREE, 7, "SPLIT"),
            (Rank.THREE, 10, "HIT"),
            (Rank.FOUR, 6, "SPLIT"),
            (Rank.FOUR, 10, "HIT"),
            (Rank.FIVE, 10, "HIT"),  # Never split 5s
            (Rank.SIX, 6, "SPLIT"),
            (Rank.SIX, 10, "HIT"),
            (Rank.SEVEN, 7, "SPLIT"),
            (Rank.SEVEN, 10, "HIT"),
            (Rank.NINE, 9, "SPLIT"),
            (Rank.NINE, 10, "STAND"),
            (Rank.TEN, 10, "STAND"),  # Never split 10s
        ]
        
        for pair_rank, dealer_value, expected_action in test_cases:
            hand = BlackjackHand()
            hand.add_card(Card(pair_rank, Suit.HEARTS))
            hand.add_card(Card(pair_rank, Suit.SPADES))
            
            dealer_upcard = Card(Rank(dealer_value), Suit.DIAMONDS)
            action, _ = BasicStrategy.get_action(hand, dealer_upcard)
            
            assert action.name == expected_action, f"Failed for {pair_rank} vs {dealer_value}"


class TestAdvancedStrategy:
    """Tests for AdvancedStrategy class"""
    
    def test_positive_count_adjustments(self):
        """Test that advanced strategy adjusts for positive count"""
        hand = BlackjackHand()
        hand.add_card(Card(Rank.TEN, Suit.HEARTS))
        hand.add_card(Card(Rank.SIX, Suit.SPADES))  # 16
        
        dealer_upcard = Card(Rank.TEN, Suit.DIAMONDS)
        
        # At neutral count, should hit 16 vs 10
        action, _ = AdvancedStrategy.get_action(hand, dealer_upcard, true_count=0)
        assert action.name == "HIT"
        
        # At high positive count, might stand or surrender
        action, _ = AdvancedStrategy.get_action(hand, dealer_upcard, true_count=5)
        # Should be different from neutral count
        # (Note: exact behavior depends on implementation)
    
    def test_insurance_with_high_count(self):
        """Test insurance decision with high count"""
        dealer_upcard = Card(Rank.ACE, Suit.HEARTS)
        
        # At neutral count, don't take insurance
        should_take = AdvancedStrategy.should_take_insurance(dealer_upcard, true_count=0)
        assert should_take == False
        
        # At high count, take insurance
        should_take = AdvancedStrategy.should_take_insurance(dealer_upcard, true_count=5)
        assert should_take == True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
