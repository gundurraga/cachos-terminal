from typing import List, Tuple
from src.models.player import Player
from src.models.human_player import HumanPlayer
from src.models.ai_player import AIPlayer
from src.utils.name_generator import NameGenerator


class Game:
    def __init__(self, num_ai_players: int):
        self.players: List[Player] = []
        self.current_player_index: int = 0
        self.current_bet: Tuple[int, int] = None  # (cantidad, valor)
        self.direction: int = 1  # 1 para sentido horario, -1 para antihorario
        self.name_generator = NameGenerator()

        # Agregar jugador humano
        self.players.append(HumanPlayer("Jugador Humano"))

        # Agregar jugadores AI
        for _ in range(num_ai_players):
            ai_name = self.name_generator.get_random_name()
            self.players.append(AIPlayer(ai_name))

    def start_game(self):
        self.renderer.display_welcome_message()
        self.renderer.display_players(self.players)

        # Determinar el jugador inicial
        starting_player = self.determine_starting_player()
        self.current_player_index = self.players.index(starting_player)

        self.renderer.display_starting_player(starting_player)

        while not self.check_game_over():
            self.play_round()

        winner = self.get_winner()
        self.renderer.display_winner(winner)

    def play_round(self):
        self.renderer.display_round_start()

        for player in self.players:
            player.roll_dice()

        self.current_bet = None
        round_over = False

        while not round_over:
            current_player = self.players[self.current_player_index]
            self.renderer.display_current_player(current_player)

            if isinstance(current_player, HumanPlayer):
                self.renderer.display_dice(current_player.get_dice_values())

            action = current_player.decide_action(self.current_bet)

            if action == 'dudar':
                round_over = self.handle_doubt()
            elif action == 'calzar':
                self.handle_calzo()
            else:  # subir
                new_bet = current_player.make_bet(self.current_bet)
                if new_bet:
                    self.current_bet = new_bet
                    self.renderer.display_bet(current_player, new_bet)
                else:
                    round_over = self.handle_doubt()

            if not round_over:
                self.next_player()

    def determine_starting_player(self) -> Player:
        max_roll = 0
        starting_player = None
        for player in self.players:
            roll = player.roll_dice()[0]  # Usamos solo el primer dado
            if roll > max_roll:
                max_roll = roll
                starting_player = player
        return starting_player

    def handle_doubt(self) -> bool:
        total_dice = sum(len(player.dice) for player in self.players)
        count = sum(dice.count(
            self.current_bet[1]) for player in self.players for dice in player.get_dice_values())

        if count >= self.current_bet[0]:
            loser = self.players[self.current_player_index]
        else:
            loser = self.players[self.current_player_index - self.direction]

        loser.remove_die()
        self.renderer.display_doubt_result(loser, count, self.current_bet)
        return True

    def handle_calzo(self):
        total_dice = sum(len(player.dice) for player in self.players)
        count = sum(dice.count(
            self.current_bet[1]) for player in self.players for dice in player.get_dice_values())

        current_player = self.players[self.current_player_index]
        if count == self.current_bet[0]:
            current_player.add_die()
            self.renderer.display_calzo_success(current_player)
        else:
            current_player.remove_die()
            self.renderer.display_calzo_failure(current_player)

    def next_player(self):
        self.current_player_index = (
            self.current_player_index + self.direction) % len(self.players)
        return self.players[self.current_player_index]

    def check_game_over(self) -> bool:
        # Verificar si solo queda un jugador con dados
        return sum(1 for player in self.players if player.dice) == 1

    def get_winner(self) -> Player:
        # Obtener el jugador ganador (el último con dados)
        for player in self.players:
            if player.dice:
                return player
        return None
