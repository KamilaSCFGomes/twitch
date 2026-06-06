import pandas as pd
import json
import csv
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_STREAMERS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "streamers_filtrado.csv"
)
ARQUIVO_DESTINO = os.path.join(
    PASTA_ATUAL,
    "dados",
    "streamers_genero.csv"
)
ARQUIVO_CONTAGEM = os.path.join(
    PASTA_ATUAL,
    "dados",
    "contagem.csv"
)
ARQUIVO_CATEGORIAS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "id_categorias.json"
)

NUMERO_POR_GENERO = 10
GENEROS_OBRIGATORIOS = ['homem', 'mulher']
GENEROS_EXTRAS = ['marca', 'outro', 'nao identificado']


# cria arquivo de contagem zerado
if not os.path.exists(ARQUIVO_CONTAGEM):
    fieldnames = ['game_id']
    for i in GENEROS_OBRIGATORIOS: fieldnames.append(i)
    for i in GENEROS_EXTRAS: fieldnames.append(i)

    lista_categorias = []
    with open(ARQUIVO_CATEGORIAS, 'r', encoding='utf-8') as file:
        dados = json.load(file)
        for d in dados: lista_categorias.append(int(d.get('id')))

    with open(ARQUIVO_CONTAGEM, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for c in lista_categorias:
            print(c)
            linha = {}
            for g in fieldnames:
                linha[g] = 0
            linha['game_id'] = c
            writer.writerow(linha)



df_streamers = pd.read_csv(ARQUIVO_STREAMERS, sep="\t")
df_contagem = pd.read_csv(ARQUIVO_CONTAGEM, sep="\t")

lista_generos = GENEROS_OBRIGATORIOS + GENEROS_EXTRAS
fieldnames = ['user_name', 'media_viewers', 'frequencia', 'relevancia', 'game_id', 'genero']

if not os.path.exists(ARQUIVO_DESTINO):
    with open(ARQUIVO_DESTINO, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()

with open(ARQUIVO_DESTINO, 'a', encoding='utf-8', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")    
    df_destino = pd.read_csv(ARQUIVO_DESTINO, sep="\t")
    
    # percorrer todas as categorias
    for i in range(len(df_contagem)):
        linha = df_contagem.iloc[i]
        print(f"\n\nCategoria: {linha['game_id']}")

        # conferir se a classificação dessa categoria já foi iniciada:
        ja_iniciado = False
        for g in linha:
            if int(g) > 0:
                ja_iniciado = True
                break
        
        #conferir se algum genero ja foi concluido
        generos_faltantes = GENEROS_OBRIGATORIOS[:]
        if ja_iniciado:
            for g in generos_faltantes:
                if linha[g] >= NUMERO_POR_GENERO:
                    generos_faltantes.pop(generos_faltantes.index(g))
        
        # conferir se a categoria foi concluida
        if len(generos_faltantes) <= 0:
            print("Categoria concluída.")
            break

        # filtrar a lista por jogo
        df_categoria = df_streamers[df_streamers['game_id'] == linha['game_id']]
        df_categoria = df_categoria.sort_values(['game_id', 'relevancia'], ascending=False)

        # percorrer todos os streamers
        for s in range (len(df_categoria)):

            streamer = df_categoria.iloc[s]
            url = f"https://www.twitch.tv/{streamer['user_name']}"
            print(f"\nStreamer: {streamer['user_name']} - {url}")

            # checar se o streamer já foi classificado
            if ((df_destino['user_name'] == streamer['user_name']) & (df_destino['game_id'] == streamer['game_id'])).any():
                print("Já classificado.")
                continue
            
            for g in range(len(lista_generos)):
                print(g, lista_generos[g])

            genero = 4
            while True:
                genero = input("Digite o genero: ")

                try:
                    genero = int(genero)
                    if int(df_contagem.iat[i, genero+1]) >= NUMERO_POR_GENERO:
                        print('Gênero já completo.')
                    else:
                        writer.writerow({
                            'user_name': streamer['user_name'],
                            'media_viewers': streamer['media_viewers'],
                            'frequencia': streamer['frequencia'],
                            'relevancia': streamer['relevancia'],
                            'game_id': streamer['game_id'],
                            'genero': lista_generos[genero]
                        })
                        df_contagem.at[i, lista_generos[genero]] += 1
                        df_contagem.to_csv(
                            ARQUIVO_CONTAGEM,
                            index=False,
                            sep="\t"
                        )
                        print(df_contagem)
                except:
                    print("\nInput inadequado. ")
                else: break

                # conferir se a categoria já está completa
            for g in generos_faltantes:
                if linha[g] >= NUMERO_POR_GENERO:
                    generos_faltantes.pop(generos_faltantes.index(g))
            print("falta:", generos_faltantes)
            
            if len(generos_faltantes)<=0:
                print('Categoria concluída.')
                break