class TournamentSprite:
    def __init__(self, tournament, db):
        self.id = tournament.id
        self.rounds = tournament.rounds
        self.round = tournament.round
        self.players = tournament.players
        self.round_details = tournament.round_details
        self.sprites = [PlayerSprite(tournament, p, db) for p in self.players]

    def __repr__(self):
        sprite = f"Tournoi: {self.id}, en {self.rounds} rondes."
        sprite += f" Ronde {self.round + 1}: {self.sprites}"
        return sprite

    def sort_players(self):
        if self.round == 1:
            self.sprites.sort(key=lambda sprite: sprite.ranking)
        if self.round > 1:
            self.sprites.sort(key=lambda s: s.ranking * 10 + s.score / self.rounds)

    def generate_matches(self):
        matches = []
        n = len(self.players) // 2
        if self.round == 0:
            self.sprites.sort(key=lambda sprite: sprite.ranking)
            for i in range(n):
                matches.append([self.sprites[i].id, self.sprites[i + n].id])
        if self.round > 0:
            self.sprites.sort(key=lambda s: - s.score * 10 - 1 / s.ranking)
            free_players = self.sprites
            while len(matches) < n:
                player_1 = free_players.pop(0)
                new_match = [player_1.id]
                for sprite in self.sprites:
                    if sprite in free_players and sprite.id not in player_1.played:
                        new_match.append(sprite.id)
                        matches.append(new_match)
                        index = free_players.index(sprite)
                        free_players.pop(index)
                        break
        return matches


class PlayerSprite:
    def __init__(self, tournament, player_id, db):
        self.id = player_id
        self.ranking = db.table("players").get(doc_id=player_id)["ranking"]
        self.score = 0
        self.played = []
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
        sprite = f"Id:{self.id}, rang: {self.ranking}, score: {self.score}."
        sprite += f" Tours précédents: {self.played}"
        return sprite
