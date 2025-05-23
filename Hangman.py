import random
from hangman_words import word_list
from art import stages

class HangmanGame:
  def __init__(self):
    self.word_list = word_list # Make the word list available to the class
    self.secret_word = self.generate_secret_word() # The word to guess
    self.display = ["_"] * len(self.secret_word) # What the user sees (e.g., "_ _ _")
    self.lives = 6 # Number of incorrect guesses allowed (corresponds to 'stages')
    self.guessed_letters = [] # To keep track of letters already tried
    self.game_over = False # A flag to control the main game loop
  
  
  def generate_secret_word(self):
    """ Generate random word"""
    return random.choice(self.word_list).lower()
  
  
  def user_guess(self):
    """get and validae user input"""
    while True:
      guess = input("Guess a letter: ").lower()
      if not guess.isalpha() or len(guess) != 1:
        print("Invalid input. Please enter a single letter.")
      elif guess in self.guessed_letters:
        print(f"You already guessed '{guess}'. Try again")
      else:
        self.guessed_letters.append(guess)
        return guess
  
  
  def check_guess(self,guess):
    """ check guess against random word in diff file"""
    if guess in self.secret_word:
      print(f"Good guess! '{guess}' is in the word")
      for position in range(len(self.secret_word)):
        letter = self.secret_word[position]
        if letter == guess:
          self.display[position] = letter
    else:
      self.lives -=1
      print(f"Sorry, '{guess}' is not in the word. You lose a life.")
        
  
  def display_hangman(self):
    """ hangman art in another file"""
    print(stages[self.lives])
    print(f"Current word: {' '.join(self.display)}")
    print(f"Guessed letters: {', '.join(sorted(self.guessed_letters))}")
    
  
  def play_game(self):
    """Main game loop to play Hangman"""
    print("Welcome to Hangman!")
    self.display_hangman()
    
    while not self.game_over:
      guess = self.user_guess()
      self.check_guess(guess)
      self.display_hangman()
      
      if "_" not in self.display:
        print("\nCongratulations! You have guessed the word!")
        self.game_over = True
      elif self.lives == 0:
        print(f"\nYou ran out of lives! The word was: {self.secret_word}\n")
        self.game_over = True
        

          
          
       
# To play the game:
if __name__ =="__main__":
  game = HangmanGame()   
  game.play_game()            
  