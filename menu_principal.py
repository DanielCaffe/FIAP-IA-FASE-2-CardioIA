import math
import os
import subprocess
import shutil
from dataclasses import dataclass, field
from typing import Optional

import pandas as pd
import requests

# Caracteres ANSI para estilização no terminal
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
VERMELHO = "\033[91m"
NEGRITO = "\033[1m"
RESET = "\033[0m"


def find_rscript():
    """Encontra o caminho do Rscript automaticamente."""
    rscript = shutil.which("Rscript")
    if rscript:
        return rscript
    # Fallback para caminhos comuns
    common_paths = [
        r"C:\Program Files\R\R-4.5.3\bin\RScript.exe",
        r"C:\Program Files\R\R-4.4.0\bin\RScript.exe",
        r"C:\Program Files\R\R-4.3.0\bin\RScript.exe",
        r"C:\R\bin\RScript.exe"
    ]
    for path in common_paths:
        if os.path.exists(path):
            return path
    return None


@dataclass
class Insumos:
    adubo: float = 0.0
    agua: float = 0.0
    fosfato: float = 0.0
    herbicida: str = "N/A"
    pesticida: str = "N/A"
    fertilizante: str = "N/A"


@dataclass
class Financeiro:
    area_total: float = 0.0
    peso_total: float = 0.0
    lucro: float = 0.0
    gastos: float = 0.0
    metodo_aplicacao: str = "N/A"


@dataclass
class FarmData:
    cultura: Optional[str] = None
    area: float = 0.0
    insumos: Insumos = field(default_factory=Insumos)
    financeiro: Financeiro = field(default_factory=Financeiro)


def validar_float(mensagem: str, minimo: float = 0.0) -> float:
    """Solicita um float validado ao usuário."""
    while True:
        try:
            valor = float(input(f"{AZUL}{mensagem}{RESET}").replace(",", ".").strip())
            if valor < minimo:
                raise ValueError(f"Valor deve ser >= {minimo}.")
            return valor
        except ValueError as exc:
            print(f"{VERMELHO}Entrada inválida: {exc}. Tente novamente.{RESET}")


def validar_int(mensagem: str, opcoes: Optional[list] = None) -> int:
    """Solicita um inteiro validado ao usuário."""
    while True:
        try:
            valor = int(input(f"{AZUL}{mensagem}{RESET}").strip())
            if opcoes and valor not in opcoes:
                raise ValueError(f"Escolha uma das opções: {opcoes}.")
            return valor
        except ValueError as exc:
            print(f"{VERMELHO}Entrada inválida: {exc}. Tente novamente.{RESET}")


def escolher_cultura(state: FarmData) -> None:
    """Define a cultura escolhida no estado."""
    opcao = input(f"{AZUL}Escolha a cultura [C]afé / [S]oja: {RESET}").strip().upper()
    if opcao == "C":
        state.cultura = "cafe"
        print(f"{VERDE}Cultura definida: café{RESET}")
    elif opcao == "S":
        state.cultura = "soja"
        print(f"{VERDE}Cultura definida: soja{RESET}")
    else:
        print(f"{VERMELHO}Opção inválida. Use C ou S.{RESET}")


def calcular_area(state: FarmData) -> None:
    """Calcula a área plantada com base na cultura."""
    if state.cultura == "cafe":
        comprimento = validar_float("Comprimento (m): ", 0.01)
        largura = validar_float("Largura (m): ", 0.01)
        state.area = comprimento * largura
        print(f"{VERDE}Área do café (retângulo): {state.area:.2f} m²{RESET}")
    elif state.cultura == "soja":
        raio = validar_float("Raio (m): ", 0.01)
        state.area = math.pi * (raio ** 2)
        print(f"{VERDE}Área da soja (círculo): {state.area:.2f} m²{RESET}")
    else:
        print(f"{VERMELHO}Defina uma cultura antes de calcular área.{RESET}")


