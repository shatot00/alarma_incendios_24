#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>

// Configuración de la comunicación.
const char* SSID = "A54 de Adrian";
const char* PASSWORD = "12345678";

// Pines de los dispositivos.
const int PIN_LED = D8;
const int PIN_SERVO = 13;

bool led_state = false;
bool servo_moving = false;

// Objeto encargado del servicio web. Se sirve en el puerto 80.
ESP8266WebServer server(80);

Servo servo;

// FUNCIONES PARA GESTIÓN DE PETICIONES.

// Petición raíz.
void home() {
  server.send(200,"text/html", "<html><head><title>Advanced Hardware Programming Course</title></head><body><h1>Congratulations, you have successfully completed exercise 4!</h1></body></html>");
}

// Encendido de LED.
void ledOn() {
  led_state = true;
  server.send(200,"text/html", "<html><head><title>Advanced Hardware Programming Course</title></head><body><h1>Led ON!</h1></body></html>");
}

// Apagado de LED.
void ledOff() {
  led_state = false;
  server.send(200,"text/html", "<html><head><title>Advanced Hardware Programming Course</title></head><body><h1>Led ON!</h1></body></html>");
}

// Rotación del servo.
void servoMoving() {
  servo_moving = true;
  server.send(200,"text/html", "<html><head><title>Advanced Hardware Programming Course</title></head><body><h1>Moving servo!</h1></body></html>");
}

// Mueve el servo.
void rotateServo(){
  servo.write(0);
  delay(100);

  for (int pos = 0; pos <= 90; pos += 1) { 
    servo.write(pos); 
    delay(15);
  }

  servo_moving = false;
}

void setup() {
  Serial.begin(9600);

  // Configuración pin LED.
  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  // Configuración pin servo.
  servo.attach(PIN_SERVO);

  // Se establece la conexión.
  WiFi.mode(WIFI_STA);
  WiFi.hostname("NodeMCU-ESP8266 2");
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
  server.on("/led_on", ledOn);
  server.on("/led_off", ledOff);
  server.on("/rotate_servo", servoMoving);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
  
  if (led_state) 
    digitalWrite(PIN_LED, HIGH);
  else
    digitalWrite(PIN_LED, LOW);

   if (servo_moving)
    rotateServo();
}