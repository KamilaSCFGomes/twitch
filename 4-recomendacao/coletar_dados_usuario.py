import requests
import json
import os
import sys
from pathlib import Path
# Add the parent folder (one level up) to the system search path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ler_informacoes as app

arquivo_canais_seguidos = os.path.join(os.getcwd(), "twitch", "4-recomendacao", "dados", "canais_seguidos.json")

url = "https://api.twitch.tv/helix/channels/followed"
headers = app.get_header_user_oauth()

params = {
    "user_id": app.get_user_id(),
    "first": 10
}

def pega_canais_seguidos():
    lista = []

    while True:
        resposta = requests.get(url, headers=headers, params=params)
        if resposta.status_code != 200:
            print(resposta.json())
            return

        resposta = resposta.json()
        dados = resposta['data']

        for s in dados:
            streamer = {
                "broadcaster_id": s.get('broadcaster_id'),
                "broadcaster_name": s.get('broadcaster_name')
            }
            lista.append(streamer)

        cursor = resposta['pagination']
        try: params['after'] = cursor['cursor']
        except: break

        if not resposta['pagination']:
            break

    return lista

def salva_canais_seguidos():
    canais_seguidos = pega_canais_seguidos()
    
    with open(arquivo_canais_seguidos, "w", encoding="utf-8") as f:
        json.dump(canais_seguidos, f, ensure_ascii=False, indent=2)

salva_canais_seguidos()