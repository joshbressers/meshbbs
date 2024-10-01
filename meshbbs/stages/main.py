import threading

import meshbbs.bbs

import meshbbs.stages.about
import meshbbs.stages.help
import meshbbs.stages.echo
import meshbbs.stages.wall
import meshbbs.stages.board

stages = [
    meshbbs.stages.about,
    meshbbs.stages.help,
    meshbbs.stages.echo,
    meshbbs.stages.wall,
    meshbbs.stages.board
]


class MainMenu(threading.Thread):
    """Main menu class

    This class is where the main menu exists, and the whole BBS runs from here
    Each user gets their own MainMenu instance
    """
    def __init__(self, user: "meshbbs.bbs.User"):
        threading.Thread.__init__(self)
        self.main_message = "\nWelcome to Meshtastic BBS\n"
        self.to_run = None
        self.to_menu = False
        self.user = user

        for i in stages:
            self.main_message = self.main_message + f"[{i.letter}] {i.name}\n"

            
    def run(self):
        # The thread enters here
        while True:
            try:
                self.user.print(self.main_message)
                input: str = self.user.get_input(timeout=None)

                if input.lower() == "hello":
                    continue
                if len(input) == 1:
                    for i in stages:
                        if input.lower() == i.letter.lower():
                            to_run = i.StageClass(self.user)
                            to_run.run()
                            break
                    else:
                        self.user.print(f"Unknown option {input}\n")
            except meshbbs.bbs.HelloMessage:
                # We say "hello", go back to the main menu
                continue