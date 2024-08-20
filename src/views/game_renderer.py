from typing import List
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.views.dice_renderer import DiceRenderer
from src.models.player import Player
import time
import logging

logger = logging.getLogger(__name__)


class GameRenderer:
    def __init__(self, console: Console):
        self.console: Console = console
        self.dice_renderer: DiceRenderer = DiceRenderer()
        logger.info("GameRenderer inicializado")

    def display_welcome_message(self) -> None:
        """Muestra el mensaje de bienvenida al juego."""
        welcome_message = Panel(
            "¡Bienvenido al juego de Cachos!", title="Cachos", expand=False)
        self.console.print(welcome_message)
        logger.info("Mensaje de bienvenida mostrado")

    def display_round_start(self) -> None:
        """Muestra el inicio de una nueva ronda."""
        self.console.rule("[bold blue]Nueva Ronda[/bold blue]")
        logger.info("Inicio de nueva ronda mostrado")

    def display_round_end(self, players: List[Player]) -> None:
        """
        Muestra el resultado de la ronda actual.

        Args:
            players (List[Player]): Lista de jugadores en la ronda.
        """
        table = Table(title="Resultado de la ronda")
        table.add_column("Jugador", style="cyan")
        table.add_column("Dados", justify="center", style="magenta")
        table.add_column("Restantes", justify="right", style="green")

        for player in players:
            dice_str = " ".join(self.dice_renderer.render(value)
                                for value in player.get_dice_values())
            table.add_row(player.name, dice_str, str(len(player.dice)))

        self.console.print(Panel(table, expand=False))
        logger.info("Resultado de la ronda mostrado")

        time.sleep(5)  # Pausa para que los jugadores puedan leer el resultado

    def display_winner(self, player: Player) -> None:
        """
        Muestra el ganador del juego.

        Args:
            player (Player): El jugador ganador.
        """
        winner_message = Panel(
            f"{player.name} ha ganado el juego!", title="Ganador", expand=False)
        self.console.print(winner_message)
        logger.info(f"Ganador mostrado: {player.name}")

    def display_error(self, message: str) -> None:
        """
        Muestra un mensaje de error.

        Args:
            message (str): El mensaje de error a mostrar.
        """
        self.console.print(f"[bold red]Error:[/bold red] {message}")
        logger.error(f"Error mostrado: {message}")
