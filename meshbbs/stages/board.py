"""The BBS board
Send and receive public messages!
"""

import meshbbs
import meshbbs.bbs
import meshbbs.config_init
import meshbbs.stages
from datetime import datetime
import peewee

# We are using the peewee ORM to store the data


letter = 'B'
name = "Boards"

db = meshbbs.config_init.db

class Board(peewee.Model):
    "The class that represents the message boards"
    name = peewee.CharField(unique=True)
    short = peewee.CharField(unique = True)

    class Meta:
        database = db

    def BoardRun(self, user: "meshbbs.bbs.User"):
        self.BBSUser = user
        while True:
            the_menu = meshbbs.bbs.UserMenu(self.BBSUser, "Messages:")
            for i in self.messages:
                the_menu.add_item(i.title, i.id)
            the_menu.add_item("Write new", "W", True)
            the_menu.add_item("Go Back", "B", True)

            input = the_menu.get_selection()
            if input.isdigit():
                # Read a message
                self.ReadMessage(input)
            elif input == 'w':
                # Write a new message
                self.WriteMessage()
            elif input == 'b':
                # Go back
                return

    def WriteMessage(self):
        self.BBSUser.print("What's the title:")
        title = self.BBSUser.get_input()
        self.BBSUser.print("Please write a new message. End the message with a single dot '.'")
        new_message = ""
        while True:
            input = self.BBSUser.get_input()
            if input == '.':
                break
            new_message = new_message + ' ' + input

        m1 = Message(title=title, message=new_message, user=self.BBSUser.long_name, board=self)
        m1.save()


    def ReadMessage(self, message_id):
        for i in self.messages:
            if i.id == int(message_id):
                output_message = f"{i.title}\nBy {i.user}"
                self.BBSUser.print(output_message)
                self.BBSUser.print(i.message)
                return

class Message(peewee.Model):
    "The class that represents the message boards"
    title = peewee.CharField()
    message = peewee.CharField()
    user = peewee.CharField()

    board = peewee.ForeignKeyField(Board, backref='messages')

    class Meta:
        database = db

# Setup the database on the first run of the module
tables = db.get_tables()
if 'message' not in tables:
    db.create_tables([Message])
if 'board' not in tables:
    db.create_tables([Board])

# We will need to create the first message if none exist
try:
    message = Board.select().get()
except:
    b1 = Board(name="General", short='G')
    b1.save()
    b2 = Board(name="Random", short='R')
    b2.save()
    m1 = Message(title="First Post!", message="This is the first post", user="sysop", board=b1)
    m1.save()
# End setup

class StageClass():
    def __init__(self, user: "meshbbs.bbs.User"):
        self.user = user

    def run(self, message:str = None) -> str:

        while True:
            the_menu = meshbbs.bbs.UserMenu(self.user, "What board would you like?")
            board_names = {}
            for i in Board.select():
                the_menu.add_item(i.name, i.short)
                board_names[i.short] = i
            the_menu.add_item("Exit", "X")
            input = the_menu.get_selection()
            if input == "x":
                return
            else:
                board_names[input.upper()].BoardRun(self.user)

