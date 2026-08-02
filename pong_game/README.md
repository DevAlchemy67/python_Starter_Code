# Pong Game Starter Code

A comprehensive, designable, and functional Pong game implementation for Python, suitable for beginners to advanced players.

## Features

- **Multiple Difficulty Levels**: Beginner, Intermediate, Advanced, Expert
- **Customizable Themes**: Classic, Modern, Retro, Dark, or Custom
- **Extensible Architecture**: Easy to modify and extend
- **Clean Code Structure**: Well-organized, modular design
- **Comprehensive Documentation**: Detailed comments and examples
- **Two-Player Support**: Human vs Human or Human vs AI
- **Customizable Settings**: Adjust every aspect of the game

## Installation

```bash
# Clone the repository or copy the pong_game folder
cd pong_game

# Install dependencies
pip install pygame numpy
```

## Quick Start

### Basic Game

```python
from pong_game import play_pong

# Run with default settings
play_pong()
```

### Custom Difficulty

```python
from pong_game import play_pong, GameConfig, Difficulty

config = GameConfig()
config.set_difficulty(Difficulty.ADVANCED)
play_pong(config)
```

### Custom Theme

```python
from pong_game import play_pong, GameConfig, Theme

config = GameConfig()
config.set_theme(Theme.RETRO)
play_pong(config)
```

## Game Structure

```
pong_game/
├── __init__.py          # Package initialization
├── config.py            # Game configuration and settings
├── entities.py          # Game entities (Ball, Paddle, ScoreBoard, SoundManager)
├── game.py              # Main game class and game loop
├── examples.py          # Usage examples and custom implementations
└── README.md            # This file
```

## Configuration Options

### Difficulty Levels

| Level | Ball Speed | Paddle Size | AI Skill |
|-------|------------|-------------|----------|
| BEGINNER | Slow | Large | Easy |
| INTERMEDIATE | Medium | Normal | Balanced |
| ADVANCED | Fast | Small | Aggressive |
| EXPERT | Very Fast | Very Small | Unpredictable |

### Visual Themes

- **CLASSIC**: Traditional black and white Pong
- **MODERN**: Colorful with gradients
- **RETRO**: 80s arcade style
- **DARK**: Dark mode with neon accents
- **CUSTOM**: User-defined colors

### Customizable Settings

```python
from pong_game import GameConfig

config = GameConfig()

# Display settings
config.settings.screen_width = 1024
config.settings.screen_height = 768
config.settings.fps = 60
config.settings.show_fps = True

# Paddle settings
config.settings.paddle_width = 15
config.settings.paddle_height = 100
config.settings.paddle_speed = 8.0
config.settings.paddle_margin = 20

# Ball settings
config.settings.ball_size = 15
config.settings.ball_speed = 5.0
config.settings.ball_speed_increase = 0.2
config.settings.max_ball_speed = 15.0

# Game rules
config.settings.points_to_win = 10
config.settings.serve_delay = 1000
config.settings.wall_bounce = True
config.settings.paddle_bounce_angle = True

# AI settings
config.set_difficulty(Difficulty.INTERMEDIATE)

# Visual settings
config.set_theme(Theme.MODERN)

# Sound settings
config.settings.enable_sound = True
config.settings.sound_volume = 0.5
```

## Controls

### Default Controls

- **Left Paddle (Player)**: W (up), S (down)
- **Right Paddle (AI)**: Automatically controlled
- **Serve**: SPACE (when ball is out of play)
- **Pause**: ESC
- **Menu Navigation**: UP/DOWN arrows, ENTER

### Two-Player Mode

To enable two-player mode:

```python
from pong_game import PongGame, GameConfig

config = GameConfig()
game = PongGame(config)

# Make right paddle human-controlled
game.right_paddle.is_ai = False

game.run()
```

**Right Paddle Controls**: UP/DOWN arrow keys

## Extending the Game

### Creating Custom Entities

```python
from pong_game.entities import Ball, Paddle

class PowerBall(Ball):
    """Custom ball with special properties."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.power_active = False
    
    def activate_power(self):
        self.power_active = True
        self.speed *= 1.5
    
    def deactivate_power(self):
        self.power_active = False
        self.speed /= 1.5
```

