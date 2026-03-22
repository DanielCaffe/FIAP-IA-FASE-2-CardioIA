import os
import math
import time

""" Caracteres ANSI para estilização no terminal """

# Exibe o texto que segue na cor indicada
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
VERMELHO = "\033[91m"

# Torna o texto negrito
NEGRITO = "\033[1m"

# Restaura o estilo padrão
RESET = "\033[0m"

""" Caracteres ANSI para manipulação de cursor e limpeza de linhas """

# Move o cursor uma linha para cima
CURSOR_UP = "\033[A"

# Limpa a linha inteira onde o cursor está
LIMPAR_LINHA = "\033[2K"

# Volta o cursor para o início da linha
INICIO_LINHA = "\r"


# Funções auxiliares


def limpar_tela():
    """Limpa a tela do terminal de forma multiplataforma"""
    os.system("clear" if os.name == "posix" else "cls")


def limpar_linhas(numero_linhas=1):
    """Limpa o conteúdo das linhas anteriores do terminal"""
    print(
        f"{CURSOR_UP}{LIMPAR_LINHA}{INICIO_LINHA}" * numero_linhas, end="", flush=True
    )


def ler_int(pergunta, minimo=None, maximo=None):
    """Lê um inteiro com validação simples"""

    # Guarda o número de linhas que o texto de pergunta tem
    num_linhas_pergunta = len(pergunta.splitlines())

    while True:
        try:
            valor = int(input(f"{AZUL}{pergunta}{RESET}"))
            if minimo is not None and valor < minimo:  # Se valor for menor que o mínimo
                print(f"{VERMELHO}✗ Digite um valor >= {minimo}{RESET}")
                # Aguarda 2 segundos
                time.sleep(2)
                # Limpa as linhas da pergunta e da mensagem
                limpar_linhas(num_linhas_pergunta + 1)

                continue  # Prossegue para perguntar novamente
            if maximo is not None and valor > maximo:  # Se valor for maior que o máximo
                print(f"{VERMELHO}✗ Digite um valor <= {maximo}{RESET}")
                # Aguarda 2 segundos
                time.sleep(2)
                # Limpa as linhas da pergunta e da mensagem
                limpar_linhas(num_linhas_pergunta + 1)

                continue  # Prossegue para perguntar novamente
            return valor
        except ValueError:
            print(f"{VERMELHO}✗ Entrada inválida. Digite um número inteiro.{RESET}")
            # Aguarda 2 segundos
            time.sleep(2)
            # Limpa as linhas da pergunta e da mensagem
            limpar_linhas(num_linhas_pergunta + 1)


def ler_float(pergunta, minimo=None):
    """Lê um float com validação simples"""

    # Guarda o número de linhas que o texto de pergunta tem
    num_linhas_pergunta = len(pergunta.splitlines())

    while True:
        try:
            valor = float(input(f"{AZUL}{pergunta}{RESET}").replace(",", "."))
            if minimo is not None and valor < minimo:  # Se valor for menor que o mínimo
                print(f"{VERMELHO}✗ Digite um valor >= {minimo}{RESET}")
                # Aguarda 2 segundos
                time.sleep(2)
                # Limpa as linhas da pergunta e da mensagem
                limpar_linhas(num_linhas_pergunta + 1)

                continue  # Prossegue para perguntar novamente
            return valor
        except ValueError:
            print(f"{VERMELHO}✗ Entrada inválida. Digite um número.{RESET}")
            # Aguarda 2 segundos
            time.sleep(2)
            # Limpa as linhas da pergunta e da mensagem
            limpar_linhas(num_linhas_pergunta + 1)


def atualiza_gastos(dados_cultura, preco, quantidade):
    """Atualiza os gastos com manejos agrícolas da cultura indicada"""
    dados_cultura["gastos"] += preco * quantidade * dados_cultura["area"]


def cria_cultura(peso, preco):
    """Estrutura de dados das culturas com insumos em vetor"""
    return {
        "area": 0,  # em ha
        "peso": 0,  # em kg
        "lucro": 0,  # em R$
        "gastos": 0,  # em R$
        # Vetor de insumos
        "insumos": [
            {"tipo": "herbicida", "nome": "", "qtd_por_ha": 0, "preco_unitario": 0},
            {"tipo": "pesticida", "nome": "", "qtd_por_ha": 0, "preco_unitario": 0},
            {"tipo": "fertilizante", "nome": "",
                "qtd_por_ha": 0, "preco_unitario": 0},
        ],
        "PESO_POR_HA": peso,
        "PRECO_POR_HA": preco,
    }


