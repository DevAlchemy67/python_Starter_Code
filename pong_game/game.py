"""
Main Game Module
===============

Contains the main PongGame class that orchestrates the entire game.
This is the entry point for running the game.
"""

import pygame
import sys
import time
from typing import Optional, Tuple, Dict, Any
from enum import Enum
from .config import GameConfig, Difficulty, Theme, GameSettings
from .entities import Ball, Paddle, ScoreBoard, SoundManager, ThemeColors


class GameState(Enum):
    """Possible game states."""
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    SETTINGS = "settings"


class PongGame:
    """
    Main Pong game class.
    
    This class manages the game loop, handles input, updates game state,
    and renders everything to the screen.
    
    Attributes:
        config: Game configuration
        screen: Pygame display surface
        clock: Pygame clock for FPS control
        state: Current game state
        ball: The game ball
        left_paddle: Left player paddle
        right_paddle: Right player paddle
        scoreboard: Game score tracker
        sound_manager: Audio manager
    
    Example:
        game = PongGame()
        game.run()
    
    For custom configuration:
        config = GameConfig()
        config.set_difficulty(Difficulty.ADVANCED)
        config.set_theme(Theme.RETRO)
        game = PongGame(config)
        game.run()
    """
    
    def __init__(self, config: Optional[GameConfig] = None):
        """
        Initialize the Pong game.
        
        Args:
            config: Optional game configuration. If None, uses default config.
        """
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption("Pong Game")
        
        # Set up configuration
        self.config = config or GameConfig()
        self.settings = self.config.settings
        
        # Create display
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        
        # Clock for FPS control
        self.clock = pygame.Clock()
        
        # Game state
        self.state = GameState.MENU
        self.running = True
        
        # Initialize game entities
        self._initialize_entities()
        
        # Sound manager
        self.sound_manager = SoundManager(
            enabled=self.settings.enable_sound,
            volume=self.settings.sound_volume
        )
        
        # Menu and UI
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.font_tiny = pygame.font.Font(None, 24)
        
        # Scoreboard font
        self.scoreboard.font = self.font_medium
        self.scoreboard.screen_width = self.settings.screen_width
        self.scoreboard.screen_height = self.settings.screen_height
        
        # Set screen dimensions for entities
        self.ball.screen_width = self.settings.screen_width
        self.ball.screen_height = self.settings.screen_height
        self.ball.max_speed = self.settings.max_ball_speed
        
        self.left_paddle.screen_height = self.settings.screen_height
        self.right_paddle.screen_height = self.settings.screen_height
        
        # Colors from theme
        self.colors = self.config.get_colors()
        
        # Serve timer
        self.serve_timer = 0
        self.serve_start_time = 0
        self.serve_to = "random"
        
        # Menu selection
        self.menu_selection = 0
        self.menu_items = ["Play Game", "Difficulty", "Theme", "Settings", "Quit"]
        
        # Settings menu
        self.settings_selection = 0
        self.settings_items = [
            "Screen Size", "Ball Speed", "Paddle Size", 
            "Points to Win", "Sound", "Back"
        ]
        
        # Difficulty selection
        self.difficulty_selection = 0
        self.difficulty_items = [
            Difficulty.BEGINNER, Difficulty.INTERMEDIATE,
            Difficulty.ADVANCED, Difficulty.EXPERT
        ]
        
        # Theme selection
        self.theme_selection = 0
        self.theme_items = [
            Theme.CLASSIC, Theme.MODERN, Theme.RETRO, Theme.DARK, Theme.CUSTOM
        ]
        
        # FPS display
        self.last_time = time.time()
        self.fps = 0
        self.frame_count = 0
    
    def _initialize_entities(self) -> None:
        """Initialize all game entities."""
        colors = self.config.get_colors()
        
        # Create ball
        self.ball = Ball(
            x=self.settings.screen_width // 2,
            y=self.settings.screen_height // 2,
            size=self.settings.ball_size,
            speed=self.settings.ball_speed,
            color=colors.ball
        )
        
        # Create paddles
        self.left_paddle = Paddle(
            x=self.settings.paddle_margin,
            y=self.settings.screen_height // 2 - self.settings.paddle_height // 2,
            width=self.settings.paddle_width,
            height=self.settings.paddle_height,
            speed=self.settings.paddle_speed,
            color=colors.paddle,
            is_ai=False  # Left paddle is player-controlled
        )
        
        self.right_paddle = Paddle(
            x=self.settings.screen_width - self.settings.paddle_margin - self.settings.paddle_width,
            y=self.settings.screen_height // 2 - self.settings.paddle_height // 2,
            width=self.settings.paddle_width,
            height=self.settings.paddle_height,
            speed=self.settings.paddle_speed,
            color=colors.paddle,
            is_ai=True  # Right paddle is AI-controlled
        )
        
        # Set AI properties from difficulty
        diff_settings = self.config.difficulty_settings.get_settings(self.settings.ai_difficulty)
        self.right_paddle.reaction_time = diff_settings.get('ai_reaction_time', 0.1)
        self.right_paddle.error_margin = diff_settings.get('ai_error_margin', 0.0)
        
        # Create scoreboard
        self.scoreboard = ScoreBoard(
            points_to_win=self.settings.points_to_win,
            color=colors.text
        )
    
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            # Calculate delta time
            now = time.time()
            dt = now - self.last_time
            self.last_time = now
            
            # Handle events
            self._handle_events()
            
            # Update game state
            self._update(dt)
            
            # Render
            self._render()
            
            # Cap FPS
            self.clock.tick(self.settings.fps)
            
            # Update FPS counter
            self.frame_count += 1
            if now - self.last_time > 1.0:
                self.fps = self.frame_count
                self.frame_count = 0
                self.last_time = now
    
    def _handle_events(self) -> None:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            
            elif event.type == pygame.KEYUP:
                self._handle_keyup(event.key)
    
    def _handle_keydown(self, key: int) -> None:
        """Handle key press events."""
        if self.state == GameState.MENU:
            self._handle_menu_keydown(key)
        
        elif self.state == GameState.PLAYING:
            self._handle_game_keydown(key)
        
        elif self.state == GameState.PAUSED:
            self._handle_paused_keydown(key)
        
        elif self.state == GameState.GAME_OVER:
            self._handle_game_over_keydown(key)
        
        elif self.state == GameState.SETTINGS:
            self._handle_settings_keydown(key)
    
    def _handle_keyup(self, key: int) -> None:
        """Handle key release events."""
        if self.state == GameState.PLAYING:
            if key == pygame.K_w:
                self.left_paddle.stop()
            elif key == pygame.K_s:
                self.left_paddle.stop()
    
    def _handle_menu_keydown(self, key: int) -> None:
        """Handle key presses in the menu."""
        if key == pygame.K_UP:
            self.menu_selection = (self.menu_selection - 1) % len(self.menu_items)
            self.sound_manager.play('paddle_hit')
        
        elif key == pygame.K_DOWN:
            self.menu_selection = (self.menu_selection + 1) % len(self.menu_items)
            self.sound_manager.play('paddle_hit')
        
        elif key == pygame.K_RETURN:
            self._select_menu_item()
        
        elif key == pygame.K_ESCAPE:
            self.running = False
    
    def _handle_game_keydown(self, key: int) -> None:
        """Handle key presses during gameplay."""
        if key == pygame.K_w:
            self.left_paddle.move_up()
        
        elif key == pygame.K_s:
            self.left_paddle.move_down()
        
        elif key == pygame.K_UP:
            # Optional: Allow right paddle to be player-controlled
            if not self.right_paddle.is_ai:
                self.right_paddle.move_up()
        
        elif key == pygame.K_DOWN:
            if not self.right_paddle.is_ai:
                self.right_paddle.move_down()
        
        elif key == pygame.K_ESCAPE:
            self.state = GameState.PAUSED
        
        elif key == pygame.K_SPACE:
            # Serve the ball if it's not in play
            if self.serve_timer > 0:
                self.serve_timer = 0
    
    def _handle_paused_keydown(self, key: int) -> None:
        """Handle key presses when paused."""
        if key == pygame.K_ESCAPE:
            self.state = GameState.PLAYING
        
        elif key == pygame.K_m:
            self.state = GameState.MENU
            self._reset_game()
    
    def _handle_game_over_keydown(self, key: int) -> None:
        """Handle key presses when game is over."""
        if key == pygame.K_RETURN or key == pygame.K_SPACE:
            self._reset_game()
            self.state = GameState.PLAYING
        
        elif key == pygame.K_ESCAPE:
            self.state = GameState.MENU
            self._reset_game()
    
    def _handle_settings_keydown(self, key: int) -> None:
        """Handle key presses in settings menu."""
        if key == pygame.K_UP:
            self.settings_selection = (self.settings_selection - 1) % len(self.settings_items)
        
        elif key == pygame.K_DOWN:
            self.settings_selection = (self.settings_selection + 1) % len(self.settings_items)
        
        elif key == pygame.K_RETURN:
            self._select_settings_item()
        
        elif key == pygame.K_ESCAPE:
            self.state = GameState.MENU
    
    def _select_menu_item(self) -> None:
        """Handle menu item selection."""
        item = self.menu_items[self.menu_selection]
        
        if item == "Play Game":
            self.state = GameState.PLAYING
            self._reset_game()
        
        elif item == "Difficulty":
            self.state = GameState.SETTINGS
            # Temporarily change settings items for difficulty
            self.settings_items = [d.value.title() for d in self.difficulty_items]
            self.settings_selection = self.difficulty_items.index(self.settings.ai_difficulty)
        
        elif item == "Theme":
            self.state = GameState.SETTINGS
            self.settings_items = [t.value.title() for t in self.theme_items]
            self.settings_selection = self.theme_items.index(self.settings.theme)
        
        elif item == "Settings":
            self.state = GameState.SETTINGS
            self.settings_items = [
                "Screen Size", "Ball Speed", "Paddle Size", 
                "Points to Win", "Sound", "Back"
            ]
            self.settings_selection = 0
        
        elif item == "Quit":
            self.running = False
    
    def _select_settings_item(self) -> None:
        """Handle settings item selection."""
        # Check if we're in difficulty or theme selection
        if all(item in [d.value.title() for d in self.difficulty_items] for item in self.settings_items):
            selected_difficulty = self.difficulty_items[self.settings_selection]
            self.config.set_difficulty(selected_difficulty)
            self._initialize_entities()  # Reinitialize with new difficulty
            self.state = GameState.MENU
            return
        
        if all(item in [t.value.title() for t in self.theme_items] for item in self.settings_items):
            selected_theme = self.theme_items[self.settings_selection]
            self.config.set_theme(selected_theme)
            self.colors = self.config.get_colors()
            self._initialize_entities()  # Reinitialize with new theme
            self.state = GameState.MENU
            return
        
        # Regular settings
        item = self.settings_items[self.settings_selection]
        
        if item == "Screen Size":
            # Toggle between common resolutions
            resolutions = [
                (800, 600),
                (1024, 768),
                (1280, 720)
            ]
            current_index = resolutions.index(
                (self.settings.screen_width, self.settings.screen_height)
            ) if (self.settings.screen_width, self.settings.screen_height) in resolutions else 0
            next_index = (current_index + 1) % len(resolutions)
            self.settings.screen_width, self.settings.screen_height = resolutions[next_index]
            
            # Recreate display
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )
            self._initialize_entities()
        
        elif item == "Ball Speed":
            self.settings.ball_speed = min(self.settings.ball_speed + 1, 15)
            self.ball.speed = self.settings.ball_speed
        
        elif item == "Paddle Size":
            self.settings.paddle_height = min(self.settings.paddle_height + 10, 200)
            self._initialize_entities()
        
        elif item == "Points to Win":
            self.settings.points_to_win = min(self.settings.points_to_win + 1, 21)
            self.scoreboard.points_to_win = self.settings.points_to_win
        
        elif item == "Sound":
            self.settings.enable_sound = not self.settings.enable_sound
            self.sound_manager.enabled = self.settings.enable_sound
        
        elif item == "Back":
            self.state = GameState.MENU
    
    def _update(self, dt: float) -> None:
        """Update game state."""
        if self.state == GameState.PLAYING:
            self._update_game(dt)
        elif self.state == GameState.PAUSED:
            pass  # Game is paused
        elif self.state == GameState.GAME_OVER:
            pass  # Waiting for input
    
    def _update_game(self, dt: float) -> None:
        """Update game logic during gameplay."""
        # Update serve timer
        if self.serve_timer > 0:
            if time.time() - self.serve_start_time >= self.settings.serve_delay / 1000:
                self.serve_timer = 0
                self.ball.reset(self.serve_to)
            return
        
        # Update ball
        self.ball.update()
        
        # Update AI paddle
        self.right_paddle.update_ai(self.ball, dt)
        
        # Check collisions
        self._check_collisions()
        
        # Check for scoring
        self._check_scoring()
        
        # Check for game over
        winner = self.scoreboard.get_winner()
        if winner:
            self.state = GameState.GAME_OVER
    
    def _check_collisions(self) -> None:
        """Check for collisions between ball and paddles/walls."""
        colors = self.config.get_colors()
        
        # Check left paddle collision
        if self.ball.check_collision_with_paddle(self.left_paddle):
            self.ball.bounce_paddle(
                self.left_paddle.y, self.left_paddle.height,
                self.settings.paddle_bounce_angle
            )
            self.sound_manager.play('paddle_hit')
            self.ball.increase_speed(self.settings.ball_speed_increase)
        
        # Check right paddle collision
        if self.ball.check_collision_with_paddle(self.right_paddle):
            self.ball.bounce_paddle(
                self.right_paddle.y, self.right_paddle.height,
                self.settings.paddle_bounce_angle
            )
            self.sound_manager.play('paddle_hit')
            self.ball.increase_speed(self.settings.ball_speed_increase)
        
        # Check wall collisions (top and bottom)
        if self.settings.wall_bounce:
            if self.ball.y - self.ball.radius <= 0 or \
               self.ball.y + self.ball.radius >= self.settings.screen_height:
                self.ball.bounce_vertical()
                self.sound_manager.play('wall_hit')
    
    def _check_scoring(self) -> None:
        """Check if ball has scored and update scores."""
        scored = self.ball.is_out_of_bounds()
        
        if scored == "left":
            # Ball went off left side, right player scores
            self.scoreboard.add_point("right")
            self.sound_manager.play('score')
            self._start_serve("left")
        
        elif scored == "right":
            # Ball went off right side, left player scores
            self.scoreboard.add_point("left")
            self.sound_manager.play('score')
            self._start_serve("right")
    
    def _start_serve(self, serve_to: str = "random") -> None:
        """Start a new serve."""
        self.serve_to = serve_to
        self.serve_timer = 1
        self.serve_start_time = time.time()
        self.ball.reset(serve_to)
    
    def _reset_game(self) -> None:
        """Reset the game to initial state."""
        self.scoreboard.reset()
        self._start_serve("random")
        
        # Reset paddles to center
        self.left_paddle.y = self.settings.screen_height // 2 - self.settings.paddle_height // 2
        self.right_paddle.y = self.settings.screen_height // 2 - self.settings.paddle_height // 2
        
        # Reset ball speed
        self.ball.speed = self.settings.ball_speed
        self.ball.dx = self.settings.ball_speed * (1 if random.random() > 0.5 else -1)
        self.ball.dy = self.settings.ball_speed * random.uniform(-1, 1)
    
    def _render(self) -> None:
        """Render the game."""
        colors = self.config.get_colors()
        
        # Fill background
        self.screen.fill(colors.background)
        
        if self.state == GameState.MENU:
            self._render_menu()
        
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            self._render_game()
            
            if self.state == GameState.PAUSED:
                self._render_pause_overlay()
        
        elif self.state == GameState.GAME_OVER:
            self._render_game()
            self._render_game_over()
        
        elif self.state == GameState.SETTINGS:
            self._render_settings()
        
        # Draw FPS if enabled
        if self.settings.show_fps:
            fps_text = self.font_tiny.render(f"FPS: {int(self.clock.get_fps())}", True, colors.text)
            self.screen.blit(fps_text, (10, 10))
        
        # Update display
        pygame.display.flip()
    
    def _render_game(self) -> None:
        """Render the game elements."""
        colors = self.config.get_colors()
        
        # Draw borders if enabled
        if self.settings.draw_borders:
            pygame.draw.rect(self.screen, colors.border,
                           (0, 0, self.settings.screen_width, self.settings.screen_height), 2)
        
        # Draw center line if enabled
        if self.settings.draw_center_line:
            for i in range(0, self.settings.screen_height, 30):
                pygame.draw.rect(self.screen, colors.border,
                               (self.settings.screen_width // 2 - 2, i, 4, 20))
        
        # Draw entities
        self.ball.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.scoreboard.draw(self.screen)
        
        # Draw serve message if ball is being served
        if self.serve_timer > 0:
            serve_text = self.font_medium.render("Press SPACE to serve", True, colors.text)
            self.screen.blit(serve_text,
                           (self.settings.screen_width // 2 - serve_text.get_width() // 2,
                            self.settings.screen_height // 2 - serve_text.get_height() // 2))
    
    def _render_menu(self) -> None:
        """Render the main menu."""
        colors = self.config.get_colors()
        
        # Title
        title_text = self.font_large.render("PONG GAME", True, colors.text)
        self.screen.blit(title_text,
                        (self.settings.screen_width // 2 - title_text.get_width() // 2, 100))
        
        # Subtitle
        subtitle_text = self.font_small.render("Beginner to Advanced", True, colors.highlight)
        self.screen.blit(subtitle_text,
                        (self.settings.screen_width // 2 - subtitle_text.get_width() // 2, 160))
        
        # Menu items
        for i, item in enumerate(self.menu_items):
            color = colors.highlight if i == self.menu_selection else colors.text
            item_text = self.font_medium.render(item, True, color)
            self.screen.blit(item_text,
                           (self.settings.screen_width // 2 - item_text.get_width() // 2,
                            250 + i * 50))
        
        # Instructions
        instructions_text = self.font_tiny.render("Use UP/DOWN arrows and ENTER", True, colors.text)
        self.screen.blit(instructions_text,
                        (self.settings.screen_width // 2 - instructions_text.get_width() // 2, 500))
    
    def _render_pause_overlay(self) -> None:
        """Render pause overlay."""
        colors = self.config.get_colors()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.font_large.render("PAUSED", True, colors.text)
        self.screen.blit(pause_text,
                        (self.settings.screen_width // 2 - pause_text.get_width() // 2,
                         self.settings.screen_height // 2 - pause_text.get_height() // 2))
        
        # Instructions
        instructions_text = self.font_small.render("Press ESC to resume", True, colors.highlight)
        self.screen.blit(instructions_text,
                        (self.settings.screen_width // 2 - instructions_text.get_width() // 2,
                         self.settings.screen_height // 2 + 50))
    
    def _render_game_over(self) -> None:
        """Render game over screen."""
        colors = self.config.get_colors()
        
        # Semi-transparent overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text from scoreboard
        winner = self.scoreboard.get_winner()
        self.scoreboard.draw_game_over(self.screen, winner)
        
        # Instructions
        instructions_text = self.font_small.render("Press ENTER to play again or ESC for menu", 
                                                   True, colors.highlight)
        self.screen.blit(instructions_text,
                        (self.settings.screen_width // 2 - instructions_text.get_width() // 2,
                         self.settings.screen_height // 2 + 100))
    
    def _render_settings(self) -> None:
        """Render settings menu."""
        colors = self.config.get_colors()
        
        # Title
        title_text = self.font_large.render("SETTINGS", True, colors.text)
        self.screen.blit(title_text,
                        (self.settings.screen_width // 2 - title_text.get_width() // 2, 100))
        
        # Settings items
        for i, item in enumerate(self.settings_items):
            color = colors.highlight if i == self.settings_selection else colors.text
            item_text = self.font_medium.render(item, True, color)
            
            # Add current value for some settings
            if item == "Screen Size":
                item += f" ({self.settings.screen_width}x{self.settings.screen_height})"
            elif item == "Ball Speed":
                item += f" ({self.settings.ball_speed})"
            elif item == "Paddle Size":
                item += f" ({self.settings.paddle_height})"
            elif item == "Points to Win":
                item += f" ({self.settings.points_to_win})"
            elif item == "Sound":
                item += f" ({'ON' if self.settings.enable_sound else 'OFF'})"
            
            item_text = self.font_medium.render(item, True, color)
            self.screen.blit(item_text,
                           (self.settings.screen_width // 2 - item_text.get_width() // 2,
                            200 + i * 50))
        
        # Instructions
        instructions_text = self.font_tiny.render("Use UP/DOWN arrows, ENTER to select, ESC to go back", 
                                                   True, colors.text)
        self.screen.blit(instructions_text,
                        (self.settings.screen_width // 2 - instructions_text.get_width() // 2, 500))


# Convenience function to run the game
def play_pong(config: Optional[GameConfig] = None) -> None:
    """
    Convenience function to create and run a Pong game.
    
    Args:
        config: Optional game configuration
    
    Example:
        from pong_game import play_pong
        play_pong()
    
    For custom configuration:
        from pong_game import play_pong, GameConfig, Difficulty, Theme
        config = GameConfig()
        config.set_difficulty(Difficulty.ADVANCED)
        config.set_theme(Theme.RETRO)
        play_pong(config)
    """
    game = PongGame(config)
    game.run()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    # Run the game if this file is executed directly
    play_pong()
