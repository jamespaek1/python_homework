"""
Task 4: Closure Practice – Hangman

This module implements a simple hangman game using a closure. The
function ``make_hangman`` accepts a secret word and returns a
``hangman_closure`` that maintains internal state (the list of
guessed letters). Each call to the returned function with a letter
updates the guesses and prints the current state of the word with
underscores for unguessed letters. The closure returns ``True`` if the
word has been completely guessed and ``False`` otherwise.

When run as a script, the program prompts the user for a secret word
and then repeatedly prompts for guesses until the word is guessed.
"""

from typing import Callable


def make_hangman(secret_word: str) -> Callable[[str], bool]:
    """Create a hangman closure for a given secret word.

    :param secret_word: The word players must guess. Case is
        preserved, but guesses are matched in a case‑insensitive
        manner.
    :returns: A closure that accepts a single character guess and
        returns True when all letters have been guessed, False otherwise.
    :rtype: Callable[[str], bool]
    """
    # Store guesses in a list. Use a set for quick lookup but keep
    # insertion order for potential future enhancements.
    guesses: list[str] = []
    # Convert secret word to lowercase for comparison without altering
    # the displayed case.
    secret_lower = secret_word.lower()

    def hangman_closure(letter: str) -> bool:
        """Handle a guessed letter and reveal the current word state.

        :param letter: A single letter guess. Only the first
            character of the input string is considered.
        :returns: True if all letters have been guessed, False otherwise.
        :rtype: bool
        """
        if not letter:
            return False
        # Normalize the guessed letter to lowercase
        guess = letter[0].lower()
        # Record the guess if it hasn't been guessed already
        if guess not in guesses:
            guesses.append(guess)
        # Build the display string with underscores for unguessed letters
        display_chars: list[str] = []
        for orig_char, lower_char in zip(secret_word, secret_lower):
            if lower_char in guesses:
                display_chars.append(orig_char)
            else:
                # Represent unguessed letters as underscores
                display_chars.append("_")
        display_string = "".join(display_chars)
        print(display_string)
        # Determine if the game is won: all letters from the secret word
        # appear in guesses (ignore non‑alphabetic characters)
        for lower_char in secret_lower:
            # Consider letters only; skip spaces or punctuation
            if lower_char.isalpha() and lower_char not in guesses:
                return False
        return True

    return hangman_closure


if __name__ == "__main__":
    # Interactive game loop. Prompt for the secret word and then for
    # guesses until the word is fully guessed.
    secret_word_input = input("Enter the secret word for hangman: ")
    game = make_hangman(secret_word_input)
    guessed = False
    while not guessed:
        guess_input = input("Guess a letter: ")
        guessed = game(guess_input)
    print("Congratulations! You guessed the word.")