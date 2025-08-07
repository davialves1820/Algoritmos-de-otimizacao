
import os
import osmnx as ox
import matplotlib.pyplot as plt
from config import IMAGES_FOLDER

def create_folders_if_not_exists():
    """Cria as pastas de imagens e resultados se não existirem."""
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    os.makedirs("results", exist_ok=True)

def plot_route(route, G, nodes, paths_matrix, title, filename):
    """
    Plota a rota no mapa e salva como um arquivo de imagem.
    """
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
    
        if (node != final_nodes[-1]):
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