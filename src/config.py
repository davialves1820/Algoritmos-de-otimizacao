
# Parâmetros da cidade
PLACE_NAME = "João Pessoa, Brazil"

# Pontos de interesse na cidade de João Pessoa (PB).
LOCAIS = {
    "UFPB": (-34.8708, -7.1377),
    "Shopping Manaíra": (-34.8360, -7.1126),
    "Busto de Tamandaré": (-34.8256, -7.1177),
    "Centro Histórico": (-34.8783, -7.1225),
    "Estação Cabo Branco": (-34.7942, -7.1480)
}

# Parâmetros dos algoritmos
SA_PARAMS = {
    'T': 1000,
    'T_min': 1e-6,
    'alpha': 0.995
}

GENETIC_ALGORITHM_PARAMS = {
    'pop_size': 20,
    'generations': 200
}

# Parâmetros de saída
RESULTS_FOLDER = "results"
IMAGES_FOLDER = "img"