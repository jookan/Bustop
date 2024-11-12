#define RED 10
#define GREEN 9
#define BLUE 8

unsigned long lastReceivedTime = 0; // 마지막 데이터 수신 시간
const unsigned long timeout = 10000; // LED를 끄기 위한 타임아웃 (2초)

void setup() {
  Serial.begin(9600);  // 시리얼 통신 시작
  pinMode(RED, OUTPUT);
  pinMode(GREEN, OUTPUT);
  pinMode(BLUE, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {  // 시리얼 데이터가 들어왔는지 확인
    char received = Serial.read();  // 시리얼 값을 문자로 읽기
    
    if (received == '1') {  // 받은 값이 '1'이면 빨간색 LED 켜기
      digitalWrite(RED, HIGH);
      digitalWrite(GREEN, LOW);
      digitalWrite(BLUE, LOW);
      lastReceivedTime = millis();  // 마지막 수신 시간 갱신
    }
    else {
      digitalWrite(RED,LOW);
      digitalWrite(GREEN,HIGH);
      digitalWrite(BLUE, LOW);
      lastReceivedTime = millis();
    }
  }
  
  // 수신된 데이터가 일정 시간 동안 없으면 LED 끄기
  if (millis() - lastReceivedTime > timeout) {
    digitalWrite(RED, LOW);
    digitalWrite(GREEN, LOW);
    digitalWrite(BLUE, LOW);
  }
}
