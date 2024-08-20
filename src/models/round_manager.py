from typing import List, Tuple, Optional
from src.models.player import Player
from src.models.human_player import HumanPlayer
from src.models.ai_player import AIPlayer
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
            current_player_index = self.player_manager.current_player_index
            self.renderer.display_players(
                self.player_manager.players, current_player_index)
            self.renderer.display_current_player(current_player)

            if isinstance(current_player, HumanPlayer):
                self.renderer.display_current_player_dice(current_player)

            action = self.get_player_action(current_player)
            self.renderer.display_action(current_player, action)

            if action == 'dudar':
                round_over = self.handle_doubt()
            elif action == 'calzar':
                round_over = self.handle_calzo(current_player)
            else:  # apostar
                round_over = self.handle_raise(current_player)

            if not round_over:
                self.player_manager.next_player()
                self.is_first_turn = False

        self.renderer.display_round_end(self.player_manager.players)

    def get_player_action(self, player: Player) -> str:
        current_bet = self.bet_manager.get_bet()
        action = player.decide_action(current_bet, self.is_first_turn)

        if self.is_first_turn and action != 'apostar':
            self.renderer.display_error("En el primer turno, debes apostar.")
            return 'apostar'

        if current_bet is None and action != 'apostar':
            self.renderer.display_error(
                "No hay apuesta previa. Debes apostar.")
            return 'apostar'

        return action

    def handle_raise(self, player: Player) -> bool:
        max_attempts = 5
        for _ in range(max_attempts):
            new_bet = player.make_bet(
                self.bet_manager.get_bet(), self.is_first_turn)
            if new_bet and self.bet_manager.is_valid_bet(new_bet, self.is_first_turn):
                current_bet = self.bet_manager.get_bet()
                if current_bet and new_bet[1] == 1 and current_bet[1] != 1:
                    # Cambiando a ases
                    min_quantity = self.bet_manager.calculate_equivalent_bet(
                        current_bet, 1)
                    if new_bet[0] < min_quantity:
                        if isinstance(player, AIPlayer):
                            self.renderer.display_invalid_ai_bet(player)
                        else:
                            self.renderer.display_error(
                                f"Al cambiar a ases, la cantidad mínima es {min_quantity}.")
                        continue
                self.bet_manager.set_bet(new_bet)
                self.renderer.display_bet(player, new_bet)
                return False
            elif isinstance(player, AIPlayer):
                self.renderer.display_invalid_ai_bet(player)
            else:
                self.renderer.display_error(
                    "Apuesta inválida. Intenta de nuevo.")

        if isinstance(player, AIPlayer):
            self.renderer.display_ai_doubt(player)
            return self.handle_doubt()
        else:
            self.renderer.display_error(
                "Demasiados intentos inválidos. Pierdes un dado.")
            player.remove_die()
            return True

    def handle_doubt(self) -> bool:
        if self.bet_manager.get_bet() is None:
            self.renderer.display_error(
                "No se puede dudar sin una apuesta previa.")
            return False

        bet_quantity, bet_value = self.bet_manager.get_bet()
        all_dice = [
            dice for player in self.player_manager.players for dice in player.get_dice_values()]
        total_count = self.bet_manager.count_dice(all_dice, bet_value)

        self.renderer.display_all_dice(self.player_manager.players)

        doubter = self.player_manager.get_current_player()
        doubted = self.player_manager.get_previous_player()

        if total_count >= bet_quantity:
            loser = doubter
            success = False
        else:
            loser = doubted
            success = True

        loser.remove_die()

        self.renderer.display_round_result(
            'doubt', (doubter, doubted), (bet_quantity, bet_value), total_count, success)
        return True

    def handle_calzo(self, player: Player) -> bool:
        if self.bet_manager.get_bet() is None:
            self.renderer.display_error(
                "No se puede calzar sin una apuesta previa.")
            return False

        bet = self.bet_manager.get_bet()
        all_dice = [
            dice for p in self.player_manager.players for dice in p.get_dice_values()]
        total_count = self.bet_manager.count_dice(all_dice, bet[1])

        success = total_count == bet[0]
        if success:
            player.add_die()
        else:
            player.remove_die()

        self.renderer.display_round_result(
            'calzo', player, bet, total_count, success)
        return True
