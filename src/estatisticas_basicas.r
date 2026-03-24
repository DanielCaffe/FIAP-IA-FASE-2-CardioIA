# Definir biblioteca pessoal para instalação de pacotes
if (!dir.exists(Sys.getenv("R_LIBS_USER"))) {
  dir.create(Sys.getenv("R_LIBS_USER"), recursive = TRUE)
}
.libPaths(c(Sys.getenv("R_LIBS_USER"), .libPaths()))

# Carregar pacotes necessários (se ainda não estiverem instalados)
if (!require("dplyr")) install.packages("dplyr")
library(dplyr)

# Leitura dos dados
# O CSV deve ter colunas: cultura, area, tipo_insumo, qnt_insumo
args <- commandArgs(trailingOnly = FALSE)
script_path <- grep("^--file=", args, value = TRUE)
if (length(script_path) == 0) {
  script_dir <- getwd()
} else {
  script_dir <- dirname(sub("^--file=", "", script_path))
}
dados <- read.csv(file.path(script_dir, "..", "dados_plantio.csv"), stringsAsFactors = FALSE)

# Visualizar os dados
print("Dados de plantio:")
print(dados)

# Cálculo de estatísticas básicas para a área plantada e quantidade de insumos
# Estatísticas gerais:
media_area <- mean(dados$area, na.rm = TRUE)
desvio_area <- sd(dados$area, na.rm = TRUE)

media_qnt_insumo <- mean(dados$qnt_insumo, na.rm = TRUE)
desvio_qnt_insumo <- sd(dados$qnt_insumo, na.rm = TRUE)

cat("== Estatísticas Gerais ==\n")
cat("Média da área plantada:", round(media_area, 2), "m²\n")
cat("Desvio padrão da área plantada:", round(desvio_area, 2), "m²\n\n")
cat("Média da quantidade de insumos:", round(media_qnt_insumo, 2), "\n")
cat("Desvio padrão da quantidade de insumos:", round(desvio_qnt_insumo, 2), "\n\n")

# Caso queira ver as estatísticas separadas por cultura (Milho e Soja)
estatisticas_por_cultura <- dados %>%
  group_by(cultura) %>%
  summarise(
    media_area = mean(area, na.rm = TRUE),
    desvio_area = sd(area, na.rm = TRUE),
    media_qnt_insumo = mean(qnt_insumo, na.rm = TRUE),
    desvio_qnt_insumo = sd(qnt_insumo, na.rm = TRUE)
  )

cat("== Estatísticas por Cultura ==\n")
print(estatisticas_por_cultura)