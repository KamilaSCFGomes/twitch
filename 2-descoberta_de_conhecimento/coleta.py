import requests
import csv
from datetime import datetime
import os
from time import sleep

url = "https://api.twitch.tv/helix/streams"

# gere o seu id e autorização e cole aqui
headers = {
    "Client-ID": "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "Authorization": "XXXXXXXXXXXXXXXXXXXXXXXXX"
}

# a API da twitch retorna as informações em páginas, escolha o tamanho e a quantidade
tam_pagina = 100
num_paginas = 10

# intervalo de tempo entre coletas (segundos)
intervalo = 14*60+55

def retorna_top_streams(filtra_br=False):
    lista = []
    params = {"language": "pt", "first": tam_pagina, "type": "live"} if filtra_br else {"first": tam_pagina, "type": "live"}

    for pagina in range(num_paginas):
        resposta = requests.get(url, headers=headers, params=params)
        if resposta.status_code != 200:
                print(resposta.json())
                return
        
        resposta = resposta.json()
        dados = resposta['data']

        for s in dados:
            stream = {
                "user_name": s.get("user_name"),
                "title": s.get("title"),
                "id": s.get("id"),
                "viewer_count": s.get("viewer_count"),
                "language": s.get("language"),
                "game_id": s.get("game_id")
            }
            lista.append(stream)

        cursor = resposta['pagination']

        try:
            if filtra_br:
                params = {
                    "language": "pt",
                    "after": cursor['cursor'],
                    "first": tam_pagina,
                    "type": "live"
                    }
            else:
                params = {
                    "after": cursor['cursor'],
                    "first": tam_pagina,
                    "type": "live"
                    }
        except:
            break

    return lista


def salva_top_streams():
    # gravar horario:
    agora = datetime.now()
    data = agora.strftime("%d-%m-%Y")
    data_hora = agora.strftime("%d/%m/%Y %H:%M:%S")

    with open('twitch/2-descoberta_de_conhecimento/dados/horarios_gravados.txt', 'a', encoding='utf-8') as file:
        file.write(f"{data_hora}\n")

    print(data_hora)

    top_streams_global = retorna_top_streams()
    # top_streams_brasil = retorna_top_streams(True)

    arquivo_csv = f"twitch/2-descoberta_de_conhecimento/dados/top_streams-{data}.csv"
    arquivo_existe = os.path.exists(arquivo_csv)

    with open(arquivo_csv, 'a', encoding='utf-8', newline='') as file:
        fieldnames = ['data_hora', 'user_name', 'title', 'id', 'viewer_count', 'language', 'game_id']
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        
        if not arquivo_existe:
            writer.writeheader()
        
        for stream in top_streams_global:
            writer.writerow({
                'data_hora': data_hora,
                'user_name': stream['user_name'],
                'title': stream['title'],
                'id': stream['id'],
                'viewer_count': stream['viewer_count'],
                'language': stream['language'],
                'game_id': stream['game_id']
            })



while True:
    salva_top_streams()

    print("esperando...")
    sleep(intervalo)
