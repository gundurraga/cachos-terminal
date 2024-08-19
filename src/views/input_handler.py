from typing import Tuple, Optional
from src.models.bet_manager import BetManager


class InputHandler:
    def get_player_name(self) -> str:
        while True:
            name = input("Por favor, ingresa tu nombre: ").strip()
            if name:
                return name
            print("El nombre no puede estar vacío. Por favor, intenta de nuevo.")

    def get_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        if current_bet:
            current_quantity, current_value = current_bet
        else:
            current_quantity, current_value = 0, 1

        bet_manager = BetManager()

        while True:
            try:
                quantity = int(input(f"Ingresa la cantidad de dados: "))
                value = int(input("Ingresa el valor de los dados (1-6): "))

                new_bet = (quantity, value)

                if bet_manager.is_valid_bet(new_bet, is_first_turn):
                    return new_bet
                else:
                    if value == 1:
                        print(
                            f"Para apostar ases, la cantidad mínima es {bet_manager.calculate_equivalent_bet(current_bet, 1)}.")
                    elif current_value == 1:
                        print(
                            f"Al subir desde ases, la cantidad mínima es {bet_manager.calculate_equivalent_bet(current_bet, value)}.")
                    elif quantity < current_quantity:
                        print(
                            "Solo puedes reducir la cantidad si cambias a ases (1).")
                    else:
                        print("Apuesta inválida. Intenta de nuevo.")
            except ValueError:
                print("Por favor, ingresa números válidos.")

    def get_action(self, current_bet):
        valid_actions = ['apostar', 'dudar', 'calzar']
        while True:
            action = input(
                "¿Qué acción quieres realizar? (apostar/dudar/calzar): ").lower().strip()
            if action in valid_actions:
                return action
            print("Por favor, elige una acción válida (apostar, dudar o calzar).")
