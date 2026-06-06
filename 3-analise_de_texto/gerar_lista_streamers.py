import pandas as pd
import json
import os

# esse programa utiliza os dados coletados para o kdd para listar os streamers relevantes de cada categoria especificada

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CATEGORIAS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "id_categorias.json"
)
ARQUIVO_DESTINO = os.path.join(
    PASTA_ATUAL,
    "dados",
    "streamers_filtrado.csv"
)
ARQUIVO_STREAMS = os.path.join(
    PASTA_ATUAL,
    "..",
    "2-descoberta_de_conhecimento",
    "dados",
    "dataset_tratado.csv"    
)

IDIOMA = "en"



lista_categorias = []
with open(ARQUIVO_CATEGORIAS, 'r', encoding='utf-8') as file:
    dados = json.load(file)
    for d in dados:
        lista_categorias.append(int(d.get('id')))

colunas_manter = ["user_name", "viewer_count", "language", "game_id"]
df = pd.read_csv(
        ARQUIVO_STREAMS,
        sep="\t",
        usecols=colunas_manter
        )

df = df[df['language'] == IDIOMA]
df = df[df['game_id'].isin(lista_categorias)]
df = df.sort_values(ascending=False, by=['user_name', 'game_id', 'viewer_count'])
df['game_id'] = df['game_id'].astype(int)

media_categoria = (
    df.groupby(['user_name', 'game_id'])['viewer_count']
    .mean().round(2)
)

frequencia_categoria = (
    df.groupby(['user_name', 'game_id'])
    .size()
)

relevancia = (media_categoria*(frequencia_categoria*2)*10).round().astype(int)

df_novo = pd.DataFrame({
    'media_viewers': media_categoria,
    'frequencia': frequencia_categoria,
    'relevancia': relevancia
})

df_novo = df_novo.dropna()
df_novo = df_novo.reset_index()

df_novo = df_novo.sort_values(['game_id', 'relevancia'], ascending=False)

df_novo.to_csv(
    ARQUIVO_DESTINO,
    index=False,
    sep="\t"
)

