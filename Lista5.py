#lista5


import random
import matplotlib.pyplot as plt
import networkx as nx
import heapq
from collections import deque

#zadanie 1
#a)

class Graph:
    def __init__(self, vertices):
        self.vertices = vertices                               # Liczba wierzchołków w grafie
        self.adj_list = {v: [] for v in range(vertices)}       # Lista sąsiedztwa: każdy wierzchołek ma listę sąsiadów

    #Dodawanie krawędzi nieskierowanej
    def add_edge(self, u, v, weight=1):

        self.adj_list[u].append((v, weight))                   #dodajemy sąsiada v do listy u (z wagą)
        self.adj_list[v].append((u, weight))                   #graf jest nieskierowany – dodajemy też odwrotnie

    #losowy grafu nieskierowy o określonej gęstości

    def generate_random_graph(vertices, density=0.3):

        g = Graph(vertices)                                    #tworzymy pusty graf z daną liczbą wierzchołków
        for i in range(vertices):
            for j in range(i + 1, vertices):                   #przechodzimy po parach wierzchołków (bez duplikatów)
                if random.random() < density:                  # Z prawdopodobieństwem density dodajemy krawędź
                    g.add_edge(i, j)                           #dodajemy krawędź między i i j
        return g                                               #zwracamy utworzony graf


#b)

    #znajdowanie składowych spójnych grafu metodą BFS
    def find_connected_components(self):

        visited = set()                                        #zbiór odwiedzonych wierzchołków
        components = []                                        #lista składowych spójnych

        for v in range(self.vertices):                         #iteracja po wszystkich wierzchołkach
            if v not in visited:
                queue = deque([v])                             #kolejka do BFS
                visited.add(v)
                component = []                                 #obecna składowa spójna

                while queue:
                    node = queue.popleft()
                    component.append(node)
                    for neighbor, _ in self.adj_list[node]:    #sprawdzamy sąsiadów bieżącego wierzchołka
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)                   #dodajemy nowo znalezioną składową
        return components

    #wizualizacja składowych spójnych z użyciem biblioteki NetworkX

    def visualize_components(self, components):

        G = nx.Graph()                                         #tworzymy obiekt grafu
        G.add_nodes_from(range(self.vertices))  #dodawanie wszystkich wierzchołków



        for u in self.adj_list:                                #nowe krawędzie
            for v, _ in self.adj_list[u]:
                if u < v:                                      #unikanie duplikatów (bo graf nieskierowany)
                    G.add_edge(u, v)

        pos = nx.spring_layout(G)                              #układ współrzędnych dla wierzchołków
        color_map = {}                                         #mapa kolorów wierzchołków wg składowych

        for i, comp in enumerate(components):
            for node in comp:
                color_map[node] = i                            #kolor dla każdej składowej

        node_colors = [color_map[node] for node in G.nodes()]                          #generowanie listy kolorów dla rysowania
        nx.draw(G, pos, node_color=node_colors, with_labels=True, cmap=plt.cm.tab20)      #rysujemy graf

        #wykres
        plt.title("Zadanie 1b:Składowe spójne grafu")
        plt.show()



g = Graph.generate_random_graph(10, 0.2)      #losowy graf o 10 wierzchołkach
print("")
print("Zadanie1_a: Wygenerowany graf (lista sąsiedztwa):")
for node in g.adj_list:
    print(f"Wierzchołek {node}: {g.adj_list[node]}")



components = g.find_connected_components()
#szukanie składowych spójnych
print("")
print("Zadanie1_b:")
print(components,"\n")  #wynik

g.visualize_components(components)        #wizualizujemy składowe


#zadanie 2  Algorytm Dijkstry
#a)

#klasyczna implementacja algorytmu Dijkstry

def dijkstra(graph, start):

    distances = {v: float('inf') for v in range(graph.vertices)}  #inicjalizacja odległości jako nieskończoność
    distances[start] = 0                                          #odległość startowa to 0
    heap = [(0, start)]                                           #kolejka priorytetowa (min-heap)
    prev = {}                                                     #mapa poprzedników (dla ścieżki)

    while heap:

        current_dist, u = heapq.heappop(heap)                     #wybieramy wierzchołek o najmniejszej odległości

        if current_dist > distances[u]:                           #pomijamy jeśli mamy lepszą ścieżkę
            continue


        for v, weight in graph.adj_list[u]:                       #iterujemy po sąsiadach
            new_dist = current_dist + weight                      #obliczamy nową odległość

            if new_dist < distances[v]:                           #aktualizujemy jeśli krótsza

                distances[v] = new_dist
                prev[v] = u
                heapq.heappush(heap, (new_dist, v))               #dodawanie do kolejki

    return distances, prev                                        #zwracanie odległości i ścieżki


