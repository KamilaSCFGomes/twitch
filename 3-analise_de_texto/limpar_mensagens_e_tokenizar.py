import pandas as pd
import os
import re
import numpy as np

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_MENSAGENS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "planob_chat_mensagens.csv"
)
MENSAGENS_LIMPO = os.path.join(
    PASTA_ATUAL,
    "dados",
    "chat_mensagens_limpo.csv"
)
LISTA_STREAMERS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "planob_streamers.csv"
)
ARQUIVO_DESTINO_STREAMER = os.path.join(
    PASTA_ATUAL,
    "dados",
    "chat_mensagens_tokenizado_streamer.csv"
)
ARQUIVO_DESTINO_CATEGORIA = os.path.join(
    PASTA_ATUAL,
    "dados",
    "chat_mensagens_tokenizado_categoria.csv"
)
STOP_WORDS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "stop_words_english.txt"
)


def substutuir_emojis(texto):
    emojis = {r'>:( )?(\(\)D)': 'angry',
              r'[B:;]( )?[\)D]': ' happy ',
              r'[:;](\')?( )?[\(cC]': 'sad',
              r' D:': ' sad ',
              r':[/\|]': 'annoyed',
              r':[oO0]': 'surprised',
              r':[pP]': 'silly',
              r'[oO0]_[oO0]': 'confused',
              r'^_^': 'happy',
              r':[sS]': 'confused',
              r':3': 'cute',
              r'[xX]D': 'happy',
              r'xdd?': 'happy',
              r'>_<': 'happy',
              r'<3': 'love',
              r'o7': 'hi'
              }
    
    for emoji in emojis:
        texto = re.sub(emoji, emojis[emoji], texto)

    return texto

def reduzir_repeticao(texto):
    # letras repetidas mais de 3 vezes
    texto = re.sub(r'(.)\1\1+', r'\1', texto)

    # risadas
    texto = re.sub(r'([bha]*haha[ha]*)+', 'haha', texto)
    texto = re.sub(r'(^\S)haha', 'haha', texto)

    # espaco duplo
    texto = re.sub(r'  +', ' ', texto)

    return texto

def limpar_texto(texto):
    try:            
        texto = re.sub(r'http\S+', '', texto) # remover links
        texto = re.sub(r'www\.\S+', '', texto) # remover links
        texto = re.sub(r'\S+\.com\S+', '', texto) # remover links
        texto = re.sub(r'discord\.gg\S+', '', texto) # remover links
        texto = re.sub(r'[0-9][0-9]?/[0-9][0-9]?(/[0-9][0-9][0-9]?[0-9]?)?', '', texto) # remover datas
        texto = re.sub(r'[0-9][0-9]?h', '', texto) # remover horarios
        texto = re.sub(r'[0-9][0-9]?[h:][0-9][0-9]?(:[0-9]?[0-9]?)?', '', texto) # remover horarios

        texto = substutuir_emojis(texto)
        texto = texto.lower() # remover maiusculas

        texto = re.sub(r'@\S+', '', texto) # remover mencoes
        texto = re.sub(r'!\S+', '', texto) # remover comandos
        texto = re.sub(r'[^a-z _]', '', texto) # remover pontuacao

        texto = re.sub(r'\S{20}\S*', '', texto) # remover palavras muito longas

        texto = texto.strip()
        texto = reduzir_repeticao(texto)

        return texto
    except:
        return ''
    
def tokenizar_1(texto):
    if re.search(r'\s', texto):
        texto = re.split(r'\s', texto)
        texto = [palavra for palavra in texto if palavra] # remove tokens vazios
        return texto
    else:
        return [texto]

def remover_stopwords(texto):
    return [palavra for palavra in texto if not palavra in lista_stopwords]



with open(STOP_WORDS, "r", newline="", encoding="utf-8") as f:
    lista_stopwords = f.read().splitlines()

df_streamers = pd.read_csv(LISTA_STREAMERS, sep="\t")
df_comentarios = pd.read_csv(ARQUIVO_MENSAGENS, sep="\t")

# filtrar comentarios utilizando a lista de streamers
df_comentarios = df_comentarios[df_comentarios.iloc[:, 0].isin(df_streamers.iloc[:, 0])]
df_comentarios = df_comentarios.sort_values(['game_id', 'user_name'])
df_comentarios_limpo = df_comentarios

tokens_streamer = {}
tokens_categoria = {}

print("\nComecando limpeza...")
for l in range(len(df_comentarios)):

    df_comentarios_limpo.iat[l, 2] = limpar_texto(df_comentarios.iat[l, 2])

    msg_tokenizada = tokenizar_1(df_comentarios_limpo.iat[l, 2])
    msg_tokenizada = remover_stopwords(msg_tokenizada)

    for token in msg_tokenizada:
        if not token: continue

        if not df_comentarios_limpo.iat[l, 0] in tokens_streamer:
            print(f"Streamer atual: {df_comentarios_limpo.iat[l, 0]}")
            tokens_streamer[df_comentarios_limpo.iat[l, 0]] = {}
        
        if not df_comentarios_limpo.iat[l, 1] in tokens_categoria:
            tokens_categoria[df_comentarios_limpo.iat[l, 1]] = {}

        if not token in tokens_streamer[df_comentarios_limpo.iat[l, 0]]:
            tokens_streamer[df_comentarios_limpo.iat[l, 0]][token] = 1
        else:
            tokens_streamer[df_comentarios_limpo.iat[l, 0]][token] += 1

        if not token in tokens_categoria[df_comentarios_limpo.iat[l, 1]]:
            tokens_categoria[df_comentarios_limpo.iat[l, 1]][token] = 1
        else:
            tokens_categoria[df_comentarios_limpo.iat[l, 1]][token] += 1

print("\nSalvando...")

with open(MENSAGENS_LIMPO, "w", newline="", encoding="utf-8") as f:
    # limpar mensagens vazias
    df_comentarios_limpo['mensagem'] = df_comentarios_limpo['mensagem'].replace(r'^\s*$', np.nan, regex=True)
    df_comentarios_limpo.dropna(subset=['mensagem'], inplace=True)

    df_comentarios_limpo.to_csv(MENSAGENS_LIMPO,
                                index=False,
                                sep="\t"
                                )

with open(ARQUIVO_DESTINO_STREAMER, "w", newline="", encoding="utf-8") as f:
    df_tokens = pd.DataFrame(tokens_streamer)
    df_tokens = df_tokens.fillna(0)
    df_tokens = df_tokens.astype(int)
    
    df_tokens['Total'] = df_tokens.sum(axis=1, numeric_only=True)
    df_tokens = df_tokens.sort_values(['Total'], ascending=False)

    df_tokens.to_csv(ARQUIVO_DESTINO_STREAMER,
                     index=True,
                     sep="\t"
                     )
    
with open(ARQUIVO_DESTINO_CATEGORIA, "w", newline="", encoding="utf-8") as f:
    df_tokens = pd.DataFrame(tokens_categoria)
    df_tokens = df_tokens.fillna(0)
    df_tokens = df_tokens.astype(int)

    df_tokens['Total'] = df_tokens.sum(axis=1, numeric_only=True)
    df_tokens = df_tokens.sort_values(['Total'], ascending=False)
    
    df_tokens.to_csv(ARQUIVO_DESTINO_CATEGORIA,
                     index=True,
                     sep="\t"
                     )

print("Fim")