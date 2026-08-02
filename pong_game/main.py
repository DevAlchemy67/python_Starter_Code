#!/usr/bin/env python3
"""
Main entry point for the Pong game.

This script provides a simple way to run the game with various options.

Usage:
    python main.py                    # Run with default settings
    python main.py --difficulty advanced  # Run with advanced difficulty
    python main.py --theme retro      # Run with retro theme
    python main.py --two-player       # Run two-player mode
    python main.py --help             # Show help
"""

import argparse
import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pong_game import play_pong, GameConfig, Difficulty, Theme
from pong_game.game import PongGame


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Pong Game - A classic arcade game",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          Run with default settings
  python main.py --difficulty expert     Run with expert difficulty
  python main.py --theme dark            Run with dark theme
  python main.py --two-player            Run two-player mode
  python main.py --width 1024 --height 768  Custom resolution
        """
    )
    
    # Difficulty options
    parser.add_argument(
        '--difficulty', '-d',
        choices=['beginner', 'intermediate', 'advanced', 'expert'],
        default='intermediate',
        help='Game difficulty level (default: intermediate)'
    )
    
    # Theme options
    parser.add_argument(
        '--theme', '-t',
        choices=['classic', 'modern', 'retro', 'dark', 'custom'],
        default='classic',
        help='Visual theme (default: classic)'
    )
    
    # Two-player mode
    parser.add_argument(
        '--two-player', '-2',
        action='store_true',
        help='Enable two-player mode (human vs human)'
    )
    
    # Screen dimensions
    parser.add_argument(
        '--width', '-w',
        type=int,
        default=800,
        help='Screen width (default: 800)'
    )
    
    parser.add_argument(
        '--height', '-h',
        type=int,
        default=600,
        help='Screen height (default: 600)'
    )
    
    # FPS
    parser.add_argument(
        '--fps', '-f',
        type=int,
        default=60,
        help='Frames per second (default: 60)'
    )
    
    # Points to win
    parser.add_argument(
        '--points', '-p',
        type=int,
        default=10,
        help='Points needed to win (default: 10)'
    )
    
    # Show FPS
    parser.add_argument(
        '--show-fps',
        action='store_true',
        help='Show FPS counter'
    )
    
    # Disable sound
    parser.add_argument(
        '--no-sound',
        action='store_true',
        help='Disable sound effects'
    )
    
    # List examples
    parser.add_argument(
        '--examples',
        action='store_true',
        help='List available examples and exit'
    )
    
    return parser.parse_args()


def list_examples():
    """List all available examples."""
    from pong_game.examples import list_examples
    list_examples()


def main():
    """Main function to run the game."""
    args = parse_args()
    
    if args.examples:
        list_examples()
        return
    
    # Create configuration
    config = GameConfig()
    
    # Set difficulty
    difficulty_map = {
        'beginner': Difficulty.BEGINNER,
        'intermediate': Difficulty.INTERMEDIATE,
        'advanced': Difficulty.ADVANCED,
        'expert': Difficulty.EXPERT
    }
    config.set_difficulty(difficulty_map[args.difficulty])
    
    # Set theme
    theme_map = {
        'classic': Theme.CLASSIC,
        'modern': Theme.MODERN,
        'retro': Theme.RETRO,
        'dark': Theme.DARK,
        'custom': Theme.CUSTOM
    }
    config.set_theme(theme_map[args.theme])
    
    # Set screen dimensions
    config.settings.screen_width = args.width
    config.settings.screen_height = args.height
    
    # Set FPS
    config.settings.fps = args.fps
    
    # Set points to win
    config.settings.points_to_win = args.points
    
    # Show FPS
    config.settings.show_fps = args.show_fps
    
    # Sound
    config.settings.enable_sound = not args.no_sound
    
    if args.two_player:
        # Run two-player mode
        game = PongGame(config)
        game.right_paddle.is_ai = False
        
        print("Two-Player Mode")
        print("Left player: W (up), S (down)")
        print("Right player: UP arrow (up), DOWN arrow (down)")
        print("Press ESC to pause, SPACE to serve")
        
        game.run()
    else:
        # Run single-player mode
        print(f"Pong Game - Difficulty: {args.difficulty.title()}, Theme: {args.theme.title()}")
        print("Controls: W/S to move, ESC to pause, SPACE to serve")
        
        play_pong(config)


if __name__ == "__main__":
    main()
