import meshbbs
import meshbbs.bbs
import meshbbs.stages

from datetime import datetime

import peewee

db = peewee.SqliteDatabase('meshbbs.db')

letter = 'W'
name = "Wall"

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

tables = db.get_tables()
if 'wallmessage' not in tables:
    db.create_tables([WallMessage])
# We will need to create the first message if none exist
try:
    message = WallMessage.select().order_by(WallMessage.update_time.desc()).get()
except:
    message = WallMessage(message="First post!", user="sysop", update_time = datetime.now())
    message.save()

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user

    def run(self, message:str = None) -> str:

        while True:
            message = WallMessage.select().order_by(WallMessage.update_time.desc()).get()
            self.user.print("The wall message is")
            self.user.print(f"{message.message}\nBy {message.user} on {message.update_time}\n")
            self.user.print("Would you like to change the message?\nY/N\n")
            input = self.user.get_input()
            if input.lower() == "y":
                # change the message
                self.user.print("Type new message. Send 'done' as its own message when you are done")
                new_message = ""
                while True:
                    new_input = self.user.get_input()
                    if new_input.lower() == "done":
                        break
                    else:
                        new_message = new_message + new_input + " "

                message = WallMessage(message=new_message, user=self.user.long_name, update_time = datetime.now())
                message.save()
            elif input.lower() == "n":
                return
            else:
                self.user.print("Unknown option")
