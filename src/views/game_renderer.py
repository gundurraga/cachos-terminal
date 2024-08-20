from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.views.dice_renderer import DiceRenderer
import time


class GameRenderer:
    def __init__(self, console: Console):
        self.console = console
        self.dice_renderer = DiceRenderer()

    def display_welcome_message(self):
        welcome_message = Panel(
            "¡Bienvenido al juego de Cachos!", title="Cachos", expand=False)
        self.console.print(welcome_message)

    def display_round_start(self):
        self.console.rule("[bold blue]Nueva Ronda[/bold blue]")

    def display_round_end(self, players):
        table = Table(title="Resultado de la ronda")
        table.add_column("Jugador", style="cyan")
        table.add_column("Dados", justify="center", style="magenta")
        table.add_column("Restantes", justify="right", style="green")

        for player in players:
            dice_str = " ".join(self.dice_renderer.render(value)
                                for value in player.get_dice_values())
            table.add_row(player.name, dice_str, str(len(player.dice)))

        self.console.print(Panel(table, expand=False))

        time.sleep(5)

    def display_winner(self, player):
        winner_message = Panel(
            f"{player.name} ha ganado el juego!", title="Ganador", expand=False)
        self.console.print(winner_message)

    def display_error(self, message):
        self.console.print(f"[bold red]Error:[/bold red] {message}")
