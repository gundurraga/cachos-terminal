import logging
from typing import List, Optional
from src.models.player import Player
from src.models.human_player import HumanPlayer
from src.models.ai_player import AIPlayer
from src.utils.name_generator import NameGenerator
from src.views.input_handler import InputHandler

logger = logging.getLogger(__name__)


class PlayerManager:
    def __init__(self, num_ai_players: int, game: 'Game'):
        if not isinstance(num_ai_players, int) or num_ai_players < 0:
            raise ValueError(
                "El número de jugadores AI debe ser un entero no negativo.")

        self.name_generator: NameGenerator = NameGenerator()
        self.input_handler: InputHandler = InputHandler()
        self.game: 'Game' = game
        self.players: List[Player] = self._initialize_players(num_ai_players)
        self.current_player_index: int = 0

        logger.info(
            f"PlayerManager inicializado con {len(self.players)} jugadores.")

    def _initialize_players(self, num_ai_players: int) -> List[Player]:
        try:
            human_name: str = self.input_handler.get_player_name()
            players: List[Player] = [HumanPlayer(human_name)]

            for _ in range(num_ai_players):
                ai_name: str = self.name_generator.get_random_name()
                players.append(AIPlayer(f"{ai_name} (AI)", self.game))

            logger.info(
                f"Jugadores inicializados: {[player.name for player in players]}")
            return players
        except Exception as e:
            logger.error(f"Error al inicializar jugadores: {str(e)}")
            raise

    def get_current_player(self) -> Player:
        return self.players[self.current_player_index]

    def get_previous_player(self) -> Player:
        return self.players[(self.current_player_index - 1) % len(self.players)]

    def next_player(self) -> None:
        self.current_player_index = (
            self.current_player_index + 1) % len(self.players)
        logger.debug(
            f"Turno pasado al jugador: {self.get_current_player().name}")

    def determine_starting_player(self) -> Player:
        max_roll: int = 0
        starting_player: Optional[Player] = None

        for player in self.players:
            roll: int = max(player.roll_dice())
            if roll > max_roll:
                max_roll = roll
                starting_player = player

        if starting_player is None:
            raise RuntimeError("No se pudo determinar el jugador inicial.")

        self.current_player_index = self.players.index(starting_player)
        logger.info(f"Jugador inicial determinado: {starting_player.name}")
        return starting_player

    def check_game_over(self) -> bool:
        return sum(1 for player in self.players if player.dice) == 1

    def get_winner(self) -> Optional[Player]:
        for player in self.players:
            if player.dice:
                logger.info(f"Ganador determinado: {player.name}")
                return player
        logger.warning("No se pudo determinar un ganador.")
        return None

    def roll_all_dice(self) -> None:
        for player in self.players:
            player.roll_dice()
        logger.debug("Todos los jugadores han lanzado sus dados.")

    def reset_game(self) -> None:
        self.name_generator.reset()
        self.current_player_index = 0
        for player in self.players:
            player.reset()
        logger.info("Juego reiniciado.")
