from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from src.views.dice_renderer import DiceRenderer


class Renderer:
    def __init__(self):
        self.console = Console()
        self.dice_renderer = DiceRenderer()

    def display_welcome_message(self):
        welcome_text = Text(
            "¡Bienvenido al juego de Cachos!", style="bold magenta")
        self.console.print(Panel(welcome_text, expand=False))

    def display_players(self, players):
        table = Table(title="Jugadores")
        table.add_column("Nombre", style="cyan")
        table.add_column("Tipo", style="green")
        table.add_column("Dados", style="yellow")

        for player in players:
            player_type = "Humano" if player.__class__.__name__ == "HumanPlayer" else "IA"
            table.add_row(player.name, player_type, str(len(player.dice)))

        self.console.print(table)

    def display_starting_player(self, player):
        self.console.print(
            f"[bold green]{player.name}[/bold green] comienza el juego.")

    def display_round_start(self):
        self.console.print("\n[bold blue]--- Nueva Ronda ---[/bold blue]")

    def display_current_player(self, player):
        self.console.print(f"\nTurno de [bold]{player.name}[/bold]")

    def display_dice(self, dice_values):
        dice_str = " ".join(self.dice_renderer.render(value)
                            for value in dice_values)
        self.console.print(f"Tus dados: {dice_str}")

    def display_bet(self, player, bet):
        quantity, value = bet
        self.console.print(
            f"[bold]{player.name}[/bold] apuesta: {quantity} dados con valor {value}")

    def display_doubt_result(self, loser, actual_count, bet):
        quantity, value = bet
        self.console.print(
            f"[bold red]¡Duda![/bold red] Había {actual_count} dados con valor {value}")
        self.console.print(f"[bold]{loser.name}[/bold] pierde un dado.")

    def display_calzo_success(self, player):
        self.console.print(
            f"[bold green]¡Calzo exitoso![/bold green] {player.name} gana un dado.")

    def display_calzo_failure(self, player):
        self.console.print(
            f"[bold red]¡Calzo fallido![/bold red] {player.name} pierde un dado.")

    def display_winner(self, player):
        winner_text = Text(
            f"¡{player.name} ha ganado el juego!", style="bold yellow")
        self.console.print(Panel(winner_text, expand=False))
