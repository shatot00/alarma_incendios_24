const int PIN_BUZZER = D5;

const int TONOS[] = {261, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494};
const int NUM_TONOS = 10;

void setup(){}

void loop(){
  // Emisión de la canción.
  for (int i = 0; i < NUM_TONOS; i++) {
    tone(PIN_BUZZER, TONOS[i]);
    delay(1000);  // Frencuencia de emisión del tono.
  }

  noTone(PIN_BUZZER);
  delay(5000);  // Descansamos un poco de ruido.
}