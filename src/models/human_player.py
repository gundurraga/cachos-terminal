import logging
from typing import Tuple, Optional
from src.models.player import Player
from src.views.input_handler import InputHandler

logger = logging.getLogger(__name__)


class HumanPlayer(Player):
    def __init__(self, name: str):
        capitalized_name = ' '.join(word.capitalize() for word in name.split())
        super().__init__(capitalized_name)
        self.input_handler: InputHandler = InputHandler()
        logger.info(f"Jugador humano '{self.name}' inicializado.")

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        """
        Solicita una apuesta al jugador humano.

        :param current_bet: La apuesta actual (si existe).
        :param is_first_turn: Indica si es el primer turno de la ronda.
        :return: La nueva apuesta como una tupla (cantidad, valor) o None si no se hace apuesta.
        """
        try:
            new_bet = self.input_handler.get_bet(current_bet, is_first_turn)
            if new_bet:
                logger.info(f"{self.name} hizo una apuesta: {new_bet}")
            else:
                logger.info(f"{self.name} decidió no apostar.")
            return new_bet
        except ValueError as e:
            logger.error(
                f"Error al obtener la apuesta de {self.name}: {str(e)}")
            return None

    def decide_action(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> str:
        """
        Solicita al jugador humano que decida su acción.

        :param current_bet: La apuesta actual (si existe).
        :param is_first_turn: Indica si es el primer turno de la ronda.
        :return: La acción decidida ('apostar', 'dudar' o 'calzar').
        """
        if is_first_turn or current_bet is None:
            logger.info(
                f"{self.name} debe apostar en el primer turno o sin apuesta previa.")
            return 'apostar'

        try:
            action = self.input_handler.get_action(current_bet)
            logger.info(f"{self.name} decidió: {action}")
            return action
        except ValueError as e:
            logger.error(
                f"Error al obtener la acción de {self.name}: {str(e)}")
            return 'apostar'  # Default to 'apostar' if there's an error

    def __str__(self) -> str:
        return f"{self.name} (Jugador Humano - Dados: {len(self.dice)})"

    def __repr__(self) -> str:
        return f"HumanPlayer(name='{self.name}', dice_count={len(self.dice)})"
