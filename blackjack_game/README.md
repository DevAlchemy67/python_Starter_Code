# Blackjack Game - Python Starter Code

A comprehensive, well-designed Python implementation of the blackjack card game, suitable for beginners to advanced players.

## Features

### Core Game Features
- ✅ Standard blackjack rules with configurable options
- ✅ Support for multiple players (1-4)
- ✅ Multiple decks (1-8) with automatic reshuffling
- ✅ Complete betting system with min/max limits
- ✅ Dealer follows standard casino rules

### Advanced Gameplay
- ✅ **Splitting pairs** - Split any pair into two separate hands
- ✅ **Doubling down** - Double your bet and receive one more card
- ✅ **Surrender** - Give up half your bet to fold (late surrender)
- ✅ **Insurance** - Bet against dealer blackjack
- ✅ **Blackjack payout** - 3:2 payout for natural blackjack
- ✅ Configurable rules (dealer hits/stands on soft 17, etc.)

### Strategy & Learning
- ✅ **Basic strategy hints** - Get optimal play recommendations
- ✅ **Advanced strategy** - Count-based deviations
- ✅ **Strategy trainer** - Test your knowledge with quizzes
- ✅ **Hand analysis** - Detailed statistics for each hand
- ✅ **Card counting** - Multiple counting systems (Hi-Lo, KO, Omega II)

### User Interface
- ✅ **Colorful CLI** - Easy-to-read terminal interface
- ✅ **Interactive gameplay** - Real-time decision making
- ✅ **Game statistics** - Track wins, losses, and bankroll
- ✅ **Hand history** - Review past rounds

## Installation

```bash
# Clone the repository or copy the blackjack_game folder
cd blackjack_game

# No additional dependencies required (pure Python)
python main.py
```

## Quick Start

### Basic Game
```bash
python main.py --quick
```

This starts a game with:
- 1 player with $1000 bankroll
- 6 decks in the shoe
- Standard rules

### Strategy Trainer
```bash
python main.py --trainer
```

Test your knowledge of basic blackjack strategy with interactive quizzes.

### Custom Game
```bash
python main.py
```

This will guide you through setup:
- Number of players
- Player names and bankrolls
- Game settings (decks, betting limits, rules)

## Project Structure

```
blackjack_game/
├── __init__.py          # Package initialization
├── main.py              # Main entry point
├── README.md            # This file
│
├── core/                # Core game components
│   ├── __init__.py
│   ├── card.py          # Card, Rank, Suit classes
│   ├── deck.py          # Deck and Shoe classes
│   └── hand.py          # Hand and BlackjackHand classes
│
├── players/             # Player-related classes
│   ├── __init__.py
│   ├── player.py        # Player and Dealer classes
│   └── strategy.py      # Strategy classes and trainer
│
├── ui/                  # User interface
│   ├── __init__.py
│   └── cli.py           # Command-line interface
│
├── utils/               # Utility modules
│   ├── __init__.py
│   ├── card_counter.py  # Card counting systems
│   └── stats.py         # Game statistics and analysis
│
└── game.py             # Main game logic
```

## Usage Examples

### Basic Usage

```python
from blackjack_game import BlackjackGame, Player, CLIInterface

# Create a game
game = BlackjackGame()

# Add players
player1 = Player(name="Alice", bankroll=1000)
player2 = Player(name="Bob", bankroll=1000)
game.add_player(player1)
game.add_player(player2)

# Start the game
game.start_game()

# Run CLI interface
cli = CLIInterface(game)
cli.run()
```

### Using Strategy Hints

```python
from blackjack_game import BlackjackGame, Player, BasicStrategy
from blackjack_game.core.card import Card, Rank, Suit

# Create a hand and get strategy advice
hand = BlackjackHand([Card(Rank.TEN, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])
dealer_upcard = Card(Rank.SIX, Suit.CLUBS)

action, explanation = BasicStrategy.get_action(hand, dealer_upcard)
print(f"Recommended: {action} - {explanation}")
# Output: Recommended: Action.STAND - Basic strategy: Stand on hard 17
```

