from src.models.player import Player
from src.views.input_handler import InputHandler


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.input_handler = InputHandler()

    def make_bet(self, current_bet):
        # Implementación para que el jugador humano haga una apuesta
        return self.input_handler.get_bet(current_bet)

    def decide_action(self, current_bet):
        # Implementación para que el jugador humano decida su acción
        return self.input_handler.get_action(current_bet)
