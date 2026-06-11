import socket
import json
import csv
import os
import requests
import pandas as pd

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_MENSAGENS = os.path.join(PASTA_ATUAL, "dados", "planob_chat_mensagens.csv")
ARQUIVO_STREAMERS = os.path.join(PASTA_ATUAL, "dados", "planob_streamers.csv")
ARQUIVO_CATEGORIAS = os.path.join(PASTA_ATUAL, "dados", "id_categorias.json")

OAUTH_TOKEN = "oauth:6koecrhs51e3tr3lits0z2zm9hcgdh"
CLIENT_ID = "gp762nuuoqcoxypju8c569th9wz7q5"
# gerar em https://twitchtokengenerator.com -> "Custom Scope Token" -> ativa "chat:read" - > "Generate Token!"
BOT_NICK = "pdrohd" # seu nick  da conta da twitch, usada no login pedido no link acima

MENSAGENS_POR_STREAMER = 100
STREAMERS_POR_CATEGORIA = 1


# cria csvs se não existirem
if not os.path.exists(ARQUIVO_MENSAGENS):
    with open(ARQUIVO_MENSAGENS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["user_name", "game_id", "mensagem"])

if not os.path.exists(ARQUIVO_STREAMERS):
    with open(ARQUIVO_STREAMERS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["user_name", "game_id", "quantidade_viewers"])


with open(ARQUIVO_CATEGORIAS, "r", encoding="utf-8") as f:
    id_categorias = json.load(f)

# carrega streamers já coletados para não repetir
df_streamers_salvos = pd.read_csv(ARQUIVO_STREAMERS, sep="\t")
streamers_ja_coletados = set(df_streamers_salvos["user_name"].str.lower())


def get_streamers(game_id, quantidade):
    # busca os top streamers em inglês de uma categoria via API da Twitch
    access_token = OAUTH_TOKEN.replace("oauth:", "")
    headers = {"Client-ID": CLIENT_ID, "Authorization": f"Bearer {access_token}"}
    params = {"game_id": game_id, "first": quantidade, "language": "en"}
    response = requests.get("https://api.twitch.tv/helix/streams", headers=headers, params=params)

    if response.status_code != 200:
        print(f"  Erro na API: {response.status_code} - {response.text}")
        return []

    streams = response.json().get("data", [])
    # filtra inglês
    streams_en = [s for s in streams if s.get("language") == "en"]
    return streams_en


def conectar_irc(canal):
    sock = socket.socket()
    sock.connect(("irc.chat.twitch.tv", 6667))
    sock.send(f"PASS {OAUTH_TOKEN}\r\n".encode())
    sock.send(f"NICK {BOT_NICK}\r\n".encode())
    sock.send("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership\r\n".encode())
    sock.send(f"JOIN #{canal}\r\n".encode())
    sock.settimeout(10)
    return sock


def coleta_mensagens(canal, quantidade_necessaria):
    mensagens = []
    try:
        sock = conectar_irc(canal)
        while len(mensagens) < quantidade_necessaria:
            try:
                dados = sock.recv(2048).decode("utf-8", errors="ignore")
                if dados == "":
                    print(f"  conexão fechada por {canal}")
                    break
            except socket.timeout:
                break

            if "NOTICE" in dados and "followers-only" in dados:
                print(f"  {canal}: modo somente seguidores, pulando.")
                sock.close()
                return "followers_only"

            if "PING" in dados:
                sock.send("PONG :tmi.twitch.tv\r\n".encode())

            for linha in dados.split("\r\n"):
                if "PRIVMSG" not in linha:
                    continue
                try:
                    texto = linha.split("PRIVMSG")[1].split(":", 1)[1].strip()
                    mensagens.append(texto)
                    sock.settimeout(45) # TEMPO DE ESPERA
                    if len(mensagens) >= quantidade_necessaria:
                        break
                except IndexError:
                    continue

        sock.close()

    except Exception as e:
        print(f"  Erro ao conectar em {canal}: {e}")
        return None

    return mensagens


with open(ARQUIVO_MENSAGENS, "a", newline="", encoding="utf-8") as arq_mensagens, \
     open(ARQUIVO_STREAMERS, "a", newline="", encoding="utf-8") as arq_streamers:

    writer_msgs = csv.writer(arq_mensagens, delimiter="\t")
    writer_streamers = csv.writer(arq_streamers, delimiter="\t")

    for categoria in id_categorias:
        game_id = categoria["id"]
        game_name = categoria["name"]
        print(f"\nCategoria: {game_name} ({game_id})")

        streamers = get_streamers(game_id, 50)  # busca mais para ter substitutos
        if not streamers:
            print("  Nenhum streamer encontrado.")
            continue

        coletados_categoria = 0
        for stream in streamers:
            if coletados_categoria >= STREAMERS_POR_CATEGORIA:
                break

            user_name = stream["user_login"]
            viewers = stream["viewer_count"]

            if user_name.lower() in streamers_ja_coletados:
                print(f"  {user_name}: já coletado.")
                continue

            print(f"  {user_name} ({viewers} viewers): coletando {MENSAGENS_POR_STREAMER} mensagens...")
            mensagens = coleta_mensagens(user_name, MENSAGENS_POR_STREAMER)

            if mensagens == "followers_only":
                continue  # não conta, tenta o próximo da lista
            
            if mensagens is None:
                print(f"  {user_name}: offline ou erro.")
                continue
            
            # se não atingiu a quantidade necessária, descarta e tenta outro streamer
            if len(mensagens) < MENSAGENS_POR_STREAMER:
                print(
                    f"  {user_name}: timeout após {len(mensagens)} mensagens. "
                    f"Pulando sem salvar."
                )
                continue
            
            mensagens = mensagens[:MENSAGENS_POR_STREAMER]

            for msg in mensagens:
                writer_msgs.writerow([user_name, game_id, msg])
            arq_mensagens.flush()

            writer_streamers.writerow([user_name, game_id, viewers])
            arq_streamers.flush()

            streamers_ja_coletados.add(user_name.lower())
            coletados_categoria += 1

            print(
                f"  {user_name}: {len(mensagens)} mensagens salvas. "
                f"({coletados_categoria}/{STREAMERS_POR_CATEGORIA})"
            )

print("\nColeta finalizada.")