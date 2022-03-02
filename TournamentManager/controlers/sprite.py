class TournamentSprite:
    """The swiss rules. Created at the beguining of each round to générate the
    matches"""
    def __init__(self, tournament, db):
        self.id = tournament.id
        self.rounds = tournament.rounds
        self.round = tournament.round
        self.players = tournament.players
        self.round_details = tournament.round_details
        self.sprites = [PlayerSprite(tournament, p, db) for p in self.players]

    def __iter__(self):
        return self.sprites.__iter__()

    def __repr__(self):
        sprite_str = f"Tournoi: {self.id}, en {self.rounds} rondes."
        sprite_str += f" Ronde actuelle:{self.round}:\n"
        for sprite in self.sprites:
            sprite_str += sprite.__repr__()
        return sprite_str

    def sort_players(self, key):
        if key == "ranking":
            self.sprites.sort(key=lambda sprite: sprite.ranking)
        if key == "swiss":
            self.sprites.sort(key=lambda s: s.ranking * 10 + s.score / self.rounds)
        if key == "score":
            self.sprites.sort(key=lambda sprite: -sprite.score)

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
                if len(new_match) == 1:
                    new_match.append(free_players.pop(0).id)
                    matches.append(new_match)
        return matches


class PlayerSprite:
    def __init__(self, tournament, player_id, db):
        self.id = player_id
        self.player_string = db.table("players").get(doc_id=player_id)
        self.full_name = self.player_string["first_name"] + self.player_string["last_name"]
        self.ranking = self.player_string["ranking"]
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
        sprite = f"({self.id}){self.full_name}, rang: {self.ranking}, score: {self.score}"
        sprite += f" adversaires précédents: {self.played}\n"
        return sprite
