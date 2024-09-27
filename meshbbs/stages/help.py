

letter = 'H'
name = "Help"

help_message = "Someday this will be helpful\n"

class StageClass():
    def __init__(self, user):
        self.user = user

    def run(self) -> str:
        self.user.print(help_message)