from typing import Tuple, Optional


class BetManager:
    def __init__(self):
        self.current_bet: Optional[Tuple[int, int]] = None

    def set_bet(self, bet: Tuple[int, int]):
        self.current_bet = bet

    def get_bet(self) -> Optional[Tuple[int, int]]:
        return self.current_bet

    def reset_bet(self):
        self.current_bet = None

    def is_valid_bet(self, new_bet: Tuple[int, int], is_first_turn: bool) -> bool:
        if is_first_turn:
            return new_bet[0] >= 1  # Al menos 1 dado en el primer turno

        if self.current_bet is None:
            return True  # Cualquier apuesta es válida si no hay apuesta previa

        current_quantity, current_value = self.current_bet
        new_quantity, new_value = new_bet

        if new_quantity > current_quantity:
            return True
        elif new_quantity == current_quantity and new_value > current_value:
            return True
        elif new_value == 1 and new_quantity >= (current_quantity + 1) // 2:
            return True  # Regla especial para ases
        else:
            return False

    def calculate_equivalent_bet(self, current_bet: Tuple[int, int], new_pinta: int) -> int:
        current_quantity, current_value = current_bet
        if new_pinta == 1:  # Bajando a ases
            return (current_quantity + 1) // 2
        elif current_value == 1:  # Subiendo desde ases
            return current_quantity * 2 + 1
        else:
            return current_quantity
