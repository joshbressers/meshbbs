"""
File to hold the main BBS class
"""

import meshbbs.stages.main
from datetime import datetime
import queue
import meshbbs.utils

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

    def get_input(self) -> str:
        "Wait for input from the user, this function blocks"
        message = self.my_q.get()
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