import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminho do arquivo
caminho_arquivo = './dados/Base de levantamento Sphenophorus.xlsx'

# Carregar a planilha com o cabeçalho correto
df = pd.read_excel(caminho_arquivo, sheet_name='Ficha de campo_Sphenophorus', header=1)

# Selecionar colunas relevantes
colunas = ['Tratamento', 'Data_Avaliacao', 'Densidade_Populacional']
df = df[colunas].dropna(how='all')

# Configurar estilo do gráfico
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Gráfico de barras agrupadas por data de avaliação
sns.barplot(
    data=df,
    x="Tratamento",
    y="Densidade_Populacional",
    hue="Data_Avaliacao",
    estimator=sum
)

# Títulos e rótulos
plt.title("Densidade populacional", fontsize=14, weight='bold')
plt.ylabel("Soma da Densidade Populacional")
plt.xlabel("Tratamento")
plt.xticks(rotation=30)
plt.legend(title="Data de Avaliação")
plt.tight_layout()

# Criar diretório de saída se não existir
os.makedirs("./graficos", exist_ok=True)

# Salvar imagem
grafico_path = "./graficos/densidade_populacional.png"
plt.savefig(grafico_path)
print(f"Gráfico salvo em: {grafico_path}")
