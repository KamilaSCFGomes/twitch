import requests

url = "https://id.twitch.tv/oauth2/token"

def gerar_acess_token(client_id, client_secret):
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, params=params)
    token_data = response.json()

    access_token = token_data["access_token"]

    return access_token