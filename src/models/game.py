import logging
from typing import List, Optional
from src.models.player_manager import PlayerManager
from src.models.round_manager import RoundManager
from src.models.bet_manager import BetManager
from src.views.renderer import Renderer
from src.models.player import Player

# Configuración del logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Game:
    def __init__(self, num_ai_players: int, renderer: Renderer):
        self._validate_inputs(num_ai_players, renderer)

        self.renderer: Renderer = renderer
        self.player_manager: PlayerManager = PlayerManager(
            num_ai_players, self)
        self.bet_manager: BetManager = BetManager()
        self.round_manager: RoundManager = RoundManager(
            self.player_manager, self.renderer)
        logger.info(f"Juego inicializado con {num_ai_players} jugadores AI.")

    @staticmethod
    def _validate_inputs(num_ai_players: int, renderer: Renderer) -> None:
        if not isinstance(num_ai_players, int) or num_ai_players < 1:
            raise ValueError(
                "El número de jugadores AI debe ser un entero positivo.")
        if not isinstance(renderer, Renderer):
            raise TypeError(
                "El renderizador debe ser una instancia de Renderer.")

    def get_players(self) -> List[Player]:
        return self.player_manager.players

    def start_game(self) -> None:
        try:
            logger.info("Iniciando el juego.")
            self.renderer.display_welcome_message()

            starting_player: Player = self.player_manager.determine_starting_player()
            starting_player_index: int = self.player_manager.players.index(
                starting_player)

            self.renderer.display_starting_player(starting_player)
            self.renderer.display_players(
                self.player_manager.players, starting_player_index)

            while not self.player_manager.check_game_over():
                self.round_manager.play_round()

            self._handle_game_end()

        except Exception as e:
            logger.error(f"Error inesperado durante el juego: {str(e)}")
            self.renderer.display_error(
                f"Ha ocurrido un error inesperado: {str(e)}")

    def _handle_game_end(self) -> None:
        winner: Optional[Player] = self.player_manager.get_winner()
        if winner:
            self.renderer.display_winner(winner)
            logger.info(f"Juego terminado. Ganador: {winner.name}")
        else:
            logger.error("El juego terminó sin un ganador.")
            self.renderer.display_error("El juego terminó sin un ganador.")
