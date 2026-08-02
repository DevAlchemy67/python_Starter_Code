"""
Game Configuration Module
=========================

Centralized configuration for the Pong game.
All game settings, difficulty levels, and themes are defined here.
"""

from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
from enum import Enum
import pygame


class Difficulty(Enum):
    """
    Difficulty levels for the game.
    
    BEGINNER: Slow ball speed, large paddles, easy AI
    INTERMEDIATE: Medium ball speed, normal paddles, balanced AI
    ADVANCED: Fast ball speed, small paddles, aggressive AI
    EXPERT: Very fast ball speed, small paddles, unpredictable AI
    """
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class Theme(Enum):
    """
    Visual themes for the game.
    
    CLASSIC: Traditional black and white Pong
    MODERN: Colorful with gradients
    RETRO: 80s arcade style
    DARK: Dark mode with neon accents
    CUSTOM: User-defined colors
    """
    CLASSIC = "classic"
    MODERN = "modern"
    RETRO = "retro"
    DARK = "dark"
    CUSTOM = "custom"


@dataclass
class ThemeColors:
    """Color scheme for a theme."""
    background: Tuple[int, int, int] = (0, 0, 0)
    paddle: Tuple[int, int, int] = (255, 255, 255)
    ball: Tuple[int, int, int] = (255, 255, 255)
    text: Tuple[int, int, int] = (255, 255, 255)
    border: Tuple[int, int, int] = (100, 100, 100)
    highlight: Tuple[int, int, int] = (200, 200, 200)
    
    def to_dict(self) -> Dict[str, Tuple[int, int, int]]:
        """Convert to dictionary for easy access."""
        return {
            'background': self.background,
            'paddle': self.paddle,
            'ball': self.ball,
            'text': self.text,
            'border': self.border,
            'highlight': self.highlight
        }


# Predefined theme color schemes
THEME_COLORS = {
    Theme.CLASSIC: ThemeColors(
        background=(0, 0, 0),
        paddle=(255, 255, 255),
        ball=(255, 255, 255),
        text=(255, 255, 255),
        border=(100, 100, 100)
    ),
    Theme.MODERN: ThemeColors(
        background=(30, 30, 40),
        paddle=(100, 180, 255),
        ball=(255, 100, 150),
        text=(240, 240, 240),
        border=(80, 80, 100),
        highlight=(150, 200, 255)
    ),
    Theme.RETRO: ThemeColors(
        background=(20, 20, 20),
        paddle=(0, 255, 0),
        ball=(255, 255, 0),
        text=(0, 255, 0),
        border=(80, 80, 80),
        highlight=(100, 255, 100)
    ),
    Theme.DARK: ThemeColors(
        background=(10, 10, 20),
        paddle=(0, 200, 255),
        ball=(255, 50, 200),
        text=(200, 200, 255),
        border=(40, 40, 60),
        highlight=(50, 255, 255)
    )
}


@dataclass
class GameSettings:
    """Individual game settings that can be customized."""
    # Display settings
    screen_width: int = 800
    screen_height: int = 600
    fps: int = 60
    show_fps: bool = False
    
    # Paddle settings
    paddle_width: int = 15
    paddle_height: int = 100
    paddle_speed: float = 8.0
    paddle_margin: int = 20
    
    # Ball settings
    ball_size: int = 15
    ball_speed: float = 5.0
    ball_speed_increase: float = 0.2
    max_ball_speed: float = 15.0
    
    # Game rules
    points_to_win: int = 10
    serve_delay: int = 1000  # milliseconds
    wall_bounce: bool = True
    paddle_bounce_angle: bool = True
    
    # AI settings
    ai_difficulty: Difficulty = Difficulty.INTERMEDIATE
    ai_reaction_time: float = 0.1  # seconds
    ai_error_margin: float = 0.0  # 0-1, higher = more errors
    
    # Visual settings
    theme: Theme = Theme.CLASSIC
    custom_colors: ThemeColors = field(default_factory=ThemeColors)
    draw_center_line: bool = True
    draw_borders: bool = True
    
    # Sound settings
    enable_sound: bool = True
    sound_volume: float = 0.5


