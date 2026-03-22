from rpy2 import robjects
import json
import pandas as pd

cidade = "Campinas"
data_inicio = "2026-03-11"
data_fim = "2026-03-14"

robjects.globalenv["cidade"] = cidade
robjects.globalenv["data_inicio"] = data_inicio
robjects.globalenv["data_fim"] = data_fim

codigo_r = """
library(httr2)
library(jsonlite)

resp_geo <- request("https://geocoding-api.open-meteo.com/v1/search") |>
  req_url_query(
    name = cidade,
    count = 1,
    language = "pt",
    format = "json"
  ) |>
  req_perform()

geo <- resp_body_json(resp_geo)

if (is.null(geo$results) || length(geo$results) == 0) {
  stop("Cidade não encontrada.")
}

lat <- geo$results[[1]]$latitude
lon <- geo$results[[1]]$longitude
nome_cidade <- geo$results[[1]]$name

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

datas <- unlist(weather$daily$time, use.names = FALSE)
temp_max <- as.numeric(unlist(weather$daily$temperature_2m_max, use.names = FALSE))
temp_min <- as.numeric(unlist(weather$daily$temperature_2m_min, use.names = FALSE))
chuva_mm <- as.numeric(unlist(weather$daily$precipitation_sum, use.names = FALSE))
prob_chuva <- as.numeric(unlist(weather$daily$precipitation_probability_max, use.names = FALSE))

resultado <- data.frame(
  cidade = rep(nome_cidade, length(datas)),
  data = datas,
  temp_max = temp_max,
  temp_min = temp_min,
  chuva_mm = chuva_mm,
  prob_chuva = prob_chuva,
  stringsAsFactors = FALSE
)

jsonlite::toJSON(resultado, dataframe = "rows", auto_unbox = TRUE)
"""

json_resultado = str(robjects.r(codigo_r)[0])
dados = json.loads(json_resultado)
df = pd.DataFrame(dados)

print(df)
print(df.columns.tolist())

df.to_csv("previsao_clima_corrigida.csv", index=False, encoding="utf-8-sig")
print("\nArquivo salvo com sucesso: previsao_clima_corrigida.csv")