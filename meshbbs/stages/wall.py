import meshbbs
import meshbbs.bbs
import meshbbs.stages

from datetime import datetime

import peewee

db = peewee.SqliteDatabase('meshbbs.db')

letter = 'W'
name = "Wall"
wall_message = "There is no message yet"

class WallMessage(peewee.Model):
    message = peewee.CharField()
    user = peewee.CharField()
    update_time = peewee.DateTimeField()

    class Meta:
        database = db

# First pass, display message
# Get input
# Check for exit
# Return output
# Get input

db.create_tables([WallMessage])
# We will need to create the first message if none exist
try:
    message = WallMessage.select().order_by(WallMessage.update_time.asc()).get()
except:
    message = WallMessage(message="New message", user="sysop", update_time = datetime.now())

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user

    def print_message(self) -> str:
        # Load the wall message
        # Return it
        pass

    def change_message(self) -> str:
        # Read user input
        # Save the input
        # call print_message
        pass

    def get_input(self, prompt: str) -> str:
        # Read what a user sent
        # Let's put a queue in the user object. Just loop waiting for input
        # Return it to the caller
        pass

    def run_stage(self, message:str = None) -> str:
        # First time in, print the messsage
        self.print_message()

        # Get change input
        input = self.get_input()
        if input.lower() == "y":
            self.change_message()
        elif input.lower() == "n":
            self.exit()
        else:
            self.exit("Unknown option")