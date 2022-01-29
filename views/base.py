from views.help import Help
from views.report import Report

class View:
    def __init__(self):
        self.help = Help()
        self.report = Report()