class Feedback:
    def __init__(self):
        self.title = ""
        self.input = None
        self.raw_command = None
        self.raw_value = None
        self.command = None
        self.values = []
        self.errors = []
        self.data = []
        self.important = ""
        self.info = ""
        self.hint = ""
        self.example = ""
        self.found_command = False
        self.found_parsed = False
        self.success = False