### Card Counting

```python
from blackjack_game import HiLoCounter
from blackjack_game.core.card import Card, Rank, Suit

# Create a counter
counter = HiLoCounter(num_decks=6)

# Update with dealt cards
cards = [
    Card(Rank.TWO, Suit.HEARTS),    # +1
    Card(Rank.KING, Suit.DIAMONDS), # -1
    Card(Rank.FIVE, Suit.CLUBS),    # +1
]

for card in cards:
    counter.update(card)

print(f"Running count: {counter.running_count}")  # +1
print(f"True count: {counter.true_count}")        # ~0.17
print(f"Advice: {counter.get_betting_advice()}")   # "Positive count - increase bet slightly"
```

### Custom Game Settings

```python
from blackjack_game import BlackjackGame, GameSettings

# Create custom settings
settings = GameSettings(
    num_decks=8,
    min_bet=25,
    max_bet=2000,
    allow_splitting=True,
    allow_doubling=True,
    allow_surrender=True,
    dealer_hits_soft_17=True,  # Dealer hits soft 17
    blackjack_payout=1.5
)

# Create game with settings
game = BlackjackGame(settings)
```

## Game Rules

### Standard Rules (Default)
- 6 decks in the shoe
- Dealer stands on all 17s (including soft 17)
- Blackjack pays 3:2
- Minimum bet: $10
- Maximum bet: $500
- Can split any pair up to 4 hands
- Can double down on any two cards
- Late surrender allowed
- Insurance allowed

### Customizable Rules
You can customize the following in `GameSettings`:
- Number of decks (1-8)
- Minimum and maximum bets
- Allow/disallow splitting
- Allow/disallow doubling down
- Allow/disallow doubling after split
- Allow/disallow surrender
- Allow/disallow insurance
- Dealer hits/stands on soft 17
- Blackjack payout ratio
- Maximum number of splits
- Reshuffle threshold

## Strategy Guide

### Basic Strategy
The game includes a complete basic strategy implementation. Here are some key points:

**Hard Hands:**
- 8 or less: Always Hit
- 9: Double vs 3-6, else Hit
- 10: Double vs 2-9, else Hit
- 11: Double vs 2-10, Hit vs Ace
- 12: Stand vs 4-6, Hit otherwise
- 13-16: Stand vs 2-6, Hit vs 7-Ace
- 17+: Always Stand

**Soft Hands (with Ace):**
- A2-A3: Double vs 5-6, else Hit
- A4-A5: Double vs 4-6, else Hit
- A6: Double vs 2-6, else Hit
- A7: Double vs 2-6, Stand vs 7-8, Hit vs 9-Ace
- A8+: Always Stand

**Pairs:**
- Aces, 8s: Always Split
- 2s, 3s: Split vs 4-7
- 4s: Split vs 5-6
- 5s: Never Split (treat as 10)
- 6s: Split vs 2-6
- 7s: Split vs 2-7
- 9s: Split vs 2-6, 8-9
- 10s: Never Split

### Card Counting
The game supports several card counting systems:

1. **Hi-Lo** (Most popular)
   - 2-6: +1
   - 7-9: 0
   - 10-A: -1

2. **KO (Knock-Out)**
   - 2-7: +1
   - 8-9: 0
   - 10-A: -1

3. **Omega II** (Advanced)
   - 2,3,7: +1
   - 4,5,6: +2
   - 8: 0
   - 9: -1
   - 10,A: -2

## API Reference

### Core Classes

#### `Card`
Represents a playing card.

```python
from blackjack_game.core.card import Card, Rank, Suit

card = Card(Rank.ACE, Suit.SPADES)
print(card)  # "A♠"
print(card.value)  # 11
print(card.is_ace)  # True
```

#### `Deck` and `Shoe`
Manage decks and multiple-deck shoes.

