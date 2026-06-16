import requests
import ler_informacoes as app

url = "https://api.twitch.tv/helix/users"
headers = app.get_header()

def get_user_id(user_name):
    params = {"login": user_name}
    resposta = requests.get(url, headers=headers, params=params)

    if resposta.status_code != 200:
        print(resposta.json())
        return
    
    resposta = resposta.json()['data'][0]
    return resposta['id']