# game.py
from typing import List, Tuple, Optional
from src.models.player_manager import PlayerManager
from src.models.round_manager import RoundManager
from src.models.bet_manager import BetManager
from src.views.renderer import Renderer


class Game:
    def __init__(self, num_ai_players: int, renderer: Renderer):
        self.renderer = renderer
        self.player_manager = PlayerManager(num_ai_players)
        self.bet_manager = BetManager()
        self.round_manager = RoundManager(self.player_manager, self.renderer)

    def start_game(self):
        self.renderer.display_welcome_message()
        self.renderer.display_players(self.player_manager.players)

        starting_player = self.player_manager.determine_starting_player()
        self.renderer.display_starting_player(starting_player)

        while not self.player_manager.check_game_over():
            self.round_manager.play_round()

        winner = self.player_manager.get_winner()
        self.renderer.display_winner(winner)


if __name__ == "__main__":
    num_ai_players = int(
        input("¿Contra cuántos jugadores AI quieres jugar? (1-7): "))
    renderer = Renderer()
    game = Game(num_ai_players, renderer)
    game.start_game()
