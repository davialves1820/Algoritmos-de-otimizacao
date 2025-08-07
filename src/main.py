
import random
import time
from config import SA_PARAMS, GENETIC_ALGORITHM_PARAMS, RESULTS_FOLDER
from data_handler import prepare_data, fitness_function
from algorithms import hill_climb, simulated_annealing, genetic_algorithm
from plotter import create_folders_if_not_exists, plot_route

def run_optimization():
    """
    Executa todo o processo de otimização de rota.
    """
    # Preparar os dados
    G, nodes, locais_nomes, dist_matrix, paths_matrix = prepare_data()

    # Gerar uma rota inicial aleatória
    rota_inicial = locais_nomes[:]
    random.shuffle(rota_inicial)
    custo_inicial = fitness_function(rota_inicial, dist_matrix)
    
    print(f"\nRota inicial gerada: {' -> '.join(rota_inicial)}")
    print(f"Custo total da rota inicial: {custo_inicial:.2f} metros")

    # Executar e medir o tempo de cada algoritmo
    
    # Hill Climbing
    start_time = time.time()
    rota_hill, custo_hill = hill_climb(rota_inicial, dist_matrix)
    time_hill = time.time() - start_time

    # Simulated Annealing
    start_time = time.time()
    rota_sa, custo_sa = simulated_annealing(rota_inicial, dist_matrix, **SA_PARAMS)
    time_sa = time.time() - start_time

    # Algoritmo Genético
    start_time = time.time()
    rota_gen, custo_gen = genetic_algorithm(locais_nomes, dist_matrix, **GENETIC_ALGORITHM_PARAMS)
    time_gen = time.time() - start_time

    # Formatar e salvar os resultados
    create_folders_if_not_exists()
    
    resultados_str = f"""
Resultados da Otimização de Rota (Problema do Caixeiro Viajante)

---
Rota inicial:
Ordem: {' -> '.join(rota_inicial)}
Custo total: {custo_inicial:.2f} metros
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

    print(resultados_str)

    with open(f"{RESULTS_FOLDER}/resultados_rotas.txt", "w", encoding="utf-8") as f:
        f.write(resultados_str)

    print("Resultados salvos no arquivo 'results/resultados_rotas.txt'.")

    # Plotar e salvar os mapas
    plot_route(rota_inicial, G, nodes, paths_matrix, "Rota Inicial (Embaralhada)", "mapa_rota_inicial.png")
    plot_route(rota_hill, G, nodes, paths_matrix, "Rota Hill Climbing", "mapa_hill_climbing.png")
    plot_route(rota_sa, G, nodes, paths_matrix, "Rota Simulated Annealing", "mapa_simulated_annealing.png")
    plot_route(rota_gen, G, nodes, paths_matrix, "Rota Algoritmo Genético", "mapa_algoritmo_genetico.png")

    print("Mapas salvos como imagens PNG na pasta 'img'.")

if __name__ == "__main__":
    run_optimization()