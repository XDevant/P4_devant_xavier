from controlers.selector import Selector


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()
        self.last_command = None


    def run(self):
        running = True
        commands = [command for command in dir(self.selector) if not command.startswith('__')]
        while running:
            input = self.view.gather_command()
            for command in commands:
                result = getattr(self.selector, command).execute(input)
                if result:
                    if command != "quit":
                        self.last_command = command
                    else:
                        running = False
                    break   
            print(self.last_command)


