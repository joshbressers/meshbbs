

class MenuItem:
    def __init__(self, user):
        pass

    def run_stage(self, message: str) -> str:
        pass

class DoneRunning(Exception):
    "Class to throw a done running excpetion back to the main menu"
    pass