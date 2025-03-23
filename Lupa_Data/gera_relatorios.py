import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from paths import PATHS  # importa caminhos das pastas

# funcao para ocultar avisos do seaborn
warnings.filterwarnings("ignore", category=FutureWarning)

# define estilo dos graficos
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# verifica se existe a pasta de destino para graficos, caso nao ele cria
os.makedirs(PATHS["destino_graficos"], exist_ok=True)

# carrega o arquivo parquet que foi tratado no codigo anterior
df = pd.read_parquet(os.path.join(PATHS["origem_parquet"], "Emissao_CO2_validos.parquet"))

# funcao para salvar graficos
def salvar_grafico(df, x, y, titulo, nome_arquivo, tipo_grafico="bar", hue=None):
    plt.figure()
    if tipo_grafico == "bar":
        ax = sns.barplot(data=df, x=x, y=y, hue=hue, palette="viridis", legend=False)

        # adiciona os valores dentro das barras
        for p in ax.patches:
            ax.text(
                p.get_x() + p.get_width() / 2.,  # posicao horizontal (centro da barra)
                p.get_height() / 2,  # posicao vertical (metade da altura da barra)
                f"{p.get_height():.2f}",  # valor formatado com 2 casas decimais
                ha="center",  # alinhamento horizontal
                va="center",  # alinhamento vertical
                color="white",  # cor do texto
                fontsize=10  # tamanho da fonte
            )
    elif tipo_grafico == "line":
        ax = sns.lineplot(data=df, x=x, y=y, hue=hue, marker="o")
    elif tipo_grafico == "heatmap":
        sns.heatmap(df, cmap="viridis", annot=True, fmt=".1f")

    plt.title(titulo.replace("CO₂", "CO2"))  # substitui "CO₂" por "CO2" pois estava retornando erro
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(PATHS["destino_graficos"], nome_arquivo))
    plt.close()

# 1. evolucao das emissoes de CO₂ ao longo dos anos (top 10 anos com maior emissao)
anos_maiores_emissao = df.groupby("Year", as_index=False)["Kilotons of Co2"].sum()
anos_maiores_emissao = anos_maiores_emissao.sort_values(by="Kilotons of Co2", ascending=False).head(10)
salvar_grafico(anos_maiores_emissao, x="Year", y="Kilotons of Co2",
               titulo="Top 10 Anos com Maior Emissão de CO₂",
               nome_arquivo="anos_maiores_emissao.png", tipo_grafico="line")

# 2. media de emissoes de CO₂ por regiao (regioes com maior emissao)
media_regiao_co2 = df.groupby("Region", as_index=False)["Kilotons of Co2"].sum()
media_regiao_co2 = media_regiao_co2.sort_values(by="Kilotons of Co2", ascending=False).head(10)
salvar_grafico(media_regiao_co2, x="Region", y="Kilotons of Co2",
               titulo="Emissão de CO₂ por Região",
               nome_arquivo="emissao_por_regiao_co2.png", tipo_grafico="bar")

# 3. ranking dos paises com maior emissao de CO₂ (top 10 paises)
ranking_paises_co2 = df.groupby("Country", as_index=False)["Kilotons of Co2"].sum()
ranking_paises_co2 = ranking_paises_co2.sort_values(by="Kilotons of Co2", ascending=False).head(10)
salvar_grafico(ranking_paises_co2, x="Country", y="Kilotons of Co2",
               titulo="Top 10 Países com Maior Emissão de CO₂",
               nome_arquivo="ranking_paises_maiores_co2.png", tipo_grafico="bar")

# 4. media de emissao de CO₂ per capita por regiao
media_per_capita_co2 = df.groupby("Region", as_index=False)["Metric Tons Per Capita"].mean()
media_per_capita_co2 = media_per_capita_co2.sort_values(by="Metric Tons Per Capita", ascending=False).head(10)
salvar_grafico(media_per_capita_co2, x="Region", y="Metric Tons Per Capita",
               titulo="Emissão de CO₂ Per Capita por Região",
               nome_arquivo="media_per_capita_co2.png", tipo_grafico="bar")

