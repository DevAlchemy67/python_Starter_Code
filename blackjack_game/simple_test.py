#!/usr/bin/env python3
"""
Simple test script for blackjack game
"""

from blackjack_game.core.card import Card, Rank, Suit
from blackjack_game.core.deck import Deck, Shoe
from blackjack_game.core.hand import Hand, BlackjackHand
from blackjack_game.players.strategy import BasicStrategy


def test_cards():
    """Test card functionality"""
    print("Testing cards...")
    
    # Test card creation
    ace = Card(Rank.ACE, Suit.HEARTS)
    assert ace.rank == Rank.ACE
    assert ace.suit == Suit.HEARTS
    assert ace.value == 11
    assert ace.is_ace == True
    
    king = Card(Rank.KING, Suit.SPADES)
    assert king.value == 10
    assert king.is_face_card == True
    assert king.is_ten_value == True
    
    seven = Card(Rank.SEVEN, Suit.DIAMONDS)
    assert seven.value == 7
    assert seven.is_ace == False
    assert seven.is_face_card == False
    
    print("✓ Cards test passed")


def test_deck():
    """Test deck functionality"""
    print("Testing deck...")
    
    deck = Deck(shuffle=False)
    assert len(deck) == 52
    assert deck.remaining == 52
    
    card = deck.deal()
    assert card is not None
    assert deck.remaining == 51
    
    # Deal all cards
    for _ in range(51):
        deck.deal()
    
    assert deck.is_empty == True
    assert deck.deal() is None
    
    print("✓ Deck test passed")


def test_shoe():
    """Test shoe functionality"""
    print("Testing shoe...")
    
    shoe = Shoe(num_decks=6)
    assert shoe.num_decks == 6
    assert shoe.remaining == 6 * 52
    
    card = shoe.deal()
    assert card is not None
    assert shoe.remaining == 6 * 52 - 1
    
    # Burn cards
    burned = shoe.burn(3)
    assert len(burned) == 3
    assert shoe.discarded_count == 3
    
    print("✓ Shoe test passed")


def test_hand():
    """Test hand functionality"""
    print("Testing hand...")
    
    hand = Hand()
    assert hand.size == 0
    assert hand.is_empty == True
    
    ace = Card(Rank.ACE, Suit.HEARTS)
    king = Card(Rank.KING, Suit.SPADES)
    
    hand.add_card(ace)
    assert hand.size == 1
    assert hand.is_empty == False
    
    hand.add_card(king)
    assert hand.size == 2
    
    print("✓ Hand test passed")


def test_blackjack_hand():
    """Test blackjack hand functionality"""
    print("Testing blackjack hand...")
    
    # Empty hand
    hand = BlackjackHand()
    assert hand.total == 0
    
    # Hard hand
    hand = BlackjackHand()
    hand.add_card(Card(Rank.TEN, Suit.HEARTS))
    hand.add_card(Card(Rank.SEVEN, Suit.SPADES))
    assert hand.total == 17
    assert hand.is_soft == False
    
    # Soft hand
    hand = BlackjackHand()
    hand.add_card(Card(Rank.ACE, Suit.HEARTS))
    hand.add_card(Card(Rank.SIX, Suit.SPADES))
    assert hand.total == 17
    assert hand.is_soft == True
    
    # Blackjack
    hand = BlackjackHand()
    hand.add_card(Card(Rank.ACE, Suit.HEARTS))
    hand.add_card(Card(Rank.KING, Suit.SPADES))
    assert hand.total == 21
    assert hand.is_blackjack == True
    
    # Bust
    hand = BlackjackHand()
    hand.add_card(Card(Rank.KING, Suit.HEARTS))
    hand.add_card(Card(Rank.KING, Suit.SPADES))
    hand.add_card(Card(Rank.KING, Suit.DIAMONDS))
    assert hand.total == 30
    assert hand.is_bust == True
    
    # Pair
    hand = BlackjackHand()
    hand.add_card(Card(Rank.EIGHT, Suit.HEARTS))
    hand.add_card(Card(Rank.EIGHT, Suit.SPADES))
    assert hand.is_pair == True
    assert hand.pair_rank == Rank.EIGHT
    
    # Split
    hand1, hand2 = hand.split()
    assert hand1.size == 1
    assert hand2.size == 1
    assert hand1.cards[0].rank == Rank.EIGHT
    assert hand2.cards[0].rank == Rank.EIGHT
    
    # Ace adjustment
    hand = BlackjackHand()
    hand.add_card(Card(Rank.ACE, Suit.HEARTS))
    hand.add_card(Card(Rank.TEN, Suit.SPADES))
    hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))
    assert hand.total == 16  # Ace counted as 1, not 11
    assert hand.is_soft == False
    
    print("✓ Blackjack hand test passed")


def test_strategy():
    """Test basic strategy"""
    print("Testing strategy...")
    
    dealer_upcard = Card(Rank.TEN, Suit.DIAMONDS)
    
    # Test hard 17 vs 10 -> Stand
    hand = BlackjackHand()
    hand.add_card(Card(Rank.TEN, Suit.HEARTS))
    hand.add_card(Card(Rank.SEVEN, Suit.SPADES))
    action, _ = BasicStrategy.get_action(hand, dealer_upcard, can_surrender=False)
    assert action.name == "STAND", f"Expected STAND, got {action.name}"
    
    # Test hard 12 vs 4 -> Stand (basic strategy: stand on 12 vs 4-6)
    hand = BlackjackHand()
    hand.add_card(Card(Rank.TEN, Suit.HEARTS))
    hand.add_card(Card(Rank.TWO, Suit.SPADES))
    dealer_upcard = Card(Rank.FOUR, Suit.DIAMONDS)
    action, _ = BasicStrategy.get_action(hand, dealer_upcard, can_surrender=False)
    assert action.name == "STAND", f"Expected STAND for 12 vs 4, got {action.name}"
    
    # Test pair of 8s -> Split
    hand = BlackjackHand()
    hand.add_card(Card(Rank.EIGHT, Suit.HEARTS))
    hand.add_card(Card(Rank.EIGHT, Suit.SPADES))
    dealer_upcard = Card(Rank.TEN, Suit.DIAMONDS)
    action, _ = BasicStrategy.get_action(hand, dealer_upcard, can_surrender=False)
    assert action.name == "SPLIT", f"Expected SPLIT for 8s, got {action.name}"
    
    # Test pair of 10s -> Stand
    hand = BlackjackHand()
    hand.add_card(Card(Rank.TEN, Suit.HEARTS))
    hand.add_card(Card(Rank.TEN, Suit.SPADES))
    action, _ = BasicStrategy.get_action(hand, dealer_upcard, can_surrender=False)
    assert action.name == "STAND", f"Expected STAND for 10s, got {action.name}"
    
    # Test hard 9 vs 5 -> Double
    hand = BlackjackHand()
    hand.add_card(Card(Rank.NINE, Suit.HEARTS))
    dealer_upcard = Card(Rank.FIVE, Suit.DIAMONDS)
    action, _ = BasicStrategy.get_action(hand, dealer_upcard, can_surrender=False)
    assert action.name == "DOUBLE", f"Expected DOUBLE for 9 vs 5, got {action.name}"
    
    print("✓ Strategy test passed")


def main():
    """Run all tests"""
    print("Running blackjack game tests...\n")
    
    try:
        test_cards()
        test_deck()
        test_shoe()
        test_hand()
        test_blackjack_hand()
        test_strategy()
        
        print("\n" + "="*50)
        print("All tests passed! ✓")
        print("="*50)
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
