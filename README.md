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