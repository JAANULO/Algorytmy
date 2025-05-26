# lista5
# 5

import random
import matplotlib.pyplot as plt
import networkx as nx
import heapq
from collections import deque


#zadanie 1

# a) Implementacja grafu i wyszukiwanie składowych spójnych

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices  # liczba wierzchołków w grafie
        self.adj_list = {v: [] for v in range(vertices)}  # lista sąsiedztwa: każdy wierzchołek ma listę sąsiadów

    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append((v, weight))  # dodajemy sąsiada v do listy u (z wagą)
        self.adj_list[v].append((u, weight))  # graf jest nieskierowany – dodajemy też odwrotnie

    @staticmethod
    def generate_random_graph(vertices, density=0.3):

        g = Graph(vertices)  # tworzymy pusty graf z daną liczbą wierzchołków
        for i in range(vertices):
            for j in range(i + 1, vertices):  # przechodzimy po parach wierzchołków (bez duplikatów)
                if random.random() < density:  # z prawdopodobieństwem density dodajemy krawędź
                    g.add_edge(i, j)  # dodajemy krawędź między i i j
        return g  # zwracamy utworzony graf


# b) Wyświetl przypisanie wierzchołków do poszczególnych składowych i wizualizacja


    def find_connected_components(self):

        visited = set()  # zbór odwiedzonych wierzchołków
        components = []  # lista składowych spójnych

        for v in range(self.vertices):  # iteracja po wszystkich wierzchołkach
            if v not in visited:
                queue = deque([v])  # kolejka do BFS
                visited.add(v)
                component = []  # obecna składowa spójna

                while queue:
                    node = queue.popleft()
                    component.append(node)
                    for neighbor, _ in self.adj_list[node]:  # sprawdzamy sąsiadów bieżącego wierzchołka
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)  # dodajemy nowo znalezioną składową
        return components


    def visualize_components(self, components):

        G = nx.Graph()  # tworzymy obiekt grafu
        G.add_nodes_from(range(self.vertices))  # dodawanie wszystkich wierzchołków

        for u in self.adj_list:  # nowe krawędzie
            for v, _ in self.adj_list[u]:
                if u < v:  # unikanie duplikatów (bo graf nieskierowany)
                    G.add_edge(u, v)

        pos = nx.spring_layout(G, seed=42)  # stały układ dla powtarzalności
        plt.figure(figsize=(10, 6))

        color_map = {}
        for i, comp in enumerate(components):
            for node in comp:
                color_map[node] = i

        nx.draw(G, pos,
                node_color=[color_map[node] for node in G.nodes()],
                edge_color='gray',
                with_labels=True,
                cmap=plt.cm.tab20,
                font_weight='bold')

        plt.title("Zadanie 1: Składowe spójne grafu")
        plt.show()


#zadanie 2: Algorytm Dijkstry i ścieżka

#a) Wyświetl odpowiedź jako ciąg wierzchołków i odległości między nimi

def dijkstra(graph, start):

    distances = {v: float('inf') for v in range(graph.vertices)}  # inicjalizacja odległości jako nieskończoność
    distances[start] = 0   # odległość startowa to 0
    heap = [(0, start)]   # kolejka priorytetowa (min-heap)
    prev = {}       # mapa poprzedników (dla ścieżki)

    while heap:
        current_dist, u = heapq.heappop(heap)  # wybieramy wierzchołek o najmniejszej odległości

        if current_dist > distances[u]:  # pomijamy jeśli mamy lepszą ścieżkę
            continue

        for v, weight in graph.adj_list[u]:  # iterujemy po sąsiadach
            new_dist = current_dist + weight  # obliczamy nową odległość

            if new_dist < distances[v]:  # aktualizujemy jeśli krótsza

                distances[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))  # dodawanie do kolejki

    return distances, prev  # zwracanie odległości i ścieżki



#b) Modyfikacja Dikstry - najkrutsza ścieżka



def multi_source_dijkstra(graph, sources):
    distances = {v: float('inf') for v in range(graph.vertices)}
    prev = {}
    heap = []

    for s in sources:                                             #inicjalizacja dla wielu źródeł
        distances[s] = 0
        heapq.heappush(heap, (0, s))

    while heap:
        current_dist, u = heapq.heappop(heap)

        if current_dist > distances[u]:
            continue

        for v, weight in graph.adj_list[u]:
            new_dist = current_dist + weight

            if new_dist < distances[v]:
                distances[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))

    return distances, prev

def shortest_path(graph, start, end):
    distances, prev = dijkstra(graph, start)


    if distances[end] == float('inf'):
        return None, None  # brak ścieżki

    path = []
    current = end

    while current in prev:
        path.insert(0, current)  # składanie ścieżki od końca
        current = prev[current]
    path.insert(0, start)

    return path, distances[end]  # zwracanie ścieżki i długości


def visualize_dijkstra(graph, path, start, end):
    G = nx.Graph()
    for u in graph.adj_list:
        for v, w in graph.adj_list[u]:
            if u < v:
                G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))

    edge_colors = []
    for u, v in G.edges():
        if (u in path and v in path and abs(path.index(u) - path.index(v)) == 1):
            edge_colors.append('red')
        else:
            edge_colors.append('gray')

    nx.draw(G, pos,
            node_color='lightblue',
            edge_color=edge_colors,
            width=2,
            with_labels=True,
            font_weight='bold')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(f"Zadanie 2: Najkrótsza ścieżka z {start} do {end}")
    plt.show()


