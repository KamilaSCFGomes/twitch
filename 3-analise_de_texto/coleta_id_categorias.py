import requests
import os
import json

# esse programa salva o id das categorias especificadas

url = "https://api.twitch.tv/helix/games"

# gere o seu id e autorização e cole aqui
headers = {
    "Client-ID": "hy29mbacqvuufwrxjiz2iva50449ri",
    "Authorization": "Bearer b2tm49kwszxxh9q5afen5ton69zpxg"
}

CATEGORIAS = [
        "Just Chatting",
        "League of Legends",
        "Counter-Strike",
        "Grand Theft Auto V",
        "Valorant",
        "IRL",
        "Dota 2",
        "Fortnite",
        "Overwatch 2",
        "Minecraft"
        ]

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
PASTA_DESTINO = os.path.join(
    PASTA_ATUAL,
    "dados",
)
ARQUIVO_DESTINO = os.path.join(
    PASTA_DESTINO,
    "id_categorias.json"
)




os.makedirs(PASTA_DESTINO, exist_ok=True)
with open(ARQUIVO_DESTINO, 'w', encoding='utf-8') as file:

    lista = []

    for jogo in CATEGORIAS:
        params = {"name": jogo}
        resposta = requests.get(url, headers=headers, params=params)
        if resposta.status_code != 200:
            print(resposta)
            break
        
        resposta = resposta.json()
        dados = resposta['data']

        for c in dados:
            categoria = {
                "name": c.get("name"),
                "id": c.get("id")
            }

        lista.append(categoria)
    
    json.dump(lista, file, ensure_ascii=False, indent=2)