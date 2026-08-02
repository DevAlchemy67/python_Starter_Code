"""
Pong Game Starter Code
======================

A comprehensive Pong game implementation designed for beginners to advanced players.
This package provides a clean, modular structure that's easy to understand and extend.

Features:
- Customizable game settings
- Multiple difficulty levels
- Themed UI options
- Extensible architecture
- Clean separation of concerns

Usage:
    from pong_game.game import PongGame
    game = PongGame()
    game.run()
"""

from .game import PongGame
from .config import GameConfig, Difficulty, Theme
from .entities import Ball, Paddle, ScoreBoard

__version__ = "1.0.0"
__all__ = ["PongGame", "GameConfig", "Difficulty", "Theme", "Ball", "Paddle", "ScoreBoard"]
