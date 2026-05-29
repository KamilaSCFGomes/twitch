import pandas as pd
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))

tabelas = [
    {'nome':'viewers',
     'colunas':['media_viewers', 'pico_viewers', 'desvio_viewers', 'volatilidade', 'crescimento_medio'],
     'novos_nomes':{'media_viewers':'Média', 'pico_viewers':'Pico', 'desvio_viewers':'Desvio', 'volatilidade':'Volatilidade', 'crescimento_medio':'Crescimento Médio'},
     'nome_linhas':{0: 'count', 1: 'mean', 2:'std', 3:'min', 4:'25%', 5:'50%', 6:'75%', 7:'max'},
     'csv_original':'estatisticas_basicas'
    },
    {'nome':'permanencia',
     'colunas':['frequencia', 'tempo_horas', 'quantidade_categorias'],
     'novos_nomes':{'frequencia':'Frequência', 'tempo_horas':'Tempo (horas)', 'quantidade_categorias':'N. Categorias'},
     'nome_linhas':{0: 'count', 1: 'mean', 2:'std', 3:'min', 4:'25%', 5:'50%', 6:'75%', 7:'max'},
     'csv_original':'estatisticas_basicas'
    },
    {'nome':'clusters',
     'colunas':['media_viewers','pico_viewers','desvio_viewers','crescimento_medio','volatilidade','tempo_horas','quantidade_categorias'],
     'novos_nomes':{'media_viewers':'Média', 'pico_viewers':'Pico', 'desvio_viewers':'Desvio', 'volatilidade':'Volatilidade', 'crescimento_medio':'Cresc. Médio', 'tempo_horas':'Tempo', 'quantidade_categorias':'N. Categorias'},
     'nome_linhas':{0:0, 1:1, 2:2},
     'csv_original':'analise_clusters'
    }
]

for coiso in tabelas:
    CAMINHO_CSV = os.path.join(
    PASTA_ATUAL,
    "dados",
    f"{coiso.get('csv_original')}.csv"
    )
    # Load the CSV file
    viewers = pd.read_csv(
        CAMINHO_CSV,
        sep=",",
        usecols=coiso.get('colunas'),
        
    )
    viewers = viewers.rename(columns=coiso.get('novos_nomes'))
    viewers = viewers.rename(index=coiso.get('nome_linhas'))

    saida_viewers = os.path.join(
        PASTA_ATUAL,
        "overleaf",
        f"{coiso.get('nome')}.csv"
    )

    viewers.to_csv(saida_viewers, index=True, float_format='%.2f')