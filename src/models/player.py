import logging
from typing import List, Tuple, Optional
from src.models.dice import Dice

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise ValueError(
                "El nombre del jugador debe ser una cadena no vacía.")
        self.name: str = name
        self.dice: List[Dice] = [Dice() for _ in range(5)]
        logger.info(
            f"Jugador '{self.name}' creado con {len(self.dice)} dados.")

    def roll_dice(self) -> List[int]:
        """
        Lanza todos los dados del jugador.

        :return: Lista de los valores obtenidos en los dados.
        """
        roll_results = [die.roll() for die in self.dice]
        logger.debug(f"{self.name} lanzó los dados: {roll_results}")
        return roll_results

    def get_dice_values(self) -> List[int]:
        """
        Obtiene los valores actuales de los dados del jugador.

        :return: Lista de los valores actuales de los dados.
        """
        return [die.value for die in self.dice]

    def remove_die(self) -> bool:
        """
        Elimina un dado del jugador.

        :return: True si se eliminó un dado, False si el jugador no tenía dados.
        """
        if self.dice:
            self.dice.pop()
            logger.info(
                f"{self.name} perdió un dado. Dados restantes: {len(self.dice)}")
            return True
        logger.warning(
            f"{self.name} intentó perder un dado, pero no tenía ninguno.")
        return False

    def add_die(self) -> None:
        """
        Añade un dado al jugador si tiene menos de 5 dados.
        """
        if len(self.dice) < 5:
            self.dice.append(Dice())
            logger.info(
                f"{self.name} ganó un dado. Dados actuales: {len(self.dice)}")
        else:
            logger.warning(
                f"{self.name} intentó ganar un dado, pero ya tenía el máximo (5).")

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        """
        Realiza una apuesta.

        :param current_bet: La apuesta actual (si existe).
        :param is_first_turn: Indica si es el primer turno de la ronda.
        :return: La nueva apuesta como una tupla (cantidad, valor) o None si no se hace apuesta.
        """
        raise NotImplementedError("Subclasses must implement make_bet method")

    def decide_action(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> str:
        """
        Decide la acción a tomar en el turno actual.

        :param current_bet: La apuesta actual (si existe).
        :param is_first_turn: Indica si es el primer turno de la ronda.
        :return: La acción decidida ('apostar', 'dudar' o 'calzar').
        """
        raise NotImplementedError(
            "Subclasses must implement decide_action method")

    def reset(self) -> None:
        """
        Reinicia el jugador a su estado inicial.
        """
        self.dice = [Dice() for _ in range(5)]
        logger.info(f"{self.name} ha sido reiniciado con 5 dados.")

    def __str__(self) -> str:
        return f"{self.name} (Dados: {len(self.dice)})"

    def __repr__(self) -> str:
        return f"Player(name='{self.name}', dice_count={len(self.dice)})"
