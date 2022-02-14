from tinydb import where
from db_models.player import Player
from db_models.tournament import Tournament


class TournamentSprite:
    def __init__(self, tournament, db):
        self.id = tournament.id
        self.rounds = tournament.rounds
        self.round = tournament.round
        self.players = tournament.players
        self.round_details = tournament.round_details
        self.sprites = [PlayerSprite(tournament, player, db) for player in self.players]


    def sort_players(self):
        if self.round == 1:
            self.sprites.sort(key=lambda sprite: sprite.ranking)
        if self.round > 1:
            self.sprites.sort(key=lambda sprite: sprite.ranking * 10 + sprite.score / self.rounds)


    def generate_matches(self):
        matches = []
        matches_len = len(self.players) // 2
        if self.round == 0:
            self.sprites.sort(key=lambda sprite: sprite.ranking)
            for i in range(matches_len):
                matches.append([self.sprites[i].id, self.sprites[i + matches_len].id])
        if self.round > 0:
            self.sprites.sort(key=lambda sprite: sprite.ranking * 10 + sprite.score / self.rounds)
            unmatched_players = self.players
            while len(matches) < matches_len:
                new_match = []
                for sprite in self.sprites:
                    if sprite.id in unmatched_players:
                        new_match.append(sprite.id)
                        index = unmatched_players.index(sprite.id)
                        unmatched_players.pop(index)
                        if len(new_match) == 2:
                            break
        return matches
        

class PlayerSprite:
    def __init__(self, tournament, player_id, db):
        self.id = player_id
        self.ranking =  db.table("players").get(doc_id=player_id)["ranking"]
        self.score = 0
        self.played= []
        if tournament.round > 1:
            for i in range(1, tournament.round):
                for match in tournament.round_details[i - 1]:
                    if match[0][0] == self.id:
                        self.score += match[0][1]
                        self.played.append(match[1][0])
                    if match[1][0] == self.id:
                        self.score += match[1][1]
                        self.played.append(match[0][0])