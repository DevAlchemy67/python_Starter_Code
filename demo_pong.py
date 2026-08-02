#!/usr/bin/env python3
"""
Demo script for the Pong game starter code.

This script demonstrates various ways to use the Pong game library.
Run this script to see the game in action with different configurations.
"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pong_game import play_pong, GameConfig, Difficulty, Theme
from pong_game.game import PongGame


def demo_basic():
    """Demo: Basic game with default settings."""
    print("\n" + "="*50)
    print("DEMO: Basic Pong Game")
    print("="*50)
    print("Controls:")
    print("  Left Paddle: W (up), S (down)")
    print("  Serve: SPACE")
    print("  Pause: ESC")
    print("  Menu: ESC when paused")
    print("\nPress ENTER to start...")
    input()
    
    play_pong()


def demo_difficulty_levels():
    """Demo: Different difficulty levels."""
    levels = [
        (Difficulty.BEGINNER, "BEGINNER - Easy for new players"),
        (Difficulty.INTERMEDIATE, "INTERMEDIATE - Balanced gameplay"),
        (Difficulty.ADVANCED, "ADVANCED - Fast-paced challenge"),
        (Difficulty.EXPERT, "EXPERT - Very difficult")
    ]
    
    for difficulty, description in levels:
        print("\n" + "="*50)
        print(f"DEMO: {difficulty.value.upper()} Difficulty")
        print(f"Description: {description}")
        print("="*50)
        print("Press ENTER to try this difficulty...")
        input()
        
        config = GameConfig()
        config.set_difficulty(difficulty)
        
        # Create game without sound for demo
        config.settings.enable_sound = False
        
        play_pong(config)


def demo_themes():
    """Demo: Different visual themes."""
    themes = [
        (Theme.CLASSIC, "CLASSIC - Traditional black and white"),
        (Theme.MODERN, "MODERN - Colorful with gradients"),
        (Theme.RETRO, "RETRO - 80s arcade style"),
        (Theme.DARK, "DARK - Dark mode with neon")
    ]
    
    for theme, description in themes:
        print("\n" + "="*50)
        print(f"DEMO: {theme.value.upper()} Theme")
        print(f"Description: {description}")
        print("="*50)
        print("Press ENTER to see this theme...")
        input()
        
        config = GameConfig()
        config.set_theme(theme)
        config.settings.enable_sound = False
        
        play_pong(config)


def demo_two_player():
    """Demo: Two-player mode."""
    print("\n" + "="*50)
    print("DEMO: Two-Player Mode")
    print("="*50)
    print("Controls:")
    print("  Left Player: W (up), S (down)")
    print("  Right Player: UP arrow (up), DOWN arrow (down)")
    print("  Serve: SPACE")
    print("  Pause: ESC")
    print("\nPress ENTER to start...")
    input()
    
    config = GameConfig()
    config.settings.enable_sound = False
    
    game = PongGame(config)
    game.right_paddle.is_ai = False
    game.run()


def demo_custom_settings():
    """Demo: Custom game settings."""
    print("\n" + "="*50)
    print("DEMO: Custom Settings")
    print("="*50)
    print("Custom configuration:")
    print("  Screen: 1024x768")
    print("  Ball Speed: 8.0")
    print("  Paddle Height: 80")
    print("  Points to Win: 15")
    print("  Theme: RETRO")
    print("  Difficulty: ADVANCED")
    print("\nPress ENTER to start...")
    input()
    
    config = GameConfig()
    config.settings.screen_width = 1024
    config.settings.screen_height = 768
    config.settings.ball_speed = 8.0
    config.settings.paddle_height = 80
    config.settings.points_to_win = 15
    config.set_theme(Theme.RETRO)
    config.set_difficulty(Difficulty.ADVANCED)
    config.settings.enable_sound = False
    
    play_pong(config)


def show_menu():
    """Show the demo menu."""
    print("\n" + "="*60)
    print("PONG GAME STARTER CODE - DEMO MENU")
    print("="*60)
    print("Choose a demo to run:")
    print("  1. Basic Game")
    print("  2. Difficulty Levels")
    print("  3. Visual Themes")
    print("  4. Two-Player Mode")
    print("  5. Custom Settings")
    print("  6. Run All Demos")
    print("  0. Exit")
    print("="*60)
    
    while True:
        try:
            choice = input("Enter your choice (0-6): ").strip()
            if choice in ['0', '1', '2', '3', '4', '5', '6']:
                return choice
            else:
                print("Invalid choice. Please enter a number between 0 and 6.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)


def main():
    """Main demo function."""
    print("PONG GAME STARTER CODE")
    print("=" * 40)
    print("A comprehensive Pong game implementation")
    print("for beginners to advanced players")
    print()
    
    while True:
        choice = show_menu()
        
        if choice == '0':
            print("Goodbye!")
            break
        
        elif choice == '1':
            demo_basic()
        
        elif choice == '2':
            demo_difficulty_levels()
        
        elif choice == '3':
            demo_themes()
        
        elif choice == '4':
            demo_two_player()
        
        elif choice == '5':
            demo_custom_settings()
        
        elif choice == '6':
            print("\nRunning all demos...")
            demo_basic()
            demo_difficulty_levels()
            demo_themes()
            demo_two_player()
            demo_custom_settings()


if __name__ == "__main__":
    main()
