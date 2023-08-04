import os
import re

# We'll use NLTK to obtain a list of every accepted word. It's not ideal (there are words missing like "pasta") but alas
try:
    from nltk.corpus import words

    WORDS = words.words()
except LookupError:
    import nltk

    nltk.download("words")
    from nltk.corpus import words

    WORDS = words.words()

from images import HANGMAN_IMAGES


class Hangman:
    """
    Hangman

    User A inputs a secret word.
    There are three difficulty modes that can be defined based on a) user input and b) word length
                    Word Length 0-5     Word Length 5+
        Easy             9                   7
        Hard             7                   5

    User B must guess within x attempts where x is defined within the matrix above

    Incorrect guesses or wrong letter guesses result in a piece of the hangman drawing being added
    The game ends when either the hangman is complete or User B (the guesser) guesses the word

    Inputs
        answer : str


    Use
        Currently, this is only working with the terminal as the front end.
        Use the initialisation of the class to set the word/difficulty.
        Use .guess(), .guess_word(), or .guess_letter() to guess characters
        Once the game is over, you can use .restart() to restart the game with a new word/difficulty.

    """

    def __init__(self, answer: str, difficulty: str = "easy") -> None:
        # Attribute Initialisations
        self.n_guesses_remaining = (
            int()
        )  # Will be used to store the number of guesses remaining
        self.n_guesses_start = (
            int()
        )  # Will be used to store the number of guesses allowed at the beginning of the game (used to draw the hangman image)
        self.incorrect_guesses = set()  # Set containing all invalid guesses
        self.correct_guesses = set()  # Set containing all correct guesses
        self.game_complete = False  # When this is True, the user can no longer guess

        # Set Answer
        if self.validate_word(answer):
            self.answer = list(answer.upper())
            self.check_for_spaces()
            self.valid_guesses = set(self.answer)
        else:
            raise ValueError("Invalid answer chosen.")

        os.system(
            "clear"
        )  # Clears the screen so the inputted answer is no longer visible

        # Set Difficulty - Overwrites n_guesses_remaining based on inputs
        self.set_difficulty(difficulty)

    # Methods used for initialisation
    def validate_word(self, word: str) -> bool:
        """Checks if a word is a valid English word."""
        pattern = "[^a-zA-Z\s:]"  # searching for non alphabetical characters (allowing spaces)
        if re.search(pattern, word):
            raise ValueError(
                "invalid character entered. no numbers or special characters allowed."
            )

        if word not in WORDS:
            overwrite = str(
                input(
                    f"{word} is not an accepted word. Would you like to continue? Y/N: "
                )
            )
            if overwrite[0].lower() == "y":
                return True
            else:
                return False
        else:
            return True

    def check_for_spaces(self):
        """If there are spaces in the answer, these get provided to the user from the start"""
        if " " in self.answer:
            self.correct_guesses.add(" ")

    def set_difficulty(self, difficulty: str) -> None:
        """This is to validate the difficulty of the game chosen"""
        if difficulty[0].lower() == "e":
            self.difficulty = "easy"
        elif difficulty[0].lower() == "h":
            self.difficulty = "hard"
        else:
            raise ValueError("Invalid difficulty selected. Choose EASY or HARD")
        self.n_guesses_remaining = self.set_guesses()
        self.n_guesses_start = (
            self.n_guesses_remaining
        )  # Number of guesses allowed at the start
        print(f"You will have {self.n_guesses_remaining} guesses. G'luck!")

    def set_guesses(self) -> int:
        """Sets the number of guesses a user has, based on the difficulty input, and the number of characters in the answer"""
        if len(self.answer) < 5 and self.difficulty == "easy":
            return 9
        if (len(self.answer) >= 5 and self.difficulty == "easy") or (
            len(self.answer) < 5 and self.difficulty == "hard"
        ):
            return 7
        else:
            return 5

    # Methods used for gameplay
    def guess_letter(self, guess: str):
        """Input: guess - a one letter guess. Checks if this is a correct guess + updates relevant parameters"""
        if not self.game_complete:
            # Validate Input
            if len(guess) != 1:
                print("Invalid guess! Your guess must be one letter.")
            else:
                os.system("clear")
                guess = guess.upper()

                # User has already guessed this value:
                if guess in (self.incorrect_guesses.union(self.correct_guesses)):
                    print(
                        f"Oops! You've already guessed {guess}.\nYour guesses so far: {self.incorrect_guesses.union(self.correct_guesses)}"
                    )

                # Add guess to relevant set depending on if the guess was Correct or Incorrect
                elif guess in self.answer:
                    print(
                        f"Correct! That appears {self.answer.count(guess)} times in the answer\nYou still have {self.n_guesses_remaining} guesses left."
                    )
                    self.correct_guesses.add(guess)
                else:
                    self.n_guesses_remaining -= 1
                    print(
                        f"Incorrect. Adding {guess} to the rubbish\nOther incorrect guesses: {self.incorrect_guesses}. You have {self.n_guesses_remaining} guesses left."
                    )
                    self.incorrect_guesses.add(guess)

                self.print_answers()
                self.check_for_completeness()
        else:
            print(
                "The game is over! Restart by re-instanitating the class, using Hangman()"
            )

    def guess_word(self, guess: str):
        """Input: guess - a word. Checks if this is a correct guess + updates relevant parameters"""
        if not self.game_complete:
            # Validate Input
            if not self.validate_word(guess):
                print("Invalid word entered! Try again.")
            else:
                os.system("clear")
                guess = guess.upper()

                # User has already guessed this value:
                if guess in (self.incorrect_guesses.union(self.correct_guesses)):
                    print(
                        f"Oops! You've already guessed {guess}.\nYour guesses so far: {self.incorrect_guesses.union(self.correct_guesses)}"
                    )

                # Add guess to relevant set depending on if the guess was Correct or Incorrect
                elif guess == "".join(self.answer):
                    print(f"Correct! You got the word!")
                    self.correct_guesses.add(list(guess))
                else:
                    self.n_guesses_remaining -= 1
                    print(
                        f"Incorrect. Adding {guess} to the rubbish\nOther incorrect guesses: {self.incorrect_guesses}. You have {self.n_guesses_remaining} guesses left."
                    )
                    self.incorrect_guesses.add(guess)

                self.print_answers()
                self.check_for_completeness()

    def guess(self, guess: str):
        """
        For ease, will allow the user to just use the 'guess' method, and will determine whether to use the
        guess_word or guess_letter method
        """
        if len(guess) == 0:
            print("Invalid guess! Your guess should be a letter or a word!")
        elif len(guess) == 1:
            self.guess_letter(guess)
        else:
            self.guess_word(guess)
            
    def check_for_completeness(self):
        """Checks if the game is complete or not. If so, it will toggle the game_complete attribute"""
        if self.correct_guesses == self.valid_guesses:
            print(f"Hurrah! You won: The word was {''.join(self.answer)}! Congrats!")
            self.game_complete = True
            return

        if self.n_guesses_remaining < 1:
            print(f"Unlucky! You lost. The word was {''.join(self.answer)}!")
            self.game_complete = True
            return

    # Functions used for visuals
    def construct_hangman(self) -> str:
        """Chooses the relevant hangman drawing to display"""
        if self.n_guesses_start == 5:
            image_to_display = {
                5: HANGMAN_IMAGES["stage_one"],
                4: HANGMAN_IMAGES["stage_four"],
                3: HANGMAN_IMAGES["stage_five"],
                2: HANGMAN_IMAGES["stage_six"],
                1: HANGMAN_IMAGES["stage_eight"],
                0: HANGMAN_IMAGES["stage_ten"],
            }

        elif self.n_guesses_start == 7:
            image_to_display = {
                7: HANGMAN_IMAGES["stage_one"],
                6: HANGMAN_IMAGES["stage_four"],
                5: HANGMAN_IMAGES["stage_five"],
                4: HANGMAN_IMAGES["stage_six"],
                3: HANGMAN_IMAGES["stage_seven"],
                2: HANGMAN_IMAGES["stage_eight"],
                1: HANGMAN_IMAGES["stage_nine"],
                0: HANGMAN_IMAGES["stage_ten"],
            }

        else:  # ie. self.n_guesses_start == 9
            image_to_display = {
                9: HANGMAN_IMAGES["stage_one"],
                8: HANGMAN_IMAGES["stage_two"],
                7: HANGMAN_IMAGES["stage_three"],
                6: HANGMAN_IMAGES["stage_four"],
                5: HANGMAN_IMAGES["stage_five"],
                4: HANGMAN_IMAGES["stage_six"],
                3: HANGMAN_IMAGES["stage_seven"],
                2: HANGMAN_IMAGES["stage_eight"],
                1: HANGMAN_IMAGES["stage_nine"],
                0: HANGMAN_IMAGES["stage_ten"],
            }

        return image_to_display[self.n_guesses_remaining]

    def print_answers(self) -> str:
        """Prints the hangman drawing, as well as the final word (with not-yet-guessed letters as _)"""
        print(self.construct_hangman())
        print(
            "Your correct letters so far: "
            + (" ".join([w if w in self.correct_guesses else "_" for w in self.answer]))
        )

    def restart(self, new_word, difficulty=self.difficulty):
        """Restarts the game with a new word."""
        self.__init__(new_word, difficulty)
