"""The menu that prints the help message
"""

import meshbbs.bbs

letter = 'H'
name = "Help"

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user
        self.help_message = """Someday this will be more helpful
For now, send 'hello' to go back to the menu
"""

    def run(self) -> str:
        self.user.print(self.help_message)