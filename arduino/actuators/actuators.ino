#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include "LiquidCrystal_I2C.h" 
#include <Servo.h>


// Configuración de la comunicación.
const char* SSID = "A54 de Adrian";
const char* PASSWORD = "12345678";

// Pines de los dispositivos.
const int PIN_BUZZER = D7;

const int TONES[] = {261, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494};
const int NUM_TONES= 5;

LiquidCrystal_I2C lcd(0x27, 16, 2); 

// Objeto encargado del servicio web. Se sirve en el puerto 80.
ESP8266WebServer server(80);

Servo servo;

bool fire = false;

void init_wifi(){
    WiFi.mode(WIFI_STA);
    WiFi.hostname("NodeMCU-ESP8266 ACTUATORS");
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
    server.on("/lcd_on", lcdOn);
    server.on("/lcd_off", lcdOff);
    server.on("/buzzer_on", buzzerOn);
    server.on("/buzzer_off", buzzerOff);
    server.on("/sprinkler_on", servoOn);
    server.on("/sprinkler_off", servoOff);
    server.begin();
    Serial.println("HTTP server started");
}

// Peticiones HTTP.

void home() {
    server.send(200,"text/html", "<html><head><title>Advanced Hardware Programming Course</title></head><body><h1>Congratulations, you have successfully completed exercise 4!</h1></body></html>");
}

void lcdOff(){
    lcd.clear();
    lcd.setCursor(1, 0);
    lcd.print("NO HAY");
    lcd.setCursor(1, 1);
    lcd.print("FUEGO");
    server.send(200,"text/html", "<html><head><title>No fire</title></html>");
}

void lcdOn(){
    lcd.clear();
    lcd.setCursor(1, 0);
    lcd.print("FUEGOOOOOOO");
    lcd.setCursor(1, 1);
    lcd.print("FUEGOOOOOOO");
    server.send(200,"text/html", "<html><head><title>FIREEE</title></html>");
}

void buzzerOn(){
    for (int i = 0; i < NUM_TONES; i++) {
        tone(PIN_BUZZER, TONES[i]);
        delay(1000);  // Frencuencia de emisión del tono.
        server.send(200,"text/html", "<html><head><title>BUZZER ON</title></html>");
  }
}

void servoOn(){  
    server.send(200,"text/html", "<html><head><title>SERVO ON</title></html>");
    Serial.println("Servo");
    for (int i = 0; i <= 180; i+=+0){
        // Desplazamos al ángulo correspondiente
        servo.write(i);
        // Hacemos una pausa de 25ms
        delay(25);
    }
    for (int i = 180; i > 0; i-=10)
    {
        // Desplazamos al ángulo correspondiente
        servo.write(i);
        // Hacemos una pausa de 25ms
        delay(25);
    }

}

void servoOff(){
    server.send(200,"text/html", "<html><head><title>SERVO ON</title></html>");
}

void buzzerOff(){
    noTone(PIN_BUZZER);
    server.send(200,"text/html", "<html><head><title>BUZZER OFF</title></html>");
}

void setup()
{
    Serial.begin(9600);
    lcd.init();
    lcd.backlight();
    lcd.home();
    init_wifi();
    lcdOff();
    
    servo.attach(D5);
    servo.write(0);
}

void loop()
{
    server.handleClient();
    // check_fire();
}