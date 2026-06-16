import ler_informacoes_aplicativo as app
import re
import os

client_id = app.get_client_id()
redirect_uri = app.get_url_oauth()

url = f"https://id.twitch.tv/oauth2/authorize?response_type=token&client_id={client_id}&redirect_uri={redirect_uri}&scope=channel%3Amanage%3Apolls+channel%3Aread%3Apolls&state=c3ab8aa609ea11e793ae92361f002671"

arquivo_oath_token = os.path.join(os.getcwd(), "twitch", "oath_token.txt")

def gerar_oath_token():
    print("\n\n\nPara conectar a sua conta, abra este link:")
    print(url)
    print("\nSe não estiver logado, faça login na sua conta.")
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

            with open(arquivo_oath_token, "w", encoding="utf-8") as f:
                print(token, file=f)
            
            print(f"salvo em {arquivo_oath_token}.")

            break

        else:
            print("\nOcorreu algum erro.")
    
def get_user_oath_token():
    try:
        with open(arquivo_oath_token, "r", encoding="utf-8") as f:
            return f.readline()
    except:
        print("\n\nErro: não foi possível ler o OAth token do arquivo")
        return