#lista5
#test



import random
import matplotlib.pyplot as plt
import networkx as nx
import heapq
from collections import deque

#zadanie 1 –

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices                               # Liczba wierzchołków w grafie
        self.adj_list = {v: [] for v in range(vertices)}       # Lista sąsiedztwa: każdy wierzchołek ma listę sąsiadów

    # a) Dodawanie krawędzi nieskierowanej
    def add_edge(self, u, v, weight=1):
        self.adj_list[u].append((v, weight))                   # Dodajemy sąsiada v do listy u (z wagą)
        self.adj_list[v].append((u, weight))                   # Ponieważ graf jest nieskierowany – dodajemy też odwrotnie

    # b) Generowanie losowego grafu nieskierowanego o określonej gęstości
    @staticmethod
    def generate_random_graph(vertices, density=0.3):
        g = Graph(vertices)                                    # Tworzymy pusty graf z daną liczbą wierzchołków
        for i in range(vertices):
            for j in range(i + 1, vertices):                   # Przechodzimy po parach wierzchołków (bez duplikatów)
                if random.random() < density:                  # Z prawdopodobieństwem density dodajemy krawędź
                    g.add_edge(i, j)                           # Dodajemy krawędź między i i j
        return g                                               # Zwracamy utworzony graf

    # c) Znajdowanie składowych spójnych grafu metodą BFS
    def find_connected_components(self):
        visited = set()                                        # Zbiór odwiedzonych wierzchołków
        components = []                                        # Lista składowych spójnych

        for v in range(self.vertices):                         # Iterujemy po wszystkich wierzchołkach
            if v not in visited:
                queue = deque([v])                             # Kolejka do BFS
                visited.add(v)
                component = []                                 # Obecna składowa spójna

                while queue:
                    node = queue.popleft()
                    component.append(node)
                    for neighbor, _ in self.adj_list[node]:    # Sprawdzamy sąsiadów bieżącego wierzchołka
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)                   # Dodajemy nowo znalezioną składową
        return components

    # d) Wizualizacja składowych spójnych z użyciem biblioteki NetworkX
    def visualize_components(self, components):
        G = nx.Graph()                                         # Tworzymy obiekt grafu
        G.add_nodes_from(range(self.vertices))                 # Dodajemy wszystkie wierzchołki

        for u in self.adj_list:                                # Dodajemy krawędzie
            for v, _ in self.adj_list[u]:
                if u < v:                                      # Unikamy duplikatów (bo graf nieskierowany)
                    G.add_edge(u, v)

        pos = nx.spring_layout(G)                              # Układ współrzędnych dla wierzchołków
        color_map = {}                                         # Mapa kolorów wierzchołków wg składowych

        for i, comp in enumerate(components):
            for node in comp:
                color_map[node] = i                            # Przypisujemy kolor każdej składowej

        node_colors = [color_map[node] for node in G.nodes()] # Generujemy listę kolorów dla rysowania
        nx.draw(G, pos, node_color=node_colors, with_labels=True, cmap=plt.cm.tab20)  # Rysujemy graf
        plt.title("Składowe spójne grafu")
        plt.show()                                             # Wyświetlamy wykres


# --- Testowanie zadania 1
g = Graph.generate_random_graph(10, 0.2)                       # Tworzymy losowy graf o 10 wierzchołkach
components = g.find_connected_components()                     # Szukamy składowych spójnych
print("Składowe spójne:", components)                          # Wyświetlamy wynik
g.visualize_components(components)                             # Wizualizujemy składowe


#zadanie 2  Algorytm Dijkstry


# a) Klasyczna implementacja algorytmu Dijkstry

