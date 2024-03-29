from Model.Encomenda import Encomenda
from Model.Node import Node, haversine_distance
import math
from queue import Queue
from math import radians, sin, cos, sqrt, atan2
import networkx as nx  # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem
import osmnx as ox
from Model.Veiculo import *


def cria_grafo():
    g = Grafo()

    # Adiciona nodes com coordenadas
    g.add_node("1", 41.5598, -8.3925)
    g.add_node("2", 41.5656, -8.3953)
    g.add_node("3", 41.5641, -8.3918)
    g.add_node("4", 41.5625, -8.3869)
    g.add_node("5", 41.5686, -8.3914)
    g.add_node("6", 41.5679, -8.3869)
    g.add_node("7", 41.566, -8.3811)
    g.add_node("8", 41.5706, -8.3889)
    g.add_node("9", 41.5706, -8.3825)
    g.add_node("10", 41.5728, -8.3792)
    g.add_node("11", 41.5694, -8.3769)
    g.add_node("12", 41.5744, -8.3811)

    # Adiciona arestas
    g.add_edge("1", "2", 1500)
    g.add_edge("1", "3", 600)
    g.add_edge("1", "4", 1000)
    g.add_edge("3", "4", 450)
    g.add_edge("3", "6", 800)
    g.add_edge("2", "3", 650)
    g.add_edge("2", "5", 900)
    g.add_edge("4", "6", 800)
    g.add_edge("4", "7", 750)
    g.add_edge("5", "6", 650)
    g.add_edge("6", "7", 1100)
    g.add_edge("5", "8", 400)
    g.add_edge("6", "8", 1000)
    g.add_edge("6", "9", 1200)
    g.add_edge("8", "12", 1100)
    g.add_edge("8", "9", 550)
    g.add_edge("7", "9", 700)
    g.add_edge("7", "10", 850)
    g.add_edge("7", "11", 750)
    g.add_edge("9", "10", 450)
    g.add_edge("9", "12", 750)
    g.add_edge("10", "11", 500)
    g.add_edge("10", "12", 400)

    return g


