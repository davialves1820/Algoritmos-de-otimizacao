import random
import math
from data_handler import fitness_function  # Função que calcula o custo (distância total) de uma rota

# ==========================
# Algoritmo Hill Climbing
# ==========================
# Procura local por uma solução melhor, realizando pequenas trocas (vizinhança).
# Só aceita mudanças se o custo for melhor (menor distância total).
def hill_climb(rota_inicial, dist_matrix):
    atual = rota_inicial[:]  # Cópia da rota atual
    atual_custo = fitness_function(atual, dist_matrix)  # Calcula o custo da rota atual
    melhorou = True  # Flag para verificar se houve melhora na iteração

    while melhorou:
        melhorou = False  # Começa assumindo que não houve melhora

        # Gera todos os vizinhos trocando pares de cidades
        for i in range(len(atual)):
            for j in range(i + 1, len(atual)):
                nova = atual[:]  # Cópia da rota
                nova[i], nova[j] = nova[j], nova[i]  # Troca dois elementos (i e j)
                novo_custo = fitness_function(nova, dist_matrix)

                # Se a nova rota for melhor, atualiza a rota atual
                if novo_custo < atual_custo:
                    atual, atual_custo = nova, novo_custo
                    melhorou = True  # Continua tentando melhorar

    return atual, atual_custo  # Retorna a melhor rota encontrada


# ===============================
# Algoritmo Simulated Annealing
# ===============================
# Permite aceitar soluções piores com uma certa probabilidade (baseada na temperatura),
# o que evita ficar preso em mínimos locais.
def simulated_annealing(rota_inicial, dist_matrix, T, T_min, alpha):
    atual = rota_inicial[:]  # Rota atual
    atual_custo = fitness_function(atual, dist_matrix)
    melhor = atual[:]  # Guarda a melhor solução encontrada
    melhor_custo = atual_custo

    # Enquanto a "temperatura" não atingir o mínimo...
    while T > T_min:
        i, j = random.sample(range(len(atual)), 2)  # Escolhe dois índices aleatórios
        nova = atual[:]
        nova[i], nova[j] = nova[j], nova[i]  # Troca os elementos para gerar nova solução
        novo_custo = fitness_function(nova, dist_matrix)
        delta = novo_custo - atual_custo  # Diferença de custo

        # Se a nova solução for melhor (menor custo) ou aceita com uma probabilidade (exploração)
        if delta < 0 or random.random() < math.exp(-delta / T):
            atual, atual_custo = nova, novo_custo  # Atualiza a solução atual

            # Atualiza o melhor se necessário
            if atual_custo < melhor_custo:
                melhor, melhor_custo = atual[:], atual_custo

        T *= alpha  # Reduz a temperatura gradualmente

    return melhor, melhor_custo  # Retorna a melhor rota encontrada


# ====================
# Algoritmo Genético
# ====================
# Inspiração biológica: seleção, cruzamento (crossover) e mutação.
# Trabalha com uma população de rotas que evolui a cada geração.

# Crossover entre dois "pais" para gerar um novo "filho"
def crossover(p1, p2):
    start, end = sorted(random.sample(range(len(p1)), 2))  # Define intervalo de corte
    meio = p1[start:end]  # Fatia da rota do primeiro pai
    resto = [x for x in p2 if x not in meio]  # Complementa com cidades do segundo pai (sem repetir)

    return resto[:start] + meio + resto[start:]  # Combina parte dos pais para formar o filho

# Mutação simples: troca dois elementos aleatórios da rota
def mutate(rota):
    i, j = random.sample(range(len(rota)), 2)
    rota[i], rota[j] = rota[j], rota[i]

# Função principal do Algoritmo Genético
def genetic_algorithm(locais_nomes, dist_matrix, pop_size, generations):
    # Cria uma população inicial com rotas aleatórias
    pop = [random.sample(locais_nomes, len(locais_nomes)) for _ in range(pop_size)]

    # Executa por um número definido de gerações
    for _ in range(generations):
        # Ordena a população pela aptidão (menor distância total)
        pop.sort(key=lambda rota: fitness_function(rota, dist_matrix))
        nova_pop = pop[:2]  # Elitismo: mantém os 2 melhores

        # Preenche o restante da nova população
        while len(nova_pop) < pop_size:
            # Seleção: escolhe dois pais aleatórios entre os 10 melhores
            p1, p2 = random.sample(pop[:10], 2)
            filho = crossover(p1, p2)  # Gera um novo filho

            # Mutação aleatória com 20% de chance
            if random.random() < 0.2:
                mutate(filho)

            nova_pop.append(filho)  # Adiciona o filho à nova população

        pop = nova_pop  # Atualiza a população para a próxima geração

    melhor = pop[0]  # A melhor rota é a primeira (menor custo)

    return melhor, fitness_function(melhor, dist_matrix)  # Retorna a melhor rota e seu custo
