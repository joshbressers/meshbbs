import meshbbs.stages

from meshbbs.stages import DoneRunning

letter = 'E'
name = "Echo"

# First pass, display message
# Get input
# Check for exit
# Return output
# Get input

class StageClass(meshbbs.stages.MenuItem):
    def __init__(self):
        self.run_next = None

    def get_input(self, message:str = None) -> str:
        if message.lower() == "exit":
            raise DoneRunning("See you later!\n\n")
        output_message = f"You typed:\n{message}\n"
        return output_message

    def run_stage(self, message:str = None) -> str:
        if self.run_next is None:
            self.run_next = self.get_input
            first_message = "Simple echo:\nEcho back whatever you type\n\n'exit' to quit"
            return first_message
        else:
            return self.run_next(message)