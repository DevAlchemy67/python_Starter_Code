"""
Examples Module
==============

Contains various examples of how to use the Pong game library.
These examples demonstrate different ways to customize and extend the game.
"""

from .game import PongGame, play_pong
from .config import GameConfig, Difficulty, Theme, ThemeColors
from .entities import Ball, Paddle, ScoreBoard


def example_basic_game():
    """
    Example: Run a basic game with default settings.
    
    This is the simplest way to run the game.
    
    Usage:
        from pong_game.examples import example_basic_game
        example_basic_game()
    """
    print("Running basic Pong game...")
    play_pong()


def example_custom_difficulty():
    """
    Example: Run the game with custom difficulty settings.
    
    This shows how to set different difficulty levels.
    
    Usage:
        from pong_game.examples import example_custom_difficulty
        example_custom_difficulty()
    """
    print("Running Pong game with ADVANCED difficulty...")
    
    config = GameConfig()
    config.set_difficulty(Difficulty.ADVANCED)
    
    play_pong(config)


def example_custom_theme():
    """
    Example: Run the game with a custom theme.
    
    This shows how to change the visual theme.
    
    Usage:
        from pong_game.examples import example_custom_theme
        example_custom_theme()
    """
    print("Running Pong game with RETRO theme...")
    
    config = GameConfig()
    config.set_theme(Theme.RETRO)
    
    play_pong(config)


def example_custom_resolution():
    """
    Example: Run the game with custom screen resolution.
    
    This shows how to change the screen size.
    
    Usage:
        from pong_game.examples import example_custom_resolution
        example_custom_resolution()
    """
    print("Running Pong game with custom resolution...")
    
    config = GameConfig()
    config.settings.screen_width = 1024
    config.settings.screen_height = 768
    
    play_pong(config)


def example_custom_colors():
    """
    Example: Run the game with custom colors.
    
    This shows how to create a custom color scheme.
    
    Usage:
        from pong_game.examples import example_custom_colors
        example_custom_colors()
    """
    print("Running Pong game with custom colors...")
    
    # Create custom color scheme
    custom_colors = ThemeColors(
        background=(20, 40, 60),      # Dark blue background
        paddle=(255, 100, 50),        # Orange paddles
        ball=(255, 255, 0),           # Yellow ball
        text=(255, 255, 255),         # White text
        border=(100, 150, 200),       # Light blue border
        highlight=(255, 200, 100)     # Gold highlight
    )
    
    config = GameConfig()
    config.set_theme(Theme.CUSTOM, custom_colors)
    
    play_pong(config)


def example_beginner_friendly():
    """
    Example: Run the game with beginner-friendly settings.
    
    This creates a game that's easy for beginners to play.
    
    Usage:
        from pong_game.examples import example_beginner_friendly
        example_beginner_friendly()
    """
    print("Running beginner-friendly Pong game...")
    
    config = GameConfig()
    config.set_difficulty(Difficulty.BEGINNER)
    config.set_theme(Theme.CLASSIC)
    config.settings.show_fps = False
    config.settings.points_to_win = 5  # Shorter game
    
    play_pong(config)


def example_expert_challenge():
    """
    Example: Run the game with expert-level challenge.
    
    This creates a very challenging game for advanced players.
    
    Usage:
        from pong_game.examples import example_expert_challenge
        example_expert_challenge()
    """
    print("Running expert-level Pong challenge...")
    
    config = GameConfig()
    config.set_difficulty(Difficulty.EXPERT)
    config.set_theme(Theme.DARK)
    config.settings.points_to_win = 15  # Longer game
    config.settings.show_fps = True
    
    play_pong(config)


def example_two_player():
    """
    Example: Run a two-player game (both human players).
    
    This shows how to set up a game where both paddles are
    controlled by human players.
    
    Usage:
        from pong_game.examples import example_two_player
        example_two_player()
    """
    print("Running two-player Pong game...")
    print("Left player: W/S keys")
    print("Right player: UP/DOWN arrow keys")
    
    config = GameConfig()
    config.settings.ai_difficulty = Difficulty.BEGINNER  # Not used, but set anyway
    
    # Create game with custom initialization
    game = PongGame(config)
    
    # Make right paddle human-controlled
    game.right_paddle.is_ai = False
    
    game.run()


def example_custom_game_settings():
    """
    Example: Run the game with fully customized settings.
    
    This shows how to customize every aspect of the game.
    
    Usage:
        from pong_game.examples import example_custom_game_settings
        example_custom_game_settings()
    """
    print("Running Pong game with custom settings...")
    
    config = GameConfig()
    
    # Customize all settings
    config.settings.screen_width = 1280
    config.settings.screen_height = 720
    config.settings.fps = 120
    config.settings.show_fps = True
    
    config.settings.paddle_width = 20
    config.settings.paddle_height = 120
    config.settings.paddle_speed = 10.0
    config.settings.paddle_margin = 30
    
    config.settings.ball_size = 20
    config.settings.ball_speed = 6.0
    config.settings.ball_speed_increase = 0.3
    config.settings.max_ball_speed = 20.0
    
    config.settings.points_to_win = 11
    config.settings.serve_delay = 1500
    config.settings.wall_bounce = True
    config.settings.paddle_bounce_angle = True
    
    config.set_difficulty(Difficulty.INTERMEDIATE)
    config.set_theme(Theme.MODERN)
    
    config.settings.enable_sound = True
    config.settings.sound_volume = 0.7
    
    play_pong(config)


