"""A menu that shows how to receive and send messages.
It's not very useful but a good example
"""

import meshbbs.bbs
import random

letter = 'G'
name = "Guess a number"

# First pass, display message
# Get input
# Check for exit
# Return output
# Get input

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user

    def run(self) -> str:
        while True:
            number = random.random() * 10
            self.user.print("\nGuess a number between 1 and 10, Q to quit\n")
            input = self.user.get_input()
            if input.lower() == "q":
                return

            try:
                float(input)
                self.user.print(f"You guessed\n{input}\nThe answer was {number}\n")
            except ValueError:
                self.user.print(f"{input} is not a number\n")