# Variáveis

PESO_SOJA = 3200  # kg/ha
PRECO_SOJA = 6300  # reais/ha

PESO_CAFE = 2300  # kg/ha
PRECO_CAFE = 72800  # reais/ha

# Vetor de culturas - cada elemento é uma cultura com seus dados
culturas = [
    {"nome": "Soja", "dados": cria_cultura(PESO_SOJA, PRECO_SOJA)},
    {"nome": "Café", "dados": cria_cultura(PESO_CAFE, PRECO_CAFE)},
]

meio_de_aplicacao = ""
gasto_total = 0  # em reais
area_total = 0  # em hectares


def listar_culturas():
    """Exibe lista de culturas com seus índices no vetor"""
    limpar_tela()
    print(f"{VERDE}{NEGRITO}=== CULTURAS CADASTRADAS ==={RESET}\n")

    for indice, cultura in enumerate(culturas):
        print(f"  [{indice}] {cultura['nome']}")

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def selecionar_cultura():
    """Retorna o índice da cultura selecionada no vetor"""
    limpar_tela()
    print(f"{VERDE}{NEGRITO}=== SELEÇÃO DE CULTURA ==={RESET}\n")

    for indice, cultura in enumerate(culturas):
        print(f"  [{indice + 1}] {cultura['nome']}")

    print("  [0] Voltar")

    indice = ler_int(f"\nEscolha a cultura: ", 0, len(culturas))

    return indice - 1


def calculo_area_total():
    """Soma as áreas de todas as culturas no vetor"""
    total = 0
    for cultura in culturas:
        total += cultura["dados"]["area"]
    return total


def calculo_gasto_total():
    """Soma os gastos de todas as culturas no vetor"""
    total = 0
    for cultura in culturas:
        total += cultura["dados"]["gastos"]
    return total


def esta_preenchida(indice_cultura):
    """Verifica se todos os dados da cultura estão preenchidos"""

    dados = culturas[indice_cultura]["dados"]
    return (
        dados["area"] != 0
        and dados["insumos"][0]["nome"] != ""
        and dados["insumos"][1]["nome"] != ""
        and dados["insumos"][2]["nome"] != ""
    )


def esta_vazia(indice_cultura):
    """Verifica se a cultura está vazia (sem dados cadastrados)"""

    dados = culturas[indice_cultura]["dados"]
    return (
        dados["area"] == 0
        and dados["insumos"][0]["nome"] == ""
        and dados["insumos"][1]["nome"] == ""
        and dados["insumos"][2]["nome"] == ""
    )


def financeiro(indice_cultura):
    """Exibe menu financeiro da cultura no índice indicado"""

    dados = culturas[indice_cultura]["dados"]
    nome_cultura = culturas[indice_cultura]["nome"]

    limpar_tela()

    print(f"{VERDE}{NEGRITO}=== FINANCEIRO - {nome_cultura.upper()} ==={RESET}")

    dados["area"] = calcular_area()
    dados["peso"] = dados["PESO_POR_HA"] * dados["area"]

    print(f"\n{AMARELO}Produção Estimada:{RESET}")
    print(f"  Peso total:  {dados['peso'] / 1000:.1f} tons")
    print(
        f"  Com perdas:  {dados['peso'] * 0.94 / 1000:.1f} tons (6% de perdas)")

    dados["lucro"] = dados["PRECO_POR_HA"] * dados["area"]

    print(f"\n{AMARELO}Receita Estimada:{RESET}")
    print(f"  Sem descontos: R$ {dados['lucro']:.2f}")
    print(f"  Com perdas:    R$ {dados['lucro'] * 0.94:.2f}")

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def herbicidas(indice_cultura):
    """Exibe menu de escolha de herbicida para a cultura no índice indicado"""

    nome_cultura = culturas[indice_cultura]["nome"]

    print(
        f"{VERDE}{NEGRITO}=== SELEÇÃO DE HERBICIDA - {nome_cultura.upper()} ==={RESET}\n"
    )

    if nome_cultura == "Soja":
        escolher_herbicida_soja(indice_cultura)
    else:  # Café
        escolher_herbicida_cafe(indice_cultura)

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def escolher_herbicida_soja(indice_cultura):
    """Exibe opções para a escolha de um herbicida para a cultura de Soja"""

    # Salva o dicionário da cultura numa variável local para referência simplificada
    dados = culturas[indice_cultura]["dados"]
    herbicida = dados["insumos"][0]

    tipo_grama = ler_int(
        "Problema com gramíneas:\n  [1] Curtas\n  [2] Longas\nOpção: ", 1, 2
    )

    if tipo_grama == 1:  # Se o problema for com gramíneas curtas
        periodo = ler_int(
            "Período de aplicação:\n  [1] Entre-safras\n  [2] Outono\nOpção: ", 1, 2
        )

        if periodo == 1:  # Se o período for entre-safras
            herbicida["nome"] = "Flumioxazin"
            herbicida["qtd_por_ha"] = 80  # gramas
            herbicida["preco_unitario"] = 3.0

            atualiza_gastos(dados, 3.0, 80)
        else:  # Se o período for outono
            herbicida["nome"] = "Diclosulam"
            herbicida["qtd_por_ha"] = 35  # gramas
            herbicida["preco_unitario"] = 1.2

            atualiza_gastos(dados, 1.2, 35)
    else:  # Se o problema for com gramíneas longas
        herbicida["nome"] = "Metsulfuron"
        herbicida["qtd_por_ha"] = 3.5
        herbicida["preco_unitario"] = 3.6

        atualiza_gastos(dados, 3.6, 3.5)

    print(
        f"{VERDE}✓ Herbicida selecionado para Soja: {herbicida['nome']}{RESET}")


