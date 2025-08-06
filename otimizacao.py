
pessoas = [("Lisboa", "LIS"),
            ("Madrid", "MAD"),
            ("Paris", "CDG"),
            ("Dublin", "DUB"),
            ("Bruxelas", "BRU"),
            ("Londres", "LHR"),
            ("Roma", "FCO"),
            ("Nova York", "JFK")
        ]

voos = {}

for linha in open("./Aula-2/voos.txt"):
    origem, destino, saida, chegada, preco = linha.split(',')
    voos.setdefault((origem, destino), []) # Adiciona no dicionário caso não exista o par
    voos[(origem, destino)].append((saida, chegada, int(preco)))

#print(voos)

agenda = 10 * [0]

destino = "FCO"
def imprimir_voos(agenda):
    id_voo = -1
    total_preco = 0
    for i in range(len(agenda) // 2):
        nome = pessoas[i][0]
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][agenda[id_voo]]
        total_preco += ida[2]
        id_voo += 1
        volta = voos[(destino, origem)][agenda[id_voo]]
        total_preco += volta[2]
        print("%10s%10s %5s-%5s %3s %5s-%5s %3s" % (nome, origem, ida[0], ida[1], ida[2], volta[0], volta[1], volta[2]))
    
    print("Preço total: ", total_preco)

imprimir_voos(agenda)

def fitness_fuction(agenda):
    id_voo = -1
    total_preco = 0
    
    for i in range(len(agenda) // 2):
        origem = pessoas[i][1]
        id_voo += 1
        ida = voos[(origem, destino)][agenda[id_voo]]
        total_preco += ida[2]
        id_voo += 1
        volta = voos[(destino, origem)][agenda[id_voo]]
        total_preco += volta[2]
        
    return total_preco