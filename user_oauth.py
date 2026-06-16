import ler_informacoes as app
import re
import os

client_id = app.get_client_id()
redirect_uri = app.get_url_oauth()
scope = "user%3Aread%3Afollows+user%3Aread%3Asubscriptions"

url = f"https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&state=c3ab8aa609ea11e793ae92361f002671"

arquivo_oauth_token = os.path.join(os.getcwd(), "twitch", "oauth_token.txt")

def gerar_oauth_token():
    print("\n\n\nPara conectar a sua conta, abra este link:")
    print(url)
    print("\nSe não estiver logado, faça login na sua conta.")
    print("Clique em  <Autorizar>.")
    print("Você será redirecionado a outra página. O URL contém as informações que queremos obter.")

    while True:
        resposta = input("Cole o URL para o qual você foi redirecionado:  ")

        if not re.search(fr'{app.get_url_oauth()}', resposta):
            print(f"\nA URL deveria coincidir com a  <URL de redirecionamento OAuth>  do aplicativo:  <{app.get_url_oauth()}>.")

        elif re.search('error=', resposta):
            erro1 = re.sub('^.*error=', '', resposta)
            erro1 = re.split('&', erro1)[0]
            erro2 = re.sub('^.*error_description=', '', resposta)
            erro2 = re.split('&', erro2)[0]
            erro2 = re.sub('\+', ' ', erro2)

            print(f"\nHouve um erro na resposta:  {erro1}\n{erro2}\n")

        elif re.search('access_token=', resposta):
            token = re.sub('^.*access_token=', '', resposta)
            token = re.split('&', token)[0]
            print(f"\nSeu OAuth token:  {token}")

            with open(arquivo_oauth_token, "w", encoding="utf-8") as f:
                print(token, file=f)
            
            print(f"salvo em {arquivo_oauth_token}.")

            break

        else:
            print("\nOcorreu algum erro.")

gerar_oauth_token()