def calcular_insumos(state: FarmData) -> None:
    """Calcula insumos a partir da área e cultura."""
    if state.area <= 0 or not state.cultura:
        print(f"{VERMELHO}Área ou cultura não definida. Não é possível calcular insumos.{RESET}")
        return

    if state.cultura == "cafe":
        state.insumos.adubo = 200 * state.area
        state.insumos.agua = 3.0 * state.area
        state.insumos.fosfato = 10 * state.area
    else:
        state.insumos.adubo = 150 * state.area
        state.insumos.agua = 2.5 * state.area
        state.insumos.fosfato = 5 * state.area

    print(f"{VERDE}Insumos calculados com sucesso.{RESET}")


def definir_herbicida(state: FarmData) -> None:
    """Seleciona herbicida conforme tipo de ervas daninhas."""
    tipo = validar_int("[1] Grama rasteira, [2] Grama de folha larga: ", [1, 2])
    state.insumos.herbicida = "Glifosato" if tipo == 1 else "2,4-D"
    print(f"Herbicida: {state.insumos.herbicida}")


def definir_pesticida(state: FarmData) -> None:
    """Seleciona pesticida conforme tipo de inseto."""
    tipo = validar_int("[1] Insetos vagens, [2] Insetos sugadores: ", [1, 2])
    state.insumos.pesticida = "Carbaryl" if tipo == 1 else "Imidacloprido"
    print(f"Pesticida: {state.insumos.pesticida}")


def definir_fertilizante(state: FarmData) -> None:
    """Seleciona fertilizante conforme condição do solo."""
    tipo = validar_int("[1] pH < 6, [2] baixa fixação biológica: ", [1, 2])
    state.insumos.fertilizante = "Calcário" if tipo == 1 else "Inoculante Rhizobium"
    print(f"Fertilizante: {state.insumos.fertilizante}")


def definir_meio_aplicacao(state: FarmData) -> None:
    """Seleciona método de aplicação e atualiza gastos."""
    tipo = validar_int("[1] Pulverizador tratorizado, [2] Drone: ", [1, 2])
    if tipo == 1:
        state.financeiro.metodo_aplicacao = "Pulverizador Tratorizado"
        state.financeiro.gastos += 225000
    else:
        state.financeiro.metodo_aplicacao = "Drone Agrícola"
        state.financeiro.gastos += 15000
    print(f"Método de aplicação: {state.financeiro.metodo_aplicacao}")


def calcular_financeiro(state: FarmData) -> None:
    """Calcula produção e lucro estimado."""
    if state.area <= 0:
        print("Área inválida para cálculo financeiro.")
        return

    hectares = state.area / 10000.0
    state.financeiro.area_total = state.area
    state.financeiro.peso_total = 3.2 * hectares
    state.financeiro.lucro = 6300 * hectares

    print(f"Peso estimado: {state.financeiro.peso_total:.2f} ton")
    print(f"Lucro estimado: R$ {state.financeiro.lucro:.2f}")


def exibir_dados(state: FarmData) -> None:
    """Exibe o estado atual configurado."""
    print(f"\n{VERDE}{NEGRITO}=== Perfil de Plantio ==={RESET}")
    print(f"{AZUL}Cultura: {state.cultura or 'N/A'}{RESET}")
    print(f"{AZUL}Área: {state.area:.2f} m²{RESET}")
    print(f"{VERDE}--- Insumos ---{RESET}")
    print(f"{AZUL}Adubo: {state.insumos.adubo:.2f} g{RESET}")
    print(f"{AZUL}Água: {state.insumos.agua:.2f} L{RESET}")
    print(f"{AZUL}Fosfato: {state.insumos.fosfato:.2f} g{RESET}")
    print(f"{AZUL}Herbicida: {state.insumos.herbicida}{RESET}")
    print(f"{AZUL}Pesticida: {state.insumos.pesticida}{RESET}")
    print(f"{AZUL}Fertilizante: {state.insumos.fertilizante}{RESET}")
    print(f"{VERDE}--- Financeiro ---{RESET}")
    print(f"{AZUL}Área total: {state.financeiro.area_total:.2f}{RESET}")
    print(f"{AZUL}Peso total (ton): {state.financeiro.peso_total:.2f}{RESET}")
    print(f"{AZUL}Lucro: R$ {state.financeiro.lucro:.2f}{RESET}")
    print(f"{AZUL}Gastos: R$ {state.financeiro.gastos:.2f}{RESET}")
    print(f"{AZUL}Meio aplicação: {state.financeiro.metodo_aplicacao}{RESET}")


