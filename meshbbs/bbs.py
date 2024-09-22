"""
File to hold the main BBS class
"""

from meshbbs.stages import main

class BBS:
    def __init__(self):
        # The main menu is special
        self.stage = main.main_menu

    def parse(self, message: str):
        if message.lower() == "hello": self.stage = main.main_menu
        (next_stage, return_message) = self.stage(message)
        self.stage = next_stage
        return return_message

class User:
    def __init__(self, id: str, short_name: str, long_name: str):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.bbs = BBS()

    def parse(self, message) -> str:
        "Deal with a message we just got from a user, we'll just pass this to the BBS function"
        new_message = self.bbs.parse(message)
        return new_message
    