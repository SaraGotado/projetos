import os

# encontra o diretório dos scripts (permite que o script seja executado independente de onde esteja a pasta do projeto)
script_dir = os.path.dirname(os.path.abspath(__file__))

# caminhos dos arquivos e diretórios
PATHS = {
    # main.py
    "csv_path": os.path.join(script_dir, "origem_csv", "Emissão_CO2_por_países.csv"),
    "destino_parquet": os.path.join(script_dir, "destino_parquet"),
    "destino_csv": os.path.join(script_dir, "erros"),

    # gera_relatorios.py
    "origem_parquet": os.path.join(script_dir, "destino_parquet"),
    "destino_graficos": os.path.join(script_dir, "destino_graficos")
}