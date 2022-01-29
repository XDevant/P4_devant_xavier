from controlers.selector import Selector

class Controler:
    def __init__(self, db, view):
        self.db = db
        self.view = view
        self.selector = Selector()

    def run(self):
        result = getattr(self.selector, 'help')('me')
        print(result)