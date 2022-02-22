from datetime import date
from tinydb import TinyDB
from models.player import Player
from models.tournament import Tournament


db = TinyDB("db/db_test.json")
players_table = db.table("players")
players_table.truncate()
players = []
players.append(Player(**{"last_name": "Cohen", "first_name": "Leonard", "date_of_birth": str(date(1942, 1, 2)), "gender": "M", "ranking": 2}))
players.append(Player(**{"last_name": "Reinhardt", "first_name": "Django", "date_of_birth": "01/01/1902", "gender": "M", "ranking": 1}))
players.append(Player(**{"last_name": "Brassen", "first_name": "George", "date_of_birth": "01/01/1902", "gender": "M", "ranking": 5}))
players.append(Player(**{"last_name": "Simone", "first_name": "Nina", "date_of_birth": "01/01/1947", "gender": "F", "ranking": 6}))
players.append(Player(**{"last_name": "Vaughan", "first_name": "Sarah", "date_of_birth": "01/01/1937", "gender": "F", "ranking": 4}))
players.append(Player(**{"last_name": "Davies", "first_name": "Miles", "date_of_birth": "01/01/1941", "gender": "M", "ranking": 3}))
players.append(Player(**{"last_name": "Vaughan", "first_name": "Jeremy", "date_of_birth": "01/01/1936", "gender": "F"}))
players.append(Player(**{"last_name": "Vaughan", "first_name": "Anna", "date_of_birth": "01/01/1978", "gender": "F"}))
for player in players:
    player.register(players_table)

tournaments_table = db.table("tournaments")
tournaments_table.truncate()
tournament1 = Tournament(db, **{"name": "First Tournament", "place": "Madisson Square Garden", "date": str(date.today()), "timer": "bullet"})
tournament1.register(db)
