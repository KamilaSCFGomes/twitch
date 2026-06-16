import os
import json

arquivo_informacoes = os.path.join(os.getcwd(), "twitch", "informacoes_aplicativo.json")

informacoes = {}

with open(arquivo_informacoes, encoding="utf-8") as f:
    informacoes = json.load(f)

def get_url_oauth():
    return informacoes['url_oauth']

def get_client_id():
    return informacoes['client_id']

def get_client_secret():
    return informacoes['client_secret']

def get_access_token():
    return informacoes['access_token']

def get_header():
    return {
        "Client-ID": informacoes['client_id'],
        "Authorization": f"Bearer {informacoes['access_token']}"
        }