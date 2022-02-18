from controlers.selector import Selector
from controlers.sprite import TournamentSprite
from controlers.state import State


class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()
        self.state = State()

    def run(self):
        running = True
        while running:
            checked = False
            input = self.view.gather_command()
            raw_command, raw_values = self.parse_input(input)
            if raw_command is None:
                raw_command = self.state.default_raw_command
            command = self.find_command(raw_command)

            if command:
                checked, values = getattr(self.selector, command).parse_values(raw_command, raw_values, self.state)
            else:
                strategy = self.view.command_error(input)
                continue

            if checked:
                try:
                    name, data = getattr(self.selector, command).execute(raw_command, values, self.db, self.state)
                except Exception as err:
                    print(type(err))
                    strategy = self.view.execution_error(input, command, values)
                else:
                    strategy = self.view.display(name, data)
                    if command in ["starttournament", "certifyround"]:
                        self.state.default_tournament = values["id"]
                        self.new_round(data[0], self.db)
                    if command == "quit":
                        running = False
                    else:
                        self.state.last_command = command
            else:
                strategy = self.view.parsing_error(input, command, raw_values)
                continue
 
            #print(self.last_command)


    def parse_input(self, input):
        base = 0
        splited_input = input.split(' ')
        if input.startswith('.'):
            raw_command = splited_input[0]
            base = 1
        else:
            raw_command = None
        if len(splited_input) > base:
            raw_values = ' '.join(splited_input[base:]).split(',')
            raw_values = [value.strip() for value in raw_values]
        else:
            raw_values = None
        return (raw_command, raw_values)


    def find_command(self, raw_command):
        if raw_command:
            for command in self.selector:
                result = getattr(self.selector, command.lower()).is_the_one(raw_command)
                if result:
                    return command.lower()
        return None


    def new_round(self, tournament, db):
        active_tournament = TournamentSprite(tournament, db)
        print(active_tournament)
        matches = active_tournament.generate_matches()
        print(matches)
        self.state.new_round['name'] = f"Round {active_tournament.round + 1}"
        self.state.new_round['matches'] = matches