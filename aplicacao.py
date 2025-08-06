import osmnx as ox
import networkx as nx
import random
import numpy as np
import math
import matplotlib.pyplot as plt

# 1. Definir pontos reais da cidade (João Pessoa - PB)
# Os valores estão no formato (longitude, latitude)
locais = {
    "UFPB": (-34.8708, -7.1377),
    "Shopping Manaíra": (-34.8360, -7.1126),
    "Busto de Tamandaré": (-34.8256, -7.1177),
    "Centro Histórico": (-34.8783, -7.1225),
    "Estação Cabo Branco": (-34.7942, -7.1480)
}

# 2. Baixar o grafo de ruas da cidade
# Utiliza OpenStreetMap via osmnx para obter as vias para veículos (drive)
G = ox.graph_from_place("João Pessoa, Brazil", network_type='drive')

# 3. Obter nós mais próximos dos locais no grafo
nodes = {nome: ox.distance.nearest_nodes(G, lon, lat) for nome, (lon, lat) in locais.items()}
locais_nomes = list(nodes.keys())

# 4. Calcular matriz de distâncias reais (vias)
# Usa o menor caminho entre nós no grafo, baseado na distância real das ruas
dist_matrix = {}
paths_matrix = {} # Adiciona uma matriz para armazenar os caminhos
for origem in locais_nomes:
    dist_matrix[origem] = {}
    paths_matrix[origem] = {}
    for destino in locais_nomes:
        if origem == destino:
            dist_matrix[origem][destino] = 0
            paths_matrix[origem][destino] = [nodes[origem]]
        else:
            caminho = nx.shortest_path(G, nodes[origem], nodes[destino], weight='length')
            dist_matrix[origem][destino] = sum(ox.utils_graph.get_route_edge_attributes(G, caminho, 'length'))
            paths_matrix[origem][destino] = caminho

# 5. Função de avaliação (fitness): distância total da rota
# Soma a distância entre todos os pontos, incluindo o retorno ao ponto inicial
def fitness_function(rota):
    total_dist = 0
    for i in range(len(rota)):
        origem = rota[i]
        destino = rota[(i + 1) % len(rota)] # Retorno ao ponto inicial
        total_dist += dist_matrix[origem][destino]
    return total_dist

# 6. Algoritmo Hill Climbing
# Faz trocas locais e aceita apenas melhorias
def hill_climb(rota_inicial):
    atual = rota_inicial[:]
    atual_custo = fitness_function(atual)
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(len(atual)):
            for j in range(i + 1, len(atual)):
                nova = atual[:]
                nova[i], nova[j] = nova[j], nova[i]
                novo_custo = fitness_function(nova)
                if novo_custo < atual_custo:
                    atual, atual_custo = nova, novo_custo
                    melhorou = True
    return atual, atual_custo

# 7. Algoritmo Simulated Annealing
# Permite piores soluções temporariamente para evitar mínimos locais
def simulated_annealing(rota_inicial, T=1000, T_min=1e-6, alpha=0.995):
    atual = rota_inicial[:]
    atual_custo = fitness_function(atual)
    melhor = atual[:]
    melhor_custo = atual_custo
    while T > T_min:
        i, j = random.sample(range(len(atual)), 2)
        nova = atual[:]
        nova[i], nova[j] = nova[j], nova[i]
        novo_custo = fitness_function(nova)
        delta = novo_custo - atual_custo
        if delta < 0 or random.random() < math.exp(-delta / T):
            atual, atual_custo = nova, novo_custo
            if atual_custo < melhor_custo:
                melhor, melhor_custo = atual[:], atual_custo
        T *= alpha
    return melhor, melhor_custo

# 8. Algoritmo Genético
# Simula evolução com cruzamento, mutação e seleção natural
def crossover(p1, p2):
    start, end = sorted(random.sample(range(len(p1)), 2))
    meio = p1[start:end]
    resto = [x for x in p2 if x not in meio]
    return resto[:start] + meio + resto[start:]

def mutate(rota):
    i, j = random.sample(range(len(rota)), 2)
    rota[i], rota[j] = rota[j], rota[i]

def genetic_algorithm(pop_size=20, generations=200):
    pop = [random.sample(locais_nomes, len(locais_nomes)) for _ in range(pop_size)]
    for _ in range(generations):
        pop.sort(key=fitness_function)
        nova_pop = pop[:2]  # elitismo: preserva os melhores
        while len(nova_pop) < pop_size:
            p1, p2 = random.sample(pop[:10], 2)
            filho = crossover(p1, p2)
            if random.random() < 0.2:
                mutate(filho)
            nova_pop.append(filho)
        pop = nova_pop
    melhor = pop[0]
    return melhor, fitness_function(melhor)

# 9. Testar algoritmos com rota embaralhada
rota_inicial = locais_nomes[:]
random.shuffle(rota_inicial)

rota_hill, custo_hill = hill_climb(rota_inicial)
rota_sa, custo_sa = simulated_annealing(rota_inicial)
rota_gen, custo_gen = genetic_algorithm()

# 10. Função para plotar uma rota no mapa
def plot_route(route, G, nodes, paths_matrix, title):
    """
    Plota uma rota no grafo de ruas usando caminhos pré-calculados.
    """
    all_paths = []
    # Cria uma lista de caminhos de nós, incluindo o retorno ao início
    for i in range(len(route)):
        origem = route[i]
        destino = route[(i + 1) % len(route)]
        all_paths.append(paths_matrix[origem][destino])

    # Concatena todos os caminhos em uma única lista de nós
    route_nodes = [node for path in all_paths for node in path]

    # Plota o mapa
    fig, ax = ox.plot_graph_route(G, route_nodes, node_size=15, show=False, close=False, route_color='b', route_linewidth=4, bgcolor='#ffffff', route_alpha=0.7)
    
    # Adiciona os marcadores dos locais
    for nome, node_id in nodes.items():
        point = G.nodes[node_id]
        ax.scatter(point['x'], point['y'], c='red', s=50, zorder=3)
        ax.text(point['x'], point['y'], f' {nome}', fontsize=8, ha='left', va='center')

    ax.set_title(title)
    plt.tight_layout()
    plt.show()

# 11. Resultados
print("Rota inicial:        ", ' -> '.join(rota_inicial), "| Custo: %.2f m" % fitness_function(rota_inicial))
print("Hill Climbing:       ", ' -> '.join(rota_hill), "| Custo: %.2f m" % custo_hill)
print("Simulated Annealing: ", ' -> '.join(rota_sa), "| Custo: %.2f m" % custo_sa)
print("Algoritmo Genético:  ", ' -> '.join(rota_gen), "| Custo: %.2f m" % custo_gen)

# 12. Visualização das rotas
plot_route(rota_inicial, G, nodes, paths_matrix, "Rota Inicial (Embaralhada)")
plot_route(rota_hill, G, nodes, paths_matrix, "Rota Hill Climbing")
plot_route(rota_sa, G, nodes, paths_matrix, "Rota Simulated Annealing")
plot_route(rota_gen, G, nodes, paths_matrix, "Rota Algoritmo Genético")