def escolher_herbicida_cafe(indice_cultura):
    """Exibe opções para a escolha de um herbicida para a cultura de Café"""

    # Salva o dicionário da cultura numa variável local para referência simplificada
    dados = culturas[indice_cultura]["dados"]
    herbicida = dados["insumos"][0]

    tipo_praga = ler_int(
        "Problema com pragas:\n  [1] Bidens pilosa\n  [2] Digitaria insularis\nOpção: ",
        1,
        2,
    )

    if tipo_praga == 1:  # Se a praga for Bidens pilosa
        herbicida["nome"] = "Flumyzin"
        herbicida["qtd_por_ha"] = 150  # mililitros
        herbicida["preco_unitario"] = 0.5

        atualiza_gastos(dados, 0.5, 150)
    else:  # Se a praga for Digitaria insularis
        herbicida["nome"] = "Cletodim"
        herbicida["qtd_por_ha"] = 450  # mililitros
        herbicida["preco_unitario"] = 0.15

        atualiza_gastos(dados, 0.15, 450)

    print(
        f"{VERDE}✓ Herbicida selecionado para Café: {herbicida['nome']}{RESET}")


def pesticidas(indice_cultura):
    """Exibe menu de escolha de pesticida para a cultura no índice indicado"""

    nome_cultura = culturas[indice_cultura]["nome"]

    print(
        f"{VERDE}{NEGRITO}=== SELEÇÃO DE PESTICIDA - {nome_cultura.upper()} ==={RESET}\n"
    )

    if nome_cultura == "Soja":
        escolher_pesticida_soja(indice_cultura)
    else:  # Café
        escolher_pesticida_cafe(indice_cultura)

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def escolher_pesticida_soja(indice_cultura):
    """Exibe opções para a escolha de um pesticida para a cultura de Soja"""

    # Salva o dicionário da cultura numa variável local para referência simplificada
    dados = culturas[indice_cultura]["dados"]
    pesticida = dados["insumos"][1]

    problema = ler_int(
        "Tipo de praga:\n  [1] Insetos em vagens\n  [2] Insetos sugadores\nOpção: ",
        1,
        2,
    )

    if problema == 1:  # Se o problema for insetos em vagens
        pesticida["nome"] = "Lambda-cialotrina"
        pesticida["qtd_por_ha"] = 40  # mililitros
        pesticida["preco_unitario"] = 0.23

        atualiza_gastos(dados, 0.23, 40)
    else:  # Se o problema for insetos sugadores
        pesticida["nome"] = "Imidacloprido"
        pesticida["qtd_por_ha"] = 150  # mililitros
        pesticida["preco_unitario"] = 0.46

        atualiza_gastos(dados, 0.46, 150)

    print(
        f"{VERDE}✓ Pesticida selecionado para Soja: {pesticida['nome']}{RESET}")


