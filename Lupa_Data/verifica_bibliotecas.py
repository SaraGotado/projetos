import subprocess
import sys

# lista de bibliotecas necessárias
bibliotecas_necessarias = ['pandas', 'matplotlib', 'seaborn', 'pyarrow']

def instala_bibliotecas():
    for lib in bibliotecas_necessarias:
        try:
            __import__(lib)
            print(f"{lib} já está instalado.")
        except ImportError:
            print(f"{lib} não está instalado. Instalando...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
            print(f"{lib} instalado com sucesso.")

if __name__ == "__main__":
    instala_bibliotecas()