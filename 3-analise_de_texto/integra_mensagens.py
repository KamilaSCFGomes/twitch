import pandas as pd
import csv
import os
import json

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_MENSAGENS = os.path.join(PASTA_ATUAL, "dados", "chat_mensagens.csv")
ARQUIVO_PLANOB_MENSAGENS = os.path.join(PASTA_ATUAL, "dados", "planob_chat_mensagens.csv")
ARQUIVO_PLANOB_STREAMERS = os.path.join(PASTA_ATUAL, "dados", "planob_streamers.csv")
ARQUIVO_CATEGORIAS = os.path.join(PASTA_ATUAL, "dados", "id_categorias.json")
ARQUIVO_STREAMERS_FILTRADO = os.path.join(PASTA_ATUAL, "dados", "streamers_filtrado.csv")

STREAMERS_POR_CATEGORIA = 10
MENSAGENS_POR_STREAMER = 100


with open(ARQUIVO_CATEGORIAS, "r", encoding="utf-8") as f:
    id_categorias = json.load(f)
ordem_categorias = [str(c["id"]) for c in id_categorias]

df_mensagens = pd.read_csv(ARQUIVO_MENSAGENS, sep="\t")
df_planob_mensagens = pd.read_csv(ARQUIVO_PLANOB_MENSAGENS, sep="\t")
df_planob_streamers = pd.read_csv(ARQUIVO_PLANOB_STREAMERS, sep="\t")
df_streamers_filtrado = pd.read_csv(ARQUIVO_STREAMERS_FILTRADO, sep="\t")

# índice de media_viewers por user_name (minúsculo para comparação)
df_streamers_filtrado["user_name_lower"] = df_streamers_filtrado["user_name"].str.lower()
media_viewers_map = df_streamers_filtrado.set_index("user_name_lower")["media_viewers"].to_dict()

# streamers já presentes no planob (minúsculos)
streamers_ja_no_planob = set(df_planob_mensagens["user_name"].str.lower().unique())

# contagem atual de streamers por categoria no planob
contagem_por_categoria = (
    df_planob_mensagens.groupby("game_id")["user_name"]
    .nunique()
    .to_dict()
)

with open(ARQUIVO_PLANOB_MENSAGENS, "a", newline="", encoding="utf-8") as arq_msgs, \
     open(ARQUIVO_PLANOB_STREAMERS, "a", newline="", encoding="utf-8") as arq_streamers:

    writer_msgs = csv.writer(arq_msgs, delimiter="\t")
    writer_streamers = csv.writer(arq_streamers, delimiter="\t")

    for game_id in ordem_categorias:
        game_id_int = int(game_id)
        atual = contagem_por_categoria.get(game_id_int, 0)

        print(f"\nCategoria {game_id}: {atual}/{STREAMERS_POR_CATEGORIA} streamers")

        if atual >= STREAMERS_POR_CATEGORIA:
            print("  Categoria já completa.")
            continue

        # streamers dessa categoria em chat_mensagens
        df_cat = df_mensagens[df_mensagens["game_id"] == game_id_int]
        streamers_cat = df_cat["user_name"].unique()

        for user_name in streamers_cat:
            if atual >= STREAMERS_POR_CATEGORIA:
                break

            if user_name.lower() in streamers_ja_no_planob:
                print(f"  {user_name}: já presente no planob.")
                continue

            msgs = df_cat[df_cat["user_name"] == user_name]["mensagem"]

            # filtra streamers com menos de 100 mensagens
            if len(msgs) < MENSAGENS_POR_STREAMER:
                print(f"  {user_name}: apenas {len(msgs)} mensagens, pulando.")
                continue

            msgs = msgs.head(MENSAGENS_POR_STREAMER)

            # busca media_viewers no streamers_filtrado
            viewers = media_viewers_map.get(user_name.lower(), None)
            viewers = int(viewers) if viewers is not None else None

            for msg in msgs:
                writer_msgs.writerow([user_name.lower(), game_id_int, msg])
            arq_msgs.flush()

            writer_streamers.writerow([user_name.lower(), game_id_int, viewers])
            arq_streamers.flush()

            streamers_ja_no_planob.add(user_name.lower())
            atual += 1
            print(f"  {user_name} (viewers: {viewers}): {len(msgs)} mensagens integradas. ({atual}/{STREAMERS_POR_CATEGORIA})")

print("\nIntegração finalizada.")