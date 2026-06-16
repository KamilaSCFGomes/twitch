import os
import json
from gerar_token_twitch import gerar_acess_token

arquivo_informacoes = os.path.join(os.getcwd(), "twitch", "informacoes_aplicativo.json")


def y_n():
    while True:
        resposta = input("y/n:  ")
        if resposta == 'y' or resposta == 'Y': return True
        if resposta == 'n' or resposta == 'N': return False
        print("Entrada inesperada")


def configurar():
    if os.path.isfile(arquivo_informacoes):
        print("\nJá existe um arquivo de informações. Deseja recomeçar a configuração?")
        resposta = y_n()
        if not resposta:
            return
        
    else: print("Arquivo de informações não encontrado. Começando configuração inicial:")

    print("\nVocê precisa criar um aplicativo no Twitch Developers. Já fez isso?")
    resposta = y_n()

    if not resposta:
        print("\n\nAcesse  <https://dev.twitch.tv/console/apps>  e clique em  <Registre seu aplicativo>.")
        print("Para a  <URL de redirecionamento OAuth>, recomendamos utilizar  <http://localhost:3000>.")
        print("Em  <Tipo de cliente>, escolha  <Confidencial>.")
        print("Após criar o aplicativo, você será redirecionado.")

    else:
        print("\n\nAcesse <https://dev.twitch.tv/console/apps>.")

    print("\nClique no botão  <Gerenciar>  na frente do seu aplicativo.")
    url_oauth = input("Informe uma  <URL de redirecionamento OAuth>:  ")
    client_id = input("Informe o  <ID do cliente>:  ")
    client_secret = input("Clique em  <Novo segredo>  para gerar um segredo de cliente e informe:  ")

    print("\nVocê já gerou o token de acesso para o programa?")
    resposta = y_n()

    if resposta:
        access_token = input("Informe o token de acesso:  ")

    else:
        print("\nGerando token de acesso...")
        access_token = gerar_acess_token(client_id, client_secret)
        print(f"Token de acesso gerado: {access_token}")
    
    informacoes = {
        "url_oauth": url_oauth,
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": access_token
    }

    with open(arquivo_informacoes, "w", encoding="utf-8") as f:
        json.dump(informacoes, f, ensure_ascii=False, indent=2)

    from get_user_id import get_user_id
    user_name = input("\nInforme seu nome de usuário:  ")
    print("Obtendo seu ID de usuário...")
    user_id = get_user_id(user_name)
    print(f"Seu ID de usuário:  {user_id}")

    informacoes = {
        "url_oauth": url_oauth,
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": access_token,
        "user_name": user_name,
        "user_id": user_id
    }

    with open(arquivo_informacoes, "w", encoding="utf-8") as f:
        json.dump(informacoes, f, ensure_ascii=False, indent=2)


print("\n\n\nPor segurança, não disponibilizamos o id e token de acesso utilizados para acessar a API da Twitch.")
print("Será necessário que você gere os próprios dados para conseguir acesso.")
print(f"Os dados gerados serão salvos em  <{arquivo_informacoes}>  e serão utilizados durante a execução dos códigos.\n\n")

configurar()

print("\n\n\nConfiguração finalizada.")
print(f"As informações estão salvas em  <{arquivo_informacoes}>.\n\n\n")



