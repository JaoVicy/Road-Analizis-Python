# 1. Importando as bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest
# 2. Lendo o arquivo CSV gerado pelo simulador
df = pd.read_csv('simulacao_lidar.csv', delimiter=';')

# 3. Visualizando as primeiras linhas
print(df.head())

# 4. Estatísticas básicas
print(df.describe())

# 5. Plotando a distância ao longo do tempo
plt.figure(figsize=(12, 6))
sns.lineplot(x='Tempo(ms)', y='Distancia(mm)', data=df, marker='o')
plt.title('Distância medida ao longo do tempo')
plt.xlabel('Tempo (ms)')
plt.ylabel('Distância (mm)')
plt.grid(True)
plt.show()

# 6. Plotando um histograma das distâncias
plt.figure(figsize=(8, 5))
sns.histplot(data=df, x='Distancia(mm)', bins=20, kde=True)
plt.title('Distribuição das Distâncias Medidas')
plt.xlabel('Distância (mm)')
plt.ylabel('Frequência')
plt.show()

# 7. Encontrando quedas bruscas ("buracos") - diferença entre leituras
df['Delta'] = df['Distancia(mm)'].diff()
buracos = df[df['Delta'] < -150]  # Ajuste o threshold conforme necessário

print("Possíveis buracos encontrados:")
print(buracos[['Tempo(ms)', 'Distancia(mm)', 'Delta']])

# 8. Visualizando os buracos no gráfico
plt.figure(figsize=(12, 6))
sns.lineplot(x='Tempo(ms)', y='Distancia(mm)', data=df, marker='o', label='Trajetória')
plt.scatter(buracos['Tempo(ms)'], buracos['Distancia(mm)'], color='red', label='Possíveis buracos', zorder=5)
plt.title('Detecção de buracos na trajetória')
plt.xlabel('Tempo (ms)')
plt.ylabel('Distância (mm)')
plt.legend()
plt.grid(True)
plt.show()

# 9. (Opcional) Detecção automática de anomalias com Scikit-Learn
modelo = IsolationForest(contamination=0.05)
df['outlier'] = modelo.fit_predict(df[['Distancia(mm)']])
buracos_ml = df[df['outlier'] == -1]
print("Buracos detectados com Machine Learning:")
print(buracos_ml[['Tempo(ms)', 'Distancia(mm)']])

# 10. Visualizando buracos detectados por ML
plt.figure(figsize=(12, 6))
sns.lineplot(x='Tempo(ms)', y='Distancia(mm)', data=df, marker='o', label='Trajetória')
plt.scatter(buracos_ml['Tempo(ms)'], buracos_ml['Distancia(mm)'], color='purple', label='Buracos (ML)', zorder=5)
plt.title('Detecção de buracos na trajetória (Isolation Forest)')
plt.xlabel('Tempo (ms)')
plt.ylabel('Distância (mm)')
plt.legend()
plt.grid(True)
plt.show()