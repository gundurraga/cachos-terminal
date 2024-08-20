import logging
from typing import Tuple, Optional, List

logger = logging.getLogger(__name__)


class BetManager:
    def __init__(self):
        self.current_bet: Optional[Tuple[int, int]] = None
        logger.info("BetManager inicializado")

    def set_bet(self, bet: Tuple[int, int]) -> None:
        """
        Establece la apuesta actual.

        :param bet: Una tupla (cantidad, valor) representando la apuesta
        """
        if not isinstance(bet, tuple) or len(bet) != 2 or not all(isinstance(x, int) for x in bet):
            raise ValueError("La apuesta debe ser una tupla de dos enteros")
        self.current_bet = bet
        logger.info(f"Nueva apuesta establecida: {bet}")

    def get_bet(self) -> Optional[Tuple[int, int]]:
        """
        Obtiene la apuesta actual.

        :return: La apuesta actual o None si no hay apuesta
        """
        return self.current_bet

    def reset_bet(self) -> None:
        """Reinicia la apuesta actual a None."""
        self.current_bet = None
        logger.info("Apuesta reiniciada")

    def is_valid_bet(self, new_bet: Tuple[int, int], is_first_turn: bool) -> bool:
        """
        Verifica si una nueva apuesta es válida según las reglas del juego.

        :param new_bet: La nueva apuesta a verificar
        :param is_first_turn: Indica si es el primer turno de la ronda
        :return: True si la apuesta es válida, False en caso contrario
        """
        if not isinstance(new_bet, tuple) or len(new_bet) != 2 or not all(isinstance(x, int) for x in new_bet):
            logger.warning(f"Apuesta inválida: {new_bet}")
            return False

        new_quantity, new_value = new_bet

        if new_value < 1 or new_value > 6:
            logger.warning(f"Valor de dados inválido: {new_value}")
            return False

        if new_quantity < 1:
            logger.warning(f"Cantidad de dados inválida: {new_quantity}")
            return False

        if is_first_turn:
            logger.info(f"Apuesta válida en el primer turno: {new_bet}")
            return True

        if self.current_bet is None:
            logger.info(f"Primera apuesta de la ronda válida: {new_bet}")
            return True

        current_quantity, current_value = self.current_bet

        if new_value == 1:  # Apuesta de ases
            if new_quantity < (current_quantity + 1) // 2:
                logger.warning(f"Apuesta de ases inválida: {new_bet}")
                return False
        elif current_value == 1:  # Subiendo desde ases
            if new_quantity < current_quantity * 2 + 1:
                logger.warning(
                    f"Apuesta subiendo desde ases inválida: {new_bet}")
                return False
        else:
            if new_quantity < current_quantity or (new_quantity == current_quantity and new_value <= current_value):
                logger.warning(f"Apuesta inválida: {new_bet}")
                return False

        logger.info(f"Apuesta válida: {new_bet}")
        return True

    def calculate_equivalent_bet(self, current_bet: Tuple[int, int], new_pinta: int) -> int:
        """
        Calcula la cantidad equivalente de dados al cambiar de pinta.

        :param current_bet: La apuesta actual
        :param new_pinta: El nuevo valor de dados
        :return: La cantidad equivalente de dados
        """
        if not isinstance(current_bet, tuple) or len(current_bet) != 2 or not all(isinstance(x, int) for x in current_bet):
            raise ValueError(
                "La apuesta actual debe ser una tupla de dos enteros")
        if not isinstance(new_pinta, int) or new_pinta < 1 or new_pinta > 6:
            raise ValueError("La nueva pinta debe ser un entero entre 1 y 6")

        current_quantity, current_value = current_bet
        if new_pinta == 1:  # Bajando a ases
            return (current_quantity + 1) // 2
        elif current_value == 1:  # Subiendo desde ases
            return current_quantity * 2 + 1
        else:
            return current_quantity

    @staticmethod
    def count_dice(dice_values: List[int], bet_value: int) -> int:
        """
        Cuenta la cantidad de dados que coinciden con el valor apostado.

        :param dice_values: Lista de valores de dados
        :param bet_value: Valor apostado
        :return: Cantidad de dados que coinciden con la apuesta
        """
        if not isinstance(dice_values, list) or not all(isinstance(x, int) and 1 <= x <= 6 for x in dice_values):
            raise ValueError(
                "dice_values debe ser una lista de enteros entre 1 y 6")
        if not isinstance(bet_value, int) or bet_value < 1 or bet_value > 6:
            raise ValueError("bet_value debe ser un entero entre 1 y 6")

        if bet_value == 1:
            return sum(1 for value in dice_values if value == 1)
        else:
            return sum(1 for value in dice_values if value == bet_value or value == 1)
