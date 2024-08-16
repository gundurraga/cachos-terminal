import os
import pathlib


def create_directory(path):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def create_file(path, content=''):
    with open(path, 'w') as f:
        f.write(content)


def create_project_structure():
    root = '.'

    # Crear estructura de directorios
    directories = [
        'src',
        'src/models',
        'src/views',
        'src/controllers',
        'src/utils',
        'src/data',
        'tests',
        'tests/test_models',
        'tests/test_views',
        'tests/test_controllers',
        'tests/test_utils',
        'docs'
    ]

    for directory in directories:
        create_directory(os.path.join(root, directory))

    # Crear archivos
    files = [
        'src/__init__.py',
        'src/main.py',
        'src/config.py',
        'src/models/__init__.py',
        'src/models/game.py',
        'src/models/player.py',
        'src/models/dice.py',
        'src/views/__init__.py',
        'src/views/renderer.py',
        'src/views/input_handler.py',
        'src/controllers/__init__.py',
        'src/controllers/game_controller.py',
        'src/controllers/ai_controller.py',
        'src/utils/__init__.py',
        'src/utils/helpers.py',
        'src/data/__init__.py',
        'src/data/save_game.py',
        'src/data/statistics.py',
        'tests/__init__.py',
        'docs/README.md',
        '.gitignore',
        'requirements.txt',
        'setup.py',
        'LICENSE'
    ]

    for file in files:
        create_file(os.path.join(root, file))

    print("Estructura del proyecto creada exitosamente.")


if __name__ == "__main__":
    create_project_structure()
