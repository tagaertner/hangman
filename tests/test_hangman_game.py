# File: tests/test_hangman_game.py

import pytest
from unittest.mock import patch, call
import builtins
import sys
import os

# This block ensures your project's root directory is in Python's search path.
# It allows 'from Hangman import HangmanGame' to work correctly.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your HangmanGame class from the parent directory
from Hangman import HangmanGame

# --- Test Data (Used by Fixtures) ---
# These are test-specific versions of word_list and stages for predictability.
TEST_WORD_LIST = ["apple", "banana", "cat"]
TEST_STAGES = [
    "Hangman Stage 6 (No lives left)", # stages[0] means 0 lives left
    "Hangman Stage 5",                 # stages[1] means 1 life left
    "Hangman Stage 4",                 # stages[2] means 2 lives left
    "Hangman Stage 3",                 # stages[3] means 3 lives left
    "Hangman Stage 2",                 # stages[4] means 4 lives left
    "Hangman Stage 1",                 # stages[5] means 5 lives left
    "Hangman Stage 0 (Full lives)"     # stages[6] means 6 lives left
]


# ==============================================================================
# 1. FIXTURES
#    Reusable setup for tests, often involving mocking external dependencies.
# ==============================================================================

@pytest.fixture
def mock_game_dependencies():
    """
    Patches external dependencies (word_list, stages, random.choice, input, print)
    to ensure predictable behavior for tests.
    """
    with patch('Hangman.word_list', new=TEST_WORD_LIST):
        with patch('Hangman.stages', new=TEST_STAGES): # Correctly patches stages in Hangman.py
            with patch('random.choice', return_value="apple") as mock_random_choice:
                with patch.object(builtins, 'input') as mock_input:
                    with patch.object(builtins, 'print') as mock_print:
                        yield mock_random_choice, mock_input, mock_print


@pytest.fixture
def hangman_game_instance(mock_game_dependencies):
    """
    Provides a fresh HangmanGame instance for each test, with mocked dependencies active.
    """
    game = HangmanGame()
    return game

# ==============================================================================
# 2. UNIT TESTS
#    Test individual methods/units in isolation, using mocked inputs/outputs.
# ==============================================================================

class TestHangmanGameUnit:
    """Unit tests for the HangmanGame class methods."""

    def test_initial_state(self, hangman_game_instance):
        """Verify the game starts with the correct initial state."""
        assert hangman_game_instance.secret_word == "apple"
        assert len(hangman_game_instance.display) == len(hangman_game_instance.secret_word)
        assert all(d == "_" for d in hangman_game_instance.display)
        assert hangman_game_instance.lives == 6
        assert hangman_game_instance.guessed_letters == []
        assert not hangman_game_instance.game_over

    def test_generate_secret_word_called_once(self, hangman_game_instance, mock_game_dependencies):
        """Tests that generate_secret_word was called by __init__ and used the mocked random.choice."""
        mock_random_choice, _, _ = mock_game_dependencies
        mock_random_choice.assert_called_once_with(TEST_WORD_LIST)

    def test_user_guess_valid_new_letter(self, hangman_game_instance, mock_game_dependencies):
        """Test user_guess for a valid, new single letter input."""
        _, mock_input, _ = mock_game_dependencies
        mock_input.side_effect = ['a']
        guess = hangman_game_instance.user_guess()
        mock_input.assert_called_once_with("Guess a letter: ")
        assert guess == 'a'
        assert 'a' in hangman_game_instance.guessed_letters

    def test_user_guess_invalid_input_then_valid(self, hangman_game_instance, mock_game_dependencies): # capsys removed
            """Test user_guess handles invalid input (e.g., numbers, multiple chars) and then accepts a valid one."""
            _, mock_input, mock_print = mock_game_dependencies
            mock_input.side_effect = ['12', 'ab', '!', 'a']
            guess = hangman_game_instance.user_guess()
            assert mock_input.call_count == 4
            assert guess == 'a'
            assert 'a' in hangman_game_instance.guessed_letters
            # Corrected assertion: check the mock_print calls
            mock_print.assert_has_calls([
                call("Invalid input. Please enter a single letter."),
                call("Invalid input. Please enter a single letter."),
                call("Invalid input. Please enter a single letter.")
        ])
        # capsys-related lines removed

    def test_user_guess_already_guessed_letter(self, hangman_game_instance, mock_game_dependencies): # capsys removed
        """Test user_guess handles already guessed letters."""
        _, mock_input, mock_print = mock_game_dependencies
        hangman_game_instance.guessed_letters.append('e')
        mock_input.side_effect = ['e', 'a']
        guess = hangman_game_instance.user_guess()
        assert mock_input.call_count == 2
        assert guess == 'a'
        assert 'e' in hangman_game_instance.guessed_letters
        assert 'a' in hangman_game_instance.guessed_letters
        # Corrected assertion: check the mock_print calls
        mock_print.assert_any_call("You already guessed 'e'. Try again")
        # capsys-related lines removed


    def test_check_guess_correct_letter(self, hangman_game_instance, mock_game_dependencies):
        """Test check_guess correctly updates display for a correct letter and prints."""
        _, _, mock_print = mock_game_dependencies # CORRECTED UNPACKING
        hangman_game_instance.check_guess("p")
        assert hangman_game_instance.display == ["_", "p", "p", "_", "_"]
        assert hangman_game_instance.lives == 6
        mock_print.assert_any_call("Good guess! 'p' is in the word")


    def test_check_guess_incorrect_letter(self, hangman_game_instance, mock_game_dependencies):
        """Test check_guess correctly decrements lives for an incorrect letter and prints."""
        _, _, mock_print = mock_game_dependencies # CORRECTED UNPACKING
        initial_lives = hangman_game_instance.lives
        hangman_game_instance.check_guess("z")
        assert hangman_game_instance.lives == initial_lives - 1
        assert hangman_game_instance.display == ["_", "_", "_", "_", "_"]
        mock_print.assert_any_call("Sorry, 'z' is not in the word. You lose a life.")


    def test_check_guess_multiple_correct_occurrences(self, hangman_game_instance):
        """Test check_guess updates all occurrences of a correct letter."""
        hangman_game_instance.check_guess("p")
        hangman_game_instance.check_guess("l")
        assert hangman_game_instance.display == ["_", "p", "p", "l", "_"]
        assert hangman_game_instance.lives == 6


    def test_display_hangman(self, hangman_game_instance, mock_game_dependencies):
        """Test display_hangman prints correctly based on state."""
        _, _, mock_print = mock_game_dependencies # CORRECTED UNPACKING
        hangman_game_instance.lives = 3
        hangman_game_instance.display = ["a", "_", "_", "_", "e"]
        hangman_game_instance.guessed_letters = ['a', 'e', 't']
        hangman_game_instance.display_hangman()
        mock_print.assert_has_calls([
            call(TEST_STAGES[3]),
            call("Current word: a _ _ _ e"),
            call("Guessed letters: a, e, t")
        ])

