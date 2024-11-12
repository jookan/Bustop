#define BLUE 11
#define GREEN 10
#define RED 9

void setup() {
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
  digitalWrite(RED, HIGH);
  digitalWrite(GREEN, LOW);
  digitalWrite(BLUE, LOW);
}

void loop() {
  int redValue;
  int greenValue;
  int blueValue;
  
  redValue = 255; 
  greenValue = 0;
  blueValue = 0;
 
  for(int i = 0; i < 255; i += 1) 
  {
    redValue -= 1;
    greenValue += 1;
    analogWrite(RED, redValue);
    analogWrite(GREEN, greenValue);
    delay(10);
  }
  
  redValue = 0;
  greenValue = 255;
  blueValue = 0;
  // Green, blue fade
  for(int i = 0; i < 255; i += 1){
  
    greenValue -= 1;
    blueValue += 1;
    analogWrite(GREEN, greenValue);
    analogWrite(BLUE, blueValue);
    delay(10);
  }
  
  redValue = 0;
  greenValue = 0;
  blueValue = 255;
  
  for(int i = 0; i < 255; i += 1){
    blueValue -= 1;
    redValue += 1;
    analogWrite(BLUE, blueValue);
    analogWrite(RED, redValue);
    delay(10);
  }
}
