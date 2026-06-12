import pandas as pd
import os
import math
import matplotlib.pyplot as plt
import seaborn as sns
import json


PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_TOKENS_STREAMER = os.path.join(
    PASTA_ATUAL,
    "dados",
    "chat_mensagens_tokenizado_streamer.csv"
)
ARQUIVO_TOKENS_CATEGORIA = os.path.join(
    PASTA_ATUAL,
    "dados",
    "chat_mensagens_tokenizado_categoria.csv"
)
PALAVRAS_POSITIVAS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "positive-words.txt"
)
PALAVRAS_NEGATIVAS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "negative-words.txt"
)
ARQUIVO_TF_IDF = os.path.join(
    PASTA_ATUAL,
    "dados",
    "TF-IDF.csv"
)
GRAFICO_CATEGORIA = os.path.join(
    PASTA_ATUAL,
    "dados",
    "grafico_categoria_positividade.png"
)
GRAFICO_STREAMER = os.path.join(
    PASTA_ATUAL,
    "dados",
    "grafico_streamer_positividade.png"
)
POSITIVIDADE = os.path.join(
    PASTA_ATUAL,
    "dados",
    "positividade.csv"
)
ID_CATEGORIAS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "id_categorias.json"
)

def tf_idf(dados):
    dados2=dados
    dados2.loc['Total'] = dados2.sum(numeric_only=True)
    dados.loc['total_documentos'] = dados.count(numeric_only=True, axis=1)
    dados.loc['total_palavras'] = dados.count(numeric_only=True)
    
    for linha in range(len(dados2)):
        print(f"TD-IDF: {linha}/{len(dados2)}")
        for col in range(1, len(dados2.columns)):
            celula = dados2.iloc[linha, col]
            total_l = dados2.iloc[linha, -1]
            total_c = dados2.iloc[-1, col]
            
            tf = celula/total_c
            idf = math.log(total_documentos/total_l)
            dados2.iat[linha, col] = round(tf*idf,5)
    
    dados2 = dados2.rename(columns={"Unnamed: 0": "words"})

    return dados2

def renomear_colunas(df):
    with open(ID_CATEGORIAS, 'r', encoding='utf-8') as file:
        arquivo = json.load(file)
        for c in df.columns:
            for j in arquivo:
                if j['id'] == c:
                    df = df.rename(columns={c: j['name']})
    df = df.rename(columns={"Total": "média"})
    return df
        


def positividade(dados):
    positivos = {}
    negativos = {}
    neutros = {}
    total = {}

    for c in dados.columns[1:]:
        positivos[c] = 0
        negativos[c] = 0
        neutros[c] = 0
        total[c] = 0
    
    for l in range(len(dados)):
        if dados.iat[l, 0] in lista_positivos:
            for c in range(1, len(dados.iloc[l])):
                positivos[dados.columns[c]] += dados.iat[l, c]
                total[dados.columns[c]] += dados.iat[l, c]

        elif dados.iat[l, 0] in lista_negativos:
            for c in range(1, len(dados.iloc[l])):
                negativos[dados.columns[c]] += dados.iat[l, c]
                total[dados.columns[c]] += dados.iat[l, c]

        else:
            for c in range(1, len(dados.iloc[l])):
                neutros[dados.columns[c]] += dados.iat[l, c]
                total[dados.columns[c]] += dados.iat[l, c]

    df = pd.DataFrame([positivos, neutros, negativos, total])
    df = renomear_colunas(df)
    df.index=["positivas", "neutras", "negativas", "total"]
    df = df.rename_axis("categoria")
    return df


