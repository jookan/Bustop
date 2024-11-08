#include <LiquidCrystal_I2C.h>    
LiquidCrystal_I2C lcd(0x27, 16, 2);  

void setup()
{
  lcd.begin(); 
}

void loop()
{
  lcd.setCursor(0, 0);    
  lcd.print("HaJungHun is Gay");             
  lcd.setCursor(0, 1);    
  lcd.print("He like maratang");           
}