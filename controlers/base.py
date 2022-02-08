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
            command, raw_values = self.find_command(input)
            if command:
                check, values = getattr(self.selector, command).parse_values(raw_values)
                if check:
                    try:
                        name, data = getattr(self.selector, command).execute(values, self.db)
                    except Exception:
                        strategy = self.view.execution_error(input, command, values)
                    else:
                        strategy = self.view.display(name, data)
                        if command == "quit":
                            running = False
                        else:
                            self.last_command = command
                else:
                    strategy = self.view.parsing_error(input, command, values)
            else:
                strategy = self.view.command_error(input)
            #print(self.last_command)


    def find_command(self, input):
        for command in self.selector:
            result, values = getattr(self.selector, command).is_the_one(input)
            if result:
                return command, values
        return None, None
