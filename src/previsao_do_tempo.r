# Instalação de pacotes necessários
if (!require("httr")) install.packages("httr", repos="http://cran.r-project.org", quiet=TRUE)
if (!require("jsonlite")) install.packages("jsonlite", repos="http://cran.r-project.org", quiet=TRUE)
if (!require("rlang")) install.packages("rlang", repos="http://cran.r-project.org", quiet=TRUE)

library(httr)
library(jsonlite)
library(rlang)

# Obter argumentos da linha de comando
args <- commandArgs(trailingOnly = TRUE)

# Mapa de cidades para coordenadas
cidades_coords <- list(
  "sao paulo" = list(lat = -23.5505, lon = -46.6333),
  "são paulo" = list(lat = -23.5505, lon = -46.6333),
  "rio de janeiro" = list(lat = -22.9068, lon = -43.1729),
  "belo horizonte" = list(lat = -19.9191, lon = -43.9386),
  "brasilia" = list(lat = -15.7942, lon = -47.8822),
  "curitiba" = list(lat = -25.4284, lon = -49.2733),
  "salvador" = list(lat = -12.9714, lon = -38.5014),
  "fortaleza" = list(lat = -3.7319, lon = -38.5267),
  "manaus" = list(lat = -3.1190, lon = -60.0217),
  "recife" = list(lat = -8.0476, lon = -34.8770)
)

# Usar cidade do argumento ou padrão
if (length(args) > 0) {
  cidade_entrada <- tolower(args[1])
} else {
  cidade_entrada <- "sao paulo"
}

# Obter coordenadas
coords <- cidades_coords[[cidade_entrada]]
if (is.null(coords)) {
  cat("Cidade não encontrada. Usando São Paulo.\n")
  coords <- cidades_coords[["sao paulo"]]
}

latitude <- coords$lat
longitude <- coords$lon

# URL do endpoint da API OpenMeteo
url <- "https://api.open-meteo.com/v1/forecast"

# Parâmetros da consulta
params <- list(
  latitude = latitude,
  longitude = longitude,
  hourly = "temperature_2m",
  current_weather = "true"
)

# Realiza a requisição GET
response <- GET(url, query = params)

# Verifica se a requisição foi bem-sucedida
if (status_code(response) == 200) {
  # Converte a resposta JSON para uma lista R
  data_text <- content(response, as = "text", encoding = "UTF-8")
  data_json <- fromJSON(data_text, flatten = TRUE)
  
  # Extrai e exibe o clima atual
  cat("== Clima Atual ==\n")
  cat("Cidade: ", gsub("_", " ", tolower(cidade_entrada)), "\n")
  cat("Data/Hora: ", data_json$current_weather$time, "\n")
  cat("Temperatura: ", data_json$current_weather$temperature, "°C\n")
  cat("Velocidade do vento: ", data_json$current_weather$windspeed, " km/h\n\n")
  
  # Exibe as previsões horárias de temperatura
  cat("== Proximas Previsoes Horarias ==\n")
  times <- data_json$hourly$time[1:5]
  temps <- data_json$hourly$temperature_2m[1:5]
  
  for(i in seq_len(length(times))) {
    cat(sprintf("%s : %.1f °C\n", times[i], temps[i]))
  }
  
} else {
  cat("Falha na requisição. Código de status:", status_code(response), "\n")
}