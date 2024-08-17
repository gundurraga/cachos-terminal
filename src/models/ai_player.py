import random
import time
from src.models.player import Player
from typing import Tuple, Optional


class AIPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        self._simulate_thinking()
        if is_first_turn or current_bet is None:
            return (random.randint(1, 3), random.randint(1, 6))
        else:
            if random.random() < 0.7:  # 70% de probabilidad de subir la apuesta
                return (current_bet[0] + 1, current_bet[1])
            else:
                return None  # Dudar

    def decide_action(self, current_bet, is_first_turn: bool):
        self._simulate_thinking()
        if is_first_turn:
            return 'apostar'
        if current_bet is None:
            return 'apostar'  # Si no hay apuesta previa, siempre subir
        actions = ['apostar', 'dudar', 'calzar']
        return random.choice(actions)

    def _simulate_thinking(self):
        thinking_time = random.uniform(2, 6)
        time.sleep(thinking_time)
