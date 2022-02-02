from controlers.selector import Selector


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()
        self.last_command = None


    def run(self):
        running = True
        while running:
            input = self.view.gather_command()
            command = self.find_command(input)
            if command:
                if command == "quit":
                        running = False
                else:
                    self.last_command = command
            print(self.last_command)


    def find_command(self, input):
        for command in self.selector:
            result = getattr(self.selector, command).is_the_one(input)
            if result:
                return command
        return None
