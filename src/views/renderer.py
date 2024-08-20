from rich.console import Console
from src.views.game_renderer import GameRenderer
from src.views.player_renderer import PlayerRenderer
from src.views.bet_renderer import BetRenderer


class Renderer:
    def __init__(self):
        self.console = Console()
        self.game_renderer = GameRenderer(self.console)
        self.player_renderer = PlayerRenderer(self.console)
        self.bet_renderer = BetRenderer(self.console)

    def display_welcome_message(self):
        self.game_renderer.display_welcome_message()

    def display_players(self, players, current_player_index):
        self.player_renderer.display_players(players, current_player_index)

    def display_current_player_dice(self, player):
        self.player_renderer.display_current_player_dice(player)

    def display_starting_player(self, player):
        self.player_renderer.display_starting_player(player)

    def display_round_start(self):
        self.game_renderer.display_round_start()

    def display_current_player(self, player):
        self.player_renderer.display_current_player(player)

    def display_bet(self, player, bet):
        self.bet_renderer.display_bet(player, bet)

    def display_round_result(self, action, player, bet, actual_count, success):
        self.bet_renderer.display_round_result(
            action, player, bet, actual_count, success)

    def display_winner(self, player):
        self.game_renderer.display_winner(player)

    def display_action(self, player, action):
        self.player_renderer.display_action(player, action)

    def display_all_dice(self, players):
        self.player_renderer.display_all_dice(players)

    def display_round_end(self, players):
        self.game_renderer.display_round_end(players)

    def display_error(self, message):
        self.game_renderer.display_error(message)

    def display_invalid_ai_bet(self, player):
        self.player_renderer.display_invalid_ai_bet(player)

    def display_ai_doubt(self, player):
        self.player_renderer.display_ai_doubt(player)
