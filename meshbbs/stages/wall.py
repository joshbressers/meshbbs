import meshbbs.stages

from meshbbs.stages import DoneRunning

letter = 'W'
name = "Wall"
wall_message = "There is no message yet"

# First pass, display message
# Get input
# Check for exit
# Return output
# Get input

class StageClass(meshbbs.stages.MenuItem):
    def __init__(self, user):
        self.run_next = None
        self.state = "show"
        self.user = user

    def get_input(self, message:str = None) -> str:
        if self.state == "change":
            self.state = "show"
            self.run_next = None
            global wall_message
            wall_message = message + "\nBy user %s" % self.user.short_name
            return self.run_stage()
        else:
            # Always change this just in case something weird happens
            self.state = "show"
            if message.lower() == "n":
                raise DoneRunning("See you later!\n\n")
            elif message.lower() == "y":
                output_message = f"Plese enter a new message:\n"
                self.state = "change"
            else:
                output_message = "I don't know that option"
            return output_message

    def run_stage(self, message:str = None) -> str:
        if self.run_next is None:
            self.run_next = self.get_input
            first_message = f"The current wall message is\n{wall_message}\n\nChange it? Y/N\n"
            return first_message
        else:
            return self.run_next(message)