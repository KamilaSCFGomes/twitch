import requests

url = "https://id.twitch.tv/oauth2/token"

# gere o seu id e segredo e obtenha a autorização com esse código
params = {
    "client_id": "XXXXXXXX",
    "client_secret": "XXXXXXXX",
    "grant_type": "client_credentials"
}

response = requests.post(url, params=params)
token_data = response.json()

access_token = token_data["access_token"]

print(access_token)