def escolher_pesticida_cafe(indice_cultura):
    """Exibe opções para a escolha de um pesticida para a cultura de Café"""

    # Salva o dicionário da cultura numa variável local para referência simplificada
    dados = culturas[indice_cultura]["dados"]
    pesticida = dados["insumos"][1]

    problema = ler_int(
        "Tipo de praga:\n  [1] Bicho-mineiro\n  [2] Ferrugem\nOpção: ", 1, 2
    )

    if problema == 1:  # Se o problema for Bicho-mineiro
        pesticida["nome"] = "Abamectina"
        pesticida["qtd_por_ha"] = 270  # mililitros
        pesticida["preco_unitario"] = 0.03

        atualiza_gastos(dados, 0.03, 270)
    else:  # Se o problema for ferrugem
        pesticida["nome"] = "Epoxiconazol"
        pesticida["qtd_por_ha"] = 750  # mililitros
        pesticida["preco_unitario"] = 0.25

        atualiza_gastos(dados, 0.25, 750)

    print(
        f"{VERDE}✓ Pesticida selecionado para Café: {pesticida['nome']}{RESET}")


def fertilizantes(indice_cultura):
    """Exibe menu de escolha de fertilizante para a cultura no índice indicado"""

    nome_cultura = culturas[indice_cultura]["nome"]

    print(
        f"{VERDE}{NEGRITO}=== SELEÇÃO DE FERTILIZANTE - {nome_cultura.upper()} ==={RESET}\n"
    )

    if nome_cultura == "Soja":
        escolher_fertilizante_soja(indice_cultura)
    else:  # Café
        escolher_fertilizante_cafe(indice_cultura)

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def escolher_fertilizante_soja(indice_cultura):
    """Exibe opções para a escolha de um fertilizante para a cultura de Soja"""

    # Salva o dicionário da cultura numa variável local para referência simplificada
    dados = culturas[indice_cultura]["dados"]
    fertilizante = dados["insumos"][2]

    problema = ler_int(
        "Característica do solo:\n  [1] pH < 6\n  [2] Fixação biológica baixa\nOpção: ",
        1,
        2,
    )

    if problema == 1:  # Se o pH for baixo
        fertilizante["nome"] = "Calcário"
        fertilizante["qtd_por_ha"] = 3000  # kilogramas
        fertilizante["preco_unitario"] = 0.104

        atualiza_gastos(dados, 0.104, 3000)
    else:  # Se a fixação biológica for baixa
        fertilizante["nome"] = "Inoculantes Rhizobium"
        fertilizante["qtd_por_ha"] = 0.2  # kilogramas
        fertilizante["preco_unitario"] = 130

        atualiza_gastos(dados, 130, 0.2)

    print(
        f"{VERDE}✓ Fertilizante selecionado para Soja: {fertilizante['nome']}{RESET}")


def escolher_fertilizante_cafe(indice_cultura):
    """Exibe opções para a escolha de um fertilizante para a cultura de Café"""

    # Salva o dicionário da cultura numa variável local para referência simplificada
    dados = culturas[indice_cultura]["dados"]
    fertilizante = dados["insumos"][2]

    problema = ler_int(
        "Necessidade do solo:\n  [1] NPK\n  [2] Magnésio\nOpção: ", 1, 2)

    if problema == 1:  # Se a necessidade for NPK
        fertilizante["nome"] = "NPK"
        fertilizante["qtd_por_ha"] = 600  # kg
        fertilizante["preco_unitario"] = 8.0

        atualiza_gastos(dados, 8.0, 600)
    else:  # Se a necessidade for Magnésio
        fertilizante["nome"] = "Magnésio"
        fertilizante["qtd_por_ha"] = 80  # kg
        fertilizante["preco_unitario"] = 7.9

        atualiza_gastos(dados, 7.9, 80)

    print(
        f"{VERDE}✓ Fertilizante selecionado para Café: {fertilizante['nome']}{RESET}")


