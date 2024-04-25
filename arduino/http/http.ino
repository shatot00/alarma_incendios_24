#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Configuración de la comunicación.
const char* SSID = "A54 de Adrian";
const char* PASSWORD = "12345678";

// Objeto encargado del servicio web. Se sirve en el puerto 80.
ESP8266WebServer server(80);

void home() {
  server.send(200,"text/html", "<html><head><title>Advanced Hardware Programming Course</title></head><body><h1>Congratulations, you have successfully completed exercise 3!</h1></body></html>");
}

void setup() {
  Serial.begin(9600);

  // Se establece la conexión.
  WiFi.mode(WIFI_STA);
  WiFi.hostname("NodeMCU-ESP8266 2");
  WiFi.begin(SSID, PASSWORD);
  
  Serial.print("Hola");

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
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}