# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Startup FarmTech Solutions

## Grupo H.M.N.R.V.

## 👨‍🎓 Integrantes: 
- <a href="https://github.com/NeuralXP">Heitor Exposito de Sousa</a>
- <a href="https://github.com/MarcoR-S">Marco Antônio Rodrigues Siqueira</a>
- <a href="https://github.com/nadnakvie">Nádia Nakamura Vieira</a> 
- <a href="https://github.com/optimizasavings-byte">Rafael Bassani</a> 
- <a href="https://github.com/ViniciusX22">Vinicius Xavier da Silva</a>

## 📜 Descrição

Aplicação CLI Python para gestão de culturas agrícolas com foco em soja e café. O sistema permite definir cultura, calcular área (retângulo/triângulo/círculo), estimar insumos (adubo, água, fosfato) e configurar produtos de manejo (herbicida/pesticida/fertilizante), além de calcular resultados financeiros (lucro/gastos).

A estrutura foi refatorada para uso de dados organizados em objetos com persistência intermediária por CSV (`dados_plantio.csv`) para análise adicional em R via scripts `estatisticas_basicas.r` e `previsao_do_tempo.r`.

A interface oferece menu interativo no terminal com cores ANSI, validação de entrada segura e opções de CRUD de dados. A execução produz relatórios de custos, previsão meteorológica e gráficos simples via R.

## 🔧 Como executar o código

`cd nome-diretorio-arquivo\nome-arquivo`
`python menu_principal.py`

Requisitos: Python 3.8+, pandas, R instalado com `Rscript` no PATH.


## 🗃 Histórico de lançamentos

* 0.3.0 - 22/03/2026
* 0.2.0 - 12/03/2026
* 0.1.0 - 07/03/2026

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>


