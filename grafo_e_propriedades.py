import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict as definir
import numpy as np
import warnings

with open("dados/streamers_dados_300.json", encoding="utf-8") as f:
    dados = json.load(f)["streamers"]

with open("dados/categorias.json", encoding="utf-8") as f:
    categorias = json.load(f)

filtro_top = sorted(dados.values(), key = lambda x: x["total_views"] / x["total_streams"], reverse = True)[:500]

vods_por_streamer = definir(set)
for info in filtro_top:
    nome = info["name"]
    for categoria in info.get("categories", []):
        vods_por_streamer[nome].add(categoria)

print(f"Streamers com VODs: {len(vods_por_streamer)}")
total_vods = sum(len(v) for v in vods_por_streamer.values())
print(f"Streamers com uma única categoria: {total_vods}")

jogo_para_streamers = definir(list)
for streamer, jogos in vods_por_streamer.items():
    for jogo in jogos:
        jogo_para_streamers[jogo].append(streamer)

G = nx.Graph()
G.add_nodes_from(vods_por_streamer.keys())
for jogo, streamers in jogo_para_streamers.items():
    for i in range(len(streamers)):
        for j in range(i + 1, len(streamers)):
            u, v = streamers[i], streamers[j]
            if G.has_edge(u, v):
                G[u][v]["peso"] += 1
            else:
                G.add_edge(u, v, peso=1)

print(f"Vértices:         {G.number_of_nodes()}")
print(f"Arestas:          {G.number_of_edges()}")
print(f"Clustering médio: {nx.average_clustering(G):.4f}")
print(f"Densidade:        {nx.density(G):.4f}")
nos_isolados = [n for n, g in G.degree() if g == 0]
print(f"Nós isolados:     {len(nos_isolados)}")

grau_valores = [g for _, g in G.degree()]
plt.figure()
plt.hist(grau_valores, bins=30)
plt.title("Distribuição de Graus — Streamers")
plt.xlabel("Grau")
plt.ylabel("Frequência")
plt.tight_layout()
plt.savefig("distribuicao_graus.png", dpi=150)
plt.close()
print("Salvo: distribuicao_graus.png")

cent_grau        = nx.degree_centrality(G)
cent_eigenvector = nx.eigenvector_centrality(G, max_iter=1000)

print("\nTop 50 por Eigenvector Centrality:")
top50 = sorted(cent_eigenvector.items(), key=lambda x: x[1], reverse=True)[:50]
for i, (nome, val) in enumerate(top50):
    print(f"  #{i+1} {nome}: {val:.6f}")

vals_eig      = np.array(list(cent_eigenvector.values()))
vals_grau_all = np.array(list(cent_grau.values()))
print(f"\nEigenvector — min: {vals_eig.min():.6f} | max: {vals_eig.max():.6f} | desvio: {vals_eig.std():.6f}")
print(f"Grau        — min: {vals_grau_all.min():.6f} | max: {vals_grau_all.max():.6f} | desvio: {vals_grau_all.std():.6f}")

nos_principais = [n for n, _ in sorted(cent_grau.items(), key=lambda x: x[1], reverse=True)[:500]]
H = G.subgraph(nos_principais)

vals      = np.array([cent_eigenvector[n] for n in H.nodes()])
vals_norm = (vals - vals.min()) / (vals.max() - vals.min() + 1e-9)
tamanhos  = (vals_norm ** 2) * 1500 + 50

vals_grau_h    = np.array([cent_grau[n] for n in H.nodes()])
vals_grau_norm = (vals_grau_h - vals_grau_h.min()) / (vals_grau_h.max() - vals_grau_h.min() + 1e-9)

fig, ax = plt.subplots(figsize=(60, 48))
pos = nx.kamada_kawai_layout(H, weight = "peso")


nx.draw_networkx(
    H, pos, ax=ax,
    node_size=tamanhos,
    node_color=vals_grau_norm,
    cmap=plt.cm.plasma,
    with_labels=True,
    labels={n: n for n in H.nodes()},
    font_size=5,
    font_color="black",
    edge_color="#cccccc",
    alpha=0.9,
    width=0.4
)

ax.set_title("Rede de Streamers da Twitch", fontsize=20)
ax.axis("off")
plt.tight_layout()
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    plt.savefig("rede_streamers.png", dpi=200, facecolor="white")
    
plt.close()
print("Salvo: rede_streamers.png")