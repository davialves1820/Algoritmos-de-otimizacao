# src/algorithms.py

import random
import math
from data_handler import fitness_function

# Algoritmo Hill Climbing
# Faz trocas locais e só aceita melhorias (menor distância).
def hill_climb(rota_inicial, dist_matrix):
    atual = rota_inicial[:]
    atual_custo = fitness_function(atual, dist_matrix)
    melhorou = True

    while melhorou:
        melhorou = False

        for i in range(len(atual)):
            for j in range(i + 1, len(atual)):
                nova = atual[:]
                nova[i], nova[j] = nova[j], nova[i] # Faz uma troca
                novo_custo = fitness_function(nova, dist_matrix)
                
                if (novo_custo < atual_custo): # Se a nova rota é melhor
                    atual, atual_custo = nova, novo_custo
                    melhorou = True # Continua buscando melhorias
    
    return atual, atual_custo

# Algoritmo Simulated Annealing
def simulated_annealing(rota_inicial, dist_matrix, T, T_min, alpha):
    atual = rota_inicial[:]
    atual_custo = fitness_function(atual, dist_matrix)
    melhor = atual[:]
    melhor_custo = atual_custo
    
    while (T > T_min):
        i, j = random.sample(range(len(atual)), 2)
        nova = atual[:]
        nova[i], nova[j] = nova[j], nova[i] # Faz uma troca
        novo_custo = fitness_function(nova, dist_matrix)
        delta = novo_custo - atual_custo
        
        # Aceita a nova rota se for melhor (delta < 0) ou por probabilidade.
        if (delta < 0 or random.random() < math.exp(-delta / T)):
            atual, atual_custo = nova, novo_custo
            
            if (atual_custo < melhor_custo):
                melhor, melhor_custo = atual[:], atual_custo
        
        T *= alpha # Reduz a temperatura (probabilidade de aceitar piores soluções)
    
    return melhor, melhor_custo

# Algoritmo Genético
def crossover(p1, p2):
    start, end = sorted(random.sample(range(len(p1)), 2))
    meio = p1[start:end]
    resto = [x for x in p2 if x not in meio]
    
    return resto[:start] + meio + resto[start:]

def mutate(rota):
    i, j = random.sample(range(len(rota)), 2)
    rota[i], rota[j] = rota[j], rota[i]

def genetic_algorithm(locais_nomes, dist_matrix, pop_size, generations):
    pop = [random.sample(locais_nomes, len(locais_nomes)) for _ in range(pop_size)]
    
    for _ in range(generations):
        pop.sort(key=lambda rota: fitness_function(rota, dist_matrix))
        nova_pop = pop[:2]
        
        while (len(nova_pop) < pop_size):
            p1, p2 = random.sample(pop[:10], 2)
            filho = crossover(p1, p2)
            
            if (random.random() < 0.2):
                mutate(filho)
            nova_pop.append(filho)
        
        pop = nova_pop
    
    melhor = pop[0]
    
    return melhor, fitness_function(melhor, dist_matrix)