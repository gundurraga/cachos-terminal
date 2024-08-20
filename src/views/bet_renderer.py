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

    def display_round_result(self, action: str, player: Union[Player, Tuple[Player, Player]],
                             bet: Tuple[int, int], actual_count: int, success: bool) -> None:
        """
        Muestra el resultado de una ronda.

        Args:
            action (str): La acción realizada ('doubt' o 'calzo').
            player (Union[Player, Tuple[Player, Player]]): El jugador o jugadores involucrados.
            bet (Tuple[int, int]): La apuesta realizada.
            actual_count (int): La cantidad real de dados.
            success (bool): Si la acción fue exitosa.
        """
        quantity, value = bet
        pinta_name = self.pinta_plurals.get(
            value, f"{self.pinta_names.get(value, str(value))}s")

        if action == 'doubt':
            self._display_doubt_result(
                player, quantity, pinta_name, actual_count, success)
        elif action == 'calzo':
            self._display_calzo_result(
                player, quantity, pinta_name, actual_count, success)
        else:
            logger.error(f"Acción desconocida: {action}")
            self.console.print(
                f"[bold red]Error: Acción desconocida '{action}'[/bold red]")

        # Pausa para que los jugadores asimilen la información
        time.sleep(5)

    def _display_doubt_result(self, players: Tuple[Player, Player], quantity: int,
                              pinta_name: str, actual_count: int, success: bool) -> None:
        """
        Muestra el resultado de una duda.

        Args:
            players (Tuple[Player, Player]): Los jugadores involucrados (dudador, dudado).
            quantity (int): La cantidad apostada.
            pinta_name (str): El nombre de la pinta apostada.
            actual_count (int): La cantidad real de dados.
            success (bool): Si la duda fue exitosa.
        """
        doubter, doubted = players
        self.console.print(
            f"\n[bold]{doubter.name}[/bold] le dudó los [cyan]{quantity} {pinta_name}[/cyan] a [bold]{doubted.name}[/bold].")
        self.console.print(
            f"Habían [cyan]{actual_count} {pinta_name}[/cyan].")
        loser = doubted if success else doubter
        self.console.print(
            f"[bold]{loser.name}[/bold] pierde un dado y comienza la próxima ronda.")
        logger.info(
            f"Resultado de duda mostrado. Dudador: {doubter.name}, Dudado: {doubted.name}, Éxito: {success}")

    def _display_calzo_result(self, player: Player, quantity: int,
                              pinta_name: str, actual_count: int, success: bool) -> None:
        """
        Muestra el resultado de un calzo.

        Args:
            player (Player): El jugador que realizó el calzo.
            quantity (int): La cantidad apostada.
            pinta_name (str): El nombre de la pinta apostada.
            actual_count (int): La cantidad real de dados.
            success (bool): Si el calzo fue exitoso.
        """
        self.console.print(
            f"\n[bold]{player.name}[/bold] calzó los [cyan]{quantity} {pinta_name}[/cyan].")
        self.console.print(
            f"Habían [cyan]{actual_count} {pinta_name}[/cyan].")
        if success:
            self.console.print(
                f"[bold green]¡Calzo exitoso![/bold green] {player.name} gana un dado y comienza la próxima ronda.")
        else:
            self.console.print(
                f"[bold red]¡Calzo fallido![/bold red] {player.name} pierde un dado y comienza la próxima ronda.")
        logger.info(
            f"Resultado de calzo mostrado. Jugador: {player.name}, Éxito: {success}")
