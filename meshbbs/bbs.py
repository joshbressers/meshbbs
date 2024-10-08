"""
The BBS functionality classes
"""

import meshbbs.stages.main
from datetime import datetime
import queue
import meshbbs.utils

from typing import List

class HelloMessage(Exception):
    """
    This exception is to be thrown when just 'hello' is sent by a user
    This will send us back to the main menu
    """
    pass
    
class User:
    "Class to hold user details and also send and receive the messages"

    def __init__(self, long_name, short_name, id, send_q: queue.Queue):
        self.last_active = datetime.now()
        self.id = id
        self.long_name = long_name
        self.short_name = short_name
        self.my_q = queue.Queue()
        self.send_q = send_q

        self.thread = meshbbs.stages.main.MainMenu(self)
        self.thread.start()

    def parse(self, packet) -> None:
        "Method called to forward a message into the receive queue"
        message = packet.get_message()
        self.my_q.put(message)

    def print(self, message: str) -> None:
        "Print a message to the user"
        self.send_q.put((self.id, message))

    def get_input(self, timeout=3600) -> str:
        "Wait for input from the user, this function blocks"
        try:
            message = self.my_q.get(timeout=timeout)
        except queue.Empty:
            # If we timeout, go back to the main menu
            raise HelloMessage()
        self.my_q.task_done()
        if message.lower() == "hello":
            raise HelloMessage()
        self.last_active = datetime.now()
        return message

    def check_timeout(self):
        "Have we been inactive for an hour or more?"
        if (datetime.now() - self.last_active).seconds > 3600:
            # Somehow exit
            return True
        else:
            return False

class MenuItem:
    "A class representing an item in a menu, you should never call this directly"

    def __init__(self, name, letter, always=False):
        self.name = name
        self.letter = letter
        self.always = always

class UserMenu:
    """
    A class to handle menu items for the user

    Pass in the user handle and a list of menu items
    The list can be very large, we paginate

    Note, when we paginate, we do not re-load data
    If something is changed by another user, we won't see that change here
    """

    def __init__(self, user: User, menu_title: str):

        # The things to show
        self.menu_items: List[MenuItem] = []

        # This is a special list that we always show, even when paginating
        self.always_items: List[MenuItem] = []
        self.user = user
        self.menu_title = menu_title
        self.timeout = 3600

        # This variable tracks how much data we're adding to the menu
        # Don't exceed 200
        # Account for "[N] Next\n" We use 10 just to be safe
        self.always_len = 10

    def add_item(self, name: str, letter: str, always=False):
        "Add an item to the menu"

        if always == True:
            self.always_items.append(MenuItem(name, str(letter), always))
            self.always_len = self.always_len + len(f"\n[{letter}] {name}")
        else:
            self.menu_items.append(MenuItem(name, str(letter), always))

    def get_selection(self, offset = 0) -> str:
        "Print the menu options, with a 'Next' if needed, then return the option chosen"

        # This variable will hold the text we send in the message
        out = self.menu_title

        possible_selections = []

        # If we're paginating, this will not be zero
        menu_index = offset

        for i in range(menu_index, len(self.menu_items)):
            m = self.menu_items[i]
            short = m.letter
            possible_selections.append(short.lower())
            long = m.name
            menu_str = f"\n[{short}] {long}"

            if len(out) + len(menu_str) + self.always_len > 190:
                # Time to paginate!
                out = out + f"\n[N] Next"
                break
            else:
                out = out + menu_str
                menu_index = menu_index + 1
        
        for i in self.always_items:
            short = i.letter
            possible_selections.append(short.lower())
            long = i.name
            out = out + f"\n[{short}] {long}"
        
        while True:
            self.user.print(out)
            input = self.user.get_input(timeout=self.timeout)
            if input.lower() == "n" and 'n' not in possible_selections:
                # Are we paginating?
                return self.get_selection(menu_index)
            elif input.lower() not in possible_selections:
                self.user.print("Unknown option")
            else:
                return input.lower()



