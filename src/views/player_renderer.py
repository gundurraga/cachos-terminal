from rich.console import Console
from rich.table import Table  # Añadimos esta importación
from src.views.table_renderer import TableRenderer
from src.views.dice_renderer import DiceRenderer


class PlayerRenderer:
    def __init__(self, console: Console):
        self.console = console
        self.dice_renderer = DiceRenderer()

    def display_players(self, players, current_player_index):
        TableRenderer.render_to_console(players, current_player_index)

    def display_current_player_dice(self, player):
        dice_str = " ".join(self.dice_renderer.render(value)
                            for value in player.get_dice_values())
        self.console.print(f"Tus dados: {dice_str}")

    def display_starting_player(self, player):
        self.console.print(
            f"\n[bold green]{player.name}[/bold green] comienza el juego.")

    def display_current_player(self, player):
        self.console.print(f"\nTurno de [bold]{player.name}[/bold]")

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

    def display_invalid_ai_bet(self, player):
        self.console.print(
            f"[bold yellow]{player.name} intentó hacer una apuesta inválida. Intentando de nuevo...[/bold yellow]")

    def display_ai_doubt(self, player):
        self.console.print(
            f"[bold yellow]{player.name} no pudo hacer una apuesta válida y decide dudar.[/bold yellow]")
