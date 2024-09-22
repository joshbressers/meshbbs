"""
File to hold the main BBS class
"""

from meshbbs.stages import main
import time

class User:
    def __init__(self, id: str, short_name: str, long_name: str):
        self.id = id
        self.short_name = short_name
        self.long_name = long_name
        self.stage = main.MainMenu()
        self.last_active = time.time()

    def parse(self, message) -> str:
        "Deal with a message we just got from a user"

        # If the user has been inactive for one hour, start over
        if time.time() - self.last_active > 3600:
            self.stage.reset()
        
        self.last_active = time.time()
        new_message = self.stage.run_stage(message)
        return new_message
    