import os
import json

arquivo_informacoes = os.path.join(os.getcwd(), "twitch", "informacoes_aplicativo.json")
arquivo_oauth_token = os.path.join(os.getcwd(), "twitch", "oauth_token.txt")

with open(arquivo_informacoes, 'r', encoding="utf-8") as f:
    informacoes = json.load(f)

def get_url_oauth():
    return informacoes['url_oauth']

def get_client_id():
    return informacoes['client_id']

def get_client_secret():
    return informacoes['client_secret']

def get_access_token():
    return informacoes['access_token']

def get_user_name():
    return informacoes['user_name']

def get_user_id():
    return informacoes['user_id']

def get_header():
    return {
        "Client-ID": informacoes['client_id'],
        "Authorization": f"Bearer {informacoes['access_token']}"
        }

def get_user_oauth_token():
    try:
        with open(arquivo_oauth_token, "r", encoding="utf-8") as f:
            return f.readline().rstrip('\n')
    except:
        print("\n\nErro: não foi possível ler o OAuth token do arquivo")
        return
    
def get_header_user_oauth():
    return{
        "Client-ID": informacoes['client_id'],
        "Authorization": f"Bearer {get_user_oauth_token()}"
        }