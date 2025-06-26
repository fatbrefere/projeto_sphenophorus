import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Carregar a planilha
df = pd.read_excel('./dados/Base de levantamento Sphenophorus.xlsx',
                   sheet_name='Ficha de campo_Sphenophorus',
                   header=1)

# Selecionar colunas relevantes
df = df[['Tratamento', 'Data_Avaliacao', 'Infestacao']].dropna()

# Agrupar soma de infestacao por tratamento e data
df_grouped = df.groupby(['Data_Avaliacao', 'Tratamento'])['Infestacao'].sum().reset_index()

# Plotar
plt.figure(figsize=(10, 6))
sns.lineplot(
    data=df_grouped,
    x='Data_Avaliacao',
    y='Infestacao',
    hue='Tratamento',
    marker='o'
)

plt.title('Infestação por Tratamento ao Longo do Tempo')
plt.xlabel('Data de Avaliação')
plt.ylabel('Infestação (soma)')
plt.xticks(rotation=30)
plt.tight_layout()

# Salvar imagem
os.makedirs('./graficos', exist_ok=True)
plt.savefig('./graficos/indice_infestacao.png')
print("Gráfico salvo em: ./graficos/indice_infestacao.png")
