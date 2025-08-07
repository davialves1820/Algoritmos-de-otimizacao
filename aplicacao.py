# Importa as bibliotecas necessárias para o projeto

import osmnx as ox # Para baixar e trabalhar com grafos de ruas do OpenStreetMap
import networkx as nx # Para analisar e manipular grafos, como encontrar o caminho mais curto
import random # Para gerar números aleatórios, usado na rota inicial e em alguns algoritmos
import numpy as np # Para operações numéricas de alta performance (opcional, mas comum)
import math # Para funções matemáticas, como a exponencial usada no Simulated Annealing
import matplotlib.pyplot as plt # Para plotar os mapas e visualizações
import time # Para medir o tempo de execução de cada algoritmo
import os # Para interagir com o sistema de arquivos, como criar pastas

# Definir os pontos de interesse na cidade de João Pessoa (PB).
# O formato é um dicionário onde a chave é o nome do local e o valor é uma tupla (longitude, latitude).
locais = {
    "UFPB": (-34.8708, -7.1377),
    "Shopping Manaíra": (-34.8360, -7.1126),
    "Busto de Tamandaré": (-34.8256, -7.1177),
    "Centro Histórico": (-34.8783, -7.1225),
    "Estação Cabo Branco": (-34.7942, -7.1480)
}

# Baixar o grafo de ruas da cidade de João Pessoa a partir do OpenStreetMap.
# O 'network_type' define que queremos um grafo de vias para veículos.
G = ox.graph_from_place("João Pessoa, Brazil", network_type='drive')

# Mapear os pontos de interesse para os nós mais próximos no grafo de ruas.
# Isso é necessário porque as coordenadas exatas dos locais podem não ser um nó de interseção.
nodes = {nome: ox.distance.nearest_nodes(G, lon, lat) for nome, (lon, lat) in locais.items()}
locais_nomes = list(nodes.keys())

# Calcular a matriz de distâncias reais (por vias) e os caminhos entre todos os pares de locais.
# Isso evita recalcular o menor caminho várias vezes durante a execução dos algoritmos.
dist_matrix = {}
paths_matrix = {}
for origem in locais_nomes:
    dist_matrix[origem] = {}
    paths_matrix[origem] = {}
    for destino in locais_nomes:
        if origem == destino:
            # A distância de um ponto para ele mesmo é zero.
            dist_matrix[origem][destino] = 0
            paths_matrix[origem][destino] = [nodes[origem]]
        else:
            try:
                # Encontrar o caminho mais curto usando o 'weight' (peso) 'length' (comprimento da rua).
                caminho = nx.shortest_path(G, nodes[origem], nodes[destino], weight='length')
                dist = 0
                # Somar o comprimento de cada aresta no caminho para obter a distância total.
                for i in range(len(caminho) - 1):
                    u, v = caminho[i], caminho[i+1]
                    dist += G.get_edge_data(u, v)[0]['length']
                dist_matrix[origem][destino] = dist
                paths_matrix[origem][destino] = caminho
            except nx.NetworkXNoPath:
                # Tratar o caso de não haver um caminho entre dois pontos no grafo.
                print(f"Aviso: Não foi encontrado um caminho entre {origem} e {destino}.")
                dist_matrix[origem][destino] = float('inf') # Define a distância como infinita
                paths_matrix[origem][destino] = []

# Função de avaliação (fitness): calcula a distância total de uma rota completa.
# Esta função é a métrica usada para medir a qualidade de cada solução.
def fitness_function(rota):
    total_dist = 0
    for i in range(len(rota)):
        origem = rota[i]
        destino = rota[(i + 1) % len(rota)] # Retorna ao ponto inicial no final
        total_dist += dist_matrix[origem][destino]
    return total_dist

# Algoritmo Hill Climbing.
# Faz trocas locais e só aceita melhorias (menor distância).
def hill_climb(rota_inicial):
    atual = rota_inicial[:]
    atual_custo = fitness_function(atual)
    melhorou = True
    while melhorou:
        melhorou = False
        for i in range(len(atual)):
            for j in range(i + 1, len(atual)):
                nova = atual[:]
                nova[i], nova[j] = nova[j], nova[i] # Faz uma troca
                novo_custo = fitness_function(nova)
                if novo_custo < atual_custo: # Se a nova rota é melhor
                    atual, atual_custo = nova, novo_custo
                    melhorou = True # Continua buscando melhorias
    return atual, atual_custo

# Algoritmo Simulated Annealing.
# Similar ao Hill Climbing, mas pode aceitar soluções piores para evitar mínimos locais.
def simulated_annealing(rota_inicial, T=1000, T_min=1e-6, alpha=0.995):
    atual = rota_inicial[:]
    atual_custo = fitness_function(atual)
    melhor = atual[:]
    melhor_custo = atual_custo
    while T > T_min:
        i, j = random.sample(range(len(atual)), 2)
        nova = atual[:]
        nova[i], nova[j] = nova[j], nova[i] # Faz uma troca
        novo_custo = fitness_function(nova)
        delta = novo_custo - atual_custo
        # Aceita a nova rota se for melhor (delta < 0) ou por probabilidade.
        if delta < 0 or random.random() < math.exp(-delta / T):
            atual, atual_custo = nova, novo_custo
            if atual_custo < melhor_custo:
                melhor, melhor_custo = atual[:], atual_custo
        T *= alpha # Reduz a temperatura (probabilidade de aceitar piores soluções)
    return melhor, melhor_custo

