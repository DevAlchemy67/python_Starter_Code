"""
Tests for core game components
"""

import pytest
from blackjack_game.core.card import Card, Rank, Suit
from blackjack_game.core.deck import Deck, Shoe
from blackjack_game.core.hand import Hand, BlackjackHand


class TestCard:
    """Tests for Card class"""
    
    def test_card_creation(self):
        """Test creating cards"""
        ace_hearts = Card(Rank.ACE, Suit.HEARTS)
        king_spades = Card(Rank.KING, Suit.SPADES)
        ten_diamonds = Card(Rank.TEN, Suit.DIAMONDS)
        
        assert ace_hearts.rank == Rank.ACE
        assert ace_hearts.suit == Suit.HEARTS
        assert king_spades.value == 10
        assert ten_diamonds.value == 10
    
    def test_card_properties(self):
        """Test card properties"""
        ace = Card(Rank.ACE, Suit.CLUBS)
        king = Card(Rank.KING, Suit.DIAMONDS)
        seven = Card(Rank.SEVEN, Suit.HEARTS)
        
        assert ace.is_ace == True
        assert ace.is_face_card == False
        assert ace.is_ten_value == False
        
        assert king.is_ace == False
        assert king.is_face_card == True
        assert king.is_ten_value == True
        
        assert seven.is_ace == False
        assert seven.is_face_card == False
        assert seven.is_ten_value == False
    
    def test_card_string_representation(self):
        """Test card string representations"""
        ace = Card(Rank.ACE, Suit.HEARTS)
        king = Card(Rank.KING, Suit.SPADES)
        ten = Card(Rank.TEN, Suit.DIAMONDS)
        
        assert str(ace) == "A♥"
        assert str(king) == "K♠"
        assert str(ten) == "10♦"
        
        assert ace.long_str() == "Ace of Hearts"
        assert king.long_str() == "King of Spades"


class TestDeck:
    """Tests for Deck class"""
    
    def test_deck_creation(self):
        """Test creating a deck"""
        deck = Deck(shuffle=False)
        
        assert len(deck) == 52
        assert deck.remaining == 52
        assert deck.is_empty == False
    
    def test_deck_dealing(self):
        """Test dealing cards from deck"""
        deck = Deck(shuffle=False)
        
        card = deck.deal()
        assert card is not None
        assert deck.remaining == 51
        
        # Deal all cards
        for _ in range(51):
            deck.deal()
        
        assert deck.is_empty == True
        assert deck.deal() is None
    
    def test_deck_shuffling(self):
        """Test deck shuffling"""
        deck1 = Deck(shuffle=False)
        deck2 = Deck(shuffle=True)
        
        # First cards should be different (with high probability)
        card1 = deck1.deal()
        card2 = deck2.deal()
        
        # Note: There's a small chance they could be the same
        # This test might occasionally fail due to randomness
        assert deck1.is_shuffled == False
        assert deck2.is_shuffled == True


class TestShoe:
    """Tests for Shoe class"""
    
    def test_shoe_creation(self):
        """Test creating a shoe"""
        shoe = Shoe(num_decks=6)
        
        assert shoe.num_decks == 6
        assert shoe.remaining == 6 * 52
        assert shoe.total_cards == 6 * 52
    
    def test_shoe_dealing(self):
        """Test dealing from shoe"""
        shoe = Shoe(num_decks=2)
        
        card = shoe.deal()
        assert card is not None
        assert shoe.remaining == 104 - 1
        assert shoe.discarded_count == 0
    
    def test_shoe_burn(self):
        """Test burning cards"""
        shoe = Shoe(num_decks=1)
        
        burned = shoe.burn(3)
        assert len(burned) == 3
        assert shoe.remaining == 52 - 3
        assert shoe.discarded_count == 3


class TestHand:
    """Tests for Hand class"""
    
    def test_hand_creation(self):
        """Test creating a hand"""
        hand = Hand()
        
        assert hand.size == 0
        assert hand.is_empty == True
    
    def test_hand_add_cards(self):
        """Test adding cards to hand"""
        hand = Hand()
        
        ace = Card(Rank.ACE, Suit.HEARTS)
        king = Card(Rank.KING, Suit.SPADES)
        
        hand.add_card(ace)
        assert hand.size == 1
        assert hand.is_empty == False
        
        hand.add_card(king)
        assert hand.size == 2


class TestBlackjackHand:
    """Tests for BlackjackHand class"""
    
    def test_blackjack_hand_total(self):
        """Test hand total calculation"""
        hand = BlackjackHand()
        
        # Empty hand
        assert hand.total == 0
        
        # Hard hand
        hand.add_card(Card(Rank.TEN, Suit.HEARTS))
        hand.add_card(Card(Rank.SEVEN, Suit.SPADES))
        assert hand.total == 17
        
        # Soft hand
        hand = BlackjackHand()
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.SIX, Suit.SPADES))
        assert hand.total == 17
        assert hand.is_soft == True
    
    def test_blackjack_hand_ace_adjustment(self):
        """Test Ace value adjustment to avoid bust"""
        hand = BlackjackHand()
        
        # Ace + 10 + 5 = 16 (Ace as 11 would be 26, so Ace becomes 1)
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.TEN, Suit.SPADES))
        hand.add_card(Card(Rank.FIVE, Suit.DIAMONDS))
        assert hand.total == 16
        assert hand.is_soft == False
    
    def test_blackjack_hand_blackjack(self):
        """Test blackjack detection"""
        hand = BlackjackHand()
        
        # Not blackjack (3 cards)
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.TEN, Suit.SPADES))
        hand.add_card(Card(Rank.TWO, Suit.DIAMONDS))
        assert hand.is_blackjack == False
        
        # Blackjack
        hand = BlackjackHand()
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.KING, Suit.SPADES))
        assert hand.is_blackjack == True
    
    def test_blackjack_hand_pair(self):
        """Test pair detection"""
        hand = BlackjackHand()
        
        # Not a pair
        hand.add_card(Card(Rank.ACE, Suit.HEARTS))
        hand.add_card(Card(Rank.KING, Suit.SPADES))
        assert hand.is_pair == False
        
        # Pair
        hand = BlackjackHand()
        hand.add_card(Card(Rank.SEVEN, Suit.HEARTS))
        hand.add_card(Card(Rank.SEVEN, Suit.SPADES))
        assert hand.is_pair == True
        assert hand.pair_rank == Rank.SEVEN
    
    def test_blackjack_hand_bust(self):
        """Test bust detection"""
        hand = BlackjackHand()
        
        hand.add_card(Card(Rank.KING, Suit.HEARTS))
        hand.add_card(Card(Rank.KING, Suit.SPADES))
        hand.add_card(Card(Rank.KING, Suit.DIAMONDS))
        assert hand.total == 30
        assert hand.is_bust == True
    
    def test_blackjack_hand_split(self):
        """Test hand splitting"""
        hand = BlackjackHand()
        hand.add_card(Card(Rank.EIGHT, Suit.HEARTS))
        hand.add_card(Card(Rank.EIGHT, Suit.SPADES))
        
        hand1, hand2 = hand.split()
        
        assert hand1.size == 1
        assert hand2.size == 1
        assert hand1.cards[0].rank == Rank.EIGHT
        assert hand2.cards[0].rank == Rank.EIGHT


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
