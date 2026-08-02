#!/usr/bin/env python3
"""
Blackjack Game - Main Entry Point

A comprehensive Python blackjack game for beginners to advanced players.

Features:
- Standard blackjack rules with configurable options
- Support for multiple players
- Advanced features: splitting, doubling down, surrender, insurance
- Basic and advanced strategy hints
- Card counting systems (Hi-Lo, KO, Omega II)
- Game statistics and analysis
- Strategy trainer mode

Usage:
    python main.py                    # Start interactive game
    python main.py --trainer          # Run strategy trainer
    python main.py --no-colors        # Disable color output
"""

import sys
import argparse
from .ui.cli import CLIInterface
from .game import BlackjackGame, GameSettings
from .players.player import Player, PlayerType
from .players.strategy import StrategyTrainer


def create_default_game() -> BlackjackGame:
    """Create a default game with one player"""
    game = BlackjackGame()
    
    # Add a default player
    player = Player(
        name="Player 1",
        bankroll=1000.0,
        player_type=PlayerType.HUMAN
    )
    game.add_player(player)
    
    return game


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Blackjack Game - A comprehensive Python blackjack implementation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    Start interactive game
  python main.py --trainer          Run strategy trainer
  python main.py --no-colors        Disable color output
  python main.py --quick            Quick start with default settings
        """
    )
    
    parser.add_argument(
        '--trainer', 
        action='store_true', 
        help='Run strategy trainer mode'
    )
    parser.add_argument(
        '--no-colors', 
        action='store_true', 
        help='Disable ANSI color output'
    )
    parser.add_argument(
        '--quick', 
        action='store_true', 
        help='Quick start with default settings'
    )
    parser.add_argument(
        '--players', 
        type=int, 
        default=1,
        help='Number of players (1-4, default: 1)'
    )
    parser.add_argument(
        '--decks', 
        type=int, 
        default=6,
        help='Number of decks in shoe (1-8, default: 6)'
    )
    
    args = parser.parse_args()
    
    # Create game
    if args.quick:
        game = create_default_game()
        game.settings.num_decks = args.decks
        game.shoe = game.shoe.__class__(
            num_decks=args.decks,
            reshuffle_threshold=game.settings.reshuffle_threshold
        )
    else:
        game = BlackjackGame()
    
    # Create CLI interface
    cli = CLIInterface(game=game, use_colors=not args.no_colors)
    
    if args.trainer:
        # Run strategy trainer
        cli.strategy_trainer()
    else:
        # Run main game
        if args.quick:
            # Skip setup and start playing
            cli.game.start_game()
            cli.play_round()
            
            while cli.ask_continue():
                cli.game.new_round()
                cli.play_round()
        else:
            # Normal flow with setup
            cli.run()


if __name__ == "__main__":
    main()
