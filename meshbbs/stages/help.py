from meshbbs.stages import DoneRunning
from meshbbs.stages import MenuItem

letter = 'H'
name = "Help"

help_message = "Someday this will be helpful\n"

class StageClass(MenuItem):
    def __init__(self):
        pass

    def run_stage(self, message:str = None) -> str:
        raise DoneRunning(help_message)