from Clases import Ataque, PokemonNuevo

pokemon_nuevo = PokemonNuevo("Magikarp", 15)
ataque = Ataque("Salpicadura", "Agua", 0)
pokemon_nuevo.agregar_ataque(ataque)
pokemon_nuevo.ver_status()
