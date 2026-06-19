import requests
import json
import csv
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import ler_informacoes as app

PASTA_DADOS = os.path.join(os.getcwd(), "twitch", "4-recomendacao", "dados")
arquivo_canais_seguidos = os.path.join(PASTA_DADOS, "canais_seguidos.json")
arquivo_perfis = os.path.join(PASTA_DADOS, "perfis_seguidos.csv")
headers = app.get_header_user_oauth()

def pega_vods(broadcaster_id, n=10):
    url = "https://api.twitch.tv/helix/videos"
    params = {"user_id": broadcaster_id, "type": "archive", "first": n}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.exceptions.Timeout:
        print(f"    timeout ao buscar VODs")
        return []
    if resp.status_code != 200:
        return []
    return resp.json().get("data", [])

def pega_info_canal(broadcaster_id):
    url = "https://api.twitch.tv/helix/channels"
    params = {"broadcaster_id": broadcaster_id}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
    except requests.exceptions.Timeout:
        print(f"    timeout ao buscar info do canal")
        return {}
    if resp.status_code != 200:
        return {}
    dados = resp.json().get("data", [])
    return dados[0] if dados else {}

def monta_perfil_streamer(broadcaster_id, broadcaster_name):
    print(f"    buscando VODs de {broadcaster_name}...")
    vods = pega_vods(broadcaster_id)
    print(f"    {len(vods)} VODs encontrados")

    print(f"    buscando info do canal {broadcaster_name}...")
    info = pega_info_canal(broadcaster_id)

    if not vods:
        print(f"    sem VODs, pulando.")
        return None

    idioma = info.get("broadcaster_language", "")

    textos = []
    for v in vods:
        partes = []
        if v.get("title"):
            partes.append(v["title"])
        if v.get("tags"):
            partes.extend(v["tags"])
        textos.append(" ".join(partes))

    if info.get("game_name"):
        textos.append(info["game_name"])
    if info.get("tags"):
        textos.extend(info["tags"])

    print(f"    perfil montado com {len(textos)} entradas de texto, idioma={idioma}")
    return {
        "broadcaster_id":   broadcaster_id,
        "broadcaster_name": broadcaster_name,
        "idioma":           idioma,
        "perfil_texto":     " ".join(textos)
    }

ja_coletados = set()
if os.path.exists(arquivo_perfis):
    with open(arquivo_perfis, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            ja_coletados.add(row["broadcaster_id"])

if not os.path.exists(arquivo_perfis):
    with open(arquivo_perfis, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["broadcaster_id", "broadcaster_name", "idioma", "perfil_texto"])

with open(arquivo_canais_seguidos, "r", encoding="utf-8") as f:
    canais_seguidos = json.load(f)

print(f"\n{len(canais_seguidos)} canais seguidos carregados.")
print(f"{len(ja_coletados)} já coletados anteriormente.")

with open(arquivo_perfis, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")

    for canal in canais_seguidos:
        if canal["broadcaster_id"] in ja_coletados:
            print(f"  {canal['broadcaster_name']}: já coletado, pulando.")
            continue

        print(f"  {canal['broadcaster_name']}...")
        perfil = monta_perfil_streamer(canal["broadcaster_id"], canal["broadcaster_name"])

        if perfil:
            writer.writerow([
                perfil["broadcaster_id"],
                perfil["broadcaster_name"],
                perfil["idioma"],
                perfil["perfil_texto"]
            ])
            f.flush()

        time.sleep(0.2)

print("\nColeta finalizada. Salvo em:", arquivo_perfis)