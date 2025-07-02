import pandas as pd
import matplotlib.pyplot as plt

# 1. Leia o CSV (substitua pelo nome correto do seu arquivo)
df = pd.read_csv('simulacao_lidar.csv', delimiter=';')

# 2. Garante que a coluna de interesse é numérica (ajuste o nome se necessário)
df['Distancia(mm)'] = pd.to_numeric(df['Distancia(mm)'], errors='coerce')

# 3. Plota o gráfico
plt.figure(figsize=(10, 6))
plt.plot(df['Tempo(ms)'], df['Distancia(mm)'], marker='o', linestyle='-', label='Distância')
plt.axhline(y=100, color='red', linestyle='--', linewidth=2, label='Linha em 10')
plt.title('Distância ao longo do tempo')
plt.xlabel('Tempo (ms)')
plt.ylabel('Distância (mm)')
plt.legend()
plt.grid(True)
plt.show()