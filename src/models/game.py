from src.models.player_manager import PlayerManager
from src.models.round_manager import RoundManager
from src.models.bet_manager import BetManager
from src.views.renderer import Renderer


class Game:
    def __init__(self, num_ai_players: int, renderer: Renderer):
        self.renderer = renderer
        self.player_manager = PlayerManager(num_ai_players, self)
        self.bet_manager = BetManager()
        self.round_manager = RoundManager(self.player_manager, self.renderer)

    def get_players(self):
        return self.player_manager.players

    def start_game(self):
        self.renderer.display_welcome_message()

        starting_player = self.player_manager.determine_starting_player()
        starting_player_index = self.player_manager.players.index(
            starting_player)

        self.renderer.display_starting_player(starting_player)
        self.renderer.display_players(
            self.player_manager.players, starting_player_index)

        while not self.player_manager.check_game_over():
            self.round_manager.play_round()

        winner = self.player_manager.get_winner()
        self.renderer.display_winner(winner)
