from tinydb import where
from models.player import Player
from models.tournament import Tournament


class TournamentSprite:
    def __init__(self, tournament, db):
        self.id = tournament.id
        self.rounds = tournament.rounds
        self.round = tournament.round
        self.players = tournament.players
        self.round_details = tournament.round_details
        self.sprites = [PlayerSprite(tournament, player, db) for player in self.players]

    
    def __repr__(self):
        return f"Tournoi: {self.id}, en {self.rounds} rondes. Ronde {self.round + 1}: {self.sprites}"


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
            self.sprites.sort(key=lambda sprite: - sprite.score * 10 - 1 / sprite.ranking)
            unmatched_players = self.sprites
            while len(matches) < matches_len:
                first_player = unmatched_players.pop(0)
                new_match = [first_player.id]
                for sprite in self.sprites:
                    if sprite in unmatched_players and sprite.id not in first_player.played:
                        new_match.append(sprite.id)
                        matches.append(new_match)
                        index = unmatched_players.index(sprite)
                        unmatched_players.pop(index)
                        break
        return matches
        

class PlayerSprite:
    def __init__(self, tournament, player_id, db):
        self.id = player_id
        self.ranking =  db.table("players").get(doc_id=player_id)["ranking"]
        self.score = 0
        self.played= []
        if tournament.round > 0:
            for i in range(0, tournament.round):
                for match in tournament.round_details[i]:
                    if match[0][0] == self.id:
                        self.score += match[0][1]
                        self.played.append(match[1][0])
                    if match[1][0] == self.id:
                        self.score += match[1][1]
                        self.played.append(match[0][0])


    def __repr__(self):
        return f"Id:{self.id}, rang: {self.ranking}, score: {self.score} TYours précédents: {self.played}"