def example_tournament_settings():
    """
    Example: Run the game with tournament-style settings.
    
    This creates a standardized game suitable for tournaments.
    
    Usage:
        from pong_game.examples import example_tournament_settings
        example_tournament_settings()
    """
    print("Running tournament-style Pong game...")
    
    config = GameConfig()
    
    # Tournament settings
    config.settings.screen_width = 1024
    config.settings.screen_height = 768
    config.settings.fps = 60
    
    config.settings.paddle_width = 15
    config.settings.paddle_height = 100
    config.settings.paddle_speed = 8.0
    
    config.settings.ball_size = 15
    config.settings.ball_speed = 7.0
    config.settings.ball_speed_increase = 0.0  # No speed increase
    config.settings.max_ball_speed = 7.0
    
    config.settings.points_to_win = 11
    config.settings.serve_delay = 1000
    
    config.set_difficulty(Difficulty.INTERMEDIATE)
    config.set_theme(Theme.CLASSIC)
    config.settings.enable_sound = False  # Often disabled in tournaments
    
    play_pong(config)


class CustomPongGame(PongGame):
    """
    Example: Extend the PongGame class to create a custom game.
    
    This demonstrates how to extend the base game class to add
    custom functionality.
    
    Usage:
        from pong_game.examples import CustomPongGame
        game = CustomPongGame()
        game.run()
    """
    
    def __init__(self, config=None):
        """Initialize custom game."""
        super().__init__(config)
        
        # Add custom properties
        self.custom_score_multiplier = 1.0
        self.power_up_active = False
        self.power_up_timer = 0
    
    def _update_game(self, dt):
        """Override game update to add custom logic."""
        # Call parent update
        super()._update_game(dt)
        
        # Add custom power-up logic
        if self.power_up_active:
            self.power_up_timer -= dt
            if self.power_up_timer <= 0:
                self.power_up_active = False
                self.custom_score_multiplier = 1.0
                print("Power-up ended!")
    
    def _check_scoring(self):
        """Override scoring to add custom score multiplier."""
        scored = self.ball.is_out_of_bounds()
        
        if scored == "left":
            # Apply multiplier
            points = int(self.custom_score_multiplier)
            for _ in range(points):
                self.scoreboard.add_point("right")
            self.sound_manager.play('score')
            self._start_serve("left")
        
        elif scored == "right":
            points = int(self.custom_score_multiplier)
            for _ in range(points):
                self.scoreboard.add_point("left")
            self.sound_manager.play('score')
            self._start_serve("right")
    
    def activate_power_up(self, multiplier=2.0, duration=10.0):
        """
        Activate a custom power-up.
        
        Args:
            multiplier: Score multiplier
            duration: Duration in seconds
        """
        self.power_up_active = True
        self.custom_score_multiplier = multiplier
        self.power_up_timer = duration
        print(f"Power-up activated! {multiplier}x score for {duration} seconds")


def example_extended_game():
    """
    Example: Run the extended custom game.
    
    This demonstrates using the CustomPongGame class.
    
    Usage:
        from pong_game.examples import example_extended_game
        example_extended_game()
    """
    print("Running extended Pong game with custom features...")
    
    config = GameConfig()
    config.set_theme(Theme.MODERN)
    
    game = CustomPongGame(config)
    
    # Activate a power-up after 5 seconds
    # In a real implementation, you'd trigger this based on game events
    
    game.run()


# Dictionary of all examples for easy access
EXAMPLES = {
    'basic': example_basic_game,
    'beginner': example_beginner_friendly,
    'intermediate': lambda: play_pong(GameConfig()),
    'advanced': example_expert_challenge,
    'two_player': example_two_player,
    'custom_theme': example_custom_theme,
    'custom_colors': example_custom_colors,
    'tournament': example_tournament_settings,
    'extended': example_extended_game,
}


def run_example(name: str):
    """
    Run a specific example by name.
    
    Args:
        name: Name of the example to run
    
    Usage:
        from pong_game.examples import run_example
        run_example('basic')
        run_example('advanced')
    """
    if name in EXAMPLES:
        EXAMPLES[name]()
    else:
        print(f"Example '{name}' not found. Available examples:")
        for example_name in EXAMPLES.keys():
            print(f"  - {example_name}")


def list_examples():
    """
    List all available examples.
    
    Usage:
        from pong_game.examples import list_examples
        list_examples()
    """
    print("Available Pong Game Examples:")
    print("=" * 40)
    for name, func in EXAMPLES.items():
        print(f"  {name}: {func.__doc__.split(chr(10))[1].strip()}")
    print("=" * 40)
    print("\nTo run an example:")
    print("  from pong_game.examples import run_example")
    print("  run_example('example_name')")
