import random


class NameGenerator:
    def __init__(self):
        self.names = [
            "Juan", "María", "Pedro", "Ana", "Carlos", "Sofía", "Luis", "Laura",
            "Diego", "Valentina", "Andrés", "Camila", "José", "Isabella", "Francisco"
        ]

    def get_random_name(self):
        return random.choice(self.names)
