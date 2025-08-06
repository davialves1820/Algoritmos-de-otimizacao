# Algoritmos de Otimização

Este projeto utiliza algoritmos de otimização heurística e meta-heurística para resolver o **Problema do Caixeiro Viajante (TSP)** em uma aplicação real na cidade de João Pessoa, na Paraíba. O objetivo é encontrar a rota mais curta para visitar um conjunto de pontos turísticos e retornar ao ponto de partida.

O script calcula e compara a eficiência de três algoritmos: **Hill Climbing**, **Simulated Annealing** e **Algoritmo Genético**, comparando seus resultados com uma rota inicial aleatória. Para a visualização, o projeto utiliza a biblioteca **OSMnx** para plotar as rotas em um mapa real da cidade.

---

## **Função de Fitness (Avaliação)**

A **Função de Fitness** é o componente mais crucial de qualquer algoritmo de otimização. Ela é responsável por **avaliar a qualidade de cada solução candidata**.

Neste projeto, a função de fitness calcula a **distância total** de uma rota. O objetivo dos algoritmos é encontrar a rota que minimize esse valor. A função de fitness atua como um guia, informando aos algoritmos se uma nova rota é melhor ou pior que a anterior, direcionando a busca por uma solução ótima.

---

## **Algoritmos Implementados**

### **1. Hill Climbing (Subida de Encosta)**
-   **Como Funciona**: Este é um algoritmo guloso (greedy) que tenta encontrar a melhor solução fazendo pequenas melhorias. Ele começa com uma rota aleatória e, a cada passo, faz uma pequena alteração (por exemplo, trocando a posição de dois pontos). Se a **função de fitness** indicar que a nova rota é melhor (menor distância), ele a aceita. O processo continua até que não seja possível encontrar uma rota melhor com uma única troca.
-   **Vantagens**: É simples e rápido, pois só busca a solução local mais próxima.
-   **Desvantagens**: Pode facilmente ficar preso em um "mínimo local", uma rota que é a melhor em sua vizinhança, mas não a melhor globalmente.

### **2. Simulated Annealing (Recozimento Simulado)**
-   **Como Funciona**: Inspirado no processo metalúrgico de aquecer e resfriar um material para torná-lo mais resistente, este algoritmo é uma evolução do Hill Climbing. Ele também faz trocas locais, mas, diferentemente do Hill Climbing, ele tem uma pequena probabilidade de aceitar uma rota "pior" temporariamente. Essa probabilidade diminui com o tempo (simulando o "resfriamento"), o que permite que o algoritmo explore mais o espaço de soluções e evite mínimos locais. A **função de fitness** é usada para calcular a diferença entre o custo da rota atual e da rota candidata, que é um fator-chave na decisão de aceitar uma solução pior.
-   **Vantagens**: A capacidade de aceitar soluções piores ajuda o algoritmo a escapar de mínimos locais e a encontrar soluções mais próximas do ideal global.
-   **Desvantagens**: É mais lento que o Hill Climbing e a qualidade da solução depende do ajuste dos parâmetros de "temperatura" e "taxa de resfriamento".

### **3. Algoritmo Genético**
-   **Como Funciona**: Inspirado na teoria da evolução, este algoritmo trabalha com uma "população" de rotas candidatas. Ao longo de várias "gerações", as rotas com o melhor **fitness** (menor distância) são selecionadas, "cruzadas" para criar novas rotas ("filhos") e sofrem "mutações" aleatórias (trocas de posições). As rotas menos aptas são eliminadas. Esse processo de seleção e variação natural leva a uma população cada vez mais otimizada ao longo do tempo.
-   **Vantagens**: Extremamente eficaz para encontrar soluções quase ideais em problemas complexos com grande número de variáveis, pois explora o espaço de busca de maneira ampla.
-   **Desvantagens**: É o mais lento dos três algoritmos, pois opera com uma população inteira, e a qualidade dos resultados pode variar dependendo dos parâmetros de população, cruzamento e mutação.

---

## **Funcionalidades do Projeto**

-   **Cálculo de Distâncias Reais**: Utiliza dados da OpenStreetMap para calcular a distância de rota entre os pontos, em vez de distâncias em linha reta.
-   **Comparação de Algoritmos**: Analisa a performance dos algoritmos de otimização, mostrando qual deles encontra a rota mais curta.
-   **Medição de Tempo**: Calcula e exibe o tempo de execução de cada algoritmo, oferecendo uma visão clara de sua eficiência computacional.
-   **Visualização da Rota**: Gera mapas em imagens PNG que mostram o trajeto de cada rota calculada, com os pontos numerados na ordem de visita.
-   **Relatório de Resultados**: Gera um arquivo de texto (`resultados_rotas.txt`) contendo a ordem das rotas, seus custos em metros e tempos de execução para uma análise detalhada.

---

## **Pontos de Interesse**

O projeto otimiza a rota para os seguintes locais em João Pessoa, Paraíba:

-   UFPB
-   Shopping Manaíra
-   Busto de Tamandaré
-   Centro Histórico
-   Estação Cabo Branco

---

## **Requisitos e Instalação**

Para rodar este projeto, você precisará ter o Python instalado.

**Instale as dependências:**
    ```bash
    pip install osmnx networkx matplotlib numpy
    ```

---

## **Como Executar**

Execute o arquivo Python principal. O script irá realizar a otimização e gerar os arquivos de saída automaticamente.
