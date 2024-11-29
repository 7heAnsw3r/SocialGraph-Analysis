from Nodo import Nodo
from Arista import Arista


class Grafo:
    def __init__(self):
        self.nodos = {}  # Diccionario de nodos
        self.aristas = []  # Lista de aristas

    def agregar_nodo(self, nombre):
        """Agrega un nodo al grafo si no existe"""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, inicio, fin):
        """Agrega una arista entre dos nodos"""
        if inicio in self.nodos and fin in self.nodos:
            nodo_inicio = self.nodos[inicio]
            nodo_fin = self.nodos[fin]
            nodo_inicio.agregar_vecino(nodo_fin)  # Conecta los nodos
            self.aristas.append(Arista(nodo_inicio, nodo_fin))  # Crea y agrega la arista
        else:
            print(f"Uno o ambos nodos {inicio} o {fin} no existen.")

    def bfs(self, start):
        """Realiza una búsqueda en amplitud (BFS) comenzando desde un nodo"""
        if start not in self.nodos:
            print(f"El nodo {start} no existe en el grafo.")
            return []

        visitados = set()  # Conjunto de nodos visitados
        cola = [self.nodos[start]]  # Cola para procesar los nodos en orden de nivel
        camino = []  # Lista para almacenar el camino

        while cola:
            nodo_actual = cola.pop(0)
            if nodo_actual.nombre not in visitados:
                camino.append(nodo_actual.nombre)  # Procesa el nodo
                visitados.add(nodo_actual.nombre)  # Marca el nodo como visitado
                # Agrega los vecinos no visitados a la cola
                for vecino in nodo_actual.vecino:
                    if vecino.nombre not in visitados:
                        cola.append(vecino)

        return camino

    def dfs(self, start, end):
        """Realiza una búsqueda en profundidad (DFS) recursiva comenzando desde un nodo"""
        if start not in self.nodos:
            print(f"El nodo {start} no existe en el grafo.")
            return []

        visitados = set()  # Conjunto de nodos visitados
        camino = []  # Lista para almacenar el camino
        self._dfs_recursivo(self.nodos[start], end, visitados, camino)
        return camino

    def _dfs_recursivo(self, nodo, end, visitados, camino):
        """Método recursivo auxiliar para DFS"""
        if nodo.nombre in visitados:
            return False

        visitados.add(nodo.nombre)  # Marca el nodo como visitado
        camino.append(nodo.nombre)  # Agrega el nodo al camino

        if nodo.nombre == end:  # Si hemos llegado al nodo final
            return True

        # Recursivamente visita los vecinos no visitados
        for vecino in nodo.vecino:
            if self._dfs_recursivo(vecino, end, visitados, camino):
                return True

        camino.pop()  # Si no encontramos el nodo final, retrocedemos (backtrack)
        return False


# Crear el grafo
grafo = Grafo()

# Agregar nodos
grafo.agregar_nodo("A")
grafo.agregar_nodo("B")
grafo.agregar_nodo("C")
grafo.agregar_nodo("D")

# Agregar aristas
grafo.agregar_arista("A", "B")
grafo.agregar_arista("A", "C")
grafo.agregar_arista("B", "D")
grafo.agregar_arista("C", "D")

# Ejecutar BFS
camino_bfs = grafo.bfs("A")
print(f"Camino más corto (BFS): {camino_bfs}")

# Ejecutar DFS
camino_dfs = grafo.dfs("A", "D")
print(f"Camino más largo (DFS): {camino_dfs}")
