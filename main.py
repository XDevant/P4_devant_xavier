from controlers.base import Controler
from controlers.selector import Selector
from controlers.state import State
from views.base import View
from tinydb import TinyDB


def main():
    db = TinyDB("db/db_test.json")
    selector = Selector()
    view = View()
    table = db.table("save")
    if len(table.all()) == 0:
        state = State()
    else:
        state = State(**table.all()[0])
        table.truncate()
    ctrl = Controler(db, selector, view, state)
    ctrl.run()


if __name__ == "__main__":
    main()
