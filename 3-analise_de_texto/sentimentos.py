import pandas as pd
from transformers import pipeline
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_COMENTARIOS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "chat_mensagens_limpo.csv"
)
ARQUIVO_COMENTARIOS_SENTIMENTO = os.path.join(
    PASTA_ATUAL,
    "dados",
    "chat_mensagens_sentimento.csv"
)
STATS_SENTIMENTO = os.path.join(
    PASTA_ATUAL,
    "dados",
    "sentimentos_estatisticas.csv"
)
GRAFICO = os.path.join(
    PASTA_ATUAL,
    "dados",
    "grafico_sentimentos.png"
)
ID_CATEGORIAS = os.path.join(
    PASTA_ATUAL,
    "dados",
    "id_categorias.json"
)

LER_DO_CSV = True

if not LER_DO_CSV:
    df = pd.read_csv(ARQUIVO_COMENTARIOS, sep="\t")

    print(df.head())
    print(f"Total de comentários: {len(df)}")
    print(df)

    classifier = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        truncation=True
    )
    def sentiment_score(text):
        try:

            result = classifier(text[:512])[0]

            label = result["label"]
            confidence = result["score"]

            if label == "positive":
                score = confidence

            elif label == "negative":
                score = -confidence

            else:
                score = 0

            return pd.Series([label, confidence, score])

        except Exception:
            return pd.Series(["error", 0, 0])

    tqdm.pandas()

    df[["sentiment", "confidence", "score"]] = (
        df["mensagem"]
        .progress_apply(sentiment_score)
    )

    # Salvar resultados individuais
    df.to_csv(ARQUIVO_COMENTARIOS_SENTIMENTO, index=False)

    stats_categoria = (
        df.groupby("game_id")
        .agg(
            total_comments=("mensagem", "count"),
            mean_sentiment=("score", "mean"),
            std_sentiment=("score", "std"),
            positive_pct=("sentiment",
                            lambda x: (x == "positive").mean()*100),
            negative_pct=("sentiment",
                            lambda x: (x == "negative").mean()*100),
            neutral_pct=("sentiment",
                        lambda x: (x == "neutral").mean()*100)
        )
        .sort_values("mean_sentiment", ascending=False)
    )

    print(stats_categoria)

    stats_categoria.to_csv(
        STATS_SENTIMENTO
    )

else:
    df = pd.read_csv(ARQUIVO_COMENTARIOS_SENTIMENTO, sep="\t")

    stats_categoria = pd.read_csv(STATS_SENTIMENTO)


# GRAFICOS

plt.figure(figsize=(12,6))

sns.barplot(
    data=stats_categoria.reset_index(),
    x="game_id",
    y="mean_sentiment"
)

plt.xticks(rotation=45)
plt.title("Average Sentiment by Category")
plt.tight_layout()

plt.savefig(GRAFICO)
plt.show()