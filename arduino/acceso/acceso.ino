#include <ESP8266WiFi.h>
const char ssid[] = "NodeMCU-ESP8266I05";
const char password[] = "12345678"; // Definimos la SSDI de nuestro servidor
void setup()
{
    Serial.begin(9600);
    WiFi.mode(WIFI_AP);
    WiFi.softAP(ssid, password);
    Serial.println();
    Serial.print("Direccion IP Access Point - por defecto: ");
    // Imprime la dirección IP
    Serial.println(WiFi.softAPIP());
    Serial.print("Direccion MAC Access Point: ");
    // Imprime la dirección MAC
    Serial.println(WiFi.softAPmacAddress());
    // IPAddress local_ip(192, 168, 1, 1);
    // Modifica la dirección IP
    // IPAddress gateway(192, 168, 1, 1);
    // IPAddress subnet(255, 255, 255, 0);
    // WiFi.softAPConfig(local_ip, gateway, subnet);
    // Serial.println();
    // Serial.print("Access Point - Nueva direccion IP: ");
    // Serial.println(WiFi.softAPIP());
}
void loop()
{
    Serial.printf("Stations connected = %d\n", WiFi.softAPgetStationNum());
    delay(3000);
}