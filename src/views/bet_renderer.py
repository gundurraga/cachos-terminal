from rich.console import Console
from typing import Tuple, Union
from src.models.player import Player
import time
import logging

logger = logging.getLogger(__name__)


class BetRenderer:
    def __init__(self, console: Console):
        self.console: Console = console
        self.pinta_names: dict[int, str] = {
            1: "as", 2: "tonto", 3: "tren", 4: "cuadra", 5: "quina", 6: "sexta"
        }
        self.pinta_plurals: dict[int, str] = {
            1: "ases", 2: "tontos", 3: "trenes", 4: "cuadras", 5: "quinas", 6: "sextas"
        }
        logger.info("BetRenderer inicializado")

    def display_bet(self, player: Player, bet: Tuple[int, int]) -> None:
        """
        Muestra la apuesta realizada por un jugador.

        Args:
            player (Player): El jugador que realizó la apuesta.
            bet (Tuple[int, int]): La apuesta realizada (cantidad, valor).
        """
        quantity, value = bet
        pinta_name = self.pinta_names.get(value, str(value))
        pinta_plural = self.pinta_plurals.get(value, f"{pinta_name}s")
        pinta_display = pinta_plural if quantity > 1 else pinta_name
        self.console.print(
            f"[bold]{player.name}[/bold] apuesta: [cyan]{quantity} {pinta_display}[/cyan]")
        logger.info(
            f"Apuesta mostrada: {player.name} apuesta {quantity} {pinta_display}")

    def display_round_result(self, action: str, players: Union[Player, Tuple[Player, Player]],
                             bet: Tuple[int, int], actual_count: int, success: bool) -> None:
        quantity, value = bet
        pinta_name = self.pinta_plurals.get(
            value, f"{self.pinta_names.get(value, str(value))}s")

        if action == 'doubt':
            if isinstance(players, tuple) and len(players) == 2:
                doubter, doubted = players
                self._display_doubt_result(
                    doubter, doubted, quantity, pinta_name, actual_count, success)
            else:
                logger.error(
                    f"Formato incorrecto de jugadores para duda: {players}")
                self.console.print(
                    "[bold red]Error: Formato incorrecto de jugadores para duda[/bold red]")
        elif action == 'calzo':
            if isinstance(players, Player):
                self._display_calzo_result(
                    players, quantity, pinta_name, actual_count, success)
            else:
                logger.error(
                    f"Formato incorrecto de jugador para calzo: {players}")
                self.console.print(
                    "[bold red]Error: Formato incorrecto de jugador para calzo[/bold red]")
        else:
            logger.error(f"Acción desconocida: {action}")
            self.console.print(
                f"[bold red]Error: Acción desconocida '{action}'[/bold red]")

        time.sleep(5)

    def _display_doubt_result(self, doubter: Player, doubted: Player, quantity: int,
                              pinta_name: str, actual_count: int, success: bool) -> None:
        self.console.print(
            f"\n[bold]{doubter.name}[/bold] le dudó los [cyan]{quantity} {pinta_name}[/cyan] a [bold]{doubted.name}[/bold].")
        self.console.print(f"Habían [cyan]{actual_count} {pinta_name}[/cyan].")
        loser = doubted if success else doubter
        self.console.print(
            f"[bold]{loser.name}[/bold] pierde un dado y comienza la próxima ronda.")

    def _display_calzo_result(self, player: Player, quantity: int,
                              pinta_name: str, actual_count: int, success: bool) -> None:
        self.console.print(
            f"\n[bold]{player.name}[/bold] calzó los [cyan]{quantity} {pinta_name}[/cyan].")
        self.console.print(f"Habían [cyan]{actual_count} {pinta_name}[/cyan].")
        if success:
            self.console.print(
                f"[bold green]¡Calzo exitoso![/bold green] {player.name} gana un dado y comienza la próxima ronda.")
        else:
            self.console.print(
                f"[bold red]¡Calzo fallido![/bold red] {player.name} pierde un dado y comienza la próxima ronda.")

    def _display_calzo_result(self, player: Player, quantity: int,
                              pinta_name: str, actual_count: int, success: bool) -> None:
        self.console.print(
            f"\n[bold]{player.name}[/bold] calzó los [cyan]{quantity} {pinta_name}[/cyan].")
        self.console.print(f"Habían [cyan]{actual_count} {pinta_name}[/cyan].")
        if success:
            self.console.print(
                f"[bold green]¡Calzo exitoso![/bold green] {player.name} gana un dado y comienza la próxima ronda.")
        else:
            self.console.print(
                f"[bold red]¡Calzo fallido![/bold red] {player.name} pierde un dado y comienza la próxima ronda.")
