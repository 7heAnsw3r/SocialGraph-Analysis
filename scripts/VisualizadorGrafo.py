import tkinter as tk
import random


class VisualizadorGrafo:
    def __init__(self, grafo):
        self.grafo = grafo

    def mostrar_grafo(self):
        """Crea una ventana para visualizar y mover nodos."""
        ventana = tk.Tk()
        ventana.title("Grafo Redes Sociales")

        # Definir dimensiones del lienzo
        canvas_width, canvas_height = 600, 400
        canvas = tk.Canvas(ventana, width=canvas_width, height=canvas_height, bg="white")
        canvas.pack()

        # Área de texto para mostrar los resultados de BFS y DFS
        resultados_texto = tk.Text(ventana, width=50, height=10, wrap=tk.WORD)
        resultados_texto.pack()

        etiqueta_fin = tk.Label(ventana, text="Nodo de fin:")
        etiqueta_fin.pack()
        entrada_fin = tk.Entry(ventana)  # Campo de entrada para nodo de fin
        entrada_fin.pack()

        # Aquí se mantienen las coordenadas y objetos gráficos de los nodos y las aristas
        coordenadas = {}
        objetos_nodos = {}
        radio = 25  # Radio de los nodos
        aristas_dibujadas = {}

        def generar_color_aleatorio():
            """Genera un color hexadecimal aleatorio."""
            return f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"

        def arrastrar_nodo(event):
            """Permite mover un nodo y actualiza las aristas conectadas."""
            nodo_id = canvas.find_withtag("current")[0]  # ID del objeto seleccionado
            nombre_nodo = canvas.gettags(nodo_id)[1]  # Nombre del nodo
            cx, cy = event.x, event.y
            # Asegurar que los nodos no salgan del lienzo
            cx = max(radio, min(canvas_width - radio, cx))
            cy = max(radio, min(canvas_height - radio, cy))
            # Actualiza la posición del nodo y su etiqueta
            canvas.coords(objetos_nodos[nombre_nodo]["oval"], cx - radio, cy - radio, cx + radio, cy + radio)
            canvas.coords(objetos_nodos[nombre_nodo]["text"], cx, cy)
            coordenadas[nombre_nodo] = (cx, cy)
            actualizar_aristas()

        def actualizar_aristas():
            """Redibuja las aristas según las nuevas posiciones de los nodos."""
            for arista_id, (inicio, fin) in aristas_dibujadas.items():
                x1, y1 = coordenadas[inicio]
                x2, y2 = coordenadas[fin]
                canvas.coords(arista_id, x1, y1, x2, y2)

        def mostrar_algoritmos(event):
            """Muestra el BFS y DFS del nodo seleccionado en el área de texto."""
            nodo_id = canvas.find_withtag("current")[0]  # ID del objeto seleccionado
            nombre_nodo = canvas.gettags(nodo_id)[1]  # Nombre del nodo seleccionado
            # Obtener los valores del nodo de inicio y nodo de fin desde los campos de entrada
            inicio = nombre_nodo
            fin = entrada_fin.get().strip()  # Tomar el nodo de fin
            # Si el campo de entrada de fin está vacío, lo dejamos como None
            if fin == "":
                fin = None
            # Obtener los resultados de BFS y DFS desde la clase Grafo
            bfs_resultado = self.grafo.bfs(inicio, fin)
            dfs_resultado = self.grafo.dfs(inicio, fin)

            # Mostrar los resultados en el área de texto
            resultados_texto.delete(1.0, tk.END)  # Limpiar el área de texto
            resultados_texto.insert(tk.END,
                                    f"Resultados para el nodo '{nombre_nodo}':\n\n"
                                    f"BFS: {', '.join(bfs_resultado)}\n"
                                    f"DFS: {', '.join(dfs_resultado) if dfs_resultado else 'No se encontró un camino hacia el nodo de fin.'}")

        # Generar nodos con posiciones aleatorias
        for nombre, nodo in self.grafo.nodos.items():
            cx = random.randint(radio, canvas_width - radio)
            cy = random.randint(radio, canvas_height - radio)
            coordenadas[nombre] = (cx, cy)

            # Dibujar nodo
            color_nodo = generar_color_aleatorio()
            nodo_oval = canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio, fill=color_nodo,
                                           tags=("nodo", nombre))
            nodo_text = canvas.create_text(cx, cy, text=nombre, tags=("texto", nombre))
            objetos_nodos[nombre] = {"oval": nodo_oval, "text": nodo_text}

            # Vincular movimiento y clic al nodo
            canvas.tag_bind(nodo_oval, "<B1-Motion>", arrastrar_nodo)
            canvas.tag_bind(nodo_oval, "<Button-1>", mostrar_algoritmos)  # Mostrar BFS/DFS al hacer clic

        # Dibujar las aristas con colores aleatorios
        for arista in self.grafo.aristas:
            inicio = arista.start.nombre
            fin = arista.fin.nombre
            if inicio in coordenadas and fin in coordenadas:
                x1, y1 = coordenadas[inicio]
                x2, y2 = coordenadas[fin]
                color = generar_color_aleatorio()
                arista_id = canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, fill=color, width=2, tags="arista")
                aristas_dibujadas[arista_id] = (inicio, fin)

        ventana.mainloop()
