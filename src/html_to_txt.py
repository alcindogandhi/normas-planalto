#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Baixa o documento HTML do CTN e converte para texto puro,
preservando as quebras de linha do HTML.
"""

import os
import requests
import re
from bs4 import BeautifulSoup

def clean_line(line: str, discard: list[str] = []) -> str:
    line = line.strip()
    line = re.sub(r"^Lcp *\d+$", "", line).strip()
    line = re.sub(r"^L *\d+$", "", line).strip()
    line = re.sub(r".+-?[Cc][Oo][Mm][Pp][Ii][Ll][Aa][Dd][OoAa]$", "", line).strip()
    line = re.sub(r"^Presid.{1}ncia da Rep.{1}blica$", "", line).strip()
    line = re.sub(r"^Secretaria Especial para Assuntos Jur.dicos$", "", line).strip()
    line = re.sub(r"^Secretaria-Geral$", "", line).strip()
    line = re.sub(r"^Casa Civil$", "", line).strip()
    line = re.sub(r"^Subchefia para Assuntos Jur.{1}dicos$", "", line).strip()
    line = re.sub(r"\(Reda[cç][aã]o.+\)", "", line).strip()
    line = re.sub(r"\(Inclu.+\)", "", line).strip()
    line = re.sub(r"\(?Vide.+\)?", "", line).strip()
    line = re.sub(r"\(Produção de efeitos.+\)", "", line).strip()
    line = re.sub(r"\(?Mensagem de veto.*\)?", "", line).strip()
    line = re.sub(r"\(?Revogados pel.*\)?", "(Revogados)", line).strip()
    line = re.sub(r"^.NDICE.*", "", line).strip()
    line = re.sub(r"Vig[eê]ncia", "", line).strip()
    line = re.sub(r"Produ.{2}o de efeitos", "", line).strip()
    line = re.sub(r"Emendas Constitucionais.*", "", line).strip()
    line = re.sub(r"^Ato das Disposi.{2}es Constitucionais.*", "", line).strip()
    line = re.sub(r"^Atos decorrentes do disposto.+", "", line).strip()
    line = re.sub(r"\s*Este texto n.{1}o substitui o publicado.*", "", line).strip()
    line = re.sub(r"P A R T E.+G E R A L", "PARTE GERAL", line).strip()
    line = re.sub(r"^\*$", "", line).strip()
    line = re.sub(r"Art\.\s*", "Art. ", line).strip()
    line = re.sub(r"^Regulamento$", "", line).strip()
    line = re.sub(r"^\(?Promulgação partes vetadas\)?", "", line).strip()

    for term in discard:
        line = re.sub(term, "", line).strip()
    return line.strip()

def html_to_text(url: str, output_file: str, discard: list[str] = []):
    # Define User-Agent do Google Chrome
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }

    # Baixa o HTML
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    response.encoding = 'iso-8859-1' #response.apparent_encoding or "utf-8"

    # Parse do HTML
    text = response.text.replace('\r\n', ' ').replace('\n', ' ').replace('&nbsp;', ' ').replace('\t', ' ') \
        .replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ')
    soup = BeautifulSoup(text, "html.parser")

    # Remove scripts e estilos
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    # Remove as tags <sup>
    for sup in soup.find_all("sup"):
        sup.replace_with("")

    # Substitui <br> por \n
    for br in soup.find_all("br"):
        br.replace_with("\n")

    # Substitui <p> por \n antes e depois
    for p in soup.find_all("p"):
        p.insert_before("\n")
        #p.insert_after("\n")

    # Insere um \n depois de uma linha de uma tabela
    for tr in soup.find_all("tr"):
        tr.insert_after("\n")

    # Extrai texto
    text = soup.get_text().replace('  ', ' ').replace('  ', ' ').replace('  ', ' ') \
        .replace(' ;', ';').replace(' .', '.')

    # Normaliza múltiplas quebras de linha
    lines = [ clean_line(line, discard) for line in text.splitlines() ]
    clean_text = "\n".join([line for line in lines if line and (not line.startswith("(")) and (not line.startswith("Vigência"))])

    # Salva no arquivo
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(clean_text)

    print(f"[OK] Texto salvo em: {output_file}")


if __name__ == "__main__":
    os.makedirs("build", exist_ok=True)

    files = [
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm", "outputFile": "build/ctn.txt", "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del4657compilado.htm", "outputFile": "build/lindb.txt", "discard": []},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm", "outputFile": "build/ccivil.txt", "discard": ["^Lei de Introdu.+"]},
        {"url": "https://www.planalto.gov.br/ccivil_03/leis/L8934compilado.htm", "outputFile": "build/cempr.txt", "discard": []},
    ]
    for f in files:
        html_to_text(f["url"], f["outputFile"], f["discard"])
