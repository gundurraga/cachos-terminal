import random
import time
from src.models.player import Player
from typing import Tuple, Optional


class AIPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:

        if is_first_turn or current_bet is None:
            return (random.randint(1, 3), random.randint(1, 6))
        else:
            current_quantity, current_value = current_bet
            new_quantity = current_quantity + \
                random.randint(1, 2)  # Siempre aumenta la cantidad
            new_value = random.randint(max(current_value, 1), 6)
            return (new_quantity, new_value)

    def decide_action(self, current_bet, is_first_turn: bool):
        self._simulate_thinking()
        if is_first_turn or current_bet is None:
            return 'apostar'
        # 80% de probabilidad de apostar, 20% de dudar
        return 'apostar' if random.random() < 0.8 else 'dudar'

    def _simulate_thinking(self):
        thinking_time = random.uniform(2, 5)
        time.sleep(thinking_time)