# 5. ranking dos paises com menores emissoes de CO₂ (top 10 paises com menores emissoes)
ranking_paises_menores_co2 = df.groupby("Country", as_index=False)["Kilotons of Co2"].sum()
ranking_paises_menores_co2 = ranking_paises_menores_co2.sort_values(by="Kilotons of Co2", ascending=True).head(10)
salvar_grafico(ranking_paises_menores_co2, x="Country", y="Kilotons of Co2",
               titulo="Top 10 Países com Menores Emissões de CO₂",
               nome_arquivo="ranking_paises_menores_co2.png", tipo_grafico="bar")

# 6. anos com menores emissoes de CO₂ (top 10 anos com menor emissao)
anos_menores_emissao = df.groupby("Year", as_index=False)["Kilotons of Co2"].sum()
anos_menores_emissao = anos_menores_emissao.sort_values(by="Kilotons of Co2", ascending=True).head(10)
salvar_grafico(anos_menores_emissao, x="Year", y="Kilotons of Co2",
               titulo="Top 10 Anos com Menores Emissões de CO₂",
               nome_arquivo="anos_menores_emissao.png", tipo_grafico="line")

# 7. emissoes de CO₂ por ano e regiao
emissao_por_ano_regiao = df.groupby(["Year", "Region"], as_index=False)["Kilotons of Co2"].sum()
salvar_grafico(emissao_por_ano_regiao, x="Year", y="Kilotons of Co2", hue="Region",
               titulo="Emissões de CO₂ por Ano e Região",
               nome_arquivo="emissao_por_ano_regiao.png", tipo_grafico="line")

# 8. emissoes de CO₂ por regiao e ano (heatmap)
emissao_heatmap = df.pivot_table(index="Region", columns="Year", values="Kilotons of Co2", aggfunc="sum")
plt.figure(figsize=(12, 8))
sns.heatmap(emissao_heatmap, cmap="viridis", annot=False)  # se for annot=True mostra valores
plt.title("Emissões de CO2 por Região e Ano")  # substitui "CO₂" por "CO2"
plt.tight_layout()
plt.savefig(os.path.join(PATHS["destino_graficos"], "emissao_heatmap.png"))
plt.close()

# 9. emissoes de CO₂ por ano (media movel)
emissao_por_ano = df.groupby("Year", as_index=False)["Kilotons of Co2"].sum()
emissao_por_ano["Media_Movel"] = emissao_por_ano["Kilotons of Co2"].rolling(window=5).mean()
salvar_grafico(emissao_por_ano, x="Year", y="Media_Movel",
               titulo="Média Móvel das Emissões de CO₂ ao Longo dos Anos",
               nome_arquivo="media_movel_emissao.png", tipo_grafico="line")

# 10. emissoes de CO₂ por pais (top 10 paises com maior crescimento)
crescimento_emissao = df.groupby(["Country", "Year"], as_index=False)["Kilotons of Co2"].sum()
crescimento_emissao = crescimento_emissao.pivot(index="Year", columns="Country", values="Kilotons of Co2").diff().sum().nlargest(10)
crescimento_emissao = crescimento_emissao.reset_index().rename(columns={0: "Crescimento"})
salvar_grafico(crescimento_emissao, x="Country", y="Crescimento",
               titulo="Top 10 Países com Maior Crescimento nas Emissões de CO₂",
               nome_arquivo="crescimento_emissao.png", tipo_grafico="bar")

# 11. emissoes de CO₂ por pais (top 10 paises com maior reducao)
reducao_emissao = df.groupby(["Country", "Year"], as_index=False)["Kilotons of Co2"].sum()
reducao_emissao = reducao_emissao.pivot(index="Year", columns="Country", values="Kilotons of Co2").diff().sum().nsmallest(10)
reducao_emissao = reducao_emissao.reset_index().rename(columns={0: "Redução"})
salvar_grafico(reducao_emissao, x="Country", y="Redução",
               titulo="Top 10 Países com Maior Redução nas Emissões de CO₂",
               nome_arquivo="reducao_emissao.png", tipo_grafico="bar")

print("graficos gerados com sucesso!")