from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from rich import box
import random


class TableRenderer:
    COLORS = ["red", "green", "yellow", "blue", "magenta",
              "cyan", "white"]  # Colores básicos compatibles con Rich

    @staticmethod
    def render_table(players, current_player_index):
        table = Table(show_header=False, show_edge=False,
                      pad_edge=False, box=None)

        for _ in range(3):
            table.add_column(justify="center", width=24)

        num_players = len(players)

        player_colors = TableRenderer._assign_unique_colors(players)

        # Distribuir jugadores
        top_row = players[:3]
        middle_row = players[3:5]
        bottom_row = players[5:]

        # Añadir filas a la tabla
        TableRenderer._add_player_row(
            table, top_row, current_player_index, player_colors)
        table.add_row("", "", "")  # Empty row for spacing
        if middle_row:
            TableRenderer._add_side_players(
                table, middle_row, current_player_index, player_colors)
        table.add_row("", "", "")  # Empty row for spacing
        if bottom_row:
            TableRenderer._add_player_row(
                table, bottom_row, current_player_index, player_colors, is_bottom=True)

        return table

    @staticmethod
    def _assign_unique_colors(players):
        colors = TableRenderer.COLORS * \
            (len(players) // len(TableRenderer.COLORS) + 1)
        random.shuffle(colors)
        return {player: colors[i] for i, player in enumerate(players)}

    @staticmethod
    def _add_player_row(table, players, current_player_index, player_colors, is_bottom=False):
        row = []
        for i in range(3):
            if i < len(players):
                player = players[i]
                is_current = players.index(player) == current_player_index
                color = player_colors[player]
                player_panel = TableRenderer._get_player_panel(
                    player, is_current, color)
                row.append(player_panel)
            else:
                row.append("")
        table.add_row(*row)

    @staticmethod
    def _add_side_players(table, players, current_player_index, player_colors):
        left_player = players[0] if len(players) > 0 else None
        right_player = players[1] if len(players) > 1 else None

        left_panel = TableRenderer._get_player_panel(left_player, players.index(
            left_player) == current_player_index, player_colors[left_player]) if left_player else ""
        right_panel = TableRenderer._get_player_panel(right_player, players.index(
            right_player) == current_player_index, player_colors[right_player]) if right_player else ""

        table.add_row(left_panel, "", right_panel)

    @staticmethod
    def _get_player_panel(player, is_current, color):
        if not player:
            return ""
        player_text = Text()
        if is_current:
            player_text.append("-> ", style="bold")
        player_text.append(f"{player.name}\n", style="bold")
        player_text.append(f"Dados: {len(player.dice)}")
        return Panel(player_text, border_style=color, expand=False)

    @staticmethod
    def render_to_console(players, current_player_index):
        table = TableRenderer.render_table(players, current_player_index)
        console = Console()
        console.print(Panel(table, title="Mesa de Juego", expand=False))
