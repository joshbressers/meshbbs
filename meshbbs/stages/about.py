from meshbbs.stages import DoneRunning
from meshbbs.stages import MenuItem

letter = 'A'
name = "About"

about_message = """This is Meshtastic BBS
The project lives at https://github.com/joshbressers/meshbbs
Feel free to file bugs

The software is not at all stable, you've been warned
"""

class StageClass(MenuItem):
    def __init__(self, user):
        pass

    def run_stage(self, message:str = None) -> str:
        raise DoneRunning(about_message)