class Grafo:
    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}
        self.m_h = {}

    def add_node(self, node_name, latitude, longitude):
        node = Node(node_name, latitude, longitude)
        if node not in self.m_nodes:
            node_id = len(self.m_nodes)
            node.setId(node_id)
            self.m_nodes.append(node)
            self.m_graph[node_name] = []

    def add_edge(self, node1, node2, weight):
        n1 = Node(node1)
        n2 = Node(node2)
        if n1 not in self.m_nodes:
            raise ValueError(f"Node {node1} não encontrado no grafo. Adicione o nó antes de adicionar a aresta.")
        if n2 not in self.m_nodes:
            raise ValueError(f"Node {node2} não encontrado no grafo. Adicione o nó antes de adicionar a aresta.")

        self.m_graph[node1].append((node2, weight))

        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))

    def calculate_distances(self, end):
        for i in range(len(self.m_nodes)):
            node1 = self.m_nodes[i]
            node2 = self.m_nodes[int(end) - 1]
            distance = haversine_distance(
                node1.getlatitude(), node1.getlongitude(),
                node2.getlatitude(), node2.getlongitude()
            )
            # print(distance)
            self.add_heuristica(node1, distance)

    def get_nodes(self):
        return self.m_nodes

    def get_vizinhos(self, node):
        return [vizinho for vizinho, _ in self.m_graph.get(node, [])]

    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.m_graph[nodo]:
            lista.append((adjacente, peso))
        return lista

    def getH(self, nodo):
        if nodo not in self.m_h.keys():
            return 1000
        else:
            return (self.m_h[nodo])

    def desenha(self):
        lista_v = self.m_nodes
        lista_a = []

        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                lista = (n, adjacente)
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    def add_heuristica(self, n, estima):
        n1 = Node(n)
        if n1 in self.m_nodes:
            self.m_h[n] = estima

    def calcula_custo(self, caminho):
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            i = i + 1
        return custo

    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]  # lista de arestas para aquele nodo
        for (nodo, custo) in a:
            if nodo == node2:
                custoT = custo

        return custoT

    def procura_DFS_aux(self, veiculo, start, end, path=None, visited=None):
        if path is None:
            path = []
        if visited is None:
            visited = set()
        path.append(start)
        visited.add(start)

        if start == end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return path, custoT

        for (adjacente, peso) in self.m_graph[start]:
            if adjacente not in visited:
                resultado = self.procura_DFS_aux(veiculo, adjacente, end, path, visited)
                if resultado is not None:
                    return resultado

        path.pop()  # se nao encontra remover o que está no caminho......
        return None

    def procura_DFS(self, setores_a_visitar, veiculo):
        global end
        resultado = ([],)
        res = []
        setores_a_visitar = list(setores_a_visitar)

        for i in range(len(setores_a_visitar)):
            if str(setores_a_visitar[i]) not in resultado[0]:
                if i == 0:
                    start = "1"
                    end = setores_a_visitar[i]
                else:
                    start = end
                    end = setores_a_visitar[i]

                resultado = self.procura_DFS_aux(veiculo, str(start), str(end), path=[], visited=set())

                if resultado is not None:
                    res.append(resultado)

        caminho_combinado, custo_total = somar_caminhos(res)

        print(f"Caminho combinado: {caminho_combinado}")
        print(f"Custo total: {custo_total}")
        print(f"Tempo de entrega: {calcula_tempo(custo_total, veiculo):.2f} minutos.")

        return res

    def procura_BFS_aux(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()
        custo = 0
        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)

        # reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return (path, custo)

    def procura_BFS(self, setores_a_visitar, veiculo):
        res = []
        setores_a_visitar = list(setores_a_visitar)

        for i in range(len(setores_a_visitar)):
            if i == 0:
                start = "1"
                end = setores_a_visitar[i]
            else:
                start = setores_a_visitar[i - 1]
                end = setores_a_visitar[i]

            resultado = self.procura_BFS_aux(str(start), str(end))

            if resultado is not None:
                res.append(resultado)

        caminho_combinado, custo_total = somar_caminhos(res)

        print(f"Caminho combinado: {caminho_combinado}")
        print(f"Custo total: {custo_total}")
        print(f"Tempo de entrega: {calcula_tempo(custo_total, veiculo):.2f} minutos.")

        return res

    ##########################################
    #    A*
    ##########################################

    def procura_aStar_aux(self, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        open_list = {start}
        closed_list = set([])

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}  ##  g é apra substiruir pelo peso  ???

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        # n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            n = None

            # find a node with the lowest value of f() - evaluation function
            for v in open_list:
                ##if n == None or g[v] + self.getH(v) < g[n] + self.getH(n):  # heuristica ver.....
                if n == None or g[v] + self.getH(v) < g[n] + self.getH(n):  # heuristica ver.....
                    n = v
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list:
                            closed_list.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def procura_aStar(self, setores_a_visitar, veiculo):
        global resultado
        res = []
        resultado = ([],)
        setores_a_visitar = list(setores_a_visitar)

        for i in range(len(setores_a_visitar)):
            if str(setores_a_visitar[i]) not in resultado[0]:
                if i == 0:
                    start = "1"
                    end = setores_a_visitar[i]
                else:
                    start = end
                    end = setores_a_visitar[i]

                self.calculate_distances(end)
                # print("Heurísticas após o cálculo:")
                # for node, heuristic in self.m_h.items():
                #    print(f"Nó {node.getName()}: {heuristic}")
                # print("\n")

                resultado = self.procura_aStar_aux(str(start), str(end))



            if resultado is not None:
                res.append(resultado)

        caminho_combinado, custo_total = somar_caminhos(res)

        print(f"Caminho combinado: {caminho_combinado}")
        print(f"Custo total: {custo_total}")
        print(f"Tempo de entrega: {calcula_tempo(custo_total, veiculo):.2f} minutos.")

        return res

    ##########################################
    #   Greedy
    ##########################################

    def greedy_aux(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        open_list = set([start])
        closed_list = set([])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontra nodo com a menor heuristica
            for v in open_list:
                if n == None or self.m_h[v] < self.m_h[n]:
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))
            # para todos os vizinhos  do nodo corrente

            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if m not in open_list and m not in closed_list:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list.add(n)

        print('Path does not exist!')
        return None

    def procura_greedy(self, setores_a_visitar, veiculo):
        global resultado
        res = []
        resultado = ([],)
        setores_a_visitar = list(setores_a_visitar)

        for i in range(len(setores_a_visitar)):
            if str(setores_a_visitar[i]) not in resultado[0]:
                if i == 0:
                    start = "1"
                    end = setores_a_visitar[i]
                else:
                    start = end
                    end = setores_a_visitar[i]

                self.calculate_distances(end)
                # print("Heurísticas após o cálculo:")
                # for node, heuristic in self.m_h.items():
                #    print(f"Nó {node.getName()}: {heuristic}")
                # print("\n")

                resultado = self.greedy_aux(str(start), str(end))

                # print(resultado)
                # print("\n")

            if resultado is not None:
                res.append(resultado)

        caminho_combinado, custo_total = somar_caminhos(res)

        print(f"Caminho combinado: {caminho_combinado}")
        print(f"Custo total: {custo_total}")
        print(f"Tempo de entrega: {calcula_tempo(custo_total, veiculo):.2f} minutos.")

        return res


