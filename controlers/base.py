from controlers.selector import Selector


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()
        self.commands = [command for command in dir(self.selector) if not command.startswith('__')]
        self.last_command = None


    def run(self):
        running = True
        print(self.commands)
        while running:
            input = self.view.gather_command()
            for command in self.commands:
                result = getattr(self.selector, command).execute(input)
                if result:
                    if command == "quit":
                        running = False
                    else:
                        self.last_command = command
                    break   
            print(self.last_command)


