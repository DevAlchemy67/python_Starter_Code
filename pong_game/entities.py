"""
Game Entities Module
====================

Contains all the core game entities: Ball, Paddle, ScoreBoard.
These are the building blocks of the Pong game.
"""

import pygame
import random
import math
from typing import Tuple, Optional
from .config import GameConfig, ThemeColors


class Ball:
    """
    The ball entity in Pong.
    
    Handles ball movement, collision detection, and physics.
    
    Attributes:
        x, y: Current position of the ball
        dx, dy: Current velocity of the ball
        size: Diameter of the ball
        color: Color of the ball
        screen_width, screen_height: Dimensions of the play area
    
    Example:
        ball = Ball(x=400, y=300, size=15, speed=5.0)
        ball.update()
        ball.draw(screen)
    """
    
    def __init__(self, x: float, y: float, size: int = 15, 
                 speed: float = 5.0, color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Initialize the ball.
        
        Args:
            x: Initial x position
            y: Initial y position
            size: Diameter of the ball
            speed: Initial speed of the ball
            color: RGB color of the ball
        """
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.color = color
        self.radius = size // 2
        
        # Initialize with random direction
        self.dx = speed * (1 if random.random() > 0.5 else -1)
        self.dy = speed * (random.uniform(-1, 1))
        
        # Ensure minimum vertical movement
        if abs(self.dy) < speed * 0.3:
            self.dy = speed * 0.3 * (1 if self.dy > 0 else -1)
        
        # Screen dimensions (set by game)
        self.screen_width = 800
        self.screen_height = 600
        
        # Maximum speed limit
        self.max_speed = 15.0
        
        # Original speed for resetting
        self.original_speed = speed
    
    def update(self) -> None:
        """Update ball position based on current velocity."""
        self.x += self.dx
        self.y += self.dy
        
        # Keep ball within screen bounds (top and bottom)
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = abs(self.dy)  # Bounce down
        elif self.y + self.radius >= self.screen_height:
            self.y = self.screen_height - self.radius
            self.dy = -abs(self.dy)  # Bounce up
    
    def reset(self, serve_to: str = "random") -> None:
        """
        Reset ball to center with random or specified direction.
        
        Args:
            serve_to: "left", "right", or "random" - which side to serve to
        """
        self.x = self.screen_width // 2
        self.y = self.screen_height // 2
        
        # Reset speed to original
        current_speed = math.sqrt(self.dx**2 + self.dy**2)
        speed_ratio = self.original_speed / current_speed if current_speed > 0 else 1
        
        if serve_to == "left":
            self.dx = -self.original_speed
            self.dy = random.uniform(-self.original_speed, self.original_speed)
        elif serve_to == "right":
            self.dx = self.original_speed
            self.dy = random.uniform(-self.original_speed, self.original_speed)
        else:  # random
            self.dx = self.original_speed * (1 if random.random() > 0.5 else -1)
            self.dy = self.original_speed * random.uniform(-1, 1)
        
        # Ensure minimum vertical movement
        if abs(self.dy) < self.original_speed * 0.3:
            self.dy = self.original_speed * 0.3 * (1 if random.random() > 0.5 else -1)
    
    def increase_speed(self, amount: float = 0.2) -> None:
        """
        Increase ball speed (for progressive difficulty).
        
        Args:
            amount: How much to increase the speed by
        """
        current_speed = math.sqrt(self.dx**2 + self.dy**2)
        if current_speed < self.max_speed:
            # Scale both components proportionally
            scale = (current_speed + amount) / current_speed if current_speed > 0 else 1
            self.dx *= scale
            self.dy *= scale
    
    def bounce_horizontal(self) -> None:
        """Reverse horizontal direction (for paddle/wall collisions)."""
        self.dx = -self.dx
    
    def bounce_vertical(self) -> None:
        """Reverse vertical direction (for paddle/wall collisions)."""
        self.dy = -self.dy
    
    def bounce_paddle(self, paddle_y: float, paddle_height: int, 
                     paddle_bounce_angle: bool = True) -> None:
        """
        Bounce off a paddle with angle based on where it hits.
        
        Args:
            paddle_y: Y position of the paddle
            paddle_height: Height of the paddle
            paddle_bounce_angle: Whether to use angle-based bouncing
        """
        self.dx = -self.dx
        
        if paddle_bounce_angle:
            # Calculate relative position on paddle (0 to 1)
            relative_pos = (self.y - paddle_y) / paddle_height
            
            # Map to angle (-60 to 60 degrees)
            angle = relative_pos * 1.047  # ~60 degrees in radians
            
            # Calculate new direction
            speed = math.sqrt(self.dx**2 + self.dy**2)
            self.dx = speed * math.cos(angle) * (-1 if self.dx < 0 else 1)
            self.dy = speed * math.sin(angle) * (-1 if self.dx < 0 else 1)
            
            # Ensure minimum vertical movement
            if abs(self.dy) < speed * 0.2:
                self.dy = speed * 0.2 * (1 if self.dy > 0 else -1)
    
    def check_collision_with_paddle(self, paddle: 'Paddle') -> bool:
        """
        Check if ball collides with a paddle.
        
        Args:
            paddle: The paddle to check collision with
            
        Returns:
            True if collision detected
        """
        # Check if ball is within paddle's x range
        if (paddle.x <= self.x + self.radius and 
            paddle.x + paddle.width >= self.x - self.radius):
            
            # Check if ball is within paddle's y range
            if (paddle.y <= self.y + self.radius and 
                paddle.y + paddle.height >= self.y - self.radius):
                
                # Additional check: ball must be moving toward paddle
                if (paddle.x < self.screen_width // 2 and self.dx < 0) or \
                   (paddle.x > self.screen_width // 2 and self.dx > 0):
                    return True
        
        return False
    
    def is_out_of_bounds(self) -> Optional[str]:
        """
        Check if ball is out of bounds (scored).
        
        Returns:
            "left" if ball went off left side, "right" if off right side, None otherwise
        """
        if self.x - self.radius <= 0:
            return "left"
        elif self.x + self.radius >= self.screen_width:
            return "right"
        return None
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the ball on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Optional: Add a highlight effect
        highlight_color = tuple(min(c + 50, 255) for c in self.color)
        pygame.draw.circle(screen, highlight_color, 
                          (int(self.x - self.radius * 0.3), 
                           int(self.y - self.radius * 0.3)), 
                          int(self.radius * 0.2))


class Paddle:
    """
    The paddle entity in Pong.
    
    Handles paddle movement, collision, and rendering.
    
    Attributes:
        x, y: Current position of the paddle
        width, height: Dimensions of the paddle
        speed: Movement speed of the paddle
        color: Color of the paddle
        is_ai: Whether this paddle is controlled by AI
    
    Example:
        paddle = Paddle(x=50, y=300, width=15, height=100, speed=8.0)
        paddle.move_up()
        paddle.move_down()
        paddle.draw(screen)
    """
    
    def __init__(self, x: float, y: float, width: int = 15, 
                 height: int = 100, speed: float = 8.0,
                 color: Tuple[int, int, int] = (255, 255, 255),
                 is_ai: bool = False):
        """
        Initialize the paddle.
        
        Args:
            x: Initial x position
            y: Initial y position
            width: Width of the paddle
            height: Height of the paddle
            speed: Movement speed of the paddle
            color: RGB color of the paddle
            is_ai: Whether this paddle is AI-controlled
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.is_ai = is_ai
        
        # Screen dimensions (set by game)
        self.screen_height = 600
        
        # AI properties
        self.target_y = y  # Target position for AI movement
        self.reaction_time = 0.1  # Seconds to react
        self.error_margin = 0.0  # 0-1, chance of making an error
    
    def move_up(self) -> None:
        """Move paddle up."""
        self.y = max(0, self.y - self.speed)
    
    def move_down(self) -> None:
        """Move paddle down."""
        self.y = min(self.screen_height - self.height, self.y + self.speed)
    
    def stop(self) -> None:
        """Stop paddle movement (for keyboard release)."""
        pass  # Paddle stops when keys are released
    
    def update_ai(self, ball: Ball, dt: float) -> None:
        """
        Update AI paddle position based on ball position.
        
        Args:
            ball: The ball to track
            dt: Delta time in seconds
        """
        if not self.is_ai:
            return
        
        # Predict ball position with reaction delay
        predict_time = self.reaction_time
        predicted_y = ball.y + ball.dy * predict_time * 60  # Approximate
        
        # Add some randomness based on error margin
        if self.error_margin > 0 and random.random() < self.error_margin * 0.1:
            predicted_y += random.uniform(-50, 50)
        
        # Target position is the predicted ball y, centered on paddle
        target_center = predicted_y
        self.target_y = target_center - self.height // 2
        
        # Smooth movement toward target
        if self.y < self.target_y:
            self.y = min(self.target_y, self.y + self.speed)
        elif self.y > self.target_y:
            self.y = max(self.target_y, self.y - self.speed)
        
        # Ensure paddle stays within bounds
        self.y = max(0, min(self.screen_height - self.height, self.y))
    
    def get_rect(self) -> pygame.Rect:
        """Get pygame Rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the paddle on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Main paddle rectangle
        pygame.draw.rect(screen, self.color, 
                        (int(self.x), int(self.y), self.width, self.height))
        
        # Add a border effect
        border_color = tuple(max(c - 50, 0) for c in self.color)
        pygame.draw.rect(screen, border_color, 
                        (int(self.x), int(self.y), self.width, self.height), 2)
        
        # Add a highlight on top
        highlight_color = tuple(min(c + 80, 255) for c in self.color)
        pygame.draw.rect(screen, highlight_color,
                        (int(self.x + 2), int(self.y + 2), 
                         self.width - 4, int(self.height * 0.1)))


class ScoreBoard:
    """
    Manages and displays the game score.
    
    Attributes:
        left_score: Score for left player
        right_score: Score for right player
        font: Pygame font for rendering
        color: Color of the text
    
    Example:
        scoreboard = ScoreBoard()
        scoreboard.add_point("left")
        scoreboard.draw(screen)
    """
    
    def __init__(self, points_to_win: int = 10,
                 color: Tuple[int, int, int] = (255, 255, 255)):
        """
        Initialize the scoreboard.
        
        Args:
            points_to_win: Number of points needed to win
            color: RGB color of the text
        """
        self.left_score = 0
        self.right_score = 0
        self.points_to_win = points_to_win
        self.color = color
        self.font = None  # Will be set by game
        self.screen_width = 800
    
    def add_point(self, side: str) -> None:
        """
        Add a point to the specified side.
        
        Args:
            side: "left" or "right"
        """
        if side == "left":
            self.left_score += 1
        elif side == "right":
            self.right_score += 1
    
    def get_winner(self) -> Optional[str]:
        """
        Check if there's a winner.
        
        Returns:
            "left", "right", or None if no winner yet
        """
        if self.left_score >= self.points_to_win:
            return "left"
        elif self.right_score >= self.points_to_win:
            return "right"
        return None
    
    def reset(self) -> None:
        """Reset scores to zero."""
        self.left_score = 0
        self.right_score = 0
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the score on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.font:
            return
        
        # Draw left score
        left_text = self.font.render(str(self.left_score), True, self.color)
        screen.blit(left_text, (self.screen_width // 4 - left_text.get_width() // 2, 20))
        
        # Draw right score
        right_text = self.font.render(str(self.right_score), True, self.color)
        screen.blit(right_text, (self.screen_width * 3 // 4 - right_text.get_width() // 2, 20))
        
        # Draw separator
        separator = self.font.render(":", True, self.color)
        screen.blit(separator, (self.screen_width // 2 - separator.get_width() // 2, 20))
    
    def draw_game_over(self, screen: pygame.Surface, winner: str) -> None:
        """
        Draw game over message.
        
        Args:
            screen: Pygame surface to draw on
            winner: "left" or "right"
        """
        if not self.font:
            return
        
        # Larger font for game over
        game_over_font = pygame.font.Font(None, 72)
        
        if winner == "left":
            text = "LEFT PLAYER WINS!"
        elif winner == "right":
            text = "RIGHT PLAYER WINS!"
        else:
            text = "GAME OVER"
        
        game_over_text = game_over_font.render(text, True, self.color)
        screen.blit(game_over_text, 
                   (self.screen_width // 2 - game_over_text.get_width() // 2,
                    self.screen_height // 2 - game_over_text.get_height() // 2))
        
        # Draw final score
        score_text = self.font.render(f"Final Score: {self.left_score} - {self.right_score}", 
                                     True, self.color)
        screen.blit(score_text,
                   (self.screen_width // 2 - score_text.get_width() // 2,
                    self.screen_height // 2 + 50))


class SoundManager:
    """
    Manages game sounds and audio.
    
    Attributes:
        enabled: Whether sound is enabled
        volume: Volume level (0.0 to 1.0)
    """
    
    def __init__(self, enabled: bool = True, volume: float = 0.5):
        """
        Initialize the sound manager.
        
        Args:
            enabled: Whether to enable sound
            volume: Volume level (0.0 to 1.0)
        """
        self.enabled = enabled
        self.volume = volume
        self.sounds = {}
        
        # Initialize pygame mixer if enabled
        if enabled:
            pygame.mixer.init()
            self._load_sounds()
    
    def _load_sounds(self) -> None:
        """Load all sound effects."""
        # In a real implementation, you would load actual sound files
        # For this starter code, we'll create placeholder sounds
        try:
            # Paddle hit sound
            self.sounds['paddle_hit'] = pygame.mixer.Sound(buffer=self._create_beep(100, 0.1))
            self.sounds['paddle_hit'].set_volume(self.volume * 0.8)
            
            # Wall hit sound
            self.sounds['wall_hit'] = pygame.mixer.Sound(buffer=self._create_beep(200, 0.05))
            self.sounds['wall_hit'].set_volume(self.volume * 0.6)
            
            # Score sound
            self.sounds['score'] = pygame.mixer.Sound(buffer=self._create_beep(400, 0.2))
            self.sounds['score'].set_volume(self.volume * 0.7)
            
        except:
            # If sound loading fails, disable sounds
            self.enabled = False
    
    def _create_beep(self, frequency: int, duration: float) -> bytes:
        """Create a simple beep sound (placeholder)."""
        # This is a very simple placeholder
        # In a real game, you'd use actual sound files
        import numpy as np
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        wave = np.sin(2 * np.pi * frequency * t)
        wave *= 32767 / np.max(np.abs(wave))
        return wave.astype(np.int16).tobytes()
    
    def play(self, sound_name: str) -> None:
        """
        Play a sound effect.
        
        Args:
            sound_name: Name of the sound to play
        """
        if not self.enabled or sound_name not in self.sounds:
            return
        self.sounds[sound_name].play()
    
    def set_volume(self, volume: float) -> None:
        """
        Set the volume level.
        
        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.volume)
    
    def toggle(self) -> None:
        """Toggle sound on/off."""
        self.enabled = not self.enabled
