
class MenuItem:
    def __init__(self):
        pass

    def run_stage(self) -> str:
        pass

class DoneRunning(Exception):
    "Class to throw a done running excpetion back to the main menu"
    pass