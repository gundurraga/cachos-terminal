from typing import List, Tuple, Optional
from src.models.player import Player
from src.models.human_player import HumanPlayer  # Añadimos esta importación
from src.models.player_manager import PlayerManager
from src.models.bet_manager import BetManager
from src.views.renderer import Renderer


class RoundManager:
    def __init__(self, player_manager: PlayerManager, renderer: Renderer):
        self.player_manager = player_manager
        self.renderer = renderer
        self.bet_manager = BetManager()
        self.is_first_turn = True

    def play_round(self):
        self.renderer.display_round_start()
        self.player_manager.roll_all_dice()
        self.bet_manager.reset_bet()

        round_over = False
        while not round_over:
            current_player = self.player_manager.get_current_player()
            self.renderer.display_current_player(current_player)

            if isinstance(current_player, HumanPlayer):
                self.renderer.display_dice(current_player.get_dice_values())

            if self.is_first_turn:
                self.renderer.display_first_turn_message()
                action = 'apostar'
            else:
                action = self.get_player_action(current_player)

            self.renderer.display_action(current_player, action)

            if action == 'dudar':
                round_over = self.handle_doubt()
            elif action == 'calzar':
                round_over = self.handle_calzo(current_player)
            else:  # subir
                round_over = self.handle_raise(current_player)

            if not round_over:
                self.player_manager.next_player()
                self.is_first_turn = False

        self.renderer.display_round_end(self.player_manager.players)

    def get_player_action(self, player: Player) -> str:
        current_bet = self.bet_manager.get_bet()
        action = player.decide_action(current_bet, self.is_first_turn)

        if current_bet is None and action != 'apostar':
            self.renderer.display_error("No hay apuesta previa. Debes subir.")
            return 'apostar'

        return action

    def handle_doubt(self) -> bool:
        if self.bet_manager.get_bet() is None:
            self.renderer.display_error(
                "No se puede dudar sin una apuesta previa.")
            return False

        bet_quantity, bet_value = self.bet_manager.get_bet()
        total_count = sum(
            dice_value == bet_value
            for player in self.player_manager.players
            for dice_value in player.get_dice_values()
        )

        self.renderer.display_all_dice(self.player_manager.players)

        if total_count >= bet_quantity:
            loser = self.player_manager.get_current_player()
        else:
            loser = self.player_manager.get_previous_player()

        loser.remove_die()
        self.renderer.display_doubt_result(
            loser, total_count, self.bet_manager.get_bet())
        return True

    def handle_calzo(self, player: Player) -> bool:
        if self.bet_manager.get_bet() is None:
            self.renderer.display_error(
                "No se puede calzar sin una apuesta previa.")
            return False

        bet_quantity, bet_value = self.bet_manager.get_bet()
        total_count = sum(
            dice_value == bet_value
            for p in self.player_manager.players
            for dice_value in p.get_dice_values()
        )

        self.renderer.display_all_dice(self.player_manager.players)

        if total_count == bet_quantity:
            player.add_die()
            self.renderer.display_calzo_success(player)
        else:
            player.remove_die()
            self.renderer.display_calzo_failure(player)
        return True

    def handle_raise(self, player: Player) -> bool:
        new_bet = player.make_bet(
            self.bet_manager.get_bet(), self.is_first_turn)
        if new_bet and self.bet_manager.is_valid_bet(new_bet, self.is_first_turn):
            self.bet_manager.set_bet(new_bet)
            self.renderer.display_bet(player, new_bet)
            return False
        else:
            self.renderer.display_error("Apuesta inválida.")
            return False