# Algoritmo Genético.
# Simula a evolução com cruzamento e mutação de uma população de rotas.
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
        nova_pop = pop[:2] # Elitismo: mantém os 2 melhores indivíduos
        while len(nova_pop) < pop_size:
            p1, p2 = random.sample(pop[:10], 2)
            filho = crossover(p1, p2)
            if random.random() < 0.2:
                mutate(filho)
            nova_pop.append(filho)
        pop = nova_pop
    melhor = pop[0]
    return melhor, fitness_function(melhor)

# Execução Principal e Medição de Tempo ---
# Testar os algoritmos e medir seus tempos de execução.
rota_inicial = locais_nomes[:]
random.shuffle(rota_inicial)

start_time = time.time()
rota_hill, custo_hill = hill_climb(rota_inicial)
time_hill = time.time() - start_time

start_time = time.time()
rota_sa, custo_sa = simulated_annealing(rota_inicial)
time_sa = time.time() - start_time

start_time = time.time()
rota_gen, custo_gen = genetic_algorithm()
time_gen = time.time() - start_time

# Funções para criar as pastas de resultados e plotar os mapas.
def create_folders_if_not_exists():
    # Cria a pasta 'img' para as imagens dos mapas, se não existir.
    if not os.path.exists("img"):
        os.makedirs("img")
    # Cria a pasta 'results' para o arquivo de texto, se não existir.
    if not os.path.exists("results"):
        os.makedirs("results")

def plot_route(route, G, nodes, paths_matrix, title, filename):
    # Constrói o caminho completo da rota unindo todos os caminhos entre os pontos.
    all_paths = []
    for i in range(len(route)):
        origem = route[i]
        destino = route[(i + 1) % len(route)]
        all_paths.append(paths_matrix[origem][destino])
    
    # Prepara a lista de nós para a função de plotagem do OSMnx.
    route_nodes = [node for path in all_paths for node in path if path]
    final_nodes = [route_nodes[0]]
    for node in route_nodes[1:]:
        if node != final_nodes[-1]:
            final_nodes.append(node)

    # Plota o grafo e a rota.
    fig, ax = ox.plot_graph_route(G, final_nodes, node_size=15, show=False, close=False, route_color='b', route_linewidth=4, bgcolor='#ffffff', route_alpha=0.7)
    
    # Adiciona a numeração e os nomes dos locais no mapa.
    for i, nome in enumerate(route):
        node_id = nodes[nome]
        point = G.nodes[node_id]
        ax.scatter(point['x'], point['y'], c='red', s=50, zorder=3)
        ax.text(point['x'], point['y'], f' {i+1}. {nome}', fontsize=8, ha='left', va='center')

    ax.set_title(title)
    plt.tight_layout()
    # Salva o mapa na pasta 'img' com alta qualidade.
    plt.savefig(f"img/{filename}", dpi=300, bbox_inches='tight')
    # Fecha a figura para liberar memória e evitar sobreposição de gráficos.
    plt.close(fig)

# Geração e Salvamento dos Resultados ---
# Formatar a string de resultados com as informações de cada algoritmo.
resultados_str = f"""
Resultados da Otimização de Rota (Problema do Caixeiro Viajante)

---
Rota inicial:
Ordem: {' -> '.join(rota_inicial)}
Custo total: {fitness_function(rota_inicial):.2f} metros
Tempo de execução: Não aplicável
---
Hill Climbing:
Ordem: {' -> '.join(rota_hill)}
Custo total: {custo_hill:.2f} metros
Tempo de execução: {time_hill:.4f} segundos
---
Simulated Annealing:
Ordem: {' -> '.join(rota_sa)}
Custo total: {custo_sa:.2f} metros
Tempo de execução: {time_sa:.4f} segundos
---
Algoritmo Genético:
Ordem: {' -> '.join(rota_gen)}
Custo total: {custo_gen:.2f} metros
Tempo de execução: {time_gen:.4f} segundos
"""

# Criar as pastas e salvar o arquivo de texto.
create_folders_if_not_exists()

print(resultados_str)

with open("results/resultados_rotas.txt", "w", encoding="utf-8") as f:
    f.write(resultados_str)

print("Resultados salvos no arquivo 'results/resultados_rotas.txt'.")

# Plotar e salvar os mapas de cada rota.
plot_route(rota_inicial, G, nodes, paths_matrix, "Rota Inicial (Embaralhada)", "mapa_rota_inicial.png")
plot_route(rota_hill, G, nodes, paths_matrix, "Rota Hill Climbing", "mapa_hill_climbing.png")
plot_route(rota_sa, G, nodes, paths_matrix, "Rota Simulated Annealing", "mapa_simulated_annealing.png")
plot_route(rota_gen, G, nodes, paths_matrix, "Rota Algoritmo Genético", "mapa_algoritmo_genetico.png")

print("Mapas salvos como imagens PNG na pasta 'img'.")