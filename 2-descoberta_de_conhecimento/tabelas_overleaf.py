import pandas as pd
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_CSV = os.path.join(
    PASTA_ATUAL,
    "dados",
    "estatisticas_basicas.csv"
)

tabelas = [
    {'nome':'viewers',
     'colunas':['media_viewers', 'pico_viewers', 'desvio_viewers', 'volatilidade', 'crescimento_medio'],
     'novos_nomes':{'media_viewers':'Média', 'pico_viewers':'Pico', 'desvio_viewers':'Desvio', 'volatilidade':'Volatilidade', 'crescimento_medio':'Crescimento Médio'}
    },
    {'nome':'permanencia',
     'colunas':['frequencia', 'tempo_horas', 'quantidade_categorias'],
     'novos_nomes':{'frequencia':'Frequência', 'tempo_horas':'Tempo (horas)', 'quantidade_categorias':'N. Categorias'}
    }
]

for coiso in tabelas:
    # Load the CSV file
    viewers = pd.read_csv(
        CAMINHO_CSV,
        sep=",",
        usecols=coiso.get('colunas'),
        
    )
    viewers = viewers.rename(columns=coiso.get('novos_nomes'))
    viewers = viewers.rename(index={0: 'count', 1: 'mean', 2:'std', 3:'min', 4:'25%', 5:'50%', 6:'75%', 7:'max'})

    saida_viewers = os.path.join(
        PASTA_ATUAL,
        "overleaf",
        f"{coiso.get('nome')}.csv"
    )

    viewers.to_csv(saida_viewers, index=True, float_format='%.2f')