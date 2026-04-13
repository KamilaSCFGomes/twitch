import requests
import json

# lista os vods mais populares das categorias listadas e monta uma lista de streamers que realizaram streams nessas categorias
# o código atualiza a lista a cada categoria pesquisada e confere categorias já pesquisadas, para evitar que trabalho seja perdido ao parar o código antes que termine de rodar

url = "https://api.twitch.tv/helix/videos"

# gere o seu id e autorização e cole aqui
headers = {
    "Client-ID": "XXXXXXXX",
    "Authorization": "Bearer XXXXXXXX"
}

limite_paginas_vods = 25
indice_categoria_inicial = 0
minimo_views = 1000
prazo = "month"

def retorna_streamer(id):
    url = "https://api.twitch.tv/helix/channels"
    params = {
        "broadcaster_id": id
    }
    response = requests.get(url, headers=headers, params=params).json()['data'][0]

    canal = {
        "name": response["broadcaster_name"],
        "channel_id": id,
        "language": response['broadcaster_language'],
        "categories": [],
        "total_views": 0,
        "total_streams": 0,
    }
    return canal

with open('dados/categorias.json', 'r', encoding='utf-8') as file:
    json_categorias = json.load(file)

with open('dados/streamers_dados.json', 'r', encoding='utf-8') as file:
    dados = json.load(file)
    lista_streamers = dados['streamers']
    lista_jogos = dados['jogos']

for jogo in json_categorias[indice_categoria_inicial:]:

    game_id = jogo['id']
    print(f"\n#{indice_categoria_inicial}: {jogo['name']}: ")

    params = {
            "game_id": game_id,
            "type": "archive",
            "period": prazo,
            "sort": "views"
        }

    lista_streamers_por_jogo = []

    # pegando todos os vods
    pagina=0

    if game_id in lista_jogos["jogos"]:
        indice_categoria_inicial+=1
        continue
    else:
        lista_jogos["jogos"].append(game_id)

    while True:
        print("=", end="", flush=True)

        

        url = "https://api.twitch.tv/helix/videos"
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(response.json())
            break

        response = response.json()
        dados = response['data']

        for v in dados:
            views = v.get("view_count")

            if views <= minimo_views: break

            video = {
                "user_id": v.get("user_id"),
                "user_name": v.get("user_name"),
                "view_count": v.get("view_count"),
            }
            id = v.get("user_id")

            if not id in lista_streamers:
                lista_streamers[id] = retorna_streamer(id)

            if not id in lista_streamers_por_jogo:
                lista_streamers_por_jogo.append(id)

                if not game_id in lista_streamers[id]['categories']:
                    lista_streamers[id]['categories'].append(game_id)

            lista_streamers[id]['total_views'] += views
            lista_streamers[id]['total_streams'] += 1
        
        cursor = response['pagination']

        try:
            params = {
                "after": cursor['cursor'],
                "game_id": game_id,
                "type": "archive",
                "period": prazo,
                "sort": "views"
            }
            
        except:
            break

        pagina+=1
        if pagina >= limite_paginas_vods: break

    indice_categoria_inicial+=1
    
    with open('dados/streamers_dados.json', 'w', encoding='utf-8') as file:
        dados = {
            'jogos': lista_jogos,
            'streamers': lista_streamers
        }
        
        json.dump(dados, file, ensure_ascii=False, indent=2)