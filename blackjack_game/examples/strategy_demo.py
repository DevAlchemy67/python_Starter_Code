#!/usr/bin/env python3
"""
Strategy Demo - Demonstrates basic and advanced blackjack strategy
"""

from blackjack_game.core.card import Card, Rank, Suit
from blackjack_game.core.hand import BlackjackHand
from blackjack_game.players.strategy import BasicStrategy, AdvancedStrategy


def demo_basic_strategy():
    """Demonstrate basic blackjack strategy"""
    print("=" * 60)
    print("BASIC BLACKJACK STRATEGY DEMO")
    print("=" * 60)
    print()
    
    # Common scenarios
    scenarios = [
        {
            'name': 'Hard 16 vs Dealer 10',
            'hand': BlackjackHand([Card(Rank.TEN, Suit.HEARTS), Card(Rank.SIX, Suit.SPADES)]),
            'dealer': Card(Rank.TEN, Suit.DIAMONDS),
        },
        {
            'name': 'Soft 17 vs Dealer 6',
            'hand': BlackjackHand([Card(Rank.ACE, Suit.HEARTS), Card(Rank.SIX, Suit.SPADES)]),
            'dealer': Card(Rank.SIX, Suit.DIAMONDS),
        },
        {
            'name': 'Pair of 8s vs Dealer 10',
            'hand': BlackjackHand([Card(Rank.EIGHT, Suit.HEARTS), Card(Rank.EIGHT, Suit.SPADES)]),
            'dealer': Card(Rank.TEN, Suit.DIAMONDS),
        },
        {
            'name': 'Hard 12 vs Dealer 2',
            'hand': BlackjackHand([Card(Rank.TEN, Suit.HEARTS), Card(Rank.TWO, Suit.SPADES)]),
            'dealer': Card(Rank.TWO, Suit.DIAMONDS),
        },
        {
            'name': 'Pair of Aces vs Dealer 7',
            'hand': BlackjackHand([Card(Rank.ACE, Suit.HEARTS), Card(Rank.ACE, Suit.SPADES)]),
            'dealer': Card(Rank.SEVEN, Suit.DIAMONDS),
        },
    ]
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        print(f"  Your hand: {scenario['hand']}")
        print(f"  Dealer shows: {scenario['dealer']}")
        
        action, explanation = BasicStrategy.get_action(
            scenario['hand'], scenario['dealer']
        )
        
        print(f"  Recommended action: {action}")
        print(f"  Explanation: {explanation}")
        print()


def demo_advanced_strategy():
    """Demonstrate advanced strategy with count"""
    print("=" * 60)
    print("ADVANCED STRATEGY DEMO (with card counting)")
    print("=" * 60)
    print()
    
    # Scenario: 16 vs 10
    hand = BlackjackHand([Card(Rank.TEN, Suit.HEARTS), Card(Rank.SIX, Suit.SPADES)])
    dealer = Card(Rank.TEN, Suit.DIAMONDS)
    
    print(f"Scenario: Hard 16 vs Dealer 10")
    print(f"  Your hand: {hand}")
    print(f"  Dealer shows: {dealer}")
    print()
    
    # Show how strategy changes with count
    counts = [-3, -1, 0, 1, 3, 5]
    
    for count in counts:
        action, explanation = AdvancedStrategy.get_action(
            hand, dealer, true_count=count
        )
        
        print(f"  True Count {count:+d}: {action} - {explanation}")
    
    print()


def demo_card_counting():
    """Demonstrate card counting"""
    from blackjack_game.utils.card_counter import HiLoCounter
    
    print("=" * 60)
    print("CARD COUNTING DEMO (Hi-Lo System)")
    print("=" * 60)
    print()
    
    counter = HiLoCounter(num_decks=6)
    
    # Simulate a shoe with various cards
    test_cards = [
        Card(Rank.TWO, Suit.HEARTS),    # +1
        Card(Rank.THREE, Suit.DIAMONDS), # +1
        Card(Rank.FOUR, Suit.CLUBS),    # +1
        Card(Rank.FIVE, Suit.SPADES),   # +1
        Card(Rank.SIX, Suit.HEARTS),    # +1
        Card(Rank.SEVEN, Suit.DIAMONDS), # 0
        Card(Rank.EIGHT, Suit.CLUBS),   # 0
        Card(Rank.NINE, Suit.SPADES),   # 0
        Card(Rank.TEN, Suit.HEARTS),    # -1
        Card(Rank.JACK, Suit.DIAMONDS), # -1
        Card(Rank.QUEEN, Suit.CLUBS),   # -1
        Card(Rank.KING, Suit.SPADES),   # -1
        Card(Rank.ACE, Suit.HEARTS),    # -1
    ]
    
    print("Dealing cards and tracking count:")
    print()
    
    for i, card in enumerate(test_cards, 1):
        counter.update(card)
        print(f"  {i:2d}. {card} - Count: {counter.running_count:+d}, True: {counter.true_count:+d}")
    
    print()
    print(f"Final: {counter}")
    print(f"Betting advice: {counter.get_betting_advice()}")
    print()


def demo_hand_analysis():
    """Demonstrate hand analysis"""
    from blackjack_game.utils.stats import HandAnalyzer
    
    print("=" * 60)
    print("HAND ANALYSIS DEMO")
    print("=" * 60)
    print()
    
    # Analyze different hands
    hands = [
        BlackjackHand([Card(Rank.ACE, Suit.HEARTS), Card(Rank.KING, Suit.SPADES)]),
        BlackjackHand([Card(Rank.TEN, Suit.HEARTS), Card(Rank.SEVEN, Suit.SPADES)]),
        BlackjackHand([Card(Rank.ACE, Suit.HEARTS), Card(Rank.SIX, Suit.SPADES)]),
        BlackjackHand([Card(Rank.KING, Suit.HEARTS), Card(Rank.KING, Suit.SPADES)]),
    ]
    
    dealer_upcard = Card(Rank.SIX, Suit.DIAMONDS)
    
    for hand in hands:
        stats = HandAnalyzer.analyze_hand(hand, dealer_upcard)
        quality = HandAnalyzer.get_hand_quality(hand)
        dealer_strength = HandAnalyzer.get_dealer_strength(dealer_upcard)
        
        print(f"Hand: {hand}")
        print(f"  Total: {stats.total}")
        print(f"  Type: {'Soft' if stats.is_soft else 'Hard'}")
        print(f"  Quality: {quality}")
        print(f"  Bust probability: {stats.bust_probability:.1%}")
        print(f"  Win probability: {stats.win_probability:.1%}")
        print(f"  Dealer strength: {dealer_strength}")
        print()


def main():
    """Run all demos"""
    demo_basic_strategy()
    demo_advanced_strategy()
    demo_card_counting()
    demo_hand_analysis()
    
    print("=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
