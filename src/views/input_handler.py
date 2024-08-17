class InputHandler:
    def get_bet(self, current_bet):
        if current_bet:
            current_quantity, current_value = current_bet
        else:
            current_quantity, current_value = 0, 0

        while True:
            try:
                quantity = int(
                    input(f"Ingresa la cantidad de dados (mínimo {current_quantity}): "))
                if quantity >= current_quantity:
                    break
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
