class Nodo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecino = []

    def agregar_vecino(self, vecino):
        self.vecino.append(vecino)
