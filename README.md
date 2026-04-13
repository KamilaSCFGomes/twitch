# Caractericação Topológica da Twitch
> Kamila Gomes e Pedro Dornelas

Estas são algumas análises sobre a Twitch para a disciplina de Mineração e Análise de Redes Sociais.

Os dados foram extraídos utilizando a API oficial da Twitch.

É necessário [gerar um ID e segredo](https://dev.twitch.tv/console/apps), [gerar token](gerar_token_twitch.py) e substituir no código para utilizar a API da Twitch.

[gerar_lista_categorias.py](gerar_lista_categorias.py) e [extrair_ultimos_videos.py](extrair_ultimos_videos.py) coletam os dados necessários, que foram salvos na pasta [dados](dados).

[grafo_e_propriedades.py](grafo_e_propriedades.py) realiza as análises e gera o grafo.