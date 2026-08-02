#!/usr/bin/env python3
"""
Test script for the Pong game.

This script tests the basic functionality of the game without
requiring a display (headless testing).
"""

import sys
import os

# Add the parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pong_game.config import GameConfig, Difficulty, Theme, ThemeColors
from pong_game.entities import Ball, Paddle, ScoreBoard


def test_config():
    """Test configuration system."""
    print("Testing configuration...")
    
    # Test default config
    config = GameConfig()
    assert config.settings.screen_width == 800
    assert config.settings.screen_height == 600
    assert config.settings.fps == 60
    
    # Test difficulty settings
    config.set_difficulty(Difficulty.ADVANCED)
    assert config.settings.ai_difficulty == Difficulty.ADVANCED
    
    # Test theme settings
    config.set_theme(Theme.RETRO)
    assert config.settings.theme == Theme.RETRO
    
    # Test custom colors
    custom_colors = ThemeColors(
        background=(20, 20, 20),
        paddle=(0, 255, 0),
        ball=(255, 255, 0)
    )
    config.set_theme(Theme.CUSTOM, custom_colors)
    assert config.settings.theme == Theme.CUSTOM
    
    print("✓ Configuration tests passed")


def test_ball():
    """Test ball entity."""
    print("Testing ball entity...")
    
    # Create ball
    ball = Ball(x=400, y=300, size=15, speed=5.0)
    ball.screen_width = 800
    ball.screen_height = 600
    
    # Test initial position
    assert ball.x == 400
    assert ball.y == 300
    assert ball.size == 15
    assert ball.radius == 7  # size // 2
    
    # Test movement
    initial_x = ball.x
    initial_y = ball.y
    ball.update()
    assert ball.x != initial_x or ball.y != initial_y
    
    # Test reset
    ball.reset("left")
    assert ball.x == 400  # Should reset to center
    assert ball.dx < 0    # Should be moving left
    
    # Test speed increase
    initial_speed = (ball.dx**2 + ball.dy**2)**0.5
    ball.increase_speed(1.0)
    new_speed = (ball.dx**2 + ball.dy**2)**0.5
    assert new_speed > initial_speed
    
    # Test bounce
    ball.dx = 5
    ball.bounce_horizontal()
    assert ball.dx == -5
    
    ball.dy = 3
    ball.bounce_vertical()
    assert ball.dy == -3
    
    print("✓ Ball tests passed")


def test_paddle():
    """Test paddle entity."""
    print("Testing paddle entity...")
    
    # Create paddle
    paddle = Paddle(x=50, y=300, width=15, height=100, speed=8.0)
    paddle.screen_height = 600
    
    # Test initial position
    assert paddle.x == 50
    assert paddle.y == 300
    assert paddle.width == 15
    assert paddle.height == 100
    
    # Test movement
    initial_y = paddle.y
    paddle.move_up()
    assert paddle.y < initial_y
    
    paddle.move_down()
    assert paddle.y > initial_y - 8  # Should move down from reduced position
    
    # Test boundaries
    paddle.y = 0
    paddle.move_up()
    assert paddle.y == 0  # Should not go above 0
    
    paddle.y = 600 - paddle.height
    paddle.move_down()
    assert paddle.y == 600 - paddle.height  # Should not go below bottom
    
    # Test rect
    rect = paddle.get_rect()
    assert rect.x == paddle.x
    assert rect.y == paddle.y
    assert rect.width == paddle.width
    assert rect.height == paddle.height
    
    print("✓ Paddle tests passed")


def test_scoreboard():
    """Test scoreboard entity."""
    print("Testing scoreboard entity...")
    
    # Create scoreboard
    scoreboard = ScoreBoard(points_to_win=10)
    
    # Test initial scores
    assert scoreboard.left_score == 0
    assert scoreboard.right_score == 0
    
    # Test adding points
    scoreboard.add_point("left")
    assert scoreboard.left_score == 1
    
    scoreboard.add_point("right")
    assert scoreboard.right_score == 1
    
    # Test winner
    assert scoreboard.get_winner() is None
    
    for _ in range(9):
        scoreboard.add_point("left")
    
    assert scoreboard.get_winner() == "left"
    
    # Test reset
    scoreboard.reset()
    assert scoreboard.left_score == 0
    assert scoreboard.right_score == 0
    
    print("✓ Scoreboard tests passed")


def test_collision_detection():
    """Test collision detection between ball and paddle."""
    print("Testing collision detection...")
    
    # Create ball and paddle
    ball = Ball(x=400, y=300, size=15, speed=5.0)
    ball.screen_width = 800
    ball.screen_height = 600
    
    paddle = Paddle(x=50, y=250, width=15, height=100, speed=8.0)
    paddle.screen_height = 600
    
    # Position ball to collide with paddle
    ball.x = 60  # Just right of paddle
    ball.y = 300
    ball.dx = -5  # Moving left
    ball.dy = 0
    
    # Check collision
    collision = ball.check_collision_with_paddle(paddle)
    assert collision == True
    
    # Move ball away
    ball.x = 200
    collision = ball.check_collision_with_paddle(paddle)
    assert collision == False
    
    print("✓ Collision detection tests passed")


def test_out_of_bounds():
    """Test out of bounds detection."""
    print("Testing out of bounds detection...")
    
    ball = Ball(x=400, y=300, size=15, speed=5.0)
    ball.screen_width = 800
    ball.screen_height = 600
    
    # Ball in bounds
    assert ball.is_out_of_bounds() is None
    
    # Ball out on left
    ball.x = -10
    assert ball.is_out_of_bounds() == "left"
    
    # Ball out on right
    ball.x = 810
    assert ball.is_out_of_bounds() == "right"
    
    print("✓ Out of bounds tests passed")


def run_all_tests():
    """Run all tests."""
    print("Running Pong Game Tests")
    print("=" * 40)
    
    try:
        test_config()
        test_ball()
        test_paddle()
        test_scoreboard()
        test_collision_detection()
        test_out_of_bounds()
        
        print("=" * 40)
        print("✓ All tests passed!")
        return True
        
    except AssertionError as e:
        print(f"✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
