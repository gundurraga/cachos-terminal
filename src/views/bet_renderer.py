from rich.console import Console
import time


class BetRenderer:
    def __init__(self, console: Console):
        self.console = console
        self.pinta_names = {
            1: "as", 2: "tonto", 3: "tren", 4: "cuadra", 5: "quina", 6: "sexta"
        }
        self.pinta_plurals = {
            1: "ases", 2: "tontos", 3: "trenes", 4: "cuadras", 5: "quinas", 6: "sextas"
        }

    def display_bet(self, player, bet):
        quantity, value = bet
        pinta_name = self.pinta_names.get(value, str(value))
        pinta_plural = self.pinta_plurals.get(value, f"{pinta_name}s")
        pinta_display = pinta_plural if quantity > 1 else pinta_name
        self.console.print(
            f"[bold]{player.name}[/bold] apuesta: [cyan]{quantity} {pinta_display}[/cyan]")

    def display_round_result(self, action, player, bet, actual_count, success):
        if action == 'doubt':
            doubter, doubted = player
            quantity, value = bet
            pinta_name = self.pinta_plurals.get(
                value, f"{self.pinta_names.get(value, str(value))}s")
            self.console.print(
                f"\n[bold]{doubter.name}[/bold] le dudó los [cyan]{quantity} {pinta_name}[/cyan] a [bold]{doubted.name}[/bold].")
            self.console.print(
                f"Habían [cyan]{actual_count} {pinta_name}[/cyan].")
            loser = doubted if success else doubter
            self.console.print(
                f"[bold]{loser.name}[/bold] pierde un dado y comienza la próxima ronda.")
        elif action == 'calzo':
            quantity, value = bet
            pinta_name = self.pinta_plurals.get(
                value, f"{self.pinta_names.get(value, str(value))}s")
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

        # Pausa de 2 segundos para que los jugadores asimilen la información
        time.sleep(3)
