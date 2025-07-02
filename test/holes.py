import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('simulacao_lidar.csv', delimiter=';')

# 3. Visualizando as primeiras linhas
print(df.head())

# 4. Estatísticas básicas
print(df.describe())

df['Delta'] = df['Distancia(mm)'].diff()
buracos = df[df['Delta'] < -150]  # Ajuste o threshold conforme necessário

# Seleciona os pontos com Distancia(mm) >= 100
acima_100 = df[df['Distancia(mm)'] >= 100]
igual_100 = df[(df['Distancia(mm)'] <= 100) & (df['Distancia(mm)'] >= 80)]

plt.figure(figsize=(12, 6))
sns.lineplot(x='Tempo(ms)', y='Distancia(mm)', data=df, marker='o', label='Trajetória')

# Plota todos os pontos >= 100 em vermelho
plt.scatter(acima_100['Tempo(ms)'], acima_100['Distancia(mm)'], color='red', label='Pontos >= 100 mm', zorder=6)
plt.scatter(igual_100['Tempo(ms)'], igual_100['Distancia(mm)'], color='blue', label='80 <= Pontos <= 100 mm', zorder=7)

plt.axhline(y=100.0, color='red', linestyle='--', label='Referência: 100 mm')
plt.axhline(y=80, color='green', linestyle='--', label='Chão liso (80 mm)')
plt.title('Detecção de buracos na trajetória')
plt.xlabel('Tempo (ms)')
plt.ylabel('Distância (mm)')
plt.legend()
plt.grid(True)
plt.show()