#zadanie 3: Minimalne Drzewo Rozpinające


# a) Kruskal

class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))  # każdy wierzchołek jest swoim rodzicem

    def find(self, x):
        if self.parent[x] != x:  # znajdujemy korzeń drzewa z kompresją ścieżki
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)  # łączenie dwóch drzew (jeśli mają różne korzenie)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x


def kruskal(graph):
    edges = []
    for u in graph.adj_list:
        for v, w in graph.adj_list[u]:
            if u < v:  # unikanie duplikatów
                edges.append((w, u, v))

    edges.sort()  # sortowanie krawędzi po wadze
    uf = UnionFind(graph.vertices)
    mst = []

    for w, u, v in edges:
        if uf.find(u) != uf.find(v):  # jesli nie tworzy cyklu, dodaj do MST
            uf.union(u, v)
            mst.append((u, v, w))

    return mst


# b) Prim

def prim(graph):
    visited = set()
    mst = []
    heap = []

    start = next(iter(graph.adj_list))  # zaczynanie od dowolnego wierzchołka
    visited.add(start)

    for v, w in graph.adj_list[start]:
        heapq.heappush(heap, (w, start, v))  # dodawanie sąsiadów do kolejki

    while heap:
        w, u, v = heapq.heappop(heap)
        if v not in visited:  # jeśli nieodwiedzony, dodaj do MST
            visited.add(v)
            mst.append((u, v, w))

            for neighbor, weight in graph.adj_list[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (weight, v, neighbor))

    return mst


def visualize_mst(graph, mst_edges, title):
    G = nx.Graph()
    for u in graph.adj_list:
        for v, w in graph.adj_list[u]:
            if u < v:
                G.add_edge(u, v, weight=w)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))

    edge_colors = ['red' if (u, v, w) in mst_edges or (v, u, w) in mst_edges else 'gray'
                   for u, v, w in G.edges(data='weight')]

    nx.draw(G, pos,
            node_color='lightgreen',
            edge_color=edge_colors,
            width=2,
            with_labels=True,
            font_weight='bold')

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.show()


#Wywoływanie

if __name__ == "__main__":

    #Zadanie 1

    g1 = Graph(7)
    g1.add_edge(1, 3, 1)
    g1.add_edge(1, 6, 1)
    g1.add_edge(3, 6, 1)
    g1.add_edge(6, 5, 1)
    g1.add_edge(5, 2, 1)
    g1.add_edge(5, 4, 1)
    g1.add_edge(4, 2, 1)

    print("\nZadanie1_a: ")
    #g1 = Graph.generate_random_graph(10, 0.2)
    print("Lista sąsiedztwa:")
    for node in g1.adj_list:
        print(f"Wierzchołek {node}: {g1.adj_list[node]}")

    components = g1.find_connected_components()
    print("\nZadanie1_b: ")
    print("Składowe spójne:", components)
    g1.visualize_components(components)

    #Zadanie 2

    # g2 = Graph(5)
    # g2.add_edge(0, 1, 4)
    # g2.add_edge(0, 2, 2)
    # g2.add_edge(1, 2, 1)
    # g2.add_edge(1, 3, 5)
    # g2.add_edge(2, 3, 8)
    # g2.add_edge(2, 4, 10)
    # g2.add_edge(3, 4, 2)

    g2 = Graph(9)
    g2.add_edge(1, 2, 1)
    g2.add_edge(1, 3, 5)
    g2.add_edge(2, 4, 8)
    g2.add_edge(3, 5, 1)
    g2.add_edge(3, 4, 1)
    g2.add_edge(4, 5, 4)
    g2.add_edge(4, 6, 2)
    g2.add_edge(5, 6, 7)

    #a
    start, end = 1, 6
    path, dist = shortest_path(g2, start, end)
    print("\nZadanie2_a: ")
    print(f"Najkrótsza ścieżka z {start} do {end}: {path}, Długość: {dist}")
    visualize_dijkstra(g2, path, start, end)

    #b
    starts_b = [0, 3]
    distances_b, _ = multi_source_dijkstra(g2, starts_b)
    print("\nZadanie2_b:")
    print(f"Odległości od najbliższego źródła: {distances_b}")

    #Zadanie 3

    #Kruskal
    # g3 = Graph(4)
    # g3.add_edge(0, 1, 10)
    # g3.add_edge(0, 2, 6)
    # g3.add_edge(0, 3, 5)
    # g3.add_edge(1, 3, 15)
    # g3.add_edge(2, 3, 4)

    g3 = Graph(9)
    g3.add_edge(1, 2, 1)
    g3.add_edge(1, 3, 5)
    g3.add_edge(2, 4, 8)
    g3.add_edge(3, 5, 1)
    g3.add_edge(3, 4, 1)
    g3.add_edge(4, 5, 4)
    g3.add_edge(4, 6, 2)
    g3.add_edge(5, 6, 7)

    mst_kruskal = kruskal(g3)
    print("\nZadanie3: ")
    print("MST Kruskala:", mst_kruskal)
    visualize_mst(g3, mst_kruskal, "MST Kruskala")

    mst_prim = prim(g3)
    print("MST Prima:", mst_prim)
    visualize_mst(g3, mst_prim, "MST Prima")
