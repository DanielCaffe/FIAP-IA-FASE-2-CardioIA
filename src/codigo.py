"""
CardioIA - Fase 2
Parte 1: Análise de frases e sugestão de diagnóstico

Objetivo:
- Ler frases de sintomas (arquivo .txt)
- Ler mapa de conhecimento (arquivo .csv)
- Identificar sintomas nas frases
- Sugerir um diagnóstico simples
"""

import csv
import unicodedata


# =========================
# 1. FUNÇÃO PARA NORMALIZAR TEXTO
# =========================

def normalizar_texto(texto):
    """
    Deixa o texto:
    - minúsculo
    - sem acentos
    """
    texto = texto.lower().strip()

    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

    return texto


# =========================
# 2. LER FRASES
# =========================

def ler_frases(arquivo_txt):
    frases = []

    with open(arquivo_txt, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if linha != "":
                frases.append(linha)

    return frases


# =========================
# 3. LER MAPA DE CONHECIMENTO
# =========================

def ler_mapa(arquivo_csv):
    mapa = []

    with open(arquivo_csv, "r", encoding="utf-8-sig") as f:
        leitor = csv.DictReader(f)

        for linha in leitor:
            mapa.append(linha)

    return mapa


# =========================
# 4. ANALISAR FRASE
# =========================

def analisar_frase(frase, mapa):
    frase_norm = normalizar_texto(frase)

    pontuacao = {}
    sintomas_encontrados = []

    for item in mapa:
        s1 = normalizar_texto(item["sintoma_1"])
        s2 = normalizar_texto(item["sintoma_2"])
        doenca = item["doenca_associada"]

        if s1 in frase_norm:
            sintomas_encontrados.append(item["sintoma_1"])
            pontuacao[doenca] = pontuacao.get(doenca, 0) + 1

        if s2 in frase_norm:
            sintomas_encontrados.append(item["sintoma_2"])
            pontuacao[doenca] = pontuacao.get(doenca, 0) + 1

    # Remove duplicados
    sintomas_encontrados = list(set(sintomas_encontrados))

    # Escolhe diagnóstico com maior pontuação
    if pontuacao:
        diagnostico = max(pontuacao, key=pontuacao.get)
    else:
        diagnostico = "Não identificado"

    return sintomas_encontrados, diagnostico, pontuacao


# =========================
# 5. PROGRAMA PRINCIPAL
# =========================

def main():
    arquivo_frases = "frases_sintomas.txt"
    arquivo_mapa = "mapa_de_conhecimento.csv"

    frases = ler_frases(arquivo_frases)
    mapa = ler_mapa(arquivo_mapa)

    print("\n=== CARDIOIA - RESULTADOS ===\n")

    for i, frase in enumerate(frases, 1):
        sintomas, diagnostico, pontuacao = analisar_frase(frase, mapa)

        print(f"\nPaciente {i}")
        print(f"Frase: {frase}")
        print(f"Sintomas encontrados: {sintomas if sintomas else 'Nenhum'}")
        print(f"Diagnóstico sugerido: {diagnostico}")
        print(f"Pontuação: {pontuacao}")


# Executa o código
if __name__ == "__main__":
    main()