def somar_caminhos(lista_caminhos):
    if not lista_caminhos:
        return [], 0

    caminho_combinado = []
    custo_total = 0

    for caminho, custo in lista_caminhos:
        caminho_combinado.extend(caminho[:-1])  # Adiciona todos os nós, exceto o último do caminho
        custo_total += custo

    caminho_combinado.append(lista_caminhos[-1][0][-1])  # Adiciona o último nó do último caminho

    return caminho_combinado, custo_total


def calcula_tempo(custo, veiculo):
    velocidade_media = veiculo.get_velMedia()
    peso_ocupado = veiculo.get_pesoOcupado()
    penalizacao = veiculo.get_penalizacaoPorPeso()

    # vel.med -> km
    # custo -> M

    velocidade_media -= (peso_ocupado * penalizacao)

    velocidade_media *= 1000

    return (custo / velocidade_media) * 60


def avaliar_estafeta(veiculo, custo_total):
    tempo_de_entrega = calcula_tempo(custo_total, veiculo)
    soma_tempos = 0
    contador_lista = 0

    for enc in veiculo.get_listaEncomendas():
        contador_lista += 1
        soma_tempos += Encomenda.get_tempoEntrega(enc)

    media_tempo = soma_tempos / contador_lista

    rating_estafeta = veiculo.get_estafeta().get_rating()

    if tempo_de_entrega <= media_tempo:
        diferenca_tempo = media_tempo - tempo_de_entrega
        novo_rating = min(5, rating_estafeta + diferenca_tempo / 60)
        veiculo.get_estafeta().set_rating(novo_rating)
        print(f"Tempo de entrega menor ou igual à média! {diferenca_tempo:.2f} minutos antecipado. \nRating atualizado: {novo_rating:.2f}")

    else:
        diferenca_tempo = tempo_de_entrega - media_tempo
        penalizacao = max(0, diferenca_tempo / 60)
        novo_rating = max(0, rating_estafeta - penalizacao)
        veiculo.get_estafeta().set_rating(novo_rating)
        print(f"Tempo de entrega maior que a média! Demorados {diferenca_tempo:.2f} minutos a mais. \nRating atualizado: {novo_rating:.2f}")


