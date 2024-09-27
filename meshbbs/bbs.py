"""
File to hold the main BBS class
"""

import meshbbs.stages.main
from datetime import datetime
import queue
import meshbbs.utils
    
class User:
    def __init__(self, id, send_q: queue.Queue):
        self.last_active = datetime.now()
        self.id = id
        self.my_q = queue.Queue()
        self.send_q = send_q

        self.thread = meshbbs.stages.main.MainMenu(self)
        self.thread.start()

    def parse(self, packet) -> None:
        message = packet.get_message()
        self.my_q.put(message)

    def print(self, message: str) -> None:
        self.send_q.put((self.id, message))

    def get_input(self) -> str:
        message = self.my_q.get()
        self.my_q.task_done()
        return message

    def check_timeout(self):
        if (datetime.now() - self.last_active).seconds > 3600:
            # Somehow exit
            return True
        else:
            return False