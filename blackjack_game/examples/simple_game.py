#!/usr/bin/env python3
"""
Simple Blackjack Game Example

This is a minimal example showing how to use the blackjack game library.
"""

from blackjack_game import BlackjackGame, Player, CLIInterface


def main():
    """Run a simple blackjack game"""
    # Create a game
    game = BlackjackGame()
    
    # Add a player
    player = Player(name="Player 1", bankroll=1000)
    game.add_player(player)
    
    # Start the game
    game.start_game()
    
    # Create CLI interface
    cli = CLIInterface(game)
    
    # Place bet
    game.place_bet(player, 50)
    
    # Deal initial cards
    game.deal_initial_cards()
    
    # Display game state
    cli.display_game_state()
    
    # Simple player strategy: hit until 17 or higher
    while game.phase.name == "PLAYER_TURN":
        current_player = game.get_current_player()
        if not current_player:
            break
        
        hand = current_player.current_hand
        
        if hand.total >= 17:
            # Stand
            game.player_action(current_player, game.players.player.Action.STAND)
        else:
            # Hit
            game.player_action(current_player, game.players.player.Action.HIT)
        
        # Display updated state
        cli.display_game_state()
    
    # Play dealer's turn
    if game.phase.name == "DEALER_TURN":
        game.play_dealer_turn()
        cli.display_game_state()
    
    # Settle bets
    results = game.settle_bets()
    cli.display_results(results)
    cli.display_bankrolls()


if __name__ == "__main__":
    main()
