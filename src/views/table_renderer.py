from typing import List, Dict, Optional, Tuple
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from rich import box
import random
import logging
from src.models.player import Player

logger = logging.getLogger(__name__)


class TableRenderer:
    COLORS: List[str] = ["red", "green", "yellow",
                         "blue", "magenta", "cyan", "white"]

    def __init__(self):
        self.player_colors: Dict[Player, str] = {}

    @staticmethod
    def render_table(players: List[Player], current_player_index: int, last_player: Optional[Player] = None, last_bet: Optional[Tuple[int, int]] = None) -> Table:
        table = Table(show_header=False, show_edge=False,
                      pad_edge=False, box=None)

        for _ in range(3):
            table.add_column(justify="center", width=24)

        player_colors = TableRenderer._assign_colors(players)

        player_positions = TableRenderer._distribute_players(len(players))

        for row in player_positions:
            table_row = []
            for position in row:
                if position is not None and position < len(players):
                    player = players[position]
                    is_current = position == current_player_index
                    color = player_colors[player]
                    is_last = player == last_player
                    player_panel = TableRenderer._get_player_panel(
                        player, is_current, color, is_last, last_bet)
                    table_row.append(player_panel)
                else:
                    table_row.append("")
            table.add_row(*table_row)

        logger.debug(f"Mesa renderizada con {len(players)} jugadores")
        return table

    @staticmethod
    def _distribute_players(num_players: int) -> List[List[Optional[int]]]:
        if num_players <= 3:
            return [[i for i in range(num_players)] + [None] * (3 - num_players), [None, None, None], [None, None, None]]
        elif num_players == 4:
            return [[0, 1, 2], [3, None, None], [None, None, None]]
        elif num_players == 5:
            return [[0, 1, 2], [4, None, 3], [None, None, None]]
        elif num_players == 6:
            return [[0, 1, 2], [5, None, 3], [4, None, None]]
        else:
            return [[0, 1, 2], [num_players - 1, None, 3], [num_players - 2, num_players - 3, 4]]

    @staticmethod
    def _assign_colors(players: List[Player]) -> Dict[Player, str]:
        if not hasattr(TableRenderer, 'player_colors'):
            TableRenderer.player_colors = {}

        for player in players:
            if player not in TableRenderer.player_colors:
                available_colors = [
                    c for c in TableRenderer.COLORS if c not in TableRenderer.player_colors.values()]
                if not available_colors:
                    available_colors = TableRenderer.COLORS
                TableRenderer.player_colors[player] = random.choice(
                    available_colors)

        return TableRenderer.player_colors

    @staticmethod
    def _get_player_panel(player: Player, is_current: bool, color: str, is_last: bool, last_bet: Optional[Tuple[int, int]]) -> Panel:
        player_text = Text()
        if is_current:
            player_text.append("-> ", style="green")
        player_text.append(f"{player.name}\n", style="bold")
        player_text.append(f"{len(player.dice)} dados")
        if is_last and last_bet:
            player_text.append(
                f"\n{last_bet[0]} {TableRenderer._get_pinta_name(last_bet[1])}", style="bold red")
        return Panel(player_text, border_style=color, expand=False, box=box.HEAVY)

    @staticmethod
    def _get_pinta_name(value: int) -> str:
        pinta_names = {1: "ases", 2: "tontos", 3: "trenes",
                       4: "cuadras", 5: "quinas", 6: "sextas"}
        return pinta_names.get(value, str(value))

    @staticmethod
    def render_to_console(players: List[Player], current_player_index: int, last_player: Optional[Player] = None, last_bet: Optional[Tuple[int, int]] = None) -> None:
        table = TableRenderer.render_table(
            players, current_player_index, last_player, last_bet)
        console = Console()
        console.print(Panel(table, title="Mesa de Juego", expand=False))
        logger.info("Mesa de juego renderizada en la consola")
