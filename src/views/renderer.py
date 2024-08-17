from src.views.dice_renderer import DiceRenderer


class Renderer:
    def __init__(self):
        self.dice_renderer = DiceRenderer()

    def display_welcome_message(self):
        print("¡Bienvenido al juego de Cachos!")

    def display_players(self, players):
        print("\nJugadores:")
        for player in players:
            player_type = "Humano" if player.__class__.__name__ == "HumanPlayer" else "IA"
            print(f"{player.name} ({player_type}) - Dados: {len(player.dice)}")

    def display_starting_player(self, player):
        print(f"\n{player.name} comienza el juego.")

    def display_round_start(self):
        print("\n--- Nueva Ronda ---")

    def display_current_player(self, player):
        print(f"\nTurno de {player.name}")

    def display_dice(self, dice_values):
        dice_str = " ".join(self.dice_renderer.render(value)
                            for value in dice_values)
        print(f"Tus dados: {dice_str}")

    def display_bet(self, player, bet):
        quantity, value = bet
        print(f"{player.name} apuesta: {quantity} dados con valor {value}")

    def display_doubt_result(self, loser, actual_count, bet):
        quantity, value = bet
        print(f"¡Duda! Había {actual_count} dados con valor {value}")
        print(f"{loser.name} pierde un dado.")

    def display_calzo_success(self, player):
        print(f"¡Calzo exitoso! {player.name} gana un dado.")

    def display_calzo_failure(self, player):
        print(f"¡Calzo fallido! {player.name} pierde un dado.")

    def display_winner(self, player):
        print(f"\n¡{player.name} ha ganado el juego!")

    def display_action(self, player, action):
        print(f"{player.name} elige: {action}")

    def display_all_dice(self, players):
        print("\nDados de todos los jugadores:")
        for player in players:
            dice_str = " ".join(self.dice_renderer.render(value)
                                for value in player.get_dice_values())
            print(f"{player.name}: {dice_str}")

    def display_round_end(self, players):
        print("\nFin de la ronda. Estado de los jugadores:")
        for player in players:
            print(f"{player.name} - Dados: {len(player.dice)}")

    def display_error(self, message):
        print(f"\nError: {message}")