# ==============================================================================
# 3. INTEGRATION TESTS
#    Test interactions between multiple units/methods, simulating game flow.
# ==============================================================================

class TestHangmanGameIntegration:
    """Integration tests for the HangmanGame's overall flow."""

    def test_play_game_win_scenario(self, hangman_game_instance, mock_game_dependencies):
        """Tests a full game win scenario by mocking user input."""
        _, mock_input, mock_print = mock_game_dependencies
        mock_inputs = ['a', 'p', 'l', 'e']
        mock_input.side_effect = mock_inputs

        hangman_game_instance.play_game()

        assert hangman_game_instance.game_over is True
        assert "_" not in hangman_game_instance.display
        mock_print.assert_any_call("\nCongratulations! You have guessed the word!")
        assert mock_input.call_count == len(mock_inputs)

    def test_play_game_lose_scenario(self, hangman_game_instance, mock_game_dependencies):
        """Tests a full game lose scenario by mocking user input."""
        _, mock_input, mock_print = mock_game_dependencies
        mock_inputs = ['x', 'y', 'z', 'q', 'w', 't']
        mock_input.side_effect = mock_inputs

        hangman_game_instance.play_game()

        assert hangman_game_instance.game_over is True
        assert hangman_game_instance.lives == 0
        mock_print.assert_any_call(f"\nYou ran out of lives! The word was: {hangman_game_instance.secret_word}\n")
        assert mock_input.call_count == len(mock_inputs)

    def test_play_game_invalid_inputs_then_win(self, hangman_game_instance, mock_game_dependencies):
        """Test a scenario with invalid inputs followed by correct guesses leading to a win."""
        _, mock_input, mock_print = mock_game_dependencies
        mock_inputs = ['1', 'p', 'a', 'a', 'p', 'l', 'e']
        mock_input.side_effect = mock_inputs

        hangman_game_instance.play_game()

        assert hangman_game_instance.game_over is True
        assert "_" not in hangman_game_instance.display
        mock_print.assert_any_call("Invalid input. Please enter a single letter.")
        mock_print.assert_any_call("You already guessed 'p'. Try again")
        mock_print.assert_any_call("\nCongratulations! You have guessed the word!")
        assert mock_input.call_count == len(mock_inputs)