def atualizar_dados(state: FarmData) -> None:
    """Atualiza os dados de cultura, área e insumos do plantio."""
    print("\n=== Atualização de Dados ===")
    print("1 - Alterar cultura")
    print("2 - Alterar área")
    print("3 - Alterar insumos")
    print("0 - Voltar")

    opcao = validar_int("Escolha opção de atualização: ", [0, 1, 2, 3])

    if opcao == 1:
        escolher_cultura(state)
        if state.area > 0:
            calcular_insumos(state)
    elif opcao == 2:
        if not state.cultura:
            print(f"{VERMELHO}Defina a cultura antes de alterar a área.{RESET}")
        else:
            calcular_area(state)
            calcular_insumos(state)
    elif opcao == 3:
        if not state.cultura:
            print(f"{VERMELHO}Defina a cultura antes de editar insumos.{RESET}")
        else:
            definir_herbicida(state)
            definir_pesticida(state)
            definir_fertilizante(state)
            definir_meio_aplicacao(state)
    else:
        print(f"{AZUL}Retornando ao menu principal.{RESET}")


def consultar_dados(state: FarmData) -> None:
    """Exibe cultura atual e insumos definidos."""
    print(f"\n{VERDE}{NEGRITO}=== Consulta de Dados ==={RESET}")
    print(f"{AZUL}Cultura atual: {state.cultura or 'Não definida'}{RESET}")
    print(f"{AZUL}Área atual: {state.area:.2f} m²{RESET}")
    print(f"{VERDE}--- Insumos ---{RESET}")
    print(f"{AZUL}Herbicida: {state.insumos.herbicida}{RESET}")
    print(f"{AZUL}Pesticida: {state.insumos.pesticida}{RESET}")
    print(f"{AZUL}Fertilizante: {state.insumos.fertilizante}{RESET}")
    print(f"{AZUL}Adubo (g): {state.insumos.adubo:.2f}{RESET}")
    print(f"{AZUL}Água (L): {state.insumos.agua:.2f}{RESET}")
    print(f"{AZUL}Fosfato (g): {state.insumos.fosfato:.2f}{RESET}")


def zerar_dados(state: FarmData) -> None:
    """Zera todos os dados da aplicação."""
    state.cultura = None
    state.area = 0.0
    state.insumos = Insumos()
    state.financeiro = Financeiro()
    print(f"{VERDE}Dados zerados com sucesso.{RESET}")


def exportar_csv(state: FarmData) -> None:
    """Exporta dados de plantio e insumos para CSV."""
    if not state.cultura or state.area <= 0:
        print(f"{VERMELHO}Não há dados válidos para exportação. Defina cultura e área.{RESET}")
        return

    registros = [
        {"cultura": state.cultura, "area": state.area, "tipo_insumo": "adubo", "qnt_insumo": state.insumos.adubo},
        {"cultura": state.cultura, "area": state.area, "tipo_insumo": "agua", "qnt_insumo": state.insumos.agua},
        {"cultura": state.cultura, "area": state.area, "tipo_insumo": "fosfato", "qnt_insumo": state.insumos.fosfato},
    ]
    df = pd.DataFrame(registros)
    nome_arquivo = "dados_plantio.csv"
    df.to_csv(nome_arquivo, index=False, encoding="utf-8-sig")
    print(f"{VERDE}CSV exportado: {nome_arquivo}{RESET}")


