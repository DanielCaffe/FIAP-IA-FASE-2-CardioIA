library(httr2)
library(jsonlite)

# 1) Entradas
cidade <- "Campinas"
data_inicio <- "2026-03-11"
data_fim <- "2026-03-14"

# 2) Buscar coordenadas da cidade
resp_geo <- request("https://geocoding-api.open-meteo.com/v1/search") |>
  req_url_query(
    name = cidade,
    count = 1,
    language = "pt",
    format = "json"
  ) |>
  req_perform()

geo <- resp_body_json(resp_geo)

# 3) Validar retorno
if (is.null(geo$results) || length(geo$results) == 0) {
  stop("Cidade não encontrada.")
}

lat <- geo$results[[1]]$latitude
lon <- geo$results[[1]]$longitude
nome_cidade <- geo$results[[1]]$name

# 4) Consultar previsão do tempo
resp_weather <- request("https://api.open-meteo.com/v1/forecast") |>
  req_url_query(
    latitude = lat,
    longitude = lon,
    daily = "temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max",
    start_date = data_inicio,
    end_date = data_fim,
    timezone = "America/Sao_Paulo"
  ) |>
  req_perform()

weather <- resp_body_json(resp_weather)

# 5) Transformar em vetores simples
datas <- unlist(weather$daily$time, use.names = FALSE)
temp_max <- as.numeric(unlist(weather$daily$temperature_2m_max, use.names = FALSE))
temp_min <- as.numeric(unlist(weather$daily$temperature_2m_min, use.names = FALSE))
chuva_mm <- as.numeric(unlist(weather$daily$precipitation_sum, use.names = FALSE))
prob_chuva <- as.numeric(unlist(weather$daily$precipitation_probability_max, use.names = FALSE))

# 6) Exibir no terminal em texto simples
cat("=== PREVISÃO DO TEMPO ===\n")
cat("Cidade:", nome_cidade, "\n")
cat("Período:", data_inicio, "até", data_fim, "\n\n")

for (i in seq_along(datas)) {
  cat(
    "Data:", datas[i],
    "| Temp. Máx:", temp_max[i], "°C",
    "| Temp. Mín:", temp_min[i], "°C",
    "| Chuva:", chuva_mm[i], "mm",
    "| Prob. de chuva:", prob_chuva[i], "%\n"
  )
}