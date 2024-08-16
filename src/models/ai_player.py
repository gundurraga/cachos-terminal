import random
from src.models.player import Player


class AIPlayer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def make_bet(self, current_bet):
        # Implementación simple de IA para hacer apuestas
        if current_bet is None:
            return (random.randint(1, 3), random.randint(1, 6))
        else:
            if random.random() < 0.7:  # 70% de probabilidad de subir la apuesta
                return (current_bet[0] + 1, current_bet[1])
            else:
                return None  # Dudar

    def decide_action(self, current_bet):
        # Implementación simple de IA para decidir acciones
        actions = ['subir', 'dudar', 'calzar']
        return random.choice(actions)
