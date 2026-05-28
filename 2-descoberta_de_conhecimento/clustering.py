import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


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

colunas = [ # ignorando frequencia pq bate muito com tempo_horas
    'media_viewers',
    'pico_viewers',
    'desvio_viewers',
    'crescimento_medio',
    'volatilidade',
    'tempo_horas',
    'quantidade_categorias'
]

dados = dataset[colunas]
print(f"\nAtributos:")
print(colunas)

scaler = StandardScaler()
dados_normalizados = scaler.fit_transform(dados)

# PCA ne
pca = PCA(n_components=2)

dados_pca = pca.fit_transform(dados_normalizados)

df_pca = pd.DataFrame({
    'PCA1': dados_pca[:,0],
    'PCA2': dados_pca[:,1]
})

print(f"kmeans clustering:\n")

inercias = []
silhuetas = []

K = range(2, 11) # testando varios valores de k
for k in K:

    modelo = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    clusters = modelo.fit_predict(
        dados_normalizados
    )

    inercia = modelo.inertia_

    silhueta = silhouette_score(
        dados_normalizados,
        clusters
    )

    inercias.append(inercia)
    silhuetas.append(silhueta)

    print(f"K = {k}")
    print(f"Inércia: {inercia:.2f}")
    print(f"Silhouette Score: {silhueta:.4f}\n")

melhor_k = K[silhuetas.index(max(silhuetas))]
print(f"\nMelhor K encontrado: {melhor_k}")
melhor_k = 3
print(f"K usado: {melhor_k}")

modelo_final = KMeans( # modelo final duh
    n_clusters=melhor_k,
    random_state=42,
    n_init=20
)

clusters_finais = modelo_final.fit_predict(dados_normalizados)
dataset['cluster'] = clusters_finais

saida_clusters = os.path.join(
    PASTA_ATUAL,
    "dados",
    "dataset_clusters.csv"
)

dataset.to_csv(
    saida_clusters,
    index=False,
    sep="\t"
)

print("\nDataset clusterizado salvo em:")
print(saida_clusters)

# analise
print(f"Análise dos Clusters:\n")

analise_clusters = dataset.groupby('cluster')[colunas].mean()
print(analise_clusters)

saida_analise = os.path.join(
    PASTA_ATUAL,
    "dados",
    "analise_clusters.csv"
)

analise_clusters.to_csv(saida_analise)
print("\nAnálise dos clusters salva em:")
print(saida_analise)


# gráfico elbow
plt.figure(figsize=(10,6))

plt.plot(
    list(K),
    inercias,
    marker='o'
)

plt.title("Método Elbow")
plt.xlabel("Número de clusters (K)")
plt.ylabel("Inércia")

caminho_elbow = os.path.join(
    PASTA_GRAFICOS,
    "grafico_elbow.png"
)

plt.savefig(caminho_elbow)
plt.close()

print("\nGráfico Elbow salvo em:")
print(caminho_elbow)

# gráfico silhouette
plt.figure(figsize=(10,6))

plt.plot(
    list(K),
    silhuetas,
    marker='o'
)

plt.title("Silhouette Score")
plt.xlabel("Número de clusters (K)")
plt.ylabel("Score")

caminho_silhouette = os.path.join(
    PASTA_GRAFICOS,
    "grafico_silhouette.png"
)

plt.savefig(caminho_silhouette)
plt.close()

print("Gráfico silhouette salvo em:")
print(caminho_silhouette)

# visualizacao pca e clusters
plt.figure(figsize=(12,8))

sns.scatterplot(
    x=df_pca['PCA1'],
    y=df_pca['PCA2'],
    hue=clusters_finais,
    palette='tab10'
)

plt.title("Clusters de Streamers (PCA)")
plt.xlabel("PCA1")
plt.ylabel("PCA2")

caminho_clusters = os.path.join(
    PASTA_GRAFICOS,
    "clusters_pca.png"
)
plt.savefig(caminho_clusters)
plt.close()

print("Visualização salva em:")
print(caminho_clusters)

print(f"Melhor K encontrado: {melhor_k}")
print(
    f"Melhor silhouette score: "
    f"{max(silhuetas):.4f}"
)