import socket
import json
import csv
import os
import time
import pandas as pd

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_STREAMERS = os.path.join(PASTA_ATUAL, "dados", "streamers_filtrado.csv")
ARQUIVO_MENSAGENS = os.path.join(PASTA_ATUAL, "dados", "chat_mensagens.csv")
ARQUIVO_CONTAGEM = os.path.join(PASTA_ATUAL, "dados", "chat_contagem.csv")
ARQUIVO_CATEGORIAS = os.path.join(PASTA_ATUAL, "dados", "id_categorias.json")

OAUTH_TOKEN = "oauth:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# é o ACCESS TOKEN em https://twitchtokengenerator.com -> "Custom Scope Token" -> ativa "chat:read" - > "Generate Token!"
BOT_NICK = "XXXXXX" # seu nick  da conta da twitch, usada no login pedido no link acima

MENSAGENS_POR_STREAMER = 300


if not os.path.exists(ARQUIVO_MENSAGENS): # cria csv de mensagens
    with open(ARQUIVO_MENSAGENS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["user_name", "game_id", "mensagem"])

if not os.path.exists(ARQUIVO_CONTAGEM): # cria csv de contagem
    with open(ARQUIVO_CONTAGEM, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["user_name", "mensagens"])

contagem_mensagens = {}
df_contagem = pd.read_csv(ARQUIVO_CONTAGEM, sep="\t")
for _, linha in df_contagem.iterrows():
    contagem_mensagens[linha["user_name"]] = int(linha["mensagens"])

df_streamers = pd.read_csv(ARQUIVO_STREAMERS, sep="\t") # laivers
with open(ARQUIVO_CATEGORIAS, "r", encoding="utf-8") as f:
    id_categorias = json.load(f)

ordem_categorias = [str(c["id"]) for c in id_categorias]

def salvar_contagens():
    pd.DataFrame([
        {"user_name": k, "mensagens": v}
        for k, v in contagem_mensagens.items()
    ]).to_csv(ARQUIVO_CONTAGEM, sep="\t", index=False)


def conectar_irc(canal):
    sock = socket.socket()
    sock.connect(("irc.chat.twitch.tv", 6667))
    sock.send(f"PASS {OAUTH_TOKEN}\r\n".encode())
    sock.send(f"NICK {BOT_NICK}\r\n".encode())
    sock.send("CAP REQ :twitch.tv/tags twitch.tv/commands twitch.tv/membership\r\n".encode())
    sock.send(f"JOIN #{canal}\r\n".encode())
    sock.settimeout(10)

    return sock


def coletar_mensagens(canal, quantidade_necessaria):
    
    mensagens = []
    try:
        sock = conectar_irc(canal)
        while len(mensagens) < quantidade_necessaria:
            try:
                dados = sock.recv(2048).decode("utf-8", errors="ignore")
                if dados == "":
                    print(f"  conexão fechada por {canal}")
                    break

            except socket.timeout: # sem dados
                break

            if "PING" in dados:
                sock.send("PONG :tmi.twitch.tv\r\n".encode())

            for linha in dados.split("\r\n"):
                if "PRIVMSG" not in linha:
                    continue

                try:
                    texto = linha.split("PRIVMSG")[1].split(":", 1)[1].strip()
                    mensagens.append(texto)

                    if len(mensagens) >= quantidade_necessaria:
                        break

                except IndexError:
                    continue

        sock.close()

    except Exception as e:
        print(f"  Erro ao conectar em {canal}: {e}")
        return None

    return mensagens


with open(ARQUIVO_MENSAGENS, "a", newline="", encoding="utf-8") as arquivo_mensagens:
    writer = csv.writer(arquivo_mensagens, delimiter="\t")

    for game_id in ordem_categorias:
        df_categoria = df_streamers[df_streamers["game_id"] == int(game_id)]
        df_categoria = df_categoria.sort_values("relevancia", ascending=False)
        print(f"\nCategoria {game_id}")

        for _, streamer in df_categoria.iterrows():

            user_name = streamer["user_name"]
            quantidade_atual = contagem_mensagens.get(user_name, 0)
            if quantidade_atual >= MENSAGENS_POR_STREAMER:
                print(f"  {user_name}: já possui {quantidade_atual} mensagens.")
                continue

            faltam = MENSAGENS_POR_STREAMER - quantidade_atual
            print(f"  {user_name}: coletando {faltam} mensagens...")
            mensagens = coletar_mensagens(user_name, faltam)
            if mensagens is None:
                print(f"  {user_name}: offline ou erro.")
                continue

            mensagens = mensagens[:faltam]
            for msg in mensagens:
                writer.writerow([user_name, game_id, msg])

            arquivo_mensagens.flush()
            contagem_mensagens[user_name] = quantidade_atual + len(mensagens)
            salvar_contagens()
            print(f"  {user_name}: {len(mensagens)} mensagens salvas. Total = {contagem_mensagens[user_name]}")

print("\nColeta finalizada.")