```python
from blackjack_game.core.deck import Deck, Shoe

# Single deck
deck = Deck(shuffle=True)
card = deck.deal()

# Multiple decks (shoe)
shoe = Shoe(num_decks=6)
card = shoe.deal()
```

#### `BlackjackHand`
Specialized hand for blackjack.

```python
from blackjack_game.core.hand import BlackjackHand
from blackjack_game.core.card import Card, Rank, Suit

hand = BlackjackHand()
hand.add_card(Card(Rank.ACE, Suit.HEARTS))
hand.add_card(Card(Rank.KING, Suit.DIAMONDS))

print(hand.total)  # 21
print(hand.is_blackjack)  # True
print(hand.is_soft)  # True
```

### Player Classes

#### `Player`
Represents a blackjack player.

```python
from blackjack_game.players.player import Player

player = Player(name="Alice", bankroll=1000)
player.place_bet(50)  # Bet $50
print(player.bankroll)  # 950
```

#### `Dealer`
Represents the dealer.

```python
from blackjack_game.players.player import Dealer

dealer = Dealer()
# Dealer follows house rules automatically
```

### Game Classes

#### `BlackjackGame`
Main game class.

```python
from blackjack_game import BlackjackGame, Player

game = BlackjackGame()
game.add_player(Player(name="Alice", bankroll=1000))
game.start_game()

# Game flow
game.place_bet(game.players[0], 50)
game.deal_initial_cards()
# ... player actions ...
game.play_dealer_turn()
results = game.settle_bets()
```

### Strategy Classes

#### `BasicStrategy`
Get optimal play recommendations.

```python
from blackjack_game.players.strategy import BasicStrategy
from blackjack_game.core.hand import BlackjackHand
from blackjack_game.core.card import Card, Rank, Suit

hand = BlackjackHand([Card(Rank.NINE, Suit.HEARTS), Card(Rank.SEVEN, Suit.DIAMONDS)])
dealer_upcard = Card(Rank.SIX, Suit.CLUBS)

action, explanation = BasicStrategy.get_action(hand, dealer_upcard)
# action = Action.STAND
# explanation = "Basic strategy: Stand on hard 16"
```

#### `AdvancedStrategy`
Count-based strategy with deviations.

```python
from blackjack_game.players.strategy import AdvancedStrategy

action, explanation = AdvancedStrategy.get_action(
    hand, dealer_upcard, true_count=3
)
```

## Testing

Run the included tests:

```bash
python -m pytest tests/ -v
```

Or test manually:

```python
# Test card creation
from blackjack_game.core.card import Card, Rank, Suit

card = Card(Rank.ACE, Suit.HEARTS)
assert card.value == 11
assert card.is_ace == True

# Test hand calculation
from blackjack_game.core.hand import BlackjackHand

hand = BlackjackHand()
hand.add_card(Card(Rank.ACE, Suit.SPADES))
hand.add_card(Card(Rank.SIX, Suit.HEARTS))
assert hand.total == 17
assert hand.is_soft == True

# Test strategy
from blackjack_game.players.strategy import BasicStrategy

hand = BlackjackHand([Card(Rank.TEN, Suit.DIAMONDS), Card(Rank.SEVEN, Suit.CLUBS)])
dealer_upcard = Card(Rank.SIX, Suit.HEARTS)
action, _ = BasicStrategy.get_action(hand, dealer_upcard)
assert action.name == "STAND"
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by standard casino blackjack rules
- Strategy based on mathematically optimal basic strategy
- Card counting systems from blackjack literature

## Resources

- [Blackjack Basic Strategy Chart](https://www.blackjackinfo.com/blackjack-basic-strategy-engine/)
- [Card Counting Guide](https://www.blackjackinfo.com/card-counting/)
- [Blackjack Rules](https://en.wikipedia.org/wiki/Blackjack)

---

**Enjoy the game!** 🎲♠♥♦♣
