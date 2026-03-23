# Instalçao dos pacotes
if (!require("httr")) install.packages("httr")
if (!require("jsonlite")) install.packages("jsonlite")
if (!require("rlang")) install.packages("rlang")

install.packages("jsonlite")
install.packages("rlang")
install.packages("httr")


#Definição das Coordenadas para São Paulo
latitude <- -23.5505
longitude <- -46.6333

# URL do endpoint da API OpenMeteo
url <- "https://api.open-meteo.com/v1/forecast"

# Parâmetros da consulta:
# - 'hourly' define quais variáveis horárias: "temperature_2m"
# - 'current_weather' solicita os dados do tempo atual
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
  cat("Data/Hora: ", data_json$current_weather$time, "\n")
  cat("Temperatura: ", data_json$current_weather$temperature, "°C\n\n")
  
  # Exibe as previsões horárias de temperatura
  cat("== Previsão Horária de Temperatura ==\n")
  times <- data_json$hourly$time
  temps <- data_json$hourly$temperature_2m
  
  # Exibe as primeiras 2 previsões (você pode ajustar conforme necessário)
  for(i in seq_len(min(2, length(times)))) {
    cat(sprintf("%s : %.1f °C\n", times[i], temps[i]))
  }
  
} else {
  cat("Falha na requisição. Código de status:", status_code(response), "\n")
}