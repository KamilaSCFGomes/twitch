# Mineração e Análise da Twitch
> Kamila Gomes e Pedro Dornelas

Estas são algumas análises sobre a Twitch para a disciplina de Mineração e Análise de Redes Sociais.

Os dados foram extraídos utilizando a API oficial da Twitch.

É necessário [gerar um ID e segredo](https://dev.twitch.tv/console/apps), [gerar token](gerar_token_twitch.py) e substituir no código para utilizar a API da Twitch.

Dependências requeridas estão listadas em [requirements.txt](requirements.txt), ou podem ser baixadas usando:

```bash
pip install -r requirements.txt
```

# Caracterização topológica de Redes Sociais
[gerar_lista_categorias.py](1-caracterizacao_topologica/gerar_lista_categorias.py) e [extrair_ultimos_videos.py](1-caracterizacao_topologica/extrair_ultimos_videos.py) coletam os dados necessários, que foram salvos na pasta [dados](1-caracterizacao_topologica/dados).

[grafo_e_propriedades.py](1-caracterizacao_topologica/grafo_e_propriedades.py) realiza as análises e gera o grafo.

# Descoberta de Conhecimento em Bases de Dados de Redes Sociais

[coleta.py](2-descoberta_de_conhecimento/coleta.py) coleta os cados sobre as maiores transmissões atuais periodicamente, e salva as informações em [dados](2-descoberta_de_conhecimento/dados), com um arquivo separado para cada dia. É possível alterar a quantidade de streamers pesquisados e o tempo de intervalo entre snapshots alterando as variáveis `tam_pagina`, `num_paginas` e `intervalo`.

Para gerar as análises a partir dos dados coletados, é necessário rodar os seguintes arquivos, na ordem especificada:

[cria_dataset.py](2-descoberta_de_conhecimento/cria_dataset.py) trata os dados coletados, gerando um arquivo CSV único para compilar todos os dias de coleta, tratando dados inválidos ou nulos e criando outras tabelas com filtros específicos. As tabelas criadas são salvas em [dados](2-descoberta_de_conhecimento/dados).

[gera_estatisticas.py](2-descoberta_de_conhecimento/gera_estatisticas.py) gera tabelas e gráficos a partir de análises dos dados das tabelas geradas na etapa anterior. As tabelas são salvas em [dados](2-descoberta_de_conhecimento/dados), e os gráficos são salvos em [graficos](2-descoberta_de_conhecimento/graficos).

[clustering.py](2-descoberta_de_conhecimento/clustering.py) realiza  clustering com alguns valores diferentes para k e analisa os resultados utilizando o Método Elbow e Silhouette Score, e salva os gráficos gerados em [graficos](2-descoberta_de_conhecimento/graficos).

[tabelas_overleaf.py](2-descoberta_de_conhecimento/tabelas_overleaf.py) apenas formata algumas das tabelas anteriores para facilitar a produção do trabalho escrito, que foi feito utilizando o Overleaf. As tabelas geradas são salvas na pasta [overleaf](2-descoberta_de_conhecimento/overleaf).

# Análise de texto


Alguns dos arquivos são referentes à nossa primeira ideia de trabalho, que seria classificar sentimentos em streamers baseando-se na categoria transmitida e no gênero do streamer, mas não conseguimos coletar dados o suficiente para uma análise satisfatória nessa temática, então resolvemos considerar apenas as categorias dos streamers.

[limpar_mensagens_e_rokenizar.py](3-analise_de_texto/limpar_mensagens_e_tokenizar.py) lê as mensagens do chat do arquivo especificado e as normaliza removendo links, datas e horários, menções, comandos da Twitch, pontuações e caracteres especiais, palavras muito longas e caracteres repetitivos, traduzindo emojis, convertendo as letras para minúsculas padronizando risadas e removendo espaços extras. O resultado é salvo em [chat_mensagens_limpo.csv](3-analise_de_texto/dados/chat_mensagens_limpo.csv). Além disso, também tokeniza as mensagens, as separando em unigramas e removendo stop-words, e então salvando em um modelo de espaço-vetorial bag-of-words, separando por streamer em [chat_mensagens_tokenizado_streamer.csv](3-analise_de_texto/dados/chat_mensagens_tokenizado_streamer.csv) e por categoria em [chat_mensagens_tokenizado_categoria.csv](3-analise_de_texto/dados/chat_mensagens_tokenizado_categoria.csv). Utilizamos uma [lista de stop words](3-analise_de_texto/dados/stop_words_english.txt) foi baixada de um [site na internet](https://countwordsfree.com/stopwords).

A análise de sentimentos simplificada é feita em [positividade.py](3-analise_de_texto/positividade.py), utilizando as mensagens separadas por tokens e as comparando com listas de palavras [positivas](3-analise_de_texto/dados/positive-words.txt) e [negativas](3-analise_de_texto/dados/negative-words.txt), que também foram baixadas [da internet](https://www.kaggle.com/datasets/prajwalkanade/sentiment-analysis-word-lists-dataset). As palavras presentes na lista foram classificadas como positivas ou negativas, e as que não foram encontradas foram classificadas como neutras. Os dados obtidos são salvos em [positividade.csv](3-analise_de_texto/dados/positividade.csv), e gráficos são gerados na pasta [dados](3-analise_de_texto/dados). Chamamos esse método de positividade e os gráficos podem ser encontrados facilmente pois possuem esse termo no nome.

Em [sentimentos.py](3-analise_de_texto/sentimentos.py), utilizamos transformers para fazer outra análise de sentimentos. Escolhemos o modelo RoBERTa, uma variante de BERT que é treinada utilizando o Twitter, e por isso pode ter mais facilidade em compreender dados oriundos de outra rede social. Uma versão do chat é salvo com a avaliação de cada mensagem em [chat_mensagens_sentimento.csv](3-analise_de_texto/dados/chat_mensagens_sentimento.csv) e os resultados das análises são salvos em [sentimentos_estatisticas.csv](3-analise_de_texto/dados/sentimentos_estatisticas.csv) e um gráfico é gerado, chamado [grafico_sentimentos.png](3-analise_de_texto/dados/grafico_sentimentos.png).

[classificar_genero2.py](3-analise_de_texto/classificar_genero2.py), inicialmente no projeto, tinha o objetivo de assistir na classificação manual do gênero de streamers listados, e cria [contagem.csv](3-analise_de_texto/dados/contagem.csv) e [streamers_filtrado2.csv](3-analise_de_texto/dados/streamers_filtrado2.csv) após execução.

[coleta_mensagens.py](3-analise_de_texto/coleta_mensagens.py) percorre categorias em [id_categorias.json](3-analise_de_texto/dados/id_categorias.json) e, em ordem de relevância, coleta até 300 mensagens de streamers, gerando [chat_contagem.csv](3-analise_de_texto/dados/chat_contagem.csv) e [chat_mensagens.csv](3-analise_de_texto/dados/chat_mensagens.csv).

[planob_coleta_mensagens.py](3-analise_de_texto/planob_coleta_mensagens.py) é a iteração de [coleta_mensagens.py](3-analise_de_texto/coleta_mensagens.py) utilizada na versão final do trabalho. A principal diferença está no salvamento de 100 mensagens por streamer, com um limite de 10 streamers por categoria, além dos novos arquivos gerados [planob_chat_mensagens.csv](3-analise_de_texto/dados/planob_chat_mensagens.csv) e [planob_streamers.csv](3-analise_de_texto/dados/planob_streamers.csv)

[integra_mensagens.py](3-analise_de_texto/integra_mensagens.py) une dados de streamers coletados em [chat_mensagens.csv](3-analise_de_texto/dados/chat_mensagens.csv) a [planob_chat_mensagens.csv](3-analise_de_texto/dados/planob_chat_mensagens.csv), complementando o volume de dados.