def salvar_grafico(df, streamers=False):
    print(df)
    df = df.T

    # Converter para porcentagem
    df['Positivas_%'] = df['positivas'] / df['total'] * 100
    df['Neutras_%'] = df['neutras'] / df['total'] * 100
    df['Negativas_%'] = df['negativas'] / df['total'] * 100

    # Estilo seaborn
    sns.set_theme(style="whitegrid")

    # Cores
    cores = {
        'Positivas': '#2ca02c',  # verde
        'Neutras': '#bdbdbd',    # cinza
        'Negativas': '#d62728'   # vermelho
    }

    # Figura
    fig, ax = plt.subplots(figsize=(10, 6))

    # Barras empilhadas
    ax.bar(
        df.index,
        df['Positivas_%'],
        color=cores['Positivas'],
        label='Positivas',
    )

    ax.bar(
        df.index,
        df['Neutras_%'],
        bottom=df['Positivas_%'],
        color=cores['Neutras'],
        label='Neutras'
    )

    ax.bar(
        df.index,
        df['Negativas_%'],
        bottom=df['Positivas_%'] + df['Neutras_%'],
        color=cores['Negativas'],
        label='Negativas'
    )

    # Adicionar rótulos
    for i in range(len(df)):

        # Positivas
        if streamers:
            ax.text(
                i,
                df['Positivas_%'].iloc[i] / 2,
                f"{df['Positivas_%'].iloc[i]:.1f}%",
                ha='center',
                va='bottom',
                fontsize=9,
                color='black',
                rotation=90
            )
        else:
            ax.text(
                i,
                df['Positivas_%'].iloc[i] / 2,
                f"{df['Positivas_%'].iloc[i]:.1f}%",
                ha='center',
                va='center',
                fontsize=9,
                color='white'
            )

        # Neutras
        if streamers:
            ax.text(
                i,
                df['Positivas_%'].iloc[i] + df['Neutras_%'].iloc[i] / 2,
                f"{df['Neutras_%'].iloc[i]:.1f}%",
                ha='center',
                va='center',
                fontsize=9,
                color='black',
                rotation=90
            )
        else:
            ax.text(
                i,
                df['Positivas_%'].iloc[i] + df['Neutras_%'].iloc[i] / 2,
                f"{df['Neutras_%'].iloc[i]:.1f}%",
                ha='center',
                va='center',
                fontsize=9,
                color='black'
            )

        # Negativas
        if streamers:
            ax.text(
                i,
                df['Positivas_%'].iloc[i] +
                df['Neutras_%'].iloc[i] +
                df['Negativas_%'].iloc[i] / 2,
                f"{df['Negativas_%'].iloc[i]:.1f}%",
                ha='center',
                va='top',
                fontsize=9,
                color='black',
                rotation=90
            )
        else:
            ax.text(
                i,
                df['Positivas_%'].iloc[i] +
                df['Neutras_%'].iloc[i] +
                df['Negativas_%'].iloc[i] / 2,
                f"{df['Negativas_%'].iloc[i]:.1f}%",
                ha='center',
                va='center',
                fontsize=9,
                color='white'
            )
    # Formatação
    ax.set_ylabel('Percentual (%)')
    if streamers: ax.set_xlabel('Streamer')
    else: ax.set_xlabel('Categoria')
    if streamers: ax.set_title('Distribuição de Sentimentos de palavras por streamer')
    else: ax.set_title('Distribuição de Sentimentos de palavras por categoria')
    ax.set_ylim(0, 100)
    if streamers: ax.legend(title='Streamer')
    else: ax.legend(title='Categoria')

    if streamers:
        plt.xticks(rotation=60, ha='right')
    else:
        plt.xticks(rotation=20, ha='right')
    plt.tight_layout()

    if streamers:
        plt.savefig(GRAFICO_STREAMER)
    else:
        plt.savefig(GRAFICO_CATEGORIA)
    plt.show()



with open(PALAVRAS_POSITIVAS, "r", newline="", encoding="utf-8") as f:
    lista_positivos = f.read().splitlines()
with open(PALAVRAS_NEGATIVAS, "r", newline="", encoding="utf-8") as f:
    lista_negativos = f.read().splitlines()


df_tokens_streamers = pd.read_csv(ARQUIVO_TOKENS_STREAMER, sep="\t")
df_tokens_streamers.loc['Total'] = df_tokens_streamers.sum(numeric_only=True)
total_documentos = len(df_tokens_streamers.columns)

df_tokens_categorias = pd.read_csv(ARQUIVO_TOKENS_CATEGORIA, sep="\t")
df_tokens_categorias.loc['Total'] = df_tokens_categorias.sum(numeric_only=True)



df_positividade = positividade(df_tokens_categorias)
df_positividade.to_csv(POSITIVIDADE, sep="\t")

salvar_grafico(df_positividade)

df_positividade = positividade(df_tokens_streamers)
salvar_grafico(df_positividade, True)