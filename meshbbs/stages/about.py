

letter = 'A'
name = "About"

about_message = """This is Meshtastic BBS
The project lives at https://github.com/joshbressers/meshbbs
Feel free to file bugs

The software is not at all stable, you've been warned
"""

class StageClass():
    def __init__(self, user):
        self.user = user

    def run(self) -> str:
        self.user.print(about_message)