import requests
import csv
import os
import sys
import time
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ler_informacoes as app
from pre_processamento import limpar_texto
PASTA_DADOS = os.path.join(os.getcwd(), "twitch", "4-recomendacao", "dados")
arquivo_perfis = os.path.join(PASTA_DADOS, "perfis_seguidos_processado.csv")
arquivo_categorias = os.path.join(PASTA_DADOS, "categorias.csv")
headers = app.get_header_user_oauth()

def carrega_categorias():
    categorias = []
    with open(arquivo_categorias, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            categorias.append({
                "game_id": row["game_id"],
                "frequency": float(row["frequency"]) / 100
            })
    return categorias

def pega_streamers_por_categoria(game_id, total):
    url = "https://api.twitch.tv/helix/streams"
    params = {"first": min(100, total), "game_id": game_id}
    streams = []
    while len(streams) < total:
        tentativas = 0
        while tentativas < 3:
            try:
                resp = requests.get(url, headers=headers, params=params, timeout=15)
                break
            except requests.exceptions.RequestException as e:
                tentativas += 1
                print(f"  erro de conexão ({e}), tentativa {tentativas}/3...")
                time.sleep(2)
        else:
            print("  falhou 3 vezes, parando.")
            return streams[:total]
        if resp.status_code != 200:
            print(f"Erro ao buscar streamers online: {resp.json()}")
            break
        dados = resp.json()
        streams.extend(dados.get("data", []))
        print(f"  {len(streams)} streamers coletados...")
        cursor = dados.get("pagination", {}).get("cursor")
        if not cursor:
            break
        params["after"] = cursor
        params["first"] = min(100, total - len(streams))
    return streams[:total]

def pega_streamers_online(total=10000):
    categorias = carrega_categorias()
    streams = []

    for cat in categorias:
        quantidade = round(cat["frequency"] * total)
        if quantidade <= 0:
            continue
        print(f"  categoria {cat['game_id']} ({cat['frequency']*100:.1f}%): buscando {quantidade} streamers...")
        streams_cat = pega_streamers_por_categoria(cat["game_id"], quantidade)
        print(f"    {len(streams_cat)} streamers coletados.")
        streams.extend(streams_cat)

    print(f"\nTotal coletado: {len(streams)} streamers.")
    return streams

def monta_perfil_bruto(stream):
    partes = []
    if stream.get("game_name"):
        partes.append(stream["game_name"])
    if stream.get("tags"):
        partes.extend(stream["tags"])
    if stream.get("title"):
        partes.append(stream["title"])
    return {
        "broadcaster_id": stream["user_id"],
        "broadcaster_name": stream["user_name"],
        "idioma": stream.get("language", ""),
        "perfil_texto": " ".join(partes)
    }


def recomendar(perfis_seguidos, perfis_online, top_n=10):
    ids_seguidos = {p["broadcaster_id"] for p in perfis_seguidos}
    perfis_online = [p for p in perfis_online if p["broadcaster_id"] not in ids_seguidos]
    todos = perfis_seguidos + perfis_online
    textos = [p["perfil_texto"] for p in todos]
    n_seguidos = len(perfis_seguidos)
    vectorizer = TfidfVectorizer(max_df=0.7, min_df=2, ngram_range=(1, 1))
    matriz = vectorizer.fit_transform(textos)
    similaridade = cosine_similarity(matriz[:n_seguidos], matriz[n_seguidos:])
    scores = similaridade.mean(axis=0)
    tamanhos = np.array([len(p["perfil_texto"].split()) for p in perfis_online])
    confianca = np.minimum(tamanhos / 10, 1.0)
    scores_ajustados = scores * confianca
    indices_top = np.argsort(scores_ajustados)[::-1][:top_n]

    recomendados = []
    for i in indices_top:
        recomendados.append({"broadcaster_name": perfis_online[i]["broadcaster_name"], "score": round(float(scores_ajustados[i]), 4)})
    return recomendados


perfis_seguidos = []
with open(arquivo_perfis, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    for row in reader:
        perfis_seguidos.append(row)

print(f"{len(perfis_seguidos)} perfis carregados de {arquivo_perfis}")

idiomas = sorted({p["idioma"] for p in perfis_seguidos if p["idioma"]})
print(f"Idiomas encontrados nos seguidos: {idiomas}")

print("\nBuscando streamers online...")
streams_online = pega_streamers_online(10000)
print(f"{len(streams_online)} streamers online encontrados.")

print("\nMontando perfis brutos...")
perfis_online = [monta_perfil_bruto(s) for s in streams_online]

print("Limpando textos dos perfis online...")
for p in perfis_online:
    p["perfil_texto"] = limpar_texto(p["perfil_texto"])
print("Limpeza concluída.")

for idioma in idiomas:
    seguidos_idioma = [p for p in perfis_seguidos if p["idioma"] == idioma]
    print(f"\n===== RECOMENDAÇÕES — idioma: {idioma} ({len(seguidos_idioma)} seguidos) =====")
    recomendados = recomendar(seguidos_idioma, perfis_online, top_n=10)
    for i, r in enumerate(recomendados):
        print(f"  #{i+1} {r['broadcaster_name']} (score: {r['score']})  -->  https://www.twitch.tv/{r['broadcaster_name']}")