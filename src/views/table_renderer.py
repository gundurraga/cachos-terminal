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

        top_row = players[:3]
        middle_row = players[3:5]
        bottom_row = players[5:]

        TableRenderer._add_player_row(
            table, top_row, current_player_index, player_colors, last_player, last_bet, players)
        table.add_row("", "", "")
        if middle_row:
            TableRenderer._add_side_players(
                table, middle_row, current_player_index, player_colors, last_player, last_bet, players)
        table.add_row("", "", "")
        if bottom_row:
            TableRenderer._add_player_row(
                table, bottom_row, current_player_index, player_colors, last_player, last_bet, players, is_bottom=True)

        logger.debug(f"Mesa renderizada con {len(players)} jugadores")
        return table

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
    def _add_player_row(table: Table, row_players: List[Player], current_player_index: int,
                        player_colors: Dict[Player, str], last_player: Optional[Player],
                        last_bet: Optional[Tuple[int, int]], all_players: List[Player], is_bottom: bool = False) -> None:
        row = []
        for i in range(3):
            if i < len(row_players):
                player = row_players[i]
                is_current = all_players.index(player) == current_player_index
                color = player_colors[player]
                is_last = player == last_player
                player_panel = TableRenderer._get_player_panel(
                    player, is_current, color, is_last, last_bet)
                row.append(player_panel)
            else:
                row.append("")
        table.add_row(*row)

    @staticmethod
    def _add_side_players(table: Table, side_players: List[Player], current_player_index: int,
                          player_colors: Dict[Player, str], last_player: Optional[Player],
                          last_bet: Optional[Tuple[int, int]], all_players: List[Player]) -> None:
        left_player = side_players[0] if side_players else None
        right_player = side_players[1] if len(side_players) > 1 else None

        left_panel = TableRenderer._get_player_panel(
            left_player,
            left_player and all_players.index(
                left_player) == current_player_index,
            player_colors[left_player] if left_player else "",
            left_player == last_player,
            last_bet
        ) if left_player else ""

        right_panel = TableRenderer._get_player_panel(
            right_player,
            right_player and all_players.index(
                right_player) == current_player_index,
            player_colors[right_player] if right_player else "",
            right_player == last_player,
            last_bet
        ) if right_player else ""

        table.add_row(left_panel, "", right_panel)

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
