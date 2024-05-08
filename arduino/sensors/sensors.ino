#include <ESP8266WiFi.h>
#include <MQUnifiedsensor.h>

const int PIN_SENSOR_FIRE = D7;

void setup()
{
    // Inicializamos el sensor de humo
    Serial.begin(9600);
    pinMode(PIN_SENSOR_FIRE, INPUT);

}

void loop()
{

    // Comprobamos si se ha activado el sensor por encima del umbral.
    if (digitalRead(PIN_SENSOR_FIRE) == HIGH)
        Serial.println("Relax, all is OK");
    else if (digitalRead(PIN_SENSOR_FIRE) == LOW)
        Serial.println("FIRE! FIRE! Find a fire extinguisher!!"); 
    
    delay(1000);

}