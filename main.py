from Hangman import HangmanGame

def main():
    """Run the game"""

    should_play_again = True # Flag to control the outer loop

    while should_play_again:
        game = HangmanGame() # Create a NEW game instance for each round
        game.play_game() # Play one round of the game

        # After a game ends, ask to play again
        play_again_choice = input("Do you want to play again? Type 'Y' for yes or 'N' for no: ").lower()
        if play_again_choice != "y": # If it's anything but 'y'
            should_play_again = False
            print("Thanks for playing! Goodbye!")
            
if __name__ == "__main__":
  main()


