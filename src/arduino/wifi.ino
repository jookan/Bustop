#include <WiFi.h>

const char* ssid     = "1132";
const char* password = "a12345678";

WiFiServer server(80);


void setup() {
  Serial.begin(115200);
  Serial.println(String("Connect try : ") + ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  while(WiFi.status() != WL_CONNECTED )
  {
    delay(500);
    Serial.println(".");
  }
  Serial.print(String("WIFI conneted\n IP : "));
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if(!client)
  {
    return;
  }
  Serial.println("Clienct connected");
  client.setTimeout(10000);
  
  while(client.available())
  {
    Serial.write(client.read());
  }
  client.print("Hello world");
}
