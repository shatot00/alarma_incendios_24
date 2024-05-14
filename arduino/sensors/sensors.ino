#include <MQUnifiedsensor.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <ArduinoJson.h>

//#include <WiFiClient.h>
//#include <HTTPClient.h>

// Configuración de la comunicación.
String SSID = "A54 de Adrian"; // A54 de Adrian
String PASSWORD = "12345678";

// Objeto encargado del servicio web. Se sirve en el puerto 80.
//ESP8266WebServer server(80);

/********************************POST********************************/
//Your Domain name with URL path or IP address with path
String serverName = "http://192.168.253.30:8000"; //192.168.198.30
unsigned long lastTime = 0;
unsigned long timerDelay = 5000;

const int PIN_SENSOR = D7;

/************************Hardware Related Macros************************************/
#define Board ("ESP8266")
#define Pin (A0)  // Analog input 3 of your arduino

/***********************Software Related Macros************************************/
#define Type ("MQ-2")  //MQ3
#define Voltage_Resolution (5)
#define ADC_Bit_Resolution (10)  // For ESP8266
#define RatioMQ2CleanAir (9.83)

MQUnifiedsensor MQ2(Board, Voltage_Resolution, ADC_Bit_Resolution, Pin, Type);

int sensorValue = 0;
int sensorFire = 0;

void init_wifi(){

    WiFi.begin(SSID, PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi..");
    }

    WiFi.setAutoReconnect(true);
    WiFi.persistent(true);

    Serial.print("My IP:");
    Serial.println(WiFi.localIP());

    Serial.println("HTTP server started");
}
 
void setup()
{
    Serial.begin(9600);
    pinMode(PIN_SENSOR, INPUT);

    MQ2.setRegressionMethod(1);
    MQ2.setA(36974);
    MQ2.setB(-3.109);
    MQ2.init();

    float calcR0 = 0;

    for (int i = 1; i <= 10; i++) {
      MQ2.update();
      calcR0 += MQ2.calibrate(RatioMQ2CleanAir);
      Serial.print(".");
    }

    MQ2.setR0(calcR0 / 10);

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

    init_wifi();
}
 
void loop()
{
  //server.handleClient();

  /**********************HUMO**********************/
  MQ2.update();      
  MQ2.readSensor();  

  sensorValue = analogRead(A0);  
  
  // Crear el JSON
  StaticJsonDocument<200> JSONData;
  JSONData["level"] = sensorValue;

  // Serializar el JSON
  char data[200];
  serializeJson(JSONData, data);
  Serial.println(data);

  WiFiClient client;
  HTTPClient http; 

  /************************POST GAS************************/

    Serial.println(serverName);

    http.begin(client, serverName+"/db_gas");
    http.addHeader("Content-Type", "application/json");
    
    int httpResponseCode = http.POST(data);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
    } else {
      Serial.print("Error en la petición HTTP: ");
      Serial.println(httpResponseCode);
    }

    /************************POST FUEGO************************/

    // Comprobamos si se ha activado el sensor por encima del umbral.
    if (digitalRead(PIN_SENSOR) == LOW){	  
      //Serial.println("FIRE! FIRE! Find a fire extinguisher!!");
      sensorFire = 1;
    } else if (digitalRead(PIN_SENSOR) == HIGH)	 {  
      //Serial.println("Relax, all is OK");
      sensorFire = 0;
    }

    JSONData["level"] = sensorFire;
    serializeJson(JSONData, data);

    http.begin(client, serverName+"/db_fire");
    http.addHeader("Content-Type", "application/json");
    httpResponseCode = http.POST(data);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      //Serial.println(payload);
    } else {
      Serial.print("Error en la petición HTTP: ");
      Serial.println(httpResponseCode);
    }

  delay(2000);
}