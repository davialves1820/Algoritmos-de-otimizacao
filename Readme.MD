# Otimização de Rota com Algoritmos Heurísticos

Este projeto demonstra a aplicação de algoritmos de otimização para resolver o **Problema do Caixeiro Viajante (TSP)** em uma aplicação real na cidade de João Pessoa, na Paraíba. O objetivo é encontrar a rota mais curta para visitar um conjunto de pontos turísticos e retornar ao ponto de partida.

O projeto utiliza a biblioteca **OSMnx** para modelar a rede de ruas da cidade como um grafo. Três algoritmos de otimização — **Hill Climbing**, **Simulated Annealing** e **Algoritmo Genético** — são implementados para encontrar a rota mais eficiente. A performance de cada algoritmo é comparada com uma rota inicial aleatória, e os resultados são visualizados em mapas da cidade.

---

## 🚀 Como Funciona

A base do projeto é a **Função de Fitness**, que avalia a qualidade de cada rota candidata calculando sua **distância total**. O objetivo de todos os algoritmos é minimizar essa distância.

### Algoritmos Implementados

Os três algoritmos utilizados buscam a melhor rota, mas com abordagens diferentes:

#### 1. Hill Climbing (Subida de Encosta)
* **Como Funciona:** Um algoritmo guloso que melhora a rota fazendo pequenas trocas. Ele só aceita uma nova rota se ela for estritamente melhor (menor distância).
* **Vantagens:** Simples, rápido e fácil de implementar.
* **Desvantagens:** Pode ficar preso em mínimos locais, sem encontrar a melhor solução global.

#### 2. Simulated Annealing (Recozimento Simulado)
* **Como Funciona:** Uma evolução do Hill Climbing. Ele também faz trocas, mas com uma pequena probabilidade de aceitar rotas "piores" temporariamente. Essa probabilidade diminui com o tempo, permitindo que o algoritmo explore o espaço de busca de forma mais ampla.
* **Vantagens:** Capaz de escapar de mínimos locais e encontrar soluções mais próximas do ideal global.
* **Desvantagens:** Mais lento que o Hill Climbing e depende do ajuste de parâmetros como a "temperatura".

#### 3. Algoritmo Genético
* **Como Funciona:** Inspirado na evolução natural, ele trabalha com uma "população" de rotas. Ao longo de várias "gerações", as melhores rotas são selecionadas, "cruzadas" para criar novas rotas e sofrem "mutações" aleatórias. Esse processo evolutivo leva a uma população de rotas cada vez mais otimizadas.
* **Vantagens:** Extremamente eficaz para encontrar soluções quase ideais em problemas complexos.
* **Desvantagens:** É o mais lento dos três algoritmos e a qualidade dos resultados pode variar com os parâmetros da população e da mutação.

---

## ✨ Funcionalidades do Projeto

-   **Cálculo de Distâncias Reais:** Utiliza dados do OpenStreetMap para calcular a distância exata em vias.
-   **Análise de Performance:** Compara a eficiência e o tempo de execução de cada algoritmo.
-   **Visualização da Rota:** Gera mapas em PNG com o trajeto e a ordem de visita de cada rota.
-   **Relatório de Resultados:** Salva um arquivo de texto (`resultados_rotas.txt`) com a análise detalhada.

---

## 📍 Pontos de Interesse

O projeto otimiza a rota para os seguintes locais em João Pessoa:
-   UFPB
-   Shopping Manaíra
-   Busto de Tamandaré
-   Centro Histórico
-   Estação Cabo Branco

---

## ⚙️ Como Usar

### Pré-requisitos
Certifique-se de ter o Python 3 instalado. Em seguida, instale as dependências necessárias:
```bash
pip install osmnx networkx matplotlib numpy
