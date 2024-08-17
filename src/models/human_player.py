from src.models.player import Player
from src.views.input_handler import InputHandler
from typing import Tuple, Optional


class HumanPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.input_handler = InputHandler()

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        return self.input_handler.get_bet(current_bet, is_first_turn)

    def decide_action(self, current_bet):
        return self.input_handler.get_action(current_bet)
