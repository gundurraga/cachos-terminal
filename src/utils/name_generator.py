import random


class NameGenerator:
    def __init__(self):
        self.names = [
            "Agustina", "Ainhoa", "Aitana", "Alba", "Alejandra", "Alexa", "Alexandra", "Almendra",
            "Amanda", "Amelia", "Anaís", "Antonella", "Antonia", "Arantxa", "Ariadna", "Aroha",
            "Azul", "Belén", "Blanca", "Brisa", "Camila", "Carla", "Carolina", "Catalina",
            "Celia", "Clara", "Claudia", "Constanza", "Daniela", "Débora", "Diana", "Dominique",
            "Elisa", "Elizabeth", "Emilia", "Emma", "Esmeralda", "Estefanía", "Fernanda", "Florencia",
            "Francisca", "Gabriela", "Giovanna", "Isabella", "Ivanna", "Javiera", "Jimena", "Josefina",
            "Juanita", "Julieta", "Karina", "Karla", "Katia", "Kiara", "Lara", "Laura",
            "Layla", "Lila", "Luciana", "Luisa", "Luna", "Macarena", "Magdalena", "Manuela",
            "María", "Martina", "Matilde", "Mía", "Mila", "Mireya", "Natalia", "Nerea",
            "Nicole", "Noelia", "Olivia", "Paloma", "Paola", "Paulina", "Paz", "Penélope",
            "Renata", "Rocío", "Romina", "Rosario", "Salomé", "Samantha", "Sara", "Sofía",
            "Sol", "Tamara", "Valentina", "Valeria", "Vania", "Verónica", "Victoria", "Violeta",
            "Ximena", "Yasna", "Yolanda", "Zoe",
            "Agustín", "Alejandro", "Alonso", "Álvaro", "Andrés", "Áxel", "Bautista", "Benjamín",
            "Brian", "Bruno", "Caleb", "Camilo", "Carlos", "Cristóbal", "Cristian", "Constantino",
            "Damián", "Daniel", "David", "Diego", "Derek", "Eduardo", "Elías", "Erick",
            "Emmanuel", "Enrique", "Esteban", "Ethan", "Federico", "Fernando", "Franco", "Francisco",
            "Gabriel", "Gael", "Gaspar", "Germán", "Gregorio", "Gustavo", "Hernán", "Ian", "Ignacio",
            "Íñigo", "Isidoro", "Isaac", "Ismael", "Iván", "Jair", "Jairo", "Jason",
            "Jeremy", "Jhon", "Joaquín", "Jorge", "Joshua", "Juan", "Julián", "Kevin",
            "Kian", "León", "Leonardo", "Liam", "Lorenzo", "Lucca", "Marcelo", "Marco",
            "Martín", "Matías", "Mateo", "Mauricio", "Maximiliano", "Miguel", "Nicolao", "Nicolás",
            "Nehemías", "Néstor", "Nilo", "Oliver", "Omar", "Orlando", "Patricio", "Paulo",
            "Pedro", "Rafael", "Ramiro", "Ricardo", "Roberto", "Rodrigo", "Rubén", "Samuel",
            "Santiago", "Sebastián", "Simón", "Thiago", "Tobías", "Tomás", "Valentino", "Víctor",
            "Vicente", "Walter", "Xander", "Zahir"
        ]
        self.used_names = set()

    def get_random_name(self):
        available_names = list(set(self.names) - self.used_names)
        if not available_names:
            raise ValueError("No hay más nombres disponibles.")
        name = random.choice(available_names)
        self.used_names.add(name)
        return name

    def reset(self):
        self.used_names.clear()
