from views.help import Help
from views.report import Report

class View:
    def __init__(self):
        self.help = Help()
        self.report = Report()

    def gather_command(self):
        answer = input() + ' '
        if answer.startswith('.'):
            command = answer.split(' ')[0]
            return command, answer[len(command):]
        return answer