
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Configuración de la comunicación.
const char* SSID = "A35 de Luis René";
const char* PASSWORD = "belzebu666";

// Objeto encargado del servicio web. Se sirve en el puerto 80.
ESP8266WebServer server(80);

const int PIN_SENSOR = D7;

void init_wifi(){
    WiFi.mode(WIFI_STA);
    WiFi.hostname("NodeMCU-ESP8266 SENSORS");
    WiFi.begin(SSID, PASSWORD);

    // Comprobamos el si se ha conectado satisfactoriamente.
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.println("Connecting to WiFi..");
    }

    WiFi.setAutoReconnect(true);
    WiFi.persistent(true);

    Serial.print("My IP:");
    Serial.println(WiFi.localIP());

    // Se inicializa el servicio web HTTP.
    
    server.on("/", home); // Función listener para la dirección raíz.
    //server.on("/lcd_on", lcdOn);
    //server.on("/lcd_off", lcdOff);
    server.begin();
    Serial.println("HTTP server started");
}

void home() {
  server.send(200,"text/html", "<html><head><title>Advanced Hardware Programming Course</title></head><body><h1>Congratulations, you have successfully completed exercise 4!</h1></body></html>");
}
 
void setup()
{
   Serial.begin(9600);
   pinMode(PIN_SENSOR, INPUT);

    init_wifi();
}
 
void loop()
{
  // Comprobamos si se ha activado el sensor por encima del umbral.
  if (digitalRead(PIN_SENSOR) == HIGH)
    //Serial.println("FIRE! FIRE! Find a fire extinguisher!!"); 
    Serial.println("Relax, all is OK");
  else if (digitalRead(PIN_SENSOR) == LOW)
    //Serial.println("Relax, all is OK");
    Serial.println("FIRE! FIRE! Find a fire extinguisher!!"); 

    // Comprobamos si se ha activado el sensor por encima del umbral.
    if (digitalRead(PIN_SENSOR_FIRE) == HIGH)
        Serial.println("Relax, all is OK");
    else if (digitalRead(PIN_SENSOR_FIRE) == LOW)
        Serial.println("FIRE! FIRE! Find a fire extinguisher!!"); 
    
    delay(1000);

}