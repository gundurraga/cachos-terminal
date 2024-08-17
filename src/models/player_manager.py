from typing import List
from src.models.player import Player
from src.models.human_player import HumanPlayer
from src.models.ai_player import AIPlayer
from src.utils.name_generator import NameGenerator


class PlayerManager:
    def __init__(self, num_ai_players: int):
        self.name_generator = NameGenerator()
        self.players: List[Player] = self.initialize_players(num_ai_players)
        self.current_player_index: int = 0

    def initialize_players(self, num_ai_players: int) -> List[Player]:
        players = [HumanPlayer("Jugador Humano")]
        for i in range(num_ai_players):
            ai_name = self.name_generator.get_random_name()
            players.append(AIPlayer(f"{ai_name} (AI {i+1})"))
        return players

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def get_previous_player(self) -> Player:
        return self.players[(self.current_player_index - 1) % len(self.players)]

    def next_player(self):
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)

    def determine_starting_player(self) -> Player:
        max_roll = 0
        starting_player = None
        for player in self.players:
            roll = max(player.roll_dice())
            if roll > max_roll:
                max_roll = roll
                starting_player = player
        self.current_player_index = self.players.index(starting_player)
        return starting_player

    def check_game_over(self) -> bool:
        return sum(1 for player in self.players if player.dice) == 1

    def get_winner(self) -> Player:
        for player in self.players:
            if player.dice:
                return player
        return None

    def roll_all_dice(self):
        for player in self.players:
            player.roll_dice()
