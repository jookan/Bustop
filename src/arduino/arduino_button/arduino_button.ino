#include <LiquidCrystal_I2C.h>    
LiquidCrystal_I2C lcd(0x27, 16, 2);  

int previousState = 0;

void setup() {
  Serial.begin(9600);
  lcd.begin(); 
  pinMode(7, INPUT);
  pinMode(11,OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(9, OUTPUT);
  pinMode(8,OUTPUT);

  lcd.setCursor(0, 0);    
  lcd.print("STOP");             
  lcd.setCursor(0, 1);    
  lcd.print("moving detected"); 
}

void loop() {
  int readValue = digitalRead(7);
  Serial.println(readValue);

  if (readValue != previousState) {
    lcd.clear();
    if (readValue == 1){
      lcd.setCursor(0, 0);    
      lcd.print("moving detected!!");             
      lcd.setCursor(0, 1);    
      lcd.print("driving score -1"); 
    }

    digitalWrite(9, HIGH);
    digitalWrite(10,LOW);
    digitalWrite(11,LOW);
    tone(8,392,250);
  }
  else {
    lcd.setCursor(0, 0);    
    lcd.print("STOP");             
    lcd.setCursor(0, 1);    
    lcd.print("moving detected"); 

    digitalWrite(9,LOW);
    digitalWrite(10,HIGH);
    digitalWrite(11,LOW);
  }
}
