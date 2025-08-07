
import osmnx as ox
import networkx as nx
from config import LOCAIS

def prepare_data():
    """
    Baixa o grafo de ruas e calcula as matrizes de distância e caminho entre os locais.
    """
    
    print("Baixando grafo de ruas de João Pessoa...")
    # Baixar o grafo de ruas da cidade de João Pessoa a partir do OpenStreetMap.
    # O 'network_type' define que queremos um grafo de vias para veículos.
    G = ox.graph_from_place("João Pessoa, Brazil", network_type='drive')

    # Mapear os pontos de interesse para os nós mais próximos no grafo de ruas.
    # Isso é necessário porque as coordenadas exatas dos locais podem não ser um nó de interseção.
    nodes = {nome: ox.distance.nearest_nodes(G, lon, lat) for nome, (lon, lat) in LOCAIS.items()}
    locais_nomes = list(nodes.keys())

    # Calcular a matriz de distâncias reais (por vias) e os caminhos entre todos os pares de locais.
    # Isso evita recalcular o menor caminho várias vezes durante a execução dos algoritmos.
    dist_matrix = {} # Armazena a distância total em metros do caminho mais curto entre o local de origem e o local de destino
    paths_matrix = {} # Armazena a lista completa dos nós que compõem o caminho mais curto entre os dois locais
    
    for origem in locais_nomes:
        dist_matrix[origem] = {}
        paths_matrix[origem] = {}
        
        for destino in locais_nomes:
            
            if (origem == destino):
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
        
    return G, nodes, locais_nomes, dist_matrix, paths_matrix

def fitness_function(rota, dist_matrix):
    # Função de avaliação (fitness): calcula a distância total de uma rota completa.
    # Esta função é a métrica usada para medir a qualidade de cada solução.
    total_dist = 0
    
    for i in range(len(rota)):
        origem = rota[i]
        destino = rota[(i + 1) % len(rota)] # Retorna ao ponto inicial no final
        total_dist += dist_matrix[origem][destino]
    
    return total_dist
