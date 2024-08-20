from typing import List, Tuple, Optional
from rich.console import Console
from src.views.game_renderer import GameRenderer
from src.views.player_renderer import PlayerRenderer
from src.views.bet_renderer import BetRenderer
from src.models.player import Player
import logging

logger = logging.getLogger(__name__)


class Renderer:
    def __init__(self):
        self.console: Console = Console()
        self.game_renderer: GameRenderer = GameRenderer(self.console)
        self.player_renderer: PlayerRenderer = PlayerRenderer(self.console)
        self.bet_renderer: BetRenderer = BetRenderer(self.console)
        logger.info("Renderer inicializado")

    def display_welcome_message(self) -> None:
        logger.debug("Mostrando mensaje de bienvenida")
        self.game_renderer.display_welcome_message()

    def display_players(self, players: List[Player], current_player_index: int) -> None:
        logger.debug(
            f"Mostrando {len(players)} jugadores. Jugador actual: {current_player_index}")
        self.player_renderer.display_players(players, current_player_index)

    def display_current_player_dice(self, player: Player) -> None:
        logger.debug(f"Mostrando dados del jugador actual: {player.name}")
        self.player_renderer.display_current_player_dice(player)

    def display_starting_player(self, player: Player) -> None:
        logger.info(f"Jugador inicial: {player.name}")
        self.player_renderer.display_starting_player(player)

    def display_round_start(self) -> None:
        logger.debug("Iniciando nueva ronda")
        self.game_renderer.display_round_start()

    def display_current_player(self, player: Player) -> None:
        logger.debug(f"Turno del jugador: {player.name}")
        self.player_renderer.display_current_player(player)

    def display_bet(self, player: Player, bet: Tuple[int, int]) -> None:
        logger.debug(f"Mostrando apuesta de {player.name}: {bet}")
        self.bet_renderer.display_bet(player, bet)

    def display_round_result(self, action: str, player: Player, bet: Tuple[int, int], actual_count: int, success: bool) -> None:
        logger.info(
            f"Resultado de la ronda: {action} por {player.name}. Éxito: {success}")
        self.bet_renderer.display_round_result(
            action, player, bet, actual_count, success)

    def display_winner(self, player: Player) -> None:
        logger.info(f"Ganador del juego: {player.name}")
        self.game_renderer.display_winner(player)

    def display_action(self, player: Player, action: str) -> None:
        logger.debug(f"Acción de {player.name}: {action}")
        self.player_renderer.display_action(player, action)

    def display_all_dice(self, players: List[Player]) -> None:
        logger.debug("Mostrando todos los dados")
        self.player_renderer.display_all_dice(players)

    def display_round_end(self, players: List[Player]) -> None:
        logger.debug("Finalizando ronda")
        self.game_renderer.display_round_end(players)

    def display_error(self, message: str) -> None:
        logger.error(f"Error: {message}")
        self.game_renderer.display_error(message)

    def display_invalid_ai_bet(self, player: Player) -> None:
        logger.warning(f"Apuesta inválida de IA: {player.name}")
        self.player_renderer.display_invalid_ai_bet(player)

    def display_ai_doubt(self, player: Player) -> None:
        logger.info(f"IA decide dudar: {player.name}")
        self.player_renderer.display_ai_doubt(player)
