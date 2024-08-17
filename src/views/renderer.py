from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from src.views.dice_renderer import DiceRenderer


class Renderer:
    def __init__(self):
        self.dice_renderer = DiceRenderer()
        self.console = Console()

    def display_welcome_message(self):
        welcome_message = Panel(
            "¡Bienvenido al juego de Cachos!", title="Cachos", expand=False)
        self.console.print(welcome_message)

    def display_players(self, players):
        table = Table(title="Jugadores")
        table.add_column("Nombre", style="cyan")
        table.add_column("Dados", justify="right", style="green")

        for player in players:
            player_type = "Humano" if player.__class__.__name__ == "HumanPlayer" else "IA"
            table.add_row(player.name, str(len(player.dice)))

        self.console.print(table)

    def display_starting_player(self, player):
        self.console.print(
            f"\n[bold green]{player.name}[/bold green] comienza el juego.")

    def display_round_start(self):
        self.console.rule("[bold blue]Nueva Ronda[/bold blue]")

    def display_first_turn_message(self):
        self.console.print(
            "[bold yellow]Primer turno: Solo puedes apostar. La apuesta mínima es 1 dado.[/bold yellow]")

    def display_current_player(self, player):
        self.console.print(f"\nTurno de [bold]{player.name}[/bold]")

    def display_dice(self, dice_values):
        dice_str = " ".join(self.dice_renderer.render(value)
                            for value in dice_values)
        self.console.print(f"Tus dados: {dice_str}")

    def display_bet(self, player, bet):
        quantity, value = bet
        self.console.print(
            f"[bold]{player.name}[/bold] apuesta: [cyan]{quantity}[/cyan] dados con valor [cyan]{value}[/cyan]")

    def display_doubt_result(self, loser, actual_count, bet):
        quantity, value = bet
        self.console.print(
            f"[bold red]¡Duda![/bold red] Había [cyan]{actual_count}[/cyan] dados con valor [cyan]{value}[/cyan]")
        self.console.print(f"[bold]{loser.name}[/bold] pierde un dado.")

    def display_calzo_success(self, player):
        self.console.print(
            f"[bold green]¡Calzo exitoso![/bold green] {player.name} gana un dado.")

    def display_calzo_failure(self, player):
        self.console.print(
            f"[bold red]¡Calzo fallido![/bold red] {player.name} pierde un dado.")

    def display_winner(self, player):
        winner_message = Panel(
            f"{player.name} ha ganado el juego!", title="Ganador", expand=False)
        self.console.print(winner_message)

    def display_action(self, player, action):
        self.console.print(
            f"{player.name} elige: [bold blue]{action}[/bold blue]")

    def display_all_dice(self, players):
        table = Table(title="Dados de todos los jugadores")
        table.add_column("Jugador", style="cyan")
        table.add_column("Dados", style="magenta")

        for player in players:
            dice_str = " ".join(self.dice_renderer.render(value)
                                for value in player.get_dice_values())
            table.add_row(player.name, dice_str)

        self.console.print(table)

    def display_round_end(self, players):
        table = Table(title="Fin de la ronda")
        table.add_column("Jugador", style="cyan")
        table.add_column("Dados", justify="right", style="green")

        for player in players:
            table.add_row(player.name, str(len(player.dice)))

        self.console.print(table)

    def display_error(self, message):
        self.console.print(f"[bold red]Error:[/bold red] {message}")