@dataclass
class DifficultySettings:
    """Settings for each difficulty level."""
    # Map difficulty to specific settings
    settings_map: Dict[Difficulty, Dict[str, Any]] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize default settings for each difficulty."""
        self.settings_map = {
            Difficulty.BEGINNER: {
                'ball_speed': 4.0,
                'paddle_height': 120,
                'paddle_speed': 6.0,
                'ai_reaction_time': 0.2,
                'ai_error_margin': 0.15,
                'max_ball_speed': 10.0
            },
            Difficulty.INTERMEDIATE: {
                'ball_speed': 6.0,
                'paddle_height': 100,
                'paddle_speed': 8.0,
                'ai_reaction_time': 0.1,
                'ai_error_margin': 0.05,
                'max_ball_speed': 12.0
            },
            Difficulty.ADVANCED: {
                'ball_speed': 8.0,
                'paddle_height': 80,
                'paddle_speed': 10.0,
                'ai_reaction_time': 0.05,
                'ai_error_margin': 0.02,
                'max_ball_speed': 15.0
            },
            Difficulty.EXPERT: {
                'ball_speed': 10.0,
                'paddle_height': 60,
                'paddle_speed': 12.0,
                'ai_reaction_time': 0.02,
                'ai_error_margin': 0.0,
                'max_ball_speed': 18.0
            }
        }
    
    def get_settings(self, difficulty: Difficulty) -> Dict[str, Any]:
        """Get settings for a specific difficulty level."""
        return self.settings_map.get(difficulty, self.settings_map[Difficulty.INTERMEDIATE])


class GameConfig:
    """
    Main configuration class for the Pong game.
    
    This class manages all game settings and provides methods to
    customize the game experience for different skill levels.
    
    Example:
        config = GameConfig()
        config.set_difficulty(Difficulty.ADVANCED)
        config.set_theme(Theme.RETRO)
        config.screen_width = 1024
        config.screen_height = 768
    """
    
    def __init__(self):
        """Initialize with default settings."""
        self.settings = GameSettings()
        self.difficulty_settings = DifficultySettings()
        self._apply_difficulty(Difficulty.INTERMEDIATE)
    
    def set_difficulty(self, difficulty: Difficulty) -> None:
        """
        Set the game difficulty level.
        
        Args:
            difficulty: The difficulty level to set
        """
        self.settings.ai_difficulty = difficulty
        self._apply_difficulty(difficulty)
    
    def set_theme(self, theme: Theme, custom_colors: ThemeColors = None) -> None:
        """
        Set the visual theme for the game.
        
        Args:
            theme: The theme to use
            custom_colors: Optional custom color scheme
        """
        self.settings.theme = theme
        if custom_colors:
            self.settings.custom_colors = custom_colors
    
    def _apply_difficulty(self, difficulty: Difficulty) -> None:
        """Apply difficulty-specific settings."""
        diff_settings = self.difficulty_settings.get_settings(difficulty)
        for key, value in diff_settings.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
    
    def get_colors(self) -> ThemeColors:
        """Get the current color scheme based on theme."""
        if self.settings.theme == Theme.CUSTOM:
            return self.settings.custom_colors
        return THEME_COLORS.get(self.settings.theme, THEME_COLORS[Theme.CLASSIC])
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary for saving/loading."""
        return {
            'screen_width': self.settings.screen_width,
            'screen_height': self.settings.screen_height,
            'fps': self.settings.fps,
            'paddle_width': self.settings.paddle_width,
            'paddle_height': self.settings.paddle_height,
            'paddle_speed': self.settings.paddle_speed,
            'ball_size': self.settings.ball_size,
            'ball_speed': self.settings.ball_speed,
            'points_to_win': self.settings.points_to_win,
            'ai_difficulty': self.settings.ai_difficulty.value,
            'theme': self.settings.theme.value,
            'enable_sound': self.settings.enable_sound,
            'sound_volume': self.settings.sound_volume
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Load settings from dictionary."""
        for key, value in data.items():
            if hasattr(self.settings, key):
                if key == 'ai_difficulty':
                    setattr(self.settings, key, Difficulty(value))
                elif key == 'theme':
                    setattr(self.settings, key, Theme(value))
                else:
                    setattr(self.settings, key, value)
        
        # Re-apply difficulty settings
        self._apply_difficulty(self.settings.ai_difficulty)


# Default configuration instance
default_config = GameConfig()
