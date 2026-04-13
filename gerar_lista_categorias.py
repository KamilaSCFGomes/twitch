import requests
import json

# gera uma lista de todas as categorias da twitch

url = "https://api.twitch.tv/helix/games/top"

# gere o seu id e autorização e cole aqui
headers = {
    "Client-ID": "XXXXXXXX",
    "Authorization": "Bearer XXXXXXXX"
}

params = {}

lista = []
pagina=1

while True:
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(response)
        break

    response = response.json()
    dados = response['data']
    
    for c in dados:
        categoria = {
            "name": c.get("name"),
            "id": c.get("id")
        }

        lista.append(categoria)

    cursor = response['pagination']

    try:
        params = {
            "after": cursor['cursor']
        }
        
    except:
        break

    pagina+=1
    print(pagina)

with open("dados/categorias.json", "w", encoding="utf-8") as f:
    json.dump(lista, f, ensure_ascii=False, indent=2)