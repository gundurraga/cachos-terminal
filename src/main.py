from src.views.renderer import Renderer
from src.models.game import Game
import sys
import os

# Añadir el directorio padre de 'src' al Python Path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)


def get_num_ai_players():
    while True:
        try:
            num = int(
                input("¿Contra cuántos jugadores AI quieres jugar? (1-7): "))
            if 1 <= num <= 7:
                return num
            else:
                print("Por favor, ingresa un número entre 1 y 7.")
        except ValueError:
            print("Por favor, ingresa un número válido.")


def main():
    renderer = Renderer()
    renderer.display_welcome_message()

    num_ai_players = get_num_ai_players()

    game = Game(num_ai_players, renderer)
    game.start_game()


if __name__ == "__main__":
    main()
