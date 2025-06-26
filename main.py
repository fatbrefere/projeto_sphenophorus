# main.py - Executa todos os scripts de KPIs do projeto Sphenophorus

import subprocess
import os

# Lista de scripts a executar
scripts = [
    'scripts/kpi_1_densidade.py',
    'scripts/kpi_2_toco_atacado.py',
    'scripts/kpi_3_infestacao.py'
]

# Executar cada script sequencialmente
for script in scripts:
    print(f"Executando: {script}")
    subprocess.run(['python', script], check=True)

print("\n✅ Todos os gráficos foram gerados com sucesso!")