def perfil(indice_cultura):
    """Exibe as informações do perfil de cultivo do usuário"""

    # Salva o dicionário da cultura numa variável local para referência simplificada
    dados = culturas[indice_cultura]["dados"]
    nome_cultura = culturas[indice_cultura]["nome"]

    # Exibe uma sequência de 60 "=" na cor verde e em negrito
    print(f"{VERDE}{NEGRITO}{'=' * 60}{RESET}")
    print(
        f"{VERDE}{NEGRITO}{' ' * 18}PERFIL DE CULTIVO - {nome_cultura.upper()}{RESET}{VERDE}{NEGRITO}{RESET}"
    )
    print(f"{VERDE}{NEGRITO}{'=' * 60}{RESET}\n")

    print(f"{AMARELO}Agricultor:{RESET} {nome}")
    print(f"{AMARELO}Cultura:{RESET} {nome_cultura}")

    print(f"\n{NEGRITO}----- DADOS FINANCEIROS -----{RESET}")
    print(f"  Área cultivável:...{dados['area']:.2f} ha")
    print(f"  Peso total:........{dados['peso'] / 1000:.2f} ton")
    print(f"  Receita estimada:..R$ {dados['lucro']:.2f}")

    print(f"\n{NEGRITO}----- MANEJO DE INSUMOS -----{RESET}")
    print(f"  Herbicida:.........{dados['insumos'][0]['nome'].strip()}")
    print(
        f"  Quantidade:........{dados['insumos'][0]['qtd_por_ha'] * dados['area']:.1f} g/ha"
    )
    print(f"  Pesticida:.........{dados['insumos'][1]['nome'].strip()}")
    print(
        f"  Quantidade:........{dados['insumos'][1]['qtd_por_ha'] * dados['area']:.1f} ml/ha"
    )
    print(f"  Fertilizante:......{dados['insumos'][2]['nome'].strip()}")
    print(
        f"  Quantidade:........{dados['insumos'][2]['qtd_por_ha'] * dados['area']:.1f} kg/ha"
    )

    print(
        f"\n{VERMELHO}{NEGRITO}  GASTOS TOTAIS:   R$ {dados['gastos']:.2f}{RESET}")

    # Exibe uma sequência de 60 "=" na cor verde e em negrito
    print(f"\n{VERDE}{NEGRITO}{'=' * 60}{RESET}")

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def calcular_area():
    """Calcula a área de plantio baseada na forma escolhida"""

    print(f"\n{VERDE}{NEGRITO}=== CALCULADORA DE ÁREA ==={RESET}\n")

    while True:
        forma = ler_int(
            "Escolha a forma da área:\n  [1] Retângulo\n  [2] Triângulo\n  [3] Círculo\nOpção: ",
            1,
            3,
        )
        limpar_tela()

        if forma == 1:  # Se for retângulo
            largura = ler_float("Largura (hectares): ", 0.01)
            comprimento = ler_float("Comprimento (hectares): ", 0.01)
            area = largura * comprimento

            print(f"{VERDE}✓ Área retangular: {area:.2f} ha{RESET}")
            return area
        elif forma == 2:  # Se for triângulo
            base = ler_float("Base (hectares): ", 0.01)
            altura = ler_float("Altura (hectares): ", 0.01)
            area = (base * altura) / 2

            print(f"{VERDE}✓ Área triangular: {area:.2f} ha{RESET}")
            return area
        else:  # Se for círculo
            raio = ler_float("Raio (hectares): ", 0.01)
            area = math.pi * raio**2

            print(f"{VERDE}✓ Área circular: {area:.2f} ha{RESET}")
            return area


