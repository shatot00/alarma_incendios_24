#include <ESP8266WiFi.h>
#include <Servo.h>
// Declaramos la variable para controlar el servo
Servo servoMotor;
void setup()
{
  // Iniciamos el monitor serie para mostrar el resultado
  Serial.begin(9600);
  // Iniciamos el servo para que emiece a trabajar con D5
  servoMotor.attach(D5);
  // Inicializamos al ángulo 0 el servomotor
  servoMotor.write(0);
  pinMode(D6, OUTPUT);
  pinMode(D7, OUTPUT);
  pinMode(D8, OUTPUT);
}
void loop()
{
  // Vamos a tener dos bucles uno para mover en sentido positivo y otro en sentido
  // Para el sentido positivo

  digitalWrite(D6, HIGH);
  for (int i = 0; i <= 180; i++)
  {

    // Desplazamos al ángulo correspondiente
    servoMotor.write(i);
    // Hacemos una pausa de 25ms
    delay(25);
  }
  
  digitalWrite(D6, LOW);
  delay(5000);
  digitalWrite(D7, HIGH);
  delay(5000);
  digitalWrite(D7, LOW);
  digitalWrite(D8, HIGH);

  // Para el sentido negativo
  for (int i = 180; i > 0; i--)
  {
    // Desplazamos al ángulo correspondiente
    servoMotor.write(i);
    // Hacemos una pausa de 25ms
    delay(25);
  }
  digitalWrite(D8, LOW);
}