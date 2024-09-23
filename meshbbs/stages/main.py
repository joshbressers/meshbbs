import meshbbs.stages
from meshbbs.stages import DoneRunning
import meshbbs.stages.about
import meshbbs.stages.help
import meshbbs.stages.echo
import meshbbs.stages.wall

stages = [
    meshbbs.stages.about,
    meshbbs.stages.help,
    meshbbs.stages.echo,
    meshbbs.stages.wall
]


class MainMenu(meshbbs.stages.MenuItem):

    def __init__(self):
        self.main_message = "Welcome to Meshtastic BBS\n"
        self.to_run = None
        self.to_menu = False

        for i in stages:
            self.main_message = self.main_message + f"[{i.letter}] {i.name}\n"

    def reset(self):
        # Reset the internal state
        self.to_run = None
        self.to_menu = False

    def get_option(self, message: str):
        return_class = self

        for i in stages:
            if message.lower() == i.letter.lower():
                self.to_run = i.StageClass()
                return self.run_stage(message)

        return "Unknown option\n\n" + main_message
            
    def main_menu(self, message: str = None):
        return_string = self.main_message
        self.to_menu = True

        return return_string
    
    def run_stage(self, message: str):
        "Every message sent starts here"

        # 'hello' by itself is a keyword to start over no matter where we are
        if message.lower() == "hello": self.reset()

        # We are special, run main_menu if we are trying to run ourselves
        if self.to_run == None:
            if self.to_menu == True:
                return self.get_option(message)
            else:
                return self.main_menu()
        try:
            return self.to_run.run_stage(message)
        except DoneRunning as e:
            self.reset()
            output_message = str(e) + self.main_menu(None)
            return output_message