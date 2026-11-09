class Ataque():
    """
    Esta clase representa un ataque
    """
    def __init__(self, nombre_ataque:str, 
                 tipo:str, nivel:int):
        """
        Inicalización del ataque
        Args:
            nombre (str): Nombre del ataque
            tipo (str): Tipo del ataque
            nivel (int): Nivel del ataque
        """
        self.nombre_ataque = nombre_ataque
        self.tipo = tipo
        self.nivel = nivel

class PokemonNuevo():
    """
    Esta clase representa un Pokemon
    """
    def __init__(self, nombre:str, nivel:int):
        """
        Inicalización del pokemon
        Args:
            nombre (str): Nombre del pokemon
            nivel (int): Nivel del pokemon
        """
        self.nombre = nombre
        self.nivel = nivel
        self.ataques = []
    def ver_status(self):
        print(self.nombre, self.nivel)
        for i in self.ataques:
            i:Ataque
            print(i.nombre_ataque, 
                  i.tipo, i.nivel)
    def agregar_ataque(self, ataque:Ataque):
        self.ataques.append(ataque)



if __name__ == "__main__":
    pokemon_nuevo = PokemonNuevo("Charizard", 36)
    ataque = Ataque("Lanzallamas", "Fuego", 90)
    pokemon_nuevo.agregar_ataque(ataque)
    pokemon_nuevo.ver_status()
else:
    print("Se importó la librería con pokemons")

