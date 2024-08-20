from typing import List, Dict
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

    @staticmethod
    def render_table(players: List[Player], current_player_index: int) -> Table:
        """
        Renderiza la mesa de juego con la información de los jugadores.

        Args:
            players (List[Player]): Lista de jugadores en el juego.
            current_player_index (int): Índice del jugador actual.

        Returns:
            Table: La mesa de juego renderizada como una tabla Rich.
        """
        table = Table(show_header=False, show_edge=False,
                      pad_edge=False, box=None)

        for _ in range(3):
            table.add_column(justify="center", width=24)

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

        logger.debug(f"Mesa renderizada con {len(players)} jugadores")
        return table

    @staticmethod
    def _assign_unique_colors(players: List[Player]) -> Dict[Player, str]:
        """
        Asigna colores únicos a cada jugador.

        Args:
            players (List[Player]): Lista de jugadores en el juego.

        Returns:
            Dict[Player, str]: Diccionario que mapea cada jugador a un color único.
        """
        colors = TableRenderer.COLORS * \
            (len(players) // len(TableRenderer.COLORS) + 1)
        random.shuffle(colors)
        return {player: colors[i] for i, player in enumerate(players)}

    @staticmethod
    def _add_player_row(table: Table, players: List[Player], current_player_index: int,
                        player_colors: Dict[Player, str], is_bottom: bool = False) -> None:
        """
        Añade una fila de jugadores a la tabla.

        Args:
            table (Table): La tabla Rich a la que se añadirá la fila.
            players (List[Player]): Lista de jugadores para añadir a la fila.
            current_player_index (int): Índice del jugador actual.
            player_colors (Dict[Player, str]): Diccionario que mapea jugadores a colores.
            is_bottom (bool, optional): Indica si es la fila inferior. Por defecto False.
        """
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
    def _add_side_players(table: Table, players: List[Player], current_player_index: int,
                          player_colors: Dict[Player, str]) -> None:
        """
        Añade jugadores a los lados de la tabla.

        Args:
            table (Table): La tabla Rich a la que se añadirán los jugadores.
            players (List[Player]): Lista de jugadores para añadir a los lados.
            current_player_index (int): Índice del jugador actual.
            player_colors (Dict[Player, str]): Diccionario que mapea jugadores a colores.
        """
        left_player = players[0] if len(players) > 0 else None
        right_player = players[1] if len(players) > 1 else None

        left_panel = TableRenderer._get_player_panel(left_player, players.index(left_player) == current_player_index,
                                                     player_colors[left_player]) if left_player else ""
        right_panel = TableRenderer._get_player_panel(right_player, players.index(right_player) == current_player_index,
                                                      player_colors[right_player]) if right_player else ""

        table.add_row(left_panel, "", right_panel)

    @staticmethod
    def _get_player_panel(player: Player, is_current: bool, color: str) -> Panel:
        """
        Crea un panel Rich para un jugador.

        Args:
            player (Player): El jugador para el que se creará el panel.
            is_current (bool): Indica si es el jugador actual.
            color (str): Color asignado al jugador.

        Returns:
            Panel: Un panel Rich con la información del jugador.
        """
        player_text = Text()
        if is_current:
            player_text.append("-> ", style="bold")
        player_text.append(f"{player.name}\n", style="bold")
        player_text.append(f"Dados: {len(player.dice)}")
        return Panel(player_text, border_style=color, expand=False)

    @staticmethod
    def render_to_console(players: List[Player], current_player_index: int) -> None:
        """
        Renderiza la mesa de juego en la consola.

        Args:
            players (List[Player]): Lista de jugadores en el juego.
            current_player_index (int): Índice del jugador actual.
        """
        table = TableRenderer.render_table(players, current_player_index)
        console = Console()
        console.print(Panel(table, title="Mesa de Juego", expand=False))
        logger.info("Mesa de juego renderizada en la consola")
