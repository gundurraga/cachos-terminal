from typing import Tuple, Optional


class InputHandler:
    def get_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        if current_bet:
            current_quantity, current_value = current_bet
        else:
            current_quantity, current_value = (1 if is_first_turn else 0), 0

        while True:
            try:
                quantity = int(input(
                    f"Ingresa la cantidad de dados (mínimo {'1' if is_first_turn else str(current_quantity)}): "))
                if is_first_turn and quantity < 1:
                    print("En el primer turno, la apuesta mínima es 1 dado.")
                elif quantity >= current_quantity:
                    break
                else:
                    print(f"La cantidad debe ser al menos {current_quantity}.")
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
        actions = ['subir', 'dudar', 'calzar']
        while True:
            action = input(
                "¿Qué acción quieres realizar? (subir/dudar/calzar): ").lower()
            if action in actions:
                return action
            print("Por favor, elige una acción válida.")
