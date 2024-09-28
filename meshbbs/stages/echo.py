"""A menu that shows how to receive and send messages.
It's not very useful but a good example
"""

import meshbbs.bbs

letter = 'E'
name = "Echo"

# First pass, display message
# Get input
# Check for exit
# Return output
# Get input

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user

    def run(self) -> str:
        self.user.print("\nType something and I'll echo it back\n")
        input = self.user.get_input()
        self.user.print(f"You typed\n{input}\n")