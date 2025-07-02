import time
import random
import csv

with open("simulacao_lidar.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(["Tempo(ms)", "Distancia(mm)"])
    tempo_inicial = time.time()
    
    for i in range(100):  # 100 medições simuladas
        tempo_ms = int((time.time() - tempo_inicial) * 1000)
        distancia = random.randint(100, 220) # Simula medidas de "buraco"
        writer.writerow([tempo_ms, distancia])
        print(f"{tempo_ms};{distancia}")
        time.sleep(0.5)  # espera 500ms igual ao Arduino

        for _ in range(5): # Simula 5 leituras de "chão liso"
            tempo_ms = int((time.time() - tempo_inicial) * 1000)
            distancia = random.randint(62, 65)
            writer.writerow([tempo_ms, distancia])
            print(f"{tempo_ms};{distancia}")
            time.sleep(0.5)