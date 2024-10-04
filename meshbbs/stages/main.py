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

        self.stages = {}
        for i in stages:
            self.stages[i.letter] = i
            
    def run(self):
        # The thread enters here

        the_stages = {}

        the_menu = meshbbs.bbs.UserMenu(self.user, "Welcome to Meshtastic BBS")
        the_menu.timeout = None
        for i in stages:
            the_menu.add_item(name=i.name, letter=i.letter, always=True)
            the_stages[i.letter.lower()] = i
        while True:
            try:
                selection = the_menu.get_selection()
                the_stages[selection].StageClass(self.user).run()

            except meshbbs.bbs.HelloMessage:
                # We say "hello", go back to the main menu
                continue