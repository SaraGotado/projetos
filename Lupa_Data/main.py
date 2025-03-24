import os
import pandas as pd
# importa caminhos das pastas
from paths import PATHS

# configuracao no pandas para exibir apenas 4 casas decimais e remover a notacao cientifica
pd.set_option('display.float_format', '{:.4f}'.format)

# cria os diretorios caso nao existam
os.makedirs(PATHS["destino_parquet"], exist_ok=True)
os.makedirs(PATHS["destino_csv"], exist_ok=True)

# le o arquivo csv
df = pd.read_csv(PATHS["csv_path"], encoding="utf-8")

# dataframe para armazenar dados invalidos
df_invalidos = pd.DataFrame()

# conversao da coluna de data
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%Y", errors='coerce')

# captura linhas com datas invalidas (nat e que nao possuirem datas)
datas_invalidas = df[df["Date"].isna()]
df_invalidos = pd.concat([df_invalidos, datas_invalidas])
df = df.dropna(subset=["Date"])

# remove datas fora do intervalo desejado
invalid_date_range = df[(df["Date"] >= "2025-01-01") | (df["Date"] <= "1900-01-01")]
df_invalidos = pd.concat([df_invalidos, invalid_date_range])
df = df[(df["Date"] < "2025-01-01") & (df["Date"] > "1900-01-01")]

# extrai ano da data
df["Year"] = df["Date"].dt.year

# de para: normalizacao dos nomes das regioes
mapeamento_regioes = {
    "Euro": "Europa",
    "Europa": "Europa",
    "Ocean": "Oceania",
    "Oceania": "Oceania",
    "Asia": "Asia",
    "ASia": "Asia",
    "ASIA": "Asia",
    "Asia": "Asia",
    "Americas": "Americas",
    "America": "Americas",
    "Americas": "Americas",
    "americ": "Americas",
    "americas": "Americas",
    "america": "Americas",
    "Africa": "Africa",
    "frica": "Africa"
}

df["Region"] = df["Region"].replace(mapeamento_regioes)

# funcao para criar um dicionario e mapear paises as suas regioes
pais_regiao = df.dropna(subset=["Region"]).drop_duplicates(subset=["Country"])[["Country", "Region"]]
pais_regiao_dict = dict(zip(pais_regiao["Country"], pais_regiao["Region"]))

# preenche os valores faltantes na coluna "region" usando o dicionario
df["Region"] = df["Country"].map(pais_regiao_dict).combine_first(df["Region"])

# captura linhas com regioes ainda faltantes
regioes_faltantes = df[df["Region"].isna()]
df_invalidos = pd.concat([df_invalidos, regioes_faltantes])
df = df.dropna(subset=["Region"])

# substitui valores nulos em "paises"  por "outros" (fiz essa funcao para aprimorar a precisao dos dados por regiao)
df["Country"] = df["Country"].fillna("Outros")

# substitui valores nulos em "kilotons of co2" e "metric tons per capita" por 0
df["Kilotons of Co2"] = df["Kilotons of Co2"].fillna(0)
df["Metric Tons Per Capita"] = df["Metric Tons Per Capita"].fillna(0)

# verificacao de valores negativos
valores_negativos = df[(df["Kilotons of Co2"] < 0) | (df["Metric Tons Per Capita"] < 0)]
df_invalidos = pd.concat([df_invalidos, valores_negativos])
df = df[(df["Kilotons of Co2"] >= 0) & (df["Metric Tons Per Capita"] >= 0)]

# remove dados duplicados
duplicados = df[df.duplicated()]
df_invalidos = pd.concat([df_invalidos, duplicados])
df = df.drop_duplicates()

# conversao de tipos dados de kilots e metrics para numerico
df["Kilotons of Co2"] = pd.to_numeric(df["Kilotons of Co2"], errors='coerce')
df["Metric Tons Per Capita"] = pd.to_numeric(df["Metric Tons Per Capita"], errors='coerce')

# verifica novamente se tem dados invalidos apos a conversao
conversao_invalida = df[df[["Kilotons of Co2", "Metric Tons Per Capita"]].isna().any(axis=1)]
df_invalidos = pd.concat([df_invalidos, conversao_invalida])
df = df.dropna(subset=["Kilotons of Co2", "Metric Tons Per Capita"])

# converte a coluna date para o formato dd-mm-yyyy como string
df["Date"] = df["Date"].dt.strftime("%d-%m-%Y")

# salva dados tratados no formato parquet
df.to_parquet(os.path.join(PATHS["destino_parquet"], "Emissao_CO2_validos.parquet"), index=False, engine="pyarrow")

# salva dados invalidos no formato csv
df_invalidos.to_csv(os.path.join(PATHS["destino_csv"], "erros.csv"), index=False, encoding="utf-8", sep=";")

print("arquivos tratados e salvos com sucesso!")