from controlers.selector import Selector
import commands


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.commands = [command for command in dir(commands) if command.istitle()]
        self.selector = Selector(*self.commands)
        self.last_command = None


    def run(self):
        running = True
        print(self.commands)
        while running:
            input = self.view.gather_command()
            for command in self.commands:
                result = getattr(self.selector, command.lower()).execute(input)
                if result:
                    if command != "Quit":
                        self.last_command = command.lower()
                    else:
                        running = False
                    break   
            print(self.last_command)


