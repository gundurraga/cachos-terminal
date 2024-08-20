import random
import time
import logging
from typing import Tuple, Optional, Dict, List
from src.models.player import Player
from src.models.bet_manager import BetManager

logger = logging.getLogger(__name__)


class AIPlayer(Player):
    def __init__(self, name: str, game: 'Game'):
        super().__init__(name)
        self.bet_manager: BetManager = BetManager()
        self.game: 'Game' = game
        self.risk_factor: float = random.uniform(
            0.9, 1.1)  # Personalidad del AI
        logger.info(
            f"Jugador AI '{self.name}' inicializado con factor de riesgo {self.risk_factor:.2f}.")

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        if is_first_turn or current_bet is None:
            return self._make_initial_bet()
        else:
            return self._make_subsequent_bet(current_bet)

    def _make_initial_bet(self) -> Tuple[int, int]:
        dice_counts = self._count_own_dice()
        most_common_value = max(dice_counts, key=dice_counts.get)
        # Aseguramos una apuesta mínima de 1
        quantity = max(dice_counts[most_common_value], 1)
        bet = (quantity, most_common_value)
        logger.info(f"{self.name} hace una apuesta inicial: {bet}")
        return bet

    def _make_subsequent_bet(self, current_bet: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        self._simulate_thinking()
        current_quantity, current_value = current_bet
        dice_counts = self._count_own_dice()
        total_dice = sum(len(player.dice)
                         for player in self.game.get_players())
        other_dice = total_dice - sum(dice_counts.values())

        estimated_count = self._estimate_dice_count(
            current_value, dice_counts, other_dice)
        probability = estimated_count / current_quantity

        if probability < 0.8 * self.risk_factor:
            logger.info(
                f"{self.name} decide dudar con probabilidad estimada {probability:.2f}")
            return None  # Indica que el AI quiere dudar
        elif probability > 1.2 * self.risk_factor:
            new_quantity = min(current_quantity +
                               random.randint(1, 2), total_dice)
            new_bet = (new_quantity, current_value)
            logger.info(
                f"{self.name} aumenta la apuesta a {new_bet} con probabilidad estimada {probability:.2f}")
            return new_bet
        else:
            if random.random() < 0.4:
                new_value = self._choose_strategic_value(
                    current_value, dice_counts)
                new_quantity = self._calculate_equivalent_quantity(
                    current_quantity, current_value, new_value, total_dice)
                new_bet = (new_quantity, new_value)
                logger.info(
                    f"{self.name} cambia estratégicamente la apuesta a {new_bet}")
                return new_bet
            else:
                new_bet = (current_quantity + 1, current_value)
                logger.info(
                    f"{self.name} aumenta ligeramente la apuesta a {new_bet}")
                return new_bet

    def _count_own_dice(self) -> Dict[int, int]:
        return {i: self.get_dice_values().count(i) for i in range(1, 7)}

    def _estimate_dice_count(self, value: int, dice_counts: Dict[int, int], other_dice: int) -> float:
        own_count = dice_counts[value] + \
            dice_counts[1]  # Contar ases como comodines
        estimated_others = other_dice / \
            3 if value != 1 else other_dice / 6  # Ajuste para ases
        return own_count + estimated_others

    def _choose_strategic_value(self, current_value: int, dice_counts: Dict[int, int]) -> int:
        if current_value == 1:
            # Elige el valor más común en los dados propios
            return max(dice_counts, key=dice_counts.get)
        else:
            possible_values = [v for v in range(2, 7) if dice_counts[v] > 0]
            return random.choice(possible_values) if possible_values else random.randint(2, 6)

    def _calculate_equivalent_quantity(self, current_quantity: int, current_value: int, new_value: int, total_dice: int) -> int:
        if current_value == 1 and new_value != 1:
            return min(current_quantity * 2 + 1, total_dice)
        elif current_value != 1 and new_value == 1:
            return max((current_quantity + 1) // 2, 1)
        else:
            return current_quantity

    def decide_action(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> str:
        self._simulate_thinking()
        if is_first_turn or current_bet is None:
            logger.info(
                f"{self.name} decide apostar en el primer turno o sin apuesta previa.")
            return 'apostar'

        dice_counts = self._count_own_dice()
        total_dice = sum(len(player.dice)
                         for player in self.game.get_players())
        other_dice = total_dice - sum(dice_counts.values())
        estimated_count = self._estimate_dice_count(
            current_bet[1], dice_counts, other_dice)
        probability = estimated_count / current_bet[0]

        if probability < 0.8 * self.risk_factor:
            logger.info(
                f"{self.name} decide dudar con probabilidad estimada {probability:.2f}")
            return 'dudar'
        elif probability > 1.2 * self.risk_factor and random.random() < 0.3:
            logger.info(
                f"{self.name} decide calzar con probabilidad estimada {probability:.2f}")
            return 'calzar'
        else:
            logger.info(
                f"{self.name} decide apostar con probabilidad estimada {probability:.2f}")
            return 'apostar'

    def _simulate_thinking(self) -> None:
        thinking_time = random.uniform(3, 6)
        time.sleep(thinking_time)
        logger.debug(
            f"{self.name} 'pensó' durante {thinking_time:.2f} segundos")

    def __str__(self) -> str:
        return f"{self.name} (Jugador AI - Dados: {len(self.dice)}, Factor de riesgo: {self.risk_factor:.2f})"

    def __repr__(self) -> str:
        return f"AIPlayer(name='{self.name}', dice_count={len(self.dice)}, risk_factor={self.risk_factor:.2f})"