### Creating Custom Game Logic

```python
from pong_game.game import PongGame

class CustomPongGame(PongGame):
    """Custom game with additional features."""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.power_ups = []
    
    def _update_game(self, dt):
        # Call parent update
        super()._update_game(dt)
        
        # Add custom power-up logic
        self._update_power_ups(dt)
    
    def _update_power_ups(self, dt):
        # Custom power-up logic here
        pass
```

## Examples

The `examples.py` file contains various usage examples:

```python
from pong_game.examples import (
    example_basic_game,
    example_custom_difficulty,
    example_custom_theme,
    example_two_player,
    example_custom_game_settings,
    list_examples,
    run_example
)

# Run a specific example
run_example('advanced')

# List all available examples
list_examples()
```

## API Reference

### Main Classes

#### `PongGame`

The main game class that orchestrates everything.

**Methods:**
- `run()`: Start the game loop
- `reset_game()`: Reset the game state

**Attributes:**
- `config`: Game configuration
- `screen`: Pygame display surface
- `ball`: The game ball
- `left_paddle`: Left player paddle
- `right_paddle`: Right player paddle
- `scoreboard`: Game score tracker

#### `GameConfig`

Manages all game settings and configuration.

**Methods:**
- `set_difficulty(difficulty)`: Set game difficulty
- `set_theme(theme, custom_colors=None)`: Set visual theme
- `get_colors()`: Get current color scheme
- `to_dict()`: Export settings to dictionary
- `from_dict(data)`: Load settings from dictionary

#### `Ball`

The ball entity.

**Methods:**
- `update()`: Update ball position
- `reset(serve_to)`: Reset ball to center
- `increase_speed(amount)`: Increase ball speed
- `bounce_horizontal()`: Reverse horizontal direction
- `bounce_vertical()`: Reverse vertical direction
- `bounce_paddle(paddle_y, paddle_height, paddle_bounce_angle)`: Bounce off paddle
- `check_collision_with_paddle(paddle)`: Check collision with paddle
- `is_out_of_bounds()`: Check if ball is out of bounds
- `draw(screen)`: Draw ball on screen

#### `Paddle`

The paddle entity.

**Methods:**
- `move_up()`: Move paddle up
- `move_down()`: Move paddle down
- `stop()`: Stop paddle movement
- `update_ai(ball, dt)`: Update AI paddle position
- `get_rect()`: Get pygame Rect for collision
- `draw(screen)`: Draw paddle on screen

#### `ScoreBoard`

Manages and displays the game score.

**Methods:**
- `add_point(side)`: Add point to specified side
- `get_winner()`: Check if there's a winner
- `reset()`: Reset scores to zero
- `draw(screen)`: Draw score on screen
- `draw_game_over(screen, winner)`: Draw game over message

## Tips for Beginners

1. **Start Simple**: Begin with the basic game and default settings
2. **Experiment**: Try different difficulty levels to find your comfort zone
3. **Modify Settings**: Adjust paddle size and ball speed to make the game easier or harder
4. **Practice**: The AI adapts to your skill level

## Tips for Advanced Players

1. **Master the Angle**: Learn how the ball bounces off the paddle at different positions
2. **Predict Movement**: Anticipate where the ball will go
3. **Control the Game**: Use paddle positioning to control ball direction
4. **Customize**: Create your own themes and difficulty settings
5. **Extend**: Add new features like power-ups, obstacles, or special balls

## Troubleshooting

### Common Issues

**Pygame not installed:**
```bash
pip install pygame
```

**No sound:**
- Check if sound is enabled in settings
- Ensure your system has working audio

**Slow performance:**
- Reduce FPS setting
- Lower screen resolution
- Close other applications

### Getting Help

- Check the documentation in each module
- Look at the examples in `examples.py`
- Experiment with different settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This code is provided as-is for educational and entertainment purposes. Feel free to use, modify, and distribute it according to your needs.

## Acknowledgments

- Inspired by the classic Pong arcade game
- Built with Pygame library
- Designed for learning and fun

---

**Enjoy the game!** 🎮