def dijkstra(graph, start):
    distances = {v: float('inf') for v in range(graph.vertices)}  # Inicjalizacja odległości jako nieskończoność
    distances[start] = 0                                          # Odległość startowa to 0
    heap = [(0, start)]                                           # Kolejka priorytetowa (min-heap)
    prev = {}                                                     # Mapa poprzedników (dla ścieżki)

    while heap:
        current_dist, u = heapq.heappop(heap)                     # Wybieramy wierzchołek o najmniejszej odległości
        if current_dist > distances[u]:                           # Pomijamy jeśli mamy lepszą ścieżkę
            continue

        for v, weight in graph.adj_list[u]:                       # Iterujemy po sąsiadach
            new_dist = current_dist + weight                      # Obliczamy nową odległość
            if new_dist < distances[v]:                           # Aktualizujemy jeśli krótsza
                distances[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))               # Dodajemy do kolejki

    return distances, prev                                        # Zwracamy odległości i ścieżki


# b) Odzyskiwanie ścieżki od punktu A do B

def shortest_path(graph, start, end):
    distances, prev = dijkstra(graph, start)

    if distances[end] == float('inf'):
        return None, None                                         # Brak ścieżki

    path = []
    current = end
    while current in prev:
        path.insert(0, current)                                   # Składamy ścieżkę od końca
        current = prev[current]
    path.insert(0, start)

    return path, distances[end]                                   # Zwracamy ścieżkę i długość

# c) Wersja wieloźródłowa Dijkstry

def multi_source_dijkstra(graph, sources):
    distances = {v: float('inf') for v in range(graph.vertices)}
    prev = {}
    heap = []

    for s in sources:                                             # Inicjalizacja dla wielu źródeł
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

# --- Testowanie zadania 2
g = Graph(5)
g.add_edge(0, 1, 4)
g.add_edge(0, 2, 2)
g.add_edge(1, 2, 1)
g.add_edge(1, 3, 5)
g.add_edge(2, 3, 8)
g.add_edge(2, 4, 10)
g.add_edge(3, 4, 2)

start, end = 0, 4
path, dist = shortest_path(g, start, end)                         # Wyznaczamy ścieżkę między 0 a 4
print(f"Najkrótsza ścieżka z {start} do {end}: {path}, Długość: {dist}")

sources = [0, 3]
distances, _ = multi_source_dijkstra(g, sources)                  # Wyznaczamy odległości od 0 lub 3
print("Odległości od najbliższego źródła:", distances)



#zadanie 3 – Minimalne Drzewo Rozpinające (MST)

# a) Struktura Union-Find do algorytmu Kruskala
class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))                           # Każdy wierzchołek jest swoim rodzicem

    def find(self, x):
        if self.parent[x] != x:                                   # Znajdujemy korzeń drzewa z kompresją ścieżki
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)                                     # Łączymy dwa drzewa (jeśli mają różne korzenie)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x


# b) Algorytm Kruskala

def kruskal(graph):
    edges = []
    for u in graph.adj_list:
        for v, w in graph.adj_list[u]:
            if u < v:                                             # Unikamy duplikatów
                edges.append((w, u, v))

    edges.sort()                                                  # Sortujemy krawędzie po wadze
    uf = UnionFind(graph.vertices)
    mst = []

    for w, u, v in edges:
        if uf.find(u) != uf.find(v):                              # Jeśli nie tworzy cyklu, dodaj do MST
            uf.union(u, v)
            mst.append((u, v, w))

    return mst


# c) Algorytm Prima
def prim(graph):
    visited = set()
    mst = []
    heap = []

    start = next(iter(graph.adj_list))                            # Zaczynamy od dowolnego wierzchołka
    visited.add(start)

    for v, w in graph.adj_list[start]:
        heapq.heappush(heap, (w, start, v))                       # Dodajemy sąsiadów do kolejki

    while heap:
        w, u, v = heapq.heappop(heap)
        if v not in visited:                                      # Jeśli nieodwiedzony, dodaj do MST
            visited.add(v)
            mst.append((u, v, w))

            for neighbor, weight in graph.adj_list[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (weight, v, neighbor))

    return mst

# --- Testowanie zadania 3
g = Graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

print("Minimalne Drzewo Rozpinające – Kruskal:", kruskal(g))
print("Minimalne Drzewo Rozpinające – Prim:", prim(g))
