import logging
from typing import List, Tuple, Optional
from src.models.player import Player
from src.models.human_player import HumanPlayer
from src.models.ai_player import AIPlayer
from src.models.player_manager import PlayerManager
from src.models.bet_manager import BetManager
from src.views.renderer import Renderer

logger = logging.getLogger(__name__)


class RoundManager:
    def __init__(self, player_manager: PlayerManager, renderer: Renderer):
        self.player_manager: PlayerManager = player_manager
        self.renderer: Renderer = renderer
        self.bet_manager: BetManager = BetManager()
        self.is_first_turn: bool = True
        self.last_player: Optional[Player] = None
        self.last_bet: Optional[Tuple[int, int]] = None

    def play_round(self) -> None:
        try:
            logger.info("Iniciando nueva ronda")
            self.renderer.display_round_start()
            self.player_manager.roll_all_dice()
            self.bet_manager.reset_bet()
            self.last_player = None
            self.last_bet = None

            round_over: bool = False
            while not round_over:
                current_player: Player = self.player_manager.get_current_player()
                current_player_index: int = self.player_manager.current_player_index
                self.renderer.display_players(
                    self.player_manager.players, current_player_index, self.last_player, self.last_bet)
                self.renderer.display_current_player(current_player)

                if isinstance(current_player, HumanPlayer):
                    self.renderer.display_current_player_dice(current_player)

                action: str = self.get_player_action(current_player)
                self.renderer.display_action(current_player, action)

                if action == 'dudar':
                    round_over = self.handle_doubt()
                elif action == 'calzar':
                    round_over = self.handle_calzo(current_player)
                else:  # apostar
                    round_over = self.handle_raise(current_player)

                if not round_over:
                    self.last_player = current_player
                    self.last_bet = self.bet_manager.get_bet()
                    self.player_manager.next_player()
                    self.is_first_turn = False

            self.renderer.display_round_end(self.player_manager.players)
            logger.info("Ronda finalizada")
        except Exception as e:
            logger.error(f"Error durante la ronda: {str(e)}")
            self.renderer.display_error(
                f"Ha ocurrido un error durante la ronda: {str(e)}")

    def get_player_action(self, player: Player) -> str:
        current_bet: Optional[Tuple[int, int]] = self.bet_manager.get_bet()
        action: str = player.decide_action(current_bet, self.is_first_turn)

        if self.is_first_turn and action != 'apostar':
            logger.warning(f"Acción inválida en el primer turno: {action}")
            self.renderer.display_error("En el primer turno, debes apostar.")
            return 'apostar'

        if current_bet is None and action != 'apostar':
            logger.warning(f"Acción inválida sin apuesta previa: {action}")
            self.renderer.display_error(
                "No hay apuesta previa. Debes apostar.")
            return 'apostar'

        return action

    def handle_raise(self, player: Player) -> bool:
        max_attempts: int = 5
        for attempt in range(max_attempts):
            new_bet: Optional[Tuple[int, int]] = player.make_bet(
                self.bet_manager.get_bet(), self.is_first_turn)
            if new_bet and self.bet_manager.is_valid_bet(new_bet, self.is_first_turn):
                current_bet: Optional[Tuple[int, int]
                                      ] = self.bet_manager.get_bet()
                if current_bet and new_bet[1] == 1 and current_bet[1] != 1:
                    # Cambiando a ases
                    min_quantity: int = self.bet_manager.calculate_equivalent_bet(
                        current_bet, 1)
                    if new_bet[0] < min_quantity:
                        if isinstance(player, AIPlayer):
                            logger.warning(
                                f"Apuesta inválida de AI: {new_bet}")
                            self.renderer.display_invalid_ai_bet(player)
                        else:
                            self.renderer.display_error(
                                f"Al cambiar a ases, la cantidad mínima es {min_quantity}.")
                        continue
                self.bet_manager.set_bet(new_bet)
                self.renderer.display_bet(player, new_bet)
                logger.info(
                    f"Nueva apuesta: {player.name} apuesta {new_bet[0]} {new_bet[1]}s")
                return False
            elif isinstance(player, AIPlayer):
                logger.warning(f"Apuesta inválida de AI: {new_bet}")
                self.renderer.display_invalid_ai_bet(player)
            else:
                self.renderer.display_error(
                    "Apuesta inválida. Intenta de nuevo.")

        if isinstance(player, AIPlayer):
            logger.info(
                f"AI {player.name} no pudo hacer una apuesta válida, decide dudar")
            self.renderer.display_ai_doubt(player)
            return self.handle_doubt()
        else:
            logger.warning(
                f"Jugador {player.name} hizo demasiados intentos inválidos")
            self.renderer.display_error(
                "Demasiados intentos inválidos. Pierdes un dado.")
            player.remove_die()
            return True

    def handle_doubt(self) -> bool:
        current_bet: Optional[Tuple[int, int]] = self.bet_manager.get_bet()
        if current_bet is None:
            logger.warning("Intento de duda sin apuesta previa")
            self.renderer.display_error(
                "No se puede dudar sin una apuesta previa.")
            return False

        bet_quantity, bet_value = current_bet
        all_dice: List[int] = [
            dice for player in self.player_manager.players for dice in player.get_dice_values()]
        total_count: int = self.bet_manager.count_dice(all_dice, bet_value)

        self.renderer.display_all_dice(self.player_manager.players)

        doubter: Player = self.player_manager.get_current_player()
        doubted: Player = self.player_manager.get_previous_player()

        if total_count >= bet_quantity:
            loser: Player = doubter
            success: bool = False
        else:
            loser: Player = doubted
            success: bool = True

        loser.remove_die()

        logger.info(
            f"Duda: {doubter.name} dudó a {doubted.name}. Resultado: {'éxito' if success else 'fracaso'}")
        self.renderer.display_round_result(
            'doubt', (doubter, doubted), (bet_quantity, bet_value), total_count, success)
        return True

    def handle_calzo(self, player: Player) -> bool:
        current_bet: Optional[Tuple[int, int]] = self.bet_manager.get_bet()
        if current_bet is None:
            logger.warning("Intento de calzo sin apuesta previa")
            self.renderer.display_error(
                "No se puede calzar sin una apuesta previa.")
            return False

        all_dice: List[int] = [
            dice for p in self.player_manager.players for dice in p.get_dice_values()]
        total_count: int = self.bet_manager.count_dice(
            all_dice, current_bet[1])

        success: bool = total_count == current_bet[0]
        if success:
            player.add_die()
        else:
            player.remove_die()

        logger.info(
            f"Calzo: {player.name} calzó. Resultado: {'éxito' if success else 'fracaso'}")
        self.renderer.display_round_result(
            'calzo', player, current_bet, total_count, success)
        return True
