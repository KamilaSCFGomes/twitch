import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))

ARQUIVO_DATASET = os.path.join(
    PASTA_ATUAL,
    "dados",
    "dataset_streamers.csv"
)

PASTA_GRAFICOS = os.path.join(
    PASTA_ATUAL,
    "graficos"
)

os.makedirs(PASTA_GRAFICOS, exist_ok=True)
dataset = pd.read_csv(
    ARQUIVO_DATASET,
    sep="\t"
)

estatisticas = dataset.describe()
print(f"\nEstatísticas básicas:")
print(estatisticas)

saida_estatisticas = os.path.join(
    PASTA_ATUAL,
    "dados",
    "estatisticas_basicas.csv"
)

estatisticas.to_csv(saida_estatisticas)
print(f"\nEstatísticas salvas em:")
print(saida_estatisticas)

colunas_numericas = [ # histogramas e bloxquesblox
    'media_viewers',
    'pico_viewers',
    'desvio_viewers',
    'frequencia',
    'crescimento_medio',
    'volatilidade',
    'tempo_horas',
    'quantidade_categorias'
]

for coluna in colunas_numericas:
    # histogramas
    plt.figure(figsize=(10,6))
    dataset[coluna].hist(
        bins=50
    )

    plt.title(f'Histograma - {coluna}')
    plt.xlabel(coluna)
    plt.ylabel('Frequência')

    caminho_hist = os.path.join(
        PASTA_GRAFICOS,
        f'histograma_{coluna}.png'
    )

    plt.savefig(caminho_hist)
    plt.close()

    print(f"Histograma salvo em:")
    print(caminho_hist)

    # boxploques
    plt.figure(figsize=(10,6))
    plt.boxplot(dataset[coluna])
    plt.title(f'Boxplot - {coluna}')

    caminho_box = os.path.join(
        PASTA_GRAFICOS,
        f'boxplot_{coluna}.png'
    )

    plt.savefig(caminho_box)
    plt.close()

    print(f"Boxplot salvo em:")
    print(caminho_box)

print("\nHistogramas e boxplots gerados.")

# correlacao
dataset_numerico = dataset[colunas_numericas]

correlacao = dataset_numerico.corr()
print("Correlação:")
print(correlacao)

saida_corr = os.path.join(
    PASTA_ATUAL,
    "dados",
    "correlacao.csv"
)

correlacao.to_csv(saida_corr)

print(f"\nCorrelação salva em:")
print(saida_corr)

# heatmap
plt.figure(figsize=(12,8))

sns.heatmap(
    correlacao,
    annot=True,
    cmap='coolwarm'
)

plt.title("Mapa de Correlação")

caminho_heatmap = os.path.join(
    PASTA_GRAFICOS,
    "heatmap_correlacao.png"
)

plt.savefig(caminho_heatmap)
plt.close()

print("Heatmap salvo em:")
print(caminho_heatmap)

# normalizar
scaler = StandardScaler()

dados_normalizados = scaler.fit_transform(dataset_numerico)

dados_normalizados_df = pd.DataFrame(
    dados_normalizados,
    columns=colunas_numericas
)

saida_normalizado = os.path.join(
    PASTA_ATUAL,
    "dados",
    "dataset_normalizado.csv"
)

dados_normalizados_df.to_csv(
    saida_normalizado,
    index=False,
    sep="\t"
)

print(f"\nDataset normalizado salvo em:")
print(saida_normalizado)

# PCA neh
pca = PCA( n_components=2)

dados_pca = pca.fit_transform(dados_normalizados)

df_pca = pd.DataFrame({
    'PCA1': dados_pca[:,0],
    'PCA2': dados_pca[:,1]
})

saida_pca = os.path.join(
    PASTA_ATUAL,
    "dados",
    "dataset_pca.csv"
)

df_pca.to_csv(
    saida_pca,
    index=False,
    sep="\t"
)

print(f"Dataset PCA salvo em:")
print(saida_pca)

print("\nVariância explicada:")
print(pca.explained_variance_ratio_)

print(
    f"\nVariância total explicada: "
    f"{sum(pca.explained_variance_ratio_):.4f}"
)

# grafico PCA
plt.figure(figsize=(10,6))
plt.scatter(
    df_pca['PCA1'],
    df_pca['PCA2']
)

plt.title("Projeção PCA")
plt.xlabel("PCA1")
plt.ylabel("PCA2")

caminho_pca = os.path.join(
    PASTA_GRAFICOS,
    "grafico_pca.png"
)

plt.savefig(caminho_pca)
plt.close()

print(f"\nGráfico PCA salvo em:")
print(caminho_pca)

# grafico categorias vs viewers
plt.figure(figsize=(10,6))

plt.scatter(
    dataset['quantidade_categorias'],
    dataset['media_viewers']
)

plt.title("Categorias vs Média de Viewers")
plt.xlabel("Quantidade de Categorias")
plt.ylabel("Média de Viewers")

caminho_cat_viewers = os.path.join(
    PASTA_GRAFICOS,
    "categorias_vs_viewers.png"
)

plt.savefig(caminho_cat_viewers)
plt.close()

print(f"\nGráfico categorias vs viewers salvo em:")
print(caminho_cat_viewers)


# grafico categorias vs volatilidade
plt.figure(figsize=(10,6))

plt.scatter(
    dataset['quantidade_categorias'],
    dataset['volatilidade']
)

plt.title("Categorias vs Volatilidade")
plt.xlabel("Quantidade de Categorias")
plt.ylabel("Volatilidade")

caminho_cat_vol = os.path.join(
    PASTA_GRAFICOS,
    "categorias_vs_volatilidade.png"
)

plt.savefig(caminho_cat_vol)
plt.close()

print(f"\nGráfico categorias vs volatilidade salvo em:")
print(caminho_cat_vol)