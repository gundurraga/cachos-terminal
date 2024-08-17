from typing import List, Tuple, Optional
from src.models.player import Player
from src.models.human_player import HumanPlayer
from src.models.ai_player import AIPlayer
from src.utils.name_generator import NameGenerator
from src.views.renderer import Renderer


class Game:
    def __init__(self, num_ai_players: int, renderer: Renderer):
        self.players: List[Player] = []
        self.current_player_index: int = 0
        self.current_bet: Optional[Tuple[int, int]] = None  # (cantidad, valor)
        self.direction: int = 1  # 1 para sentido horario, -1 para antihorario
        self.name_generator = NameGenerator()
        self.renderer = renderer

        # Agregar jugador humano
        self.players.append(HumanPlayer("Jugador Humano"))

        # Agregar jugadores AI
        for i in range(num_ai_players):
            ai_name = self.name_generator.get_random_name()
            self.players.append(AIPlayer(f"{ai_name} (AI {i+1})"))

    def start_game(self):
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
            self.renderer.display_action(current_player, action)

            if action == 'dudar':
                if self.current_bet is None:
                    self.renderer.display_error(
                        "No se puede dudar sin una apuesta previa.")
                    continue
                round_over = self.handle_doubt()
            elif action == 'calzar':
                if self.current_bet is None:
                    self.renderer.display_error(
                        "No se puede calzar sin una apuesta previa.")
                    continue
                round_over = self.handle_calzo()
            else:  # subir
                new_bet = current_player.make_bet(self.current_bet)
                if new_bet:
                    self.current_bet = new_bet
                    self.renderer.display_bet(current_player, new_bet)
                else:
                    self.renderer.display_error("Apuesta inválida.")
                    continue

            if not round_over:
                self.next_player()

        self.renderer.display_round_end(self.players)

    def handle_doubt(self) -> bool:
        bet_quantity, bet_value = self.current_bet
        total_count = sum(
            dice_value == bet_value for player in self.players for dice_value in player.get_dice_values())

        self.renderer.display_all_dice(self.players)

        if total_count >= bet_quantity:
            loser = self.players[self.current_player_index]
        else:
            loser = self.players[self.current_player_index - self.direction]

        loser.remove_die()
        self.renderer.display_doubt_result(
            loser, total_count, self.current_bet)
        return True

    def handle_calzo(self) -> bool:
        bet_quantity, bet_value = self.current_bet
        total_count = sum(
            dice_value == bet_value for player in self.players for dice_value in player.get_dice_values())

        self.renderer.display_all_dice(self.players)

        current_player = self.players[self.current_player_index]
        if total_count == bet_quantity:
            current_player.add_die()
            self.renderer.display_calzo_success(current_player)
        else:
            current_player.remove_die()
            self.renderer.display_calzo_failure(current_player)
        return True

    def next_player(self):
        self.current_player_index = (
            self.current_player_index + self.direction) % len(self.players)
        return self.players[self.current_player_index]

    def check_game_over(self) -> bool:
        return sum(1 for player in self.players if player.dice) == 1

    def get_winner(self) -> Player:
        for player in self.players:
            if player.dice:
                return player
        return None

    def determine_starting_player(self) -> Player:
        max_roll = 0
        starting_player = None
        for player in self.players:
            roll = max(player.roll_dice())
            if roll > max_roll:
                max_roll = roll
                starting_player = player
        return starting_player