def executar_estatisticas_r() -> None:
    """Executa script estatisticas_basicas.r com dados exportados."""
    arquivo = "dados_plantio.csv"
    if not os.path.exists(arquivo):
        print(f"{VERMELHO}Arquivo dados_plantio.csv não encontrado. Exporte antes.{RESET}")
        return

    rscript_path = find_rscript()
    if not rscript_path:
        print(f"{VERMELHO}Rscript não encontrado. Instale R ou adicione ao PATH.{RESET}")
        return

    try:
        resultado = subprocess.run([rscript_path, "estatisticas_basicas.r"], capture_output=True, text=True, check=True)
        print(f"{VERDE}== Estatísticas (R) =={RESET}")
        print(resultado.stdout)
    except subprocess.CalledProcessError as exc:
        print(f"{VERMELHO}Erro ao executar R: {exc.stderr}{RESET}")
    except FileNotFoundError:
        print(f"{VERMELHO}Rscript não encontrado.{RESET}")


def consultar_previsao_tempo() -> None:
    """Executa o script previsao_do_tempo.r com cidade escolhida pelo usuário."""
    cidade = input(f"{AZUL}Digite o nome da cidade para consulta do tempo: {RESET}").strip()
    if not cidade:
        print(f"{AMARELO}Cidade não informada. Usando São Paulo como padrão.{RESET}")
        cidade = "São Paulo"

    rscript_path = find_rscript()
    if not rscript_path:
        print(f"{VERMELHO}Rscript não encontrado. Instale R ou adicione ao PATH.{RESET}")
        return

    try:
        resultado = subprocess.run([rscript_path, "previsao_do_tempo.r", cidade], capture_output=True, text=True, check=True)
        print(f"{VERDE}== Previsão do tempo (R) =={RESET}")
        print(resultado.stdout)
    except subprocess.CalledProcessError as exc:
        print(f"{VERMELHO}Erro ao executar R: {exc.stderr}{RESET}")
    except FileNotFoundError:
        print(f"{VERMELHO}Rscript não encontrado.{RESET}")



def menu() -> int:
    """Exibe o menu principal e retorna opção."""
    print(f"\n{VERDE}{NEGRITO}=== MENU PRINCIPAL ==={RESET}")
    print("1 - Dados de Plantio")
    print("2 - Manipulação de Insumos (Herbicida/Pesticida/Fertilizante/Aplicação)")
    print("3 - Financeiro")
    print("4 - Estatísticas Básicas (R)")
    print("5 - API Meteorológica (R)")
    print("6 - Exportar CSV")
    print("7 - Exibir Perfil")
    print("8 - Consultar Dados")
    print("9 - Atualização de Dados")
    print("10 - Deletar de Dados")
    print(f"11 - Sair{RESET}")
    return validar_int(f"{AZUL}Selecione a opção: {RESET}", list(range(1, 12)))


def main() -> None:
    state = FarmData()

    while True:
        opcao = menu()
        if opcao == 1:
            escolher_cultura(state)
            calcular_area(state)
            calcular_insumos(state)
        elif opcao == 2:
            if not state.cultura:
                print(f"{VERMELHO}Defina a cultura antes de configurar insumos.{RESET}")
                continue
            definir_herbicida(state)
            definir_pesticida(state)
            definir_fertilizante(state)
            definir_meio_aplicacao(state)
        elif opcao == 3:
            calcular_financeiro(state)
            exibir_dados(state)
        elif opcao == 4:
            exportar_csv(state)
            executar_estatisticas_r()
        elif opcao == 5:
            consultar_previsao_tempo()
        elif opcao == 6:
            exportar_csv(state)
        elif opcao == 7:
            exibir_dados(state)
        elif opcao == 8:
            consultar_dados(state)
        elif opcao == 9:
            atualizar_dados(state)
        elif opcao == 10:
            zerar_dados(state)
        elif opcao == 11:
            print(f"{VERDE}Encerrando aplicação. Até breve!{RESET}")
            break


if __name__ == "__main__":
    main()
