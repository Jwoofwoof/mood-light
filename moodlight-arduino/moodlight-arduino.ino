#include <WiFiNINA.h>
#include <FastLED.h>
#define NUM_LEDS  18
#define LED_PIN   2

CRGB leds[NUM_LEDS];

WiFiClient client;
int    HTTP_PORT   = 3000;
String HTTP_METHOD = "GET";
char   HOST_NAME[] = "172.20.10.10";
String PATH_NAME   = "/getInfo";
String queryString = "";
char buffer[1000];
int color = 0;
String tmp;

char ssid[] = "Gaurav";             
char pass[] = "12345567";               
int status = WL_IDLE_STATUS;
float tempo = 100.0;
void setup() {
  //Initialize serial and wait for port to open:
  Serial.begin(9600);
  while (!Serial);

  // LED strip setup
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(50);


  // check for the WiFi module:
  if (WiFi.status() == WL_NO_MODULE) {
    Serial.println("Communication with WiFi module failed!");
    // don't continue
    while (true);
  }

  // attempt to connect to Wi-Fi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    //status = WiFi.beginEnterprise(ssid, user, pass);
    status = WiFi.begin(ssid,pass);
    // wait 10 seconds for connection:
    delay(5000);
  }

  // you're connected now, so print out the data:
  Serial.println("You're connected to the network");
  Serial.println("---------------------------------------");


}

void loop() {


 // connect to web server on port 80:
  if(client.connect(HOST_NAME, HTTP_PORT)) {
    // if connected:
    Serial.println("Connected to server");
    // make a HTTP request:
    // send HTTP header
    client.println(HTTP_METHOD + " " + PATH_NAME + queryString + " HTTP/1.1");
    client.println("Host: " + String(HOST_NAME));
    client.println("Connection: close");
    client.println(); // end HTTP header
    int j = 0;
    int aux =0;
    while(client.connected()) {
      if(client.available()){
        // read an incoming byte from the server and print it to serial monitor:
        String c = client.readStringUntil('\r');
        Serial.println(c);
        aux = c.indexOf(" ");
        String clr = c.substring(aux+1);
        tmp = c.substring(0, aux);
        color = clr.toInt();
        Serial.println(color);
        Serial.println(tmp);
        tempo = tmp.toFloat();
        //buffer[j] = c;
        //j++;      
      }
    }
    Serial.println(buffer);

    // the server's disconnected, stop the client:
    client.stop();
    Serial.println();
    Serial.println("disconnected");
  } else {// if not connected:
    Serial.println("connection failed");
  }

  switch(color){
    case 0 :
    for(int t = 0; t<10; t++){
      for(int j = 0; j<NUM_LEDS; j++){
        leds[j] = CRGB :: Red;
      }
      FastLED.show();
      delay( (60000/tempo)/2 );
      fade();
      delay( (60000/tempo)/2 );
    } break;
    case 1 :
        for(int t = 0; t<10; t++){
      for(int j = 0; j<NUM_LEDS; j++){
        leds[j] = CRGB :: Green;
      }
      FastLED.show();
      delay( (60000/tempo)/2 );
      fade();
      delay( (60000/tempo)/2 );
    } break;
    case 2 :
      for(int t = 0; t<10; t++){
        for(int j = 0; j<NUM_LEDS; j++){
          leds[j] = CRGB :: Blue;
        }
      FastLED.show();
      delay( (60000/tempo)/2 );
      fade();
      delay( (60000/tempo)/2 );
    } break;
    case 3 :
            for(int t = 0; t<10; t++){
      for(int j = 0; j<NUM_LEDS; j++){
        leds[j] = CRGB :: Yellow;
      }
      FastLED.show();
      delay( (60000/tempo)/2 );
      fade();
      delay( (60000/tempo)/2 );
    } break;
  }


}

void fade(){
  for(int j = 0; j<NUM_LEDS; j++){
    leds[j] = CRGB :: Black;
  }
  FastLED.show();
}
