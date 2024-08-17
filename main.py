from src.views.renderer import Renderer
from src.models.game import Game
import sys
import os

# Añadir el directorio padre de 'src' al Python Path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, src_path)


def main():
    num_ai_players = int(
        input("¿Contra cuántos jugadores AI quieres jugar? (1-7): "))
    renderer = Renderer()
    game = Game(num_ai_players, renderer)
    game.start_game()


if __name__ == "__main__":
    main()
