import csv
import os
import sys
import re
from pathlib import Path
import unicodedata

PASTA_DADOS = os.path.join(os.getcwd(), "twitch", "4-recomendacao", "dados")
arquivo_entrada = os.path.join(PASTA_DADOS, "perfis_seguidos.csv")
arquivo_saida = os.path.join(PASTA_DADOS, "perfis_seguidos_processado.csv")

def remover_acentos(texto):
    nfkd = unicodedata.normalize('NFKD', texto)
    sem_acentos = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return sem_acentos

def remover_emojis(texto):
    emojis = [
        r'>:( )?(\(\)D)',
        r'[B:;]( )?[\)D]',
        r'[:;](\')?( )?[\(cC]',
        r' D:',
        r':[/\|]',
        r':[oO0]',
        r':[pP]',
        r'[oO0]_[oO0]',
        r'\^_\^',
        r':[sS]',
        r':3',
        r'[xX]D',
        r'xdd?',
        r'>_<',
        r'<3',
        r'o7'
    ]

    for emoji in emojis:
        texto = re.sub(emoji, '', texto)

    return texto


def reduzir_repeticao(texto):
    texto = re.sub(r'(.)\1\1+', r'\1', texto)
    texto = re.sub(r'([bha]*haha[ha]*)+', 'haha', texto)
    texto = re.sub(r'(^\S)haha', 'haha', texto)
    texto = re.sub(r'  +', ' ', texto)
    return texto


def limpar_texto(texto):
    try:
        texto = re.sub(r'http\S+', '', texto)
        texto = re.sub(r'www\.\S+', '', texto)
        texto = re.sub(r'\S+\.com\S+', '', texto)
        texto = re.sub(r'discord\.gg\S+', '', texto)
        texto = re.sub(r'[0-9][0-9]?/[0-9][0-9]?(/[0-9][0-9][0-9]?[0-9]?)?', '', texto)
        texto = re.sub(r'[0-9][0-9]?h', '', texto)
        texto = re.sub(r'[0-9][0-9]?[h:][0-9][0-9]?(:[0-9]?[0-9]?)?', '', texto)
        texto = remover_emojis(texto)
        texto = texto.lower()
        texto = re.sub(r'@\S+', '', texto)
        texto = re.sub(r'!\S+', '', texto)
        texto = remover_acentos(texto)
        texto = re.sub(r'[^a-z _]', '', texto)
        texto = re.sub(r'\S{20}\S*', '', texto)
        texto = re.sub(r' \S ', '', texto)
        texto = re.sub(r'^\S', '', texto)
        texto = texto.strip()
        texto = reduzir_repeticao(texto)
        return texto
    except:
        return ''


with open(arquivo_entrada, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    linhas = list(reader)

print(f"{len(linhas)} perfis carregados de {arquivo_entrada}")

with open(arquivo_saida, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter="\t")
    writer.writerow(["broadcaster_id", "broadcaster_name", "idioma", "perfil_texto"])

    for linha in linhas:
        texto_limpo = limpar_texto(linha["perfil_texto"])
        writer.writerow([
            linha["broadcaster_id"],
            linha["broadcaster_name"],
            linha["idioma"],
            texto_limpo
        ])
        print(f"  {linha['broadcaster_name']}: processado")

print(f"\nSalvo em {arquivo_saida}")