#b) Modyfikacja Dikstry

#odzyskiwanie ścieżki od punktu A do B

def shortest_path(graph, start, end):

    distances, prev = dijkstra(graph, start)

    if distances[end] == float('inf'):
        return None, None                                         # brak ścieżki

    path = []
    current = end

    while current in prev:
        path.insert(0, current)                                   #składanie ścieżki od końca
        current = prev[current]
    path.insert(0, start)

    return path, distances[end]                                   #zwracanie ścieżkę i długość

# c) Wersja wieloźródłowa Dijkstry

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

g = Graph(5)
g.add_edge(0, 1, 4)
g.add_edge(0, 2, 2)
g.add_edge(1, 2, 1)
g.add_edge(1, 3, 5)
g.add_edge(2, 3, 8)
g.add_edge(2, 4, 10)
g.add_edge(3, 4, 2)

start, end = 0, 4
path, dist = shortest_path(g, start, end)                         #wyznaczanie ścieżki między 0 a 4
print("Zadanie2_a:")
print(f"Najkrótsza ścieżka z {start} do {end}: {path}, Długość: {dist}","\n")

sources = [0, 3]
distances, _ = multi_source_dijkstra(g, sources)                  #wyznaczanie odległości od 0 lub 3
print("Zadanie2_b:")
print("Odległości od najbliższego źródła:", distances,"\n")

#c)
print("Zadanie2_c:")
print("Drzewo rozpinające utworzone przez ścieżki Dijkstry jest drzewem najkrótszych ścieżek od źródła. Jego własnością jest minimalizacja sumy wag ścieżek do wszystkich wierzchołków.","\n")


#zadanie 3  Algorytmy Kruskala i Prima
#a)

#Struktura Union-Find do algorytmu Kruskala
class UnionFind:
    def __init__(self, size):

        self.parent = list(range(size))                           #każdy wierzchołek jest swoim rodzicem

    def find(self, x):

        if self.parent[x] != x:                                   #znajdujemy korzeń drzewa z kompresją ścieżki
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):

        root_x = self.find(x)                                     #łączenie dwóch drzew (jeśli mają różne korzenie)
        root_y = self.find(y)
        if root_x != root_y:
            self.parent[root_y] = root_x


#Algorytm Kruskala

def kruskal(graph):
    edges = []

    for u in graph.adj_list:

        for v, w in graph.adj_list[u]:
            if u < v:                                             #unikanie duplikatów
                edges.append((w, u, v))

    edges.sort()                                                  #sortowanie krawędzi po wadze
    uf = UnionFind(graph.vertices)
    mst = []

    for w, u, v in edges:
        if uf.find(u) != uf.find(v):                              #jesli nie tworzy cyklu, dodaj do MST
            uf.union(u, v)
            mst.append((u, v, w))

    return mst

#b) Algorytm Prima


def prim(graph):

    visited = set()
    mst = []
    heap = []

    start = next(iter(graph.adj_list))                            #zaczynanie od dowolnego wierzchołka
    visited.add(start)

    for v, w in graph.adj_list[start]:
        heapq.heappush(heap, (w, start, v))                       #dodawanie sąsiadów do kolejki

    while heap:

        w, u, v = heapq.heappop(heap)
        if v not in visited:                                      #jeśli nieodwiedzony, dodaj do MST
            visited.add(v)
            mst.append((u, v, w))

            for neighbor, weight in graph.adj_list[v]:
                if neighbor not in visited:
                    heapq.heappush(heap, (weight, v, neighbor))

    return mst


g = Graph(4)
g.add_edge(0, 1, 10)
g.add_edge(0, 2, 6)
g.add_edge(0, 3, 5)
g.add_edge(1, 3, 15)
g.add_edge(2, 3, 4)

print("Zadanie3_a:")
print("Minimalne Drzewo Rozpinające – Kruskal:", kruskal(g),"\n")

print("Zadanie3_b:")
print("Minimalne Drzewo Rozpinające – Prim:", prim(g),"\n")