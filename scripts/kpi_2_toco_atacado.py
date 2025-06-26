import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminho da planilha
df = pd.read_excel('./dados/Base de levantamento Sphenophorus.xlsx',
                   sheet_name='Ficha de campo_Sphenophorus',
                   header=1)

# Selecionar colunas relevantes
df = df[['Tratamento', 'Tocos_Analisados', 'Tocos_Atacados']].dropna()

# Agrupar por tratamento e calcular a média
grupado = df.groupby('Tratamento').agg({
    'Tocos_Analisados': 'mean',
    'Tocos_Atacados': 'mean'
}).reset_index()

# Plotagem
plt.figure(figsize=(10, 6))
bar_width = 0.4
x = range(len(grupado))

plt.bar([i - bar_width/2 for i in x], grupado['Tocos_Analisados'],
        width=bar_width, label='Tocos Analisados')
plt.bar([i + bar_width/2 for i in x], grupado['Tocos_Atacados'],
        width=bar_width, label='Tocos Atacados')

# Estética
tplt = plt.gca()
tplt.set_xticks(x)
tplt.set_xticklabels(grupado['Tratamento'], rotation=30)
plt.ylabel('Média por Tratamento')
plt.title('Índice de Toco Atacado')
plt.legend()
plt.tight_layout()

# Criar diretório de saída
grafico_path = './graficos/indice_toco_atacado.png'
os.makedirs('./graficos', exist_ok=True)
plt.savefig(grafico_path)
print(f"Gráfico salvo em: {grafico_path}")
