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
            current_quantity, current_value = 0, 1

        min_quantity = max(1, current_quantity)

        while True:
            try:
                quantity = int(
                    input(f"Ingresa la cantidad de dados (mínimo {min_quantity}): "))
                if quantity < min_quantity:
                    print(f"La cantidad debe ser al menos {min_quantity}.")
                else:
                    break
            except ValueError:
                print("Por favor, ingresa un número válido.")

        while True:
            try:
                value = int(input("Ingresa el valor de los dados (1-6): "))
                if 1 <= value <= 6:
                    if quantity == current_quantity and value <= current_value:
                        print(
                            f"Si mantienes la misma cantidad, el valor debe ser mayor que {current_value}.")
                    elif quantity < current_quantity and value != 1:
                        print(
                            "Solo puedes reducir la cantidad si cambias a ases (1).")
                    else:
                        break
                else:
                    print("El valor debe estar entre 1 y 6.")
            except ValueError:
                print("Por favor, ingresa un número válido.")

        return (quantity, value)

    def get_action(self, current_bet):
        valid_actions = ['apostar', 'dudar', 'calzar']
        while True:
            action = input(
                "¿Qué acción quieres realizar? (apostar/dudar/calzar): ").lower().strip()
            if action in valid_actions:
                return action
            print("Por favor, elige una acción válida (apostar, dudar o calzar).")
