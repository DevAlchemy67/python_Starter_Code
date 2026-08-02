"""
CLI module - Command-line interface for blackjack
"""

import sys
import time
from typing import Optional, List, Dict, Any
from enum import Enum
from ..game import BlackjackGame, GamePhase, GameSettings
from ..players.player import Player, Dealer, Action, PlayerType
from ..players.strategy import BasicStrategy, AdvancedStrategy, StrategyTrainer
from ..core.card import Card, Rank, Suit
from ..core.hand import BlackjackHand


class Color:
    """ANSI color codes for terminal output"""
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    
    @classmethod
    def disable(cls):
        """Disable color output"""
        cls.BLACK = cls.RED = cls.GREEN = cls.YELLOW = cls.BLUE = \
            cls.MAGENTA = cls.CYAN = cls.WHITE = cls.BOLD = cls.UNDERLINE = cls.RESET = ""


class CLIInterface:
    """
    Command-line interface for the blackjack game.
    Provides a text-based interface for playing blackjack.
    """
    
    def __init__(self, game: Optional[BlackjackGame] = None, 
                 use_colors: bool = True):
        """
        Initialize the CLI interface.
        
        Args:
            game: BlackjackGame instance, or None to create a new one
            use_colors: Whether to use ANSI colors in output
        """
        self.game = game or BlackjackGame()
        self.use_colors = use_colors
        
        if not use_colors:
            Color.disable()
    
    def run(self) -> None:
        """Run the main game loop"""
        self.clear_screen()
        self.display_welcome()
        
        # Setup game
        self.setup_game()
        
        # Main game loop
        while True:
            try:
                self.play_round()
                
                # Check if players want to continue
                if not self.ask_continue():
                    break
                    
                # Start new round
                self.game.new_round()
                
            except KeyboardInterrupt:
                print("\nGame interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"{Color.RED}Error: {e}{Color.RESET}")
                break
        
        self.display_goodbye()
    
    def setup_game(self) -> None:
        """Setup the game with players and settings"""
        # Get number of players
        num_players = self.ask_number("How many players?", 1, 4, default=1)
        
        # Create players
        for i in range(num_players):
            name = self.ask_string(f"Enter name for player {i+1}", default=f"Player {i+1}")
            bankroll = self.ask_number(f"Starting bankroll for {name}", 100, 10000, default=1000)
            
            player = Player(name=name, bankroll=bankroll, player_type=PlayerType.HUMAN)
            self.game.add_player(player)
        
        # Configure settings
        self.configure_settings()
    
    def configure_settings(self) -> None:
        """Configure game settings"""
        print(f"\n{Color.YELLOW}=== Game Settings ==={Color.RESET}")
        
        settings = self.game.settings
        
        # Number of decks
        settings.num_decks = self.ask_number(
            "Number of decks", 1, 8, default=settings.num_decks
        )
        
        # Betting limits
        settings.min_bet = self.ask_number(
            "Minimum bet", 1, 100, default=settings.min_bet
        )
        settings.max_bet = self.ask_number(
            "Maximum bet", settings.min_bet, 5000, default=settings.max_bet
        )
        
        # Rule options
        settings.allow_splitting = self.ask_yes_no(
            "Allow splitting pairs?", default=settings.allow_splitting
        )
        settings.allow_doubling = self.ask_yes_no(
            "Allow doubling down?", default=settings.allow_doubling
        )
        settings.allow_surrender = self.ask_yes_no(
            "Allow surrender?", default=settings.allow_surrender
        )
        settings.allow_insurance = self.ask_yes_no(
            "Allow insurance?", default=settings.allow_insurance
        )
        settings.dealer_hits_soft_17 = self.ask_yes_no(
            "Dealer hits soft 17?", default=settings.dealer_hits_soft_17
        )
        
        # Recreate shoe with new settings
        self.game.shoe = self.game.shoe = self.game.shoe.__class__(
            num_decks=settings.num_decks,
            reshuffle_threshold=settings.reshuffle_threshold
        )
    
    def play_round(self) -> None:
        """Play a single round of blackjack"""
        self.clear_screen()
        
        # Display round info
        print(f"{Color.CYAN}=== Round {self.game.round_number} ==={Color.RESET}")
        print(f"Shoe: {self.game.shoe.remaining} cards remaining")
        print()
        
        # Place bets
        self.place_bets_phase()
        
        # Deal initial cards
        self.game.deal_initial_cards()
        
        # Check for dealer blackjack
        if self.dealer_has_blackjack():
            self.handle_dealer_blackjack()
            return
        
        # Player turns
        self.player_turns_phase()
        
        # Dealer turn
        if self.game.phase == GamePhase.DEALER_TURN:
            self.dealer_turn_phase()
        
        # Settle bets
        results = self.game.settle_bets()
        self.display_results(results)
        
        # Show updated bankrolls
        self.display_bankrolls()
        
        # Pause before next round
        self.ask_string("Press Enter to continue...", default="")
    
    def place_bets_phase(self) -> None:
        """Handle the betting phase"""
        print(f"{Color.YELLOW}=== Place Your Bets ==={Color.RESET}")
        
        for player in self.game.players:
            while True:
                self.display_player_info(player)
                
                min_bet = self.game.settings.min_bet
                max_bet = min(self.game.settings.max_bet, player.bankroll)
                
                if max_bet < min_bet:
                    print(f"{Color.RED}{player.name} cannot afford the minimum bet!{Color.RESET}")
                    bet = 0
                    break
                
                bet = self.ask_number(
                    f"{player.name}, place your bet (${min_bet:.2f}-${max_bet:.2f})",
                    min_bet, max_bet, default=min_bet
                )
                
                if self.game.place_bet(player, bet):
                    print(f"{Color.GREEN}{player.name} bets ${bet:.2f}{Color.RESET}")
                    break
                else:
                    print(f"{Color.RED}Invalid bet. Please try again.{Color.RESET}")
    
    def player_turns_phase(self) -> None:
        """Handle all player turns"""
        print(f"{Color.YELLOW}=== Player Turns ==={Color.RESET}")
        
        while self.game.phase == GamePhase.PLAYER_TURN:
            player = self.game.get_current_player()
            if not player:
                break
            
            self.clear_screen()
            self.display_game_state()
            
            # Play each hand
            for hand_index in range(len(player.hands)):
                hand = player.hands[hand_index]
                
                # Skip busted hands
                if hand.is_bust:
                    print(f"{Color.RED}Hand {hand_index + 1}: {hand} - BUST!{Color.RESET}")
                    continue
                
                # Skip blackjack hands (already handled)
                if hand.is_blackjack:
                    print(f"{Color.GREEN}Hand {hand_index + 1}: {hand} - BLACKJACK!{Color.RESET}")
                    continue
                
                # Display strategy hint
                if self.ask_yes_no("Show strategy hint?", default=False):
                    hint = self.game.get_strategy_hint(player, hand_index)
                    print(f"{Color.BLUE}{hint}{Color.RESET}")
                
                # Get player action
                action = self.get_player_action(player, hand_index)
                
                if action is None:
                    continue
                
                # Execute action
                success = self.game.player_action(player, action, hand_index)
                
                if success:
                    # Show result
                    self.clear_screen()
                    self.display_game_state()
                    
                    # Check if hand busted
                    if hand.is_bust:
                        print(f"{Color.RED}Hand {hand_index + 1}: {hand} - BUST!{Color.RESET}")
                        self.ask_string("Press Enter to continue...", default="")
                        break
                    elif action == Action.STAND:
                        print(f"{Color.YELLOW}Hand {hand_index + 1}: {hand} - Standing{Color.RESET}")
                        self.ask_string("Press Enter to continue...", default="")
                    elif action == Action.DOUBLE:
                        print(f"{Color.YELLOW}Hand {hand_index + 1}: {hand} - Doubled down{Color.RESET}")
                        self.ask_string("Press Enter to continue...", default="")
                        break  # After doubling, must stand
                    elif action == Action.SPLIT:
                        print(f"{Color.YELLOW}Hand {hand_index + 1}: Split into two hands{Color.RESET}")
                        self.ask_string("Press Enter to continue...", default="")
                        # Restart hand processing for this player
                        break
                else:
                    print(f"{Color.RED}Invalid action. Please try again.{Color.RESET}")
    
    def dealer_turn_phase(self) -> None:
        """Handle the dealer's turn"""
        print(f"{Color.YELLOW}=== Dealer's Turn ==={Color.RESET}")
        
        # Reveal hole card
        print(f"Dealer reveals hole card...")
        self.ask_string("Press Enter to continue...", default="")
        
        self.game.play_dealer_turn()
        
        # Display dealer's final hand
        self.clear_screen()
        print(f"{Color.CYAN}Dealer's Hand: {self.game.dealer.current_hand}{Color.RESET}")
        
        if self.game.dealer.current_hand.is_bust:
            print(f"{Color.GREEN}Dealer BUSTS!{Color.RESET}")
        elif self.game.dealer.current_hand.is_blackjack:
            print(f"{Color.RED}Dealer has BLACKJACK!{Color.RESET}")
        else:
            print(f"Dealer stands on {self.game.dealer.current_hand.total}")
        
        self.ask_string("Press Enter to continue...", default="")
    
    def get_player_action(self, player: Player, hand_index: int) -> Optional[Action]:
        """Get action from player"""
        hand = player.hands[hand_index]
        
        # Determine available actions
        actions = [Action.HIT, Action.STAND]
        
        if (self.game.settings.allow_doubling and 
            hand.size == 2 and 
            player.bankroll >= player.current_bet):
            actions.append(Action.DOUBLE)
        
        if (self.game.settings.allow_splitting and 
            hand.is_pair and 
            len(player.hands) < self.game.settings.max_splits and
            player.bankroll >= player.current_bet):
            actions.append(Action.SPLIT)
        
        if (self.game.settings.allow_surrender and 
            hand.size == 2):
            actions.append(Action.SURRENDER)
        
        # Check for insurance (only on first hand, dealer has Ace)
        if (self.game.settings.allow_insurance and 
            hand_index == 0 and 
            self.game.dealer.can_peek and
            self.game.dealer.upcard and 
            self.game.dealer.upcard.is_ace):
            actions.append(Action.INSURANCE)
        
        # Display available actions
        print(f"\n{player.name}'s turn (Hand {hand_index + 1}): {hand}")
        print("Available actions:")
        for i, action in enumerate(actions, 1):
            print(f"  {i}. {action}")
        
        # Get choice
        choice = self.ask_number("Choose action", 1, len(actions))
        return actions[choice - 1]
    
    def dealer_has_blackjack(self) -> bool:
        """Check if dealer has blackjack and handle it"""
        if self.game.dealer.can_peek and self.game.dealer.peek_for_blackjack():
            self.clear_screen()
            print(f"{Color.RED}=== Dealer has BLACKJACK! ==={Color.RESET}")
            print(f"Dealer: {self.game.dealer.upcard}, {self.game.dealer.hole_card}")
            
            # Check each player's hands
            for player in self.game.players:
                for hand in player.hands:
                    if hand.is_blackjack:
                        print(f"{Color.YELLOW}{player.name}: {hand} - PUSH (both have blackjack){Color.RESET}")
                        player.push()
                    else:
                        print(f"{Color.RED}{player.name}: {hand} - LOSE (dealer has blackjack){Color.RESET}")
                        player.lose()
            
            self.game.phase = GamePhase.GAME_OVER
            return True
        
        return False
    
    def handle_dealer_blackjack(self) -> None:
        """Handle the case where dealer has blackjack"""
        # This is called when dealer has blackjack
        # Settle all bets immediately
        results = []
        
        for player in self.game.players:
            for hand in player.hands:
                bet_amount = player.current_bet / len(player.hands) if len(player.hands) > 1 else player.current_bet
                
                if hand.is_blackjack:
                    # Push
                    result = f"{player.name}: {hand} - PUSH"
                    player.push()
                else:
                    # Player loses
                    result = f"{player.name}: {hand} - LOSE"
                    player.lose()
                
                results.append(result)
        
        self.display_results(results)
        self.game.phase = GamePhase.GAME_OVER
    
    def display_game_state(self) -> None:
        """Display the current game state"""
        print(f"{Color.CYAN}=== Round {self.game.round_number} ==={Color.RESET}")
        print(f"Shoe: {self.game.shoe.remaining} cards remaining")
        print()
        
        # Display dealer's hand
        if self.game.dealer.upcard:
            if self.game.phase == GamePhase.PLAYER_TURN:
                print(f"Dealer: {self.game.dealer.upcard}, ?")
            else:
                print(f"Dealer: {self.game.dealer.current_hand}")
        print()
        
        # Display each player's hands
        for player in self.game.players:
            self.display_player_info(player)
            
            for i, hand in enumerate(player.hands):
                hand_prefix = f"  Hand {i+1}"
                if i == player.active_hand_index:
                    hand_prefix += " (Active)"
                
                if hand.is_blackjack:
                    print(f"{hand_prefix}: {hand} - {Color.GREEN}BLACKJACK{Color.RESET}")
                elif hand.is_bust:
                    print(f"{hand_prefix}: {hand} - {Color.RED}BUST{Color.RESET}")
                else:
                    print(f"{hand_prefix}: {hand}")
            
            print()
    
    def display_player_info(self, player: Player) -> None:
        """Display player information"""
        print(f"{Color.YELLOW}{player.name}: ${player.bankroll:.2f}{Color.RESET}")
        if player.current_bet > 0:
            print(f"  Bet: ${player.current_bet:.2f}")
    
    def display_results(self, results: List) -> None:
        """Display round results"""
        print(f"{Color.YELLOW}=== Round Results ==={Color.RESET}")
        
        for result in results:
            if isinstance(result, str):
                print(f"  {result}")
            else:
                # HandResult object
                result_str = {
                    'PLAYER_WIN': f"{Color.GREEN}WIN{Color.RESET}",
                    'PLAYER_LOSE': f"{Color.RED}LOSE{Color.RESET}",
                    'PUSH': f"{Color.YELLOW}PUSH{Color.RESET}",
                    'BLACKJACK': f"{Color.GREEN}BLACKJACK{Color.RESET}",
                    'SURRENDER': f"{Color.YELLOW}SURRENDER{Color.RESET}",
                }.get(result.result.name, result.result.name)
                
                print(f"  {result.hand} - {result_str} (${result.payout:.2f})")
    
    def display_bankrolls(self) -> None:
        """Display all players' bankrolls"""
        print(f"{Color.YELLOW}=== Bankrolls ==={Color.RESET}")
        for player in self.game.players:
            print(f"  {player.name}: ${player.bankroll:.2f}")
        print()
    
    def display_welcome(self) -> None:
        """Display welcome message"""
        print(f"{Color.CYAN}{'='*50}{Color.RESET}")
        print(f"{Color.CYAN}{'BLACKJACK':^50}{Color.RESET}")
        print(f"{Color.CYAN}{'='*50}{Color.RESET}")
        print()
        print("Welcome to Blackjack!")
        print()
        print("Rules:")
        print("  - Beat the dealer by getting closer to 21 without going over")
        print("  - Ace can be 1 or 11")
        print("  - Blackjack (Ace + 10-value card) pays 3:2")
        print("  - Dealer hits on 16 or less, stands on 17 or more")
        print()
    
    def display_goodbye(self) -> None:
        """Display goodbye message"""
        print()
        print(f"{Color.CYAN}{'='*50}{Color.RESET}")
        print("Thanks for playing Blackjack!")
        print(f"{Color.CYAN}{'='*50}{Color.RESET}")
    
    def strategy_trainer(self) -> None:
        """Run the strategy trainer mode"""
        print(f"{Color.CYAN}=== Strategy Trainer ==={Color.RESET}")
        print()
        print("Test your knowledge of basic blackjack strategy!")
        print()
        
        trainer = StrategyTrainer()
        score = 0
        total = 0
        
        while True:
            question = trainer.get_quiz_question()
            
            print(f"Question {total + 1}:")
            print(question['question'])
            print()
            
            # Display options
            print("Options:")
            for i, option in enumerate(question['options'], 1):
                print(f"  {i}. {option}")
            
            # Get answer
            choice = self.ask_number("Your answer", 1, len(question['options']))
            chosen_action = question['options'][choice - 1]
            
            # Check answer
            if chosen_action == question['correct_action']:
                print(f"{Color.GREEN}Correct!{Color.RESET}")
                score += 1
            else:
                print(f"{Color.RED}Incorrect!{Color.RESET}")
                print(f"Correct answer: {question['correct_action']}")
            
            print(f"Explanation: {question['explanation']}")
            print()
            
            total += 1
            
            # Show score
            print(f"Score: {score}/{total} ({score/total*100:.1f}%)")
            print()
            
            # Continue?
            if not self.ask_yes_no("Another question?", default=True):
                break
    
    # Helper methods for user input
    def ask_string(self, prompt: str, default: str = "") -> str:
        """Ask user for a string input"""
        try:
            result = input(f"{prompt} [{default}]: ").strip()
            return result if result else default
        except KeyboardInterrupt:
            raise
    
    def ask_number(self, prompt: str, min_val: float, max_val: float, 
                   default: Optional[float] = None) -> float:
        """Ask user for a number input"""
        while True:
            try:
                result = self.ask_string(f"{prompt} [{min_val}-{max_val}]: ", 
                                        str(default) if default is not None else "")
                if not result and default is not None:
                    return default
                
                value = float(result)
                if min_val <= value <= max_val:
                    return value
                else:
                    print(f"Please enter a number between {min_val} and {max_val}")
            except ValueError:
                print("Please enter a valid number")
    
    def ask_yes_no(self, prompt: str, default: bool = True) -> bool:
        """Ask user for a yes/no input"""
        while True:
            result = self.ask_string(
                f"{prompt} [y/n]: ", 
                "y" if default else "n"
            ).lower()
            
            if result in ['y', 'yes']:
                return True
            elif result in ['n', 'no']:
                return False
            elif not result:
                return default
    
    def ask_continue(self) -> bool:
        """Ask if user wants to continue"""
        return self.ask_yes_no("Play another round?", default=True)
    
    def clear_screen(self) -> None:
        """Clear the terminal screen"""
        # Use ANSI escape code to clear screen
        print("\033[2J\033[H", end="")
    
    def show_stats(self) -> None:
        """Show game statistics"""
        print(f"{Color.YELLOW}=== Game Statistics ==={Color.RESET}")
        
        for player in self.game.players:
            stats = player.get_stats()
            print(f"\n{player.name}:")
            print(f"  Bankroll: ${stats['bankroll']:.2f}")
            print(f"  Wins: {stats['wins']}")
            print(f"  Losses: {stats['losses']}")
            print(f"  Pushes: {stats['pushes']}")
            print(f"  Blackjacks: {stats['blackjacks']}")
            print(f"  Win rate: {stats['win_rate']:.1f}%")
            print(f"  Total hands: {stats['total_hands']}")


def main():
    """Main entry point for the CLI interface"""
    # Parse command line arguments
    import argparse
    
    parser = argparse.ArgumentParser(description='Blackjack Game')
    parser.add_argument('--no-colors', action='store_true', help='Disable color output')
    parser.add_argument('--trainer', action='store_true', help='Run strategy trainer mode')
    
    args = parser.parse_args()
    
    # Create and run interface
    cli = CLIInterface(use_colors=not args.no_colors)
    
    if args.trainer:
        cli.strategy_trainer()
    else:
        cli.run()


if __name__ == "__main__":
    main()
