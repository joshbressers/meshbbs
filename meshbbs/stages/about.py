"""The menu that prints the about message
"""

import meshbbs.bbs

letter = 'A'
name = "About"

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user
        self.message = about_message = """This is Meshtastic BBS
The project lives at https://github.com/joshbressers/meshbbs
Feel free to file bugs

The software is not at all stable, you've been warned
"""

    def run(self) -> str:
        self.user.print(self.message)