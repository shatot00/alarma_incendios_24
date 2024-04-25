const int PIN_SENSOR = D7;
 
void setup()
{
   Serial.begin(9600);
   pinMode(PIN_SENSOR, INPUT);
}
 
void loop()
{
   // Comprobamos si se ha activado el sensor por encima del umbral.
   if (digitalRead(PIN_SENSOR) == HIGH)
      Serial.println("FIRE! FIRE! Find a fire extinguisher!!"); 
   else if (digitalRead(PIN_SENSOR) == LOW)
      Serial.println("Relax, all is OK");
 
   delay(1000);
}