def atualizar_dados(indice_cultura):
    """Atualiza dados de um insumo (posição do vetor) da cultura indicada"""

    limpar_tela()

    dados = culturas[indice_cultura]["dados"]
    nome_cultura = culturas[indice_cultura]["nome"]

    print(
        f"{VERDE}{NEGRITO}=== ATUALIZAÇÃO DE DADOS - {nome_cultura.upper()} ==={RESET}\n"
    )

    opcao = ler_int(
        "Qual dado deseja atualizar?\n"
        "  [1] Área de plantio\n"
        "  [2] Herbicida\n"
        "  [3] Pesticida\n"
        "  [4] Fertilizante\n"
        "Opção: ",
        1,
        4,
    )

    limpar_tela()

    if opcao == 1:  # Atualizar área
        financeiro(indice_cultura)
    elif opcao == 2:  # Atualizar herbicida
        dados["gastos"] -= dados["insumos"][0]["preco_unitario"] * \
            dados["insumos"][0]["qtd_por_ha"] * dados["area"]

        herbicidas(indice_cultura)
    elif opcao == 3:  # Atualizar pesticida
        dados["gastos"] -= dados["insumos"][1]["preco_unitario"] * \
            dados["insumos"][1]["qtd_por_ha"] * dados["area"]
        pesticidas(indice_cultura)
    else:  # Atualizar fertilizante
        dados["gastos"] -= dados["insumos"][2]["preco_unitario"] * \
            dados["insumos"][2]["qtd_por_ha"] * dados["area"]

        fertilizantes(indice_cultura)

    print(f"\n{VERDE}✓ Dados atualizados com sucesso!{RESET}")
    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def deletar_dados(indice_cultura):
    """Deleta dados de uma posição específica (índice) do vetor de insumos"""

    limpar_tela()

    if esta_vazia(indice_cultura):
        print(f"{VERMELHO}✗ Sem dados disponíveis nesta cultura.{RESET}")
        input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")
        return

    dados = culturas[indice_cultura]["dados"]
    nome_cultura = culturas[indice_cultura]["nome"]

    print(f"{VERDE}{NEGRITO}=== DELEÇÃO DE DADOS - {nome_cultura.upper()} ==={RESET}\n")

    opcao = ler_int(
        "O que deseja deletar?\n"
        "  [1] Apenas um insumo\n"
        "  [2] Todos os dados da cultura\n"
        "Opção: ",
        1,
        2,
    )

    limpar_tela()

    if opcao == 1:  # Deletar um insumo específico por posição no vetor
        insumo_idx = ler_int(
            "Qual insumo deseja deletar?\n"
            "  [0] Herbicida\n"
            "  [1] Pesticida\n"
            "  [2] Fertilizante\n"
            "Opção: ",
            0,
            2,
        )

        limpar_tela()

        insumo = dados["insumos"][insumo_idx]

        if insumo["nome"] != "":
            dados["gastos"] -= (
                insumo["preco_unitario"] * insumo["qtd_por_ha"] * dados["area"]
            )

            # Resetar elemento do vetor na posição indicada
            dados["insumos"][insumo_idx] = {
                "tipo": insumo["tipo"],
                "nome": "",
                "qtd_por_ha": 0,
                "preco_unitario": 0,
            }

            print(
                f"{VERDE}✓ {insumo['tipo'].capitalize()} deletado com sucesso!{RESET}"
            )
        else:
            print(
                f"{AMARELO}⚠ Nenhum {insumo['tipo']} definido.{RESET}")

    else:  # Deletar todos os dados da cultura
        confirmacao = (
            input(
                f"{VERMELHO}Tem certeza que deseja deletar TODOS os dados de {nome_cultura}? (s/n): {RESET}"
            )
            .strip()
            .upper()
        )

        if confirmacao in ["SIM", "S"]:
            culturas[indice_cultura] = {
                "nome": nome_cultura,
                "dados": cria_cultura(
                    culturas[indice_cultura]["dados"]["PESO_POR_HA"],
                    culturas[indice_cultura]["dados"]["PRECO_POR_HA"],
                ),
            }
            print(
                f"{VERDE}✓ Todos os dados de {nome_cultura} foram deletados!{RESET}")
        else:
            print(f"{AMARELO}○ Operação cancelada{RESET}")

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def exibir_dados(indice_cultura):
    """Exibe os dados da cultura no índice indicado"""

    limpar_tela()

    dados = culturas[indice_cultura]["dados"]
    nome_cultura = culturas[indice_cultura]["nome"]

    print(f"{VERDE}{NEGRITO}=== SAÍDA DE DADOS - {nome_cultura.upper()} ==={RESET}\n")

    if not esta_preenchida(indice_cultura):
        print(
            f"{AMARELO}⚠ Alguns dados da cultura ainda não foram preenchidos.{RESET}\n"
        )

    print(f"{NEGRITO}Dados financeiros:{RESET}")
    print(f"  Área: {dados['area']:.2f} ha")
    print(f"  Peso estimado: {dados['peso'] / 1000:.2f} ton")
    print(f"  Lucro: R$ {dados['lucro']:.2f}")
    print(f"  Gastos com insumos: R$ {dados['gastos']:.2f}\n")

    print(f"{NEGRITO}Insumos utilizados:{RESET}")
    for insumo in dados["insumos"]:
        nome = insumo["nome"].strip() if insumo["nome"] else "(não definido)"
        print(f"  {insumo['tipo'].title()}: {nome}")

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")


def entrada_dados():
    """Menu para entrada de dados das culturas"""

    while True:
        indice = selecionar_cultura()

        if indice >= 0 and indice < len(culturas):
            limpar_tela()
            menu(indice)
        else:
            break


