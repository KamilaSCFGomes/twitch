# Mineração e Análise da Twitch
> Kamila Gomes e Pedro Dornelas

Estas são algumas análises sobre a Twitch para a disciplina de Mineração e Análise de Redes Sociais.

Os dados foram extraídos utilizando a API oficial da Twitch.

É necessário [gerar um ID e segredo](https://dev.twitch.tv/console/apps), [gerar token](gerar_token_twitch.py) e substituir no código para utilizar a API da Twitch.

# Caracterização topológica de Redes Sociais
[gerar_lista_categorias.py](1-caracterizacao_topologica/gerar_lista_categorias.py) e [extrair_ultimos_videos.py](1-caracterizacao_topologica/extrair_ultimos_videos.py) coletam os dados necessários, que foram salvos na pasta [dados](1-caracterizacao_topologica/dados).

[grafo_e_propriedades.py](1-caracterizacao_topologica/grafo_e_propriedades.py) realiza as análises e gera o grafo.

# Descoberta de Conhecimento em Bases de Dados de Redes Sociais

[coleta.py](2-descoberta_de_conhecimento/coleta.py) coleta os cados sobre as maiores transmissões atuais periodicamente, e salva as informações em [dados](2-descoberta_de_conhecimento/dados), com um arquivo separado para cada dia.

[x](x) realiza a KDD (Descoberta de Conhecimento em bases de Dados) e gera os gráficos.