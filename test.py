from tinydb import TinyDB
from models.player import Player
from datetime import date

db = TinyDB("db_test.json")
players_table = db.table("players")
players_table.truncate()
players = []
date1 = date(1942, 1, 2)
players.append(Player("Cohen", "Leonard", str(date1), "M", 2))
players.append(Player("Reinhardt", "Django", "01/01/1902", "M", 1))
players.append(Player("Brassen", "George", "01/01/1902", "M", 5))
players.append(Player("Simone", "Nina", "01/01/1947", "F", 3))
players.append(Player("Vaughan", "Sarah", "01/01/1937", "F", 4))
players.append(Player("Davies", "Miles", "01/01/1941", "M", 6))
players.append(Player("Vaughan", "Sarah", "01/01/1937", "F", 8))
players.append(Player("Vaughan", "Sarah", "01/01/1937", "F", 4))
for player in players:
    player.register(players_table)
