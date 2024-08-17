from typing import List, Tuple, Optional
from src.models.dice import Dice


class Player:
    def __init__(self, name: str):
        self.name = name
        self.dice: List[Dice] = [Dice() for _ in range(5)]

    def roll_dice(self) -> List[int]:
        return [die.roll() for die in self.dice]

    def get_dice_values(self) -> List[int]:
        return [die.value for die in self.dice]

    def remove_die(self) -> bool:
        if self.dice:
            self.dice.pop()
            return True
        return False

    def add_die(self) -> None:
        if len(self.dice) < 5:
            self.dice.append(Dice())

    def make_bet(self, current_bet: Optional[Tuple[int, int]], is_first_turn: bool) -> Optional[Tuple[int, int]]:
        raise NotImplementedError("Subclasses must implement make_bet method")

    def __str__(self) -> str:
        return f"{self.name} (Dice: {len(self.dice)})"
