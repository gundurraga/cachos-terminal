from typing import List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from src.views.table_renderer import TableRenderer
from src.views.dice_renderer import DiceRenderer
from src.models.player import Player
import logging

logger = logging.getLogger(__name__)


class PlayerRenderer:
    def __init__(self, console: Console):
        self.console: Console = console
        self.dice_renderer: DiceRenderer = DiceRenderer()
        logger.info("PlayerRenderer inicializado")

    def display_players(self, players: List[Player], current_player_index: int, last_player: Optional[Player] = None, last_bet: Optional[Tuple[int, int]] = None) -> None:
        """
        Muestra la información de todos los jugadores en la mesa.

        Args:
            players (List[Player]): Lista de jugadores en el juego.
            current_player_index (int): Índice del jugador actual.
            last_player (Optional[Player]): Último jugador que realizó una acción.
            last_bet (Optional[Tuple[int, int]]): Última apuesta realizada.
        """
        TableRenderer.render_to_console(
            players, current_player_index, last_player, last_bet)
        logger.info(
            f"Mostrando {len(players)} jugadores. Jugador actual: {current_player_index}")

    def display_current_player_dice(self, player: Player) -> None:
        """
        Muestra los dados del jugador actual.

        Args:
            player (Player): El jugador actual.
        """
        dice_str = " ".join(self.dice_renderer.render(value)
                            for value in player.get_dice_values())
        self.console.print(f"Tus dados: {dice_str}")
        logger.debug(f"Mostrando dados del jugador {player.name}: {dice_str}")

    def display_starting_player(self, player: Player) -> None:
        """
        Muestra el jugador que comienza el juego.

        Args:
            player (Player): El jugador que inicia el juego.
        """
        self.console.print(
            f"\n[bold green]{player.name}[/bold green] comienza el juego.")
        logger.info(f"Jugador inicial: {player.name}")

    def display_current_player(self, player: Player) -> None:
        """
        Muestra el jugador actual.

        Args:
            player (Player): El jugador actual.
        """
        self.console.print(f"\nTurno de [bold]{player.name}[/bold]")
        logger.debug(f"Turno del jugador: {player.name}")

    def display_action(self, player: Player, action: str) -> None:
        """
        Muestra la acción elegida por un jugador.

        Args:
            player (Player): El jugador que realiza la acción.
            action (str): La acción elegida.
        """
        self.console.print(
            f"{player.name} elige: [bold blue]{action}[/bold blue]")
        logger.info(f"Acción de {player.name}: {action}")

    def display_all_dice(self, players: List[Player]) -> None:
        """
        Muestra los dados de todos los jugadores.

        Args:
            players (List[Player]): Lista de jugadores en el juego.
        """
        table = Table(title="Dados de todos los jugadores")
        table.add_column("Jugador", style="cyan")
        table.add_column("Dados", style="magenta")

        for player in players:
            dice_str = " ".join(self.dice_renderer.render(value)
                                for value in player.get_dice_values())
            table.add_row(player.name, dice_str)

        self.console.print(table)
        logger.debug("Mostrando dados de todos los jugadores")

    def display_invalid_ai_bet(self, player: Player) -> None:
        """
        Muestra un mensaje cuando una IA hace una apuesta inválida.

        Args:
            player (Player): El jugador IA que hizo la apuesta inválida.
        """
        self.console.print(
            f"[bold yellow]{player.name} intentó hacer una apuesta inválida. Intentando de nuevo...[/bold yellow]")
        logger.warning(f"Apuesta inválida de IA: {player.name}")

    def display_ai_doubt(self, player: Player) -> None:
        """
        Muestra un mensaje cuando una IA decide dudar.

        Args:
            player (Player): El jugador IA que decide dudar.
        """
        self.console.print(
            f"[bold yellow]{player.name} no pudo hacer una apuesta válida y decide dudar.[/bold yellow]")
        logger.info(f"IA decide dudar: {player.name}")
