from controlers.base import Controler
from views.base import View
from tinydb import TinyDB


def main():
    db = TinyDB("db/db_test.json")
    view = View()
    ctrl = Controler(db, view)
    ctrl.run()

if __name__ == "__main__":
    main()