import pandas as pd
import glob
import os


PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(
    PASTA_ATUAL,
    "dados",
    "top_streams-*.csv"
)
INTERVALO_MINUTOS = 15

arquivos = glob.glob(CAMINHO_CSV)

if len(arquivos) == 0:
    exit()

# dataset concatenado
dfs = []

for arq in arquivos:

    df_temp = pd.read_csv(
        arq,
        sep="\t"
    )

    dfs.append(df_temp)

df_concatenado = pd.concat(
    dfs,
    ignore_index=True
)

saida_concatenado = os.path.join(
    PASTA_ATUAL,
    "dados",
    "dataset_concatenado.csv"
)

df_concatenado.to_csv(
    saida_concatenado,
    index=False,
    sep="\t"
)

print(f"\nDataset concatenado salvo em:")
print(saida_concatenado)

# dataset tratado wowwwww 

df = df_concatenado.copy()

linhas_antes = len(df)

df = df.drop_duplicates() # remover duplicados
df = df.dropna() # remover valores nulos

df['viewer_count'] = df['viewer_count'].astype(int) # viewers como inteiro

df['data_hora'] = pd.to_datetime( # converter data se n essa biblioteca pandas explode scrrrrr
    df['data_hora'],
    dayfirst=True
)
# ordenar por streamer e tempo
df = df.sort_values(['user_name', 'data_hora'])

df['viewer_diff'] = ( # diferença de viewers entre snapshots
    df.groupby('user_name')['viewer_count']
    .diff()
)

saida_tratado = os.path.join(
    PASTA_ATUAL,
    "dados",
    "dataset_tratado.csv"
)

df.to_csv(
    saida_tratado,
    index=False,
    sep="\t"
)

print(f"\nDataset tratado salvo em:")
print(saida_tratado)

# dataset derivado
media_viewers = (
    df.groupby('user_name')['viewer_count']
    .mean()
)

pico_viewers = (
    df.groupby('user_name')['viewer_count']
    .max()
)

desvio_viewers = (
    df.groupby('user_name')['viewer_count']
    .std()
)

frequencia = (
    df.groupby('user_name')
    .size()
)

crescimento_medio = (
    df.groupby('user_name')['viewer_diff']
    .mean()
)

volatilidade = (
    df.groupby('user_name')['viewer_diff']
    .std()
)

tempo_observado = (
    df.groupby('user_name')['data_hora']
    .count()
)

tempo_horas = (tempo_observado * INTERVALO_MINUTOS / 60)

idioma = (
    df.groupby('user_name')['language']
    .agg(lambda x: x.mode()[0])
)

jogo = (
    df.groupby('user_name')['game_id']
    .agg(lambda x: x.mode()[0])
)

quantidade_categorias = (
    df.groupby('user_name')['game_id']
    .nunique()
)

dataset = pd.DataFrame({ # dataset final
    'media_viewers': media_viewers,
    'pico_viewers': pico_viewers,
    'desvio_viewers': desvio_viewers,
    'frequencia': frequencia,
    'crescimento_medio': crescimento_medio,
    'volatilidade': volatilidade,
    'tempo_horas': tempo_horas,
    'quantidade_categorias': quantidade_categorias,
    'language': idioma,
    'game_id': jogo
})

dataset = dataset.dropna() # remover linhas inválidas
dataset = dataset.reset_index() # resetar índice

print(f"Dataset final após limpeza: {len(dataset)} streamers")

saida_dataset = os.path.join(
    PASTA_ATUAL,
    "dados",
    "dataset_streamers.csv"
)

dataset.to_csv(
    saida_dataset,
    index=False,
    sep="\t"
)

print(f"\nDataset derivado salvo em:")
print(saida_dataset)