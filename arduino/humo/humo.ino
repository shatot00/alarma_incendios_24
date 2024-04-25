#include <MQUnifiedsensor.h>

// Código indicado en el github.

/************************Hardware Related Macros************************************/
#define Board ("ESP8266")
#define Pin (A0)  // Analog input 3 of your arduino

/***********************Software Related Macros************************************/
#define Type ("MQ-2")  //MQ3
#define Voltage_Resolution (5)
#define ADC_Bit_Resolution (10)  // For ESP8266
#define RatioMQ2CleanAir (9.83)

MQUnifiedsensor MQ2(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);

void setup() {
  Serial.begin(9600);

  // Se define el método matemático para el cálculo. Los valores de A y B dependen de
  // la tabla que define el repositorio para el sensor MQ2.
  MQ2.setRegressionMethod(1);
  MQ2.setA(36974);
  MQ2.setB(-3.109);

  /*
    Exponential regression:
    Gas    | a      | b
    H2     | 987.99 | -2.162
    LPG    | 574.25 | -2.222
    CO     | 36974  | -3.109
    Alcohol| 3616.1 | -2.675
    Propane| 658.71 | -2.168
  */

  MQ2.init();

  // Calibración.
  Serial.print("Calibrating please wait");
  float calcR0 = 0;

  for (int i = 1; i <= 10; i++) {
    MQ2.update();
    calcR0 += MQ2.calibrate(RatioMQ2CleanAir);
    Serial.print(".");
  }

  MQ2.setR0(calcR0 / 10);
  Serial.println("Calibration done!");

  // Por seguridad, si detectamos algún fallo se avisa y nunca pasa al loop.
  if (isinf(calcR0)) {
    Serial.println("Warning: Conection issue founded, R0 is infite (Open circuit detected) please check your wiring and supply");
    while (1);
  }

  if (calcR0 == 0) {
    Serial.println("Warning: Conection issue founded, R0 is zero (Analog pin with short circuit to ground) please check your wiring and supply");
    while (1);
  }

  MQ2.serialDebug(true);
}

void loop() {
  // Lectura del valor del sensor en ppm.
  MQ2.update();      
  MQ2.readSensor();  

  // Muestra por pantalla el valor obtenido.
  MQ2.serialDebug();

  delay(1000);         
}