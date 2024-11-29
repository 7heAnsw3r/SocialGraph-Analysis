import csv
import sys
import os
from Nodo import Nodo
from Arista import Arista
from VisualizadorGrafo import VisualizadorGrafo


class Grafo:
    def __init__(self):
        self.nodos = {}  # Diccionario de nodos
        self.aristas = []  # Lista de aristas

    def agregar_nodo(self, nombre):
        """Agrega un nodo al grafo si no existe."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, inicio, fin):
        """Agrega una arista entre dos nodos existentes."""
        if inicio in self.nodos and fin in self.nodos:
            nodo_inicio = self.nodos[inicio]
            nodo_fin = self.nodos[fin]
            nodo_inicio.agregar_vecino(nodo_fin)  # Conecta los nodos
            self.aristas.append(Arista(nodo_inicio, nodo_fin))  # Crea y agrega la arista
        else:
            print(f"Error: Uno o ambos nodos '{inicio}' o '{fin}' no existen.")

    def bfs(self, start, end=None):
        """Realiza una búsqueda en amplitud (BFS) comenzando desde un nodo."""
        if start not in self.nodos:
            return []  # Siempre retorna una lista vacía si no existe el nodo

        visitados = set()  # Conjunto de nodos visitados
        cola = [(self.nodos[start], [start])]  # Cola para procesar los nodos en orden de nivel
        camino = []  # Lista para almacenar el camino

        while cola:
            nodo_actual, path = cola.pop(0)
            if nodo_actual.nombre not in visitados:
                visitados.add(nodo_actual.nombre)  # Marca el nodo como visitado
                if nodo_actual.nombre == end:
                    return path  # Devuelve el camino si llegamos al nodo de fin
                camino.append(nodo_actual.nombre)  # Procesa el nodo
                # Agrega los vecinos no visitados a la cola
                for vecino in nodo_actual.vecino:
                    if vecino.nombre not in visitados:
                        cola.append((vecino, path + [vecino.nombre]))

        return camino if end is None else []

    def dfs(self, start, end=None):
        """Realiza una búsqueda en profundidad (DFS) desde un nodo hacia todos los nodos alcanzables."""
        if start not in self.nodos:
            return []  # Siempre retorna una lista vacía si no existe el nodo

        visitados = set()  # Conjunto de nodos visitados

        # Si se proporcionó un nodo de fin y no se encontró, muestra un mensaje
        camino_actual = []  # Lista para almacenar el camino actual
        camino_largo = []  # Lista para almacenar el camino más largo encontrado
        self._dfs_recursivo(self.nodos[start], end, visitados, camino_actual, camino_largo)

        return camino_largo

    def _dfs_recursivo(self, nodo, end, visitados, camino_actual, camino_largo):
        """Metodo recursivo auxiliar para DFS."""
        if nodo.nombre in visitados:
            return
        visitados.add(nodo.nombre)  # Marca el nodo como visitado
        camino_actual.append(nodo.nombre)

        # Si se llega al nodo de fin, termina el recorrido
        if end and nodo.nombre == end:
            if len(camino_actual) > len(camino_largo):
                camino_largo.clear()
                camino_largo.extend(camino_actual)

        # Recursivamente visita los vecinos no visitados
        for vecino in nodo.vecino:
            if vecino.nombre not in visitados:
                self._dfs_recursivo(vecino, end, visitados, camino_actual, camino_largo)
                
        camino_actual.pop()
        visitados.remove(nodo.nombre)

    def cargar_desde_csv(self, archivo_csv):
        """Carga el grafo desde un archivo CSV."""
        try:
            with open(archivo_csv, mode='r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Salta la cabecera
                for row in reader:
                    nodo_inicio, nodo_fin = row
                    self.agregar_nodo(nodo_inicio)
                    self.agregar_nodo(nodo_fin)
                    self.agregar_arista(nodo_inicio, nodo_fin)
        except Exception as e:
            print(f"Error al procesar el archivo '{archivo_csv}': {e}")

# Bloque principal
if __name__ == "__main__":
    # Verificar argumentos desde la línea de comandos
    if len(sys.argv) < 2:
        print("Uso: python grafo.py <archivo_csv>")
        sys.exit(1)

    archivo_csv = sys.argv[1]

    # Verificar si el archivo existe
    if not os.path.isfile(archivo_csv):
        print(f"Error: El archivo '{archivo_csv}' no existe.")
        sys.exit(1)

    # Cargar grafo y mostrar
    try:
        grafo = Grafo()
        grafo.cargar_desde_csv(archivo_csv)
        visualizador = VisualizadorGrafo(grafo)
        visualizador.mostrar_grafo()
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        sys.exit(1)