#include <Wire.h>
#include <Adafruit_VL53L0X.h>

// === Ponte H ===
#define ENA 10
#define IN1 9
#define IN2 8
#define IN3 7
#define IN4 6
#define ENB 5

// === LiDAR ===
Adafruit_VL53L0X lox = Adafruit_VL53L0X();
#define NUM_MEDIDAS 5  // Número de leituras para média móvel

// === Controle ===
int direcao = 5; // Pode manter, mas não vai para o CSV

// === Controle de tempo ===
unsigned long tempoAnterior = 0;
const unsigned long intervalo = 500; // Tempo entre leituras (ms)

void setup() {
  // Ponte H
  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);

  // Serial para HC-05 ou USB
  Serial.begin(9600);

  // Inicializa LiDAR
  if (!lox.begin()) {
    Serial.println("VL53L0X não detectado!");
    while (1);
  }

  // Cabeçalho CSV
  Serial.println("Tempo(ms);Distancia(mm)");
}

void loop() {
  // 1. Lê comando Bluetooth
  if (Serial.available()) {
    char comando = Serial.read();
    switch (comando) {
      case 'F': direcao = 1; break;
      case 'B': direcao = 2; break;
      case 'R': direcao = 3; break;
      case 'L': direcao = 4; break;
      case 'S': direcao = 5; break;
    }
  }

  // 2. Mede LiDAR e envia CSV
  unsigned long tempoAtual = millis();
  if (tempoAtual - tempoAnterior >= intervalo) {
    tempoAnterior = tempoAtual;

    int distanciaMedia = obterDistanciaMedia();
    if (distanciaMedia >= 0) {
      Serial.print(tempoAtual);
      Serial.print(";");
      Serial.println(distanciaMedia);
    } else {
      Serial.print(tempoAtual);
      Serial.println(";Leitura_invalida");
    }
  }

  // 3. Executa movimento normal
  controlarMovimento();
}

void controlarMovimento() {
  switch (direcao) {
    case 1: // Frente
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, 180);
      analogWrite(ENB, 180);
      break;

    case 2: // Trás
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      analogWrite(ENA, 180);
      analogWrite(ENB, 180);
      break;

    case 3: // Direita
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      analogWrite(ENA, 180);
      analogWrite(ENB, 180);
      break;

    case 4: // Esquerda
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, 180);
      analogWrite(ENB, 180);
      break;

    default: // Parar
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      analogWrite(ENA, 0);
      analogWrite(ENB, 0);
      break;
  }
}

int obterDistanciaMedia() {
  long soma = 0;
  int leiturasValidas = 0;

  for (int i = 0; i < NUM_MEDIDAS; i++) {
    VL53L0X_RangingMeasurementData_t medida;
    lox.rangingTest(&medida, false);

    if (medida.RangeStatus != 4) {
      soma += medida.RangeMilliMeter;
      leiturasValidas++;
    }
    delay(50);  // intervalo entre leituras para suavizar ruído
  }

  if (leiturasValidas > 0) {
    return soma / leiturasValidas;
  } else {
    return -1; // indica leitura inválida
  }
}