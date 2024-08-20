from typing import Tuple, Optional
from src.models.bet_manager import BetManager
import logging

logger = logging.getLogger(__name__)


class InputHandler:
    def __init__(self):
        self.bet_manager: BetManager = BetManager()
        logger.info("InputHandler inicializado")

    def get_player_name(self) -> str:
        """
        Solicita y valida el nombre del jugador.

        Returns:
            str: El nombre del jugador validado.
        """
        while True:
            name = input("Por favor, ingresa tu nombre: ").strip()
            if name:
                logger.info(f"Nombre de jugador obtenido: {name}")
                return name
            logger.warning("Se ingresó un nombre vacío")
            print("El nombre no puede estar vacío. Por favor, intenta de nuevo.")

    def get_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        """
        Solicita y valida una apuesta del jugador.

        Args:
            current_bet (Optional[Tuple[int, int]]): La apuesta actual, si existe.
            is_first_turn (bool): Indica si es el primer turno de la ronda.

        Returns:
            Optional[Tuple[int, int]]: La nueva apuesta validada o None si hubo un error.
        """
        if current_bet:
            current_quantity, current_value = current_bet
        else:
            current_quantity, current_value = 0, 1

        while True:
            try:
                quantity = self._get_valid_int_input(
                    "Ingresa la cantidad de dados: ")
                value = self._get_valid_int_input(
                    "Ingresa el valor de los dados (1-6): ", 1, 6)

                new_bet = (quantity, value)

                if self.bet_manager.is_valid_bet(new_bet, is_first_turn):
                    logger.info(f"Apuesta válida obtenida: {new_bet}")
                    return new_bet
                else:
                    self._handle_invalid_bet(current_bet, new_bet)
            except ValueError as e:
                logger.error(f"Error al obtener la apuesta: {str(e)}")
                print("Por favor, ingresa números válidos.")

    def get_action(self, current_bet: Tuple[int, int]) -> str:
        """
        Solicita y valida una acción del jugador.

        Args:
            current_bet (Tuple[int, int]): La apuesta actual.

        Returns:
            str: La acción validada ('apostar', 'dudar' o 'calzar').
        """
        valid_actions = ['apostar', 'dudar', 'calzar']
        while True:
            action = input(
                "¿Qué acción quieres realizar? (apostar/dudar/calzar): ").lower().strip()
            if action in valid_actions:
                logger.info(f"Acción válida obtenida: {action}")
                return action
            logger.warning(f"Se ingresó una acción inválida: {action}")
            print("Por favor, elige una acción válida (apostar, dudar o calzar).")

    def _get_valid_int_input(self, prompt: str, min_value: int = 1, max_value: Optional[int] = None) -> int:
        """
        Solicita y valida una entrada de número entero.

        Args:
            prompt (str): El mensaje para solicitar la entrada.
            min_value (int): El valor mínimo permitido (inclusive).
            max_value (Optional[int]): El valor máximo permitido (inclusive), si se especifica.

        Returns:
            int: El número entero validado.

        Raises:
            ValueError: Si la entrada no es un número entero válido o está fuera del rango especificado.
        """
        while True:
            try:
                value = int(input(prompt))
                if value < min_value:
                    raise ValueError(f"El valor debe ser al menos {min_value}")
                if max_value is not None and value > max_value:
                    raise ValueError(
                        f"El valor debe ser como máximo {max_value}")
                return value
            except ValueError as e:
                logger.warning(f"Entrada inválida: {str(e)}")
                print(f"Entrada inválida. {str(e)}. Intenta de nuevo.")

    def _handle_invalid_bet(self, current_bet: Optional[Tuple[int, int]], new_bet: Tuple[int, int]) -> None:
        """
        Maneja el caso de una apuesta inválida.

        Args:
            current_bet (Optional[Tuple[int, int]]): La apuesta actual, si existe.
            new_bet (Tuple[int, int]): La nueva apuesta inválida.
        """
        quantity, value = new_bet
        if current_bet:
            current_quantity, current_value = current_bet
            if value == 1:
                min_quantity = self.bet_manager.calculate_equivalent_bet(
                    current_bet, 1)
                print(
                    f"Para apostar ases, la cantidad mínima es {min_quantity}.")
            elif current_value == 1:
                min_quantity = self.bet_manager.calculate_equivalent_bet(
                    current_bet, value)
                print(
                    f"Al subir desde ases, la cantidad mínima es {min_quantity}.")
            elif quantity < current_quantity:
                print("Solo puedes reducir la cantidad si cambias a ases (1).")
            else:
                print("Apuesta inválida. Intenta de nuevo.")
        else:
            print("Apuesta inválida. Intenta de nuevo.")
        logger.warning(f"Apuesta inválida: {new_bet}")
