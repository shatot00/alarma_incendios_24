#include <MQUnifiedsensor.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>
//#include <HTTPClient.h>

// Configuración de la comunicación.
 String SSID = "A54 de Adrian";
 String PASSWORD = "12345678";

// Objeto encargado del servicio web. Se sirve en el puerto 80.
ESP8266WebServer server(80);

/********************************POST********************************/
//Your Domain name with URL path or IP address with path
const char* serverName = "http://192.168.198.30:8000/";
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

void init_wifi(){
    WiFi.mode(WIFI_STA);
    WiFi.hostname("NodeMCU-ESP8266 SENSORS");
    WiFi.begin(SSID, PASSWORD);

    // Comprobamos el si se ha conectado satisfactoriamente.
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
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
  // Comprobamos si se ha activado el sensor por encima del umbral.
  if (digitalRead(PIN_SENSOR) == HIGH)
    //Serial.println("FIRE! FIRE! Find a fire extinguisher!!"); 
    Serial.println("Relax, all is OK");
  else if (digitalRead(PIN_SENSOR) == LOW)
    //Serial.println("Relax, all is OK");
    Serial.println("FIRE! FIRE! Find a fire extinguisher!!"); 

  server.handleClient();

  /**********************HUMO**********************/
  MQ2.update();      
  MQ2.readSensor();  

  sensorValue = analogRead(A0);  //tried 14 with same results...         
  Serial.print("sensor = " );                       
  Serial.println(sensorValue);

  /************************POST************************/
    WiFiClient client;
    HTTPClient http;

    String urlGas = serverName + String("db_gas");
    Serial.println(urlGas);

    http.begin(client, urlGas);

    http.addHeader("Content-Type", "application/json");
    // "{\"api_key\":\"tPmAT5Ab3j7F9\",\"sensor\":\"BME280\",\"value1\":\"24.25\",\"value2\":\"49.54\",\"value3\":\"1005.14\"}"
    String jsonParam = String("{\"level\":\"") + sensorValue + String("\"}");
    Serial.println(jsonParam);
    
    int httpResponseCode = http.POST(jsonParam);

  delay(1000);
}