def saida_dados():
    """Menu para saída de dados das culturas"""

    while True:
        limpar_tela()

        print(f"{VERDE}{NEGRITO}=== SAÍDA DE DADOS ==={RESET}\n")

        opcao = ler_int(
            "Escolha a operação:\n"
            "  [1] Exibir uma cultura específica\n"
            "  [2] Listar todas as culturas\n"
            "  [0] Voltar ao menu principal\n"
            "Opção: ",
            0,
            2,
        )

        if opcao == 0:
            break
        elif opcao == 1:
            indice = selecionar_cultura()

            if indice < 0:  # Se o usuário escolheu "Voltar"
                continue

            if esta_vazia(indice):  # Se a cultura escolhida estiver vazia
                limpar_tela()
                print(f"{VERMELHO}✗ Cultura não cadastrada!{RESET}")
                input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")
            else:
                exibir_dados(indice)
        else:
            limpar_tela()
            print(f"{VERDE}{NEGRITO}=== CULTURAS CADASTRADAS ==={RESET}\n")
            cultura_exibida = False
            for indice, cultura in enumerate(culturas):
                if not esta_vazia(indice):
                    print(f"  [{indice}] {cultura['nome']}")
                    cultura_exibida = True
            if not cultura_exibida:
                print(f"{AMARELO}Nenhuma cultura cadastrada.{RESET}")
            input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")

            for indice in range(len(culturas)):
                if not esta_vazia(indice):
                    exibir_dados(indice)


def atualizacao_dados():
    """Menu para atualização de dados das culturas"""

    while True:
        indice = selecionar_cultura()

        if indice < 0:  # Se o usuário escolheu "Voltar"
            break

        if esta_vazia(indice):
            limpar_tela()
            print(f"{VERMELHO}✗ Nenhum dado disponível para atualização{RESET}")
            input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")
        else:
            atualizar_dados(indice)


def delecao_dados():
    """Menu para deleção de dados das culturas"""

    while True:
        indice = selecionar_cultura()

        if indice >= 0 and indice < len(culturas):
            deletar_dados(indice)
        else:
            break


def menu(indice_cultura):
    """Exibe o menu principal para o preenchimento dos dados da cultura no índice indicado"""

    while True:
        limpar_tela()

        nome_cultura = culturas[indice_cultura]["nome"]

        print(f"{VERDE}{NEGRITO}=== MENU PRINCIPAL - {nome_cultura.upper()} ==={RESET}")

        completo = esta_preenchida(indice_cultura)

        status = (
            f"{VERDE}✓ Completo{RESET}" if completo else f"{AMARELO}○ Incompleto{RESET}"
        )
        opcao_extra = "  [0] Voltar\n" if completo else ""

        print(f"Status: {status}\n")

        opcao = ler_int(
            "Escolha uma opção:\n"
            "  [1] Financeiro\n"
            "  [2] Herbicida\n"
            "  [3] Pesticida\n"
            "  [4] Fertilizante\n"
            "  [5] Perfil\n" + opcao_extra + "Opção: "
        )

        if opcao == 1:
            limpar_tela()
            financeiro(indice_cultura)
        elif opcao == 2:
            limpar_tela()
            herbicidas(indice_cultura)
        elif opcao == 3:
            limpar_tela()
            pesticidas(indice_cultura)
        elif opcao == 4:
            limpar_tela()
            fertilizantes(indice_cultura)
        elif opcao == 5:
            limpar_tela()
            perfil(indice_cultura)
        elif opcao == 0 and completo:
            break
        else:
            print(f"{VERMELHO}Opção inválida.{RESET}")
            time.sleep(2)


