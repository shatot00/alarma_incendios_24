#include "LiquidCrystal_I2C.h" 
LiquidCrystal_I2C lcd(0x27, 16, 2); 

byte HUMAN_CHAR [] = 
{
  B01110,
  B01110,
  B00100,
  B11111,
  B00100,
  B01110,
  B01010,
  B01010
};

byte HUMAN_CHAR_2 [] = 
{
  B01110,
  B01110,
  B10101,
  B01110,
  B00100,
  B00100,
  B01010,
  B10001
};

void setup()
{
  lcd.init();
  lcd.backlight();
  lcd.home();

  // Definimos caracteres especiales.
  lcd.createChar(0, HUMAN_CHAR);
  lcd.createChar(1, HUMAN_CHAR_2);

  // Printeamos el texto.
  lcd.setCursor(1, 0);
  lcd.print("SOY UN");
  lcd.setCursor(3, 1);
  lcd.print("CRACK");
  
  lcd.createChar(8, HUMAN_CHAR);
  lcd.createChar(9, HUMAN_CHAR_2);
}

void loop()
{
  lcd.setCursor(1, 1);
  lcd.write(0);
  delay(1000);
  
  lcd.setCursor(1, 1);
  lcd.write(1);
  delay(1000);
}