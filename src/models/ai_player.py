import random
import time
from src.models.player import Player
from src.models.bet_manager import BetManager
from typing import Tuple, Optional


class AIPlayer(Player):
    def __init__(self, name: str, game):
        super().__init__(name)
        self.bet_manager = BetManager()
        self.game = game

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        if is_first_turn or current_bet is None:
            return self._make_initial_bet()
        else:
            return self._make_subsequent_bet(current_bet)

    def _make_initial_bet(self) -> Tuple[int, int]:
        dice_counts = self._count_own_dice()
        most_common_value = max(dice_counts, key=dice_counts.get)
        quantity = dice_counts[most_common_value] + random.randint(0, 2)
        return (quantity, most_common_value)

    def _make_subsequent_bet(self, current_bet: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        current_quantity, current_value = current_bet
        dice_counts = self._count_own_dice()
        total_dice = sum(len(player.dice)
                         for player in self.game.get_players())

        probability = self._estimate_probability(
            current_quantity, current_value, dice_counts, total_dice)

        if probability < 0.3:
            return None  # Indica que el AI quiere dudar
        elif probability > 0.7:
            new_quantity = current_quantity + random.randint(1, 2)
            return (new_quantity, current_value)
        else:
            if random.random() < 0.5:
                new_value = random.choice(
                    [v for v in range(1, 7) if v != current_value])
                return (current_quantity, new_value)
            else:
                return (current_quantity + 1, current_value)

    def _count_own_dice(self) -> dict:
        return {i: self.get_dice_values().count(i) for i in range(1, 7)}

    def _estimate_probability(self, quantity: int, value: int, dice_counts: dict, total_dice: int) -> float:
        expected_count = quantity / total_dice * 6
        actual_count = dice_counts[value] + dice_counts[1]
        return actual_count / expected_count

    def decide_action(self, current_bet, is_first_turn: bool):
        self._simulate_thinking()
        if is_first_turn or current_bet is None:
            return 'apostar'

        dice_counts = self._count_own_dice()
        total_dice = sum(len(player.dice)
                         for player in self.game.get_players())
        probability = self._estimate_probability(
            current_bet[0], current_bet[1], dice_counts, total_dice)

        if probability < 0.3:
            return 'dudar'
        elif probability > 0.9 and random.random() < 0.3:
            return 'calzar'
        else:
            return 'apostar'

    def _simulate_thinking(self):
        thinking_time = random.uniform(1, 3)
        time.sleep(thinking_time)