def aplicacao():
    """Exibe menu de escolha do meio de aplicação das culturas"""

    global gasto_total
    global area_total
    global meio_de_aplicacao

    limpar_tela()
    print(f"{VERDE}{NEGRITO}=== SELEÇÃO DE MEIO DE APLICAÇÃO ==={RESET}\n")

    meio = ler_int(
        "Escolha o meio de aplicação:\n"
        "  [1] Pulverizador tratorizado (R$ 225.000)\n"
        "  [2] Drone agrícola (R$ 15.000)\n"
        "Opção: ",
        1,
        2,
    )
    limpar_tela()

    if meio == 1:  # Se o meio for Pulverizador tratorizado
        print(f"{AMARELO}Calculando redução da área para trator...{RESET}\n")

        area_trator = area_total * 0.12
        area_total_final = area_total - area_trator

        print(f"  Área inicial:       {area_total:.2f} ha")
        print(f"  Espaço p/ trator:   {area_trator:.2f} ha (12%)")
        print(f"  Área final útil:    {area_total_final:.2f} ha")
        print(f"  Custo:              R$ 225.000,00")

        meio_de_aplicacao = "Pulverizador Tratorizado"
        area_total = area_total_final
        gasto_total += 225000

        print(f"\n{VERDE}✓ Método selecionado: {meio_de_aplicacao}{RESET}")
    else:  # Se o meio for Drone agrícola
        print(f"  Área utilizada:     {area_total:.2f} ha")
        print(f"  Custo:              R$ 15.000,00")

        meio_de_aplicacao = "Drone Agrícola"
        gasto_total += 15000

        print(f"\n{VERDE}✓ Método selecionado: {meio_de_aplicacao}{RESET}")

    input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")
    limpar_tela()


def resumo_final():
    """Exibe resumo final com todos os dados"""

    limpar_tela()

    print(f"{VERDE}{NEGRITO}{'=' * 60}{RESET}")
    print(
        f"{VERDE}{NEGRITO}{' ' * 18}RESUMO FINAL DO PROJETO{RESET}{VERDE}{NEGRITO}{RESET}"
    )
    print(f"{VERDE}{NEGRITO}{'=' * 60}{RESET}\n")

    print(f"{AMARELO}Agricultor:{RESET} {nome}\n")

    for indice, cultura in enumerate(culturas):
        dados = cultura["dados"]
        print(f"{NEGRITO}--- {cultura['nome'].upper()} ---{RESET}")
        print(f"  Área:           {dados['area']:.2f} ha")
        print(f"  Produção:       {dados['peso'] / 1000:.2f} ton")
        print(f"  Receita:        R$ {dados['lucro']:.2f}")
        print(f"  Gastos insumos: R$ {dados['gastos']:.2f}\n")

    print(f"{NEGRITO}=== TOTAIS ==={RESET}")
    print(f"  Área total:     {area_total:.2f} ha")
    print(f"  Gastos totais:  R$ {gasto_total:.2f}")
    print(f"  Aplicação:      {meio_de_aplicacao}")

    print(f"\n{VERDE}{NEGRITO}{'=' * 70}{RESET}")
    input(f"\n{AZUL}[Pressione ENTER para finalizar]{RESET}")


def menu_principal():
    """Exibe o menu principal com as operações flexível de CRUD"""

    global area_total
    global gasto_total
    global meio_de_aplicacao

    while True:
        limpar_tela()

        print(f"{VERDE}{NEGRITO}=== MENU PRINCIPAL - FARMTECH SOLUTIONS ==={RESET}\n")
        print(f"{AMARELO}Agricultor: {nome}{RESET}\n")

        opcao = ler_int(
            "Escolha uma operação:\n"
            "  [1] Entrada de dados\n"
            "  [2] Saída de dados\n"
            "  [3] Atualização de dados\n"
            "  [4] Deleção de dados\n"
            "  [5] Gerar resumo final\n"
            "  [0] Sair do programa\n"
            "Opção: ",
            0,
            5,
        )

        if opcao == 1:
            entrada_dados()
        elif opcao == 2:
            saida_dados()
        elif opcao == 3:
            atualizacao_dados()
        elif opcao == 4:
            delecao_dados()
        elif opcao == 5:
            area_total = calculo_area_total()
            gasto_total = calculo_gasto_total()

            culturas_preenchidas = [i for i in range(
                len(culturas)) if esta_preenchida(i)]

            if len(culturas_preenchidas) != len(culturas):
                limpar_tela()
                print(
                    f"{VERMELHO}✗ Erro: Todas as culturas precisam estar {NEGRITO}completamente{RESET}{VERMELHO} preenchidas.{RESET}")
                input(f"\n{AZUL}[Pressione ENTER para continuar]{RESET}")
            else:
                aplicacao()
                resumo_final()
        else:  # Sair
            limpar_tela()
            print(f"\n{VERDE}Obrigado por usar FarmTech Solutions!{RESET}\n")
            break


if __name__ == "__main__":
    nome = ""
    while nome.strip() == "":
        limpar_tela()

        print(f"{VERDE}{NEGRITO}=== BEM-VINDO À FARMTECH SOLUTIONS ==={RESET}\n")

        nome = input(f"Digite seu nome: ").strip().title()

    menu_principal()
