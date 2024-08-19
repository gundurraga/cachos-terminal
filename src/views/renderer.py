from rich.console import Console
from rich.panel import Panel
from src.views.dice_renderer import DiceRenderer
from src.views.table_renderer import TableRenderer
from rich.table import Table


class Renderer:
    def __init__(self):
        self.dice_renderer = DiceRenderer()
        self.console = Console()
        self.pinta_names = {
            1: "as",
            2: "tonto",
            3: "tren",
            4: "cuadra",
            5: "quina",
            6: "sexta"
        }
        self.pinta_plurals = {
            1: "ases",
            2: "tontos",
            3: "trenes",
            4: "cuadras",
            5: "quinas",
            6: "sextas"
        }

    def display_welcome_message(self):
        welcome_message = Panel(
            "¡Bienvenido al juego de Cachos!", title="Cachos", expand=False)
        self.console.print(welcome_message)

    def display_players(self, players, current_player_index):
        TableRenderer.render_to_console(players, current_player_index)

    def display_current_player_dice(self, player):
        dice_str = " ".join(self.dice_renderer.render(value)
                            for value in player.get_dice_values())
        self.console.print(f"Tus dados: {dice_str}")

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
        pinta_name = self.pinta_names.get(value, str(value))
        pinta_plural = self.pinta_plurals.get(value, f"{pinta_name}s")
        pinta_display = pinta_plural if quantity > 1 else pinta_name
        self.console.print(
            f"[bold]{player.name}[/bold] apuesta: [cyan]{quantity} {pinta_display}[/cyan]")

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

    def display_invalid_ai_bet(self, player):
        self.console.print(
            f"[bold yellow]{player.name} intentó hacer una apuesta inválida. Intentando de nuevo...[/bold yellow]")

    def display_ai_doubt(self, player):
        self.console.print(
            f"[bold yellow]{player.name} no pudo hacer una apuesta válida y decide dudar.[/bold yellow]")
