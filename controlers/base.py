from controlers.selector import Selector


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()
        self.last_command = None


    def run(self):
        time_to_leave = False
        result = getattr(self.selector, 'help')('me')
        print(result)
        while True:
            command, values = self.view.gather_command()
            command, values = self.refine_input(command, values)
            print(command, "+", values.strip())
            if time_to_leave:
                break
            self.last_command = command
            print(self.last_command)


    def refine_input(self, command, values):
        return command, values
