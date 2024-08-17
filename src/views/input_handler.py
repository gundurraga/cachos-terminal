from typing import Tuple, Optional


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
            current_quantity, current_value = 1, 1

        while True:
            try:
                quantity = int(
                    input(f"Ingresa la cantidad de dados (mínimo {current_quantity}): "))
                if quantity < current_quantity:
                    print(f"La cantidad debe ser al menos {current_quantity}.")
                else:
                    break
            except ValueError:
                print("Por favor, ingresa un número válido.")

        while True:
            try:
                value = int(input("Ingresa el valor de los dados (1-6): "))
                if 1 <= value <= 6:
                    break
                print("El valor debe estar entre 1 y 6.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

        return (quantity, value)

    def get_action(self, current_bet):
        actions = ['apostar', 'dudar', 'calzar']
        while True:
            action = input(
                "¿Qué acción quieres realizar? (subir/dudar/calzar): ").lower()
            if action in actions:
                return action
            print("Por favor, elige una acción válida.")
