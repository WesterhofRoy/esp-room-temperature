#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <WiFi.h>
#include <WebServer.h>
#include <WiFiUdp.h>
#include <NTPClient.h>
#include <ArduinoJson.h>
#include <vector>

const char* ssid = "ssid";
const char* password = "pass";

WebServer server(80);
WiFiClient client;
// Define NTP Client to get dutch (winter) time
WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "europe.pool.ntp.org", 3600, 60000);
// Set up the time client to update every 15 minutes

Adafruit_BME280 bme; // I2C

// Sensor data
struct SensorData {
    String time;
    float temperature;
};
// Array to store sensor data (data will be 4 times per hour for 24 hours)
std::vector<SensorData> sensorDataVec;
// Last time data was added to prevent multiple entries in the same minute
unsigned int lastDataAdd = 0;

void setup() {
    // Start serial communication
    Serial.begin(115200);
    while(!Serial) {
        delay(10);
    }
    // Connect to WiFi
    Serial.println();
    Serial.print("Connecting to WiFi..");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    // Start the time client
    timeClient.begin();
    timeClient.update();
    // Print WiFi connection details
    Serial.println("\nConnected to WiFi");
    server.begin();
    Serial.print("Server started on ip: ");
    Serial.println(WiFi.localIP());
    
    // Initialize the BME sensor
    Serial.println("Initializing BME sensor..");
    Wire.begin(21, 22);
    bme.begin(0x76, &Wire);


    // --------------------------------- API ---------------------------------
    Serial.println("Setting up API..");
    server.on("/", HTTP_GET, []() {
        server.send(200, "text/plain", "Hello World");
    });
    // If /time is requested, send the current time as a json object
    server.on("/time", HTTP_GET, []() {
        timeClient.update();
        JsonDocument doc;
        doc["time"] = timeClient.getFormattedTime();
        String output;
        serializeJson(doc, output);
        server.send(200, "application/json", output);
    });
    // If /temperature is requested, send the current temperature as a json object
    server.on("/temperature", HTTP_GET, []() {
        float temperature = bme.readTemperature();
        JsonDocument doc;
        doc["temperature"] = temperature;
        String output;
        serializeJson(doc, output);
        server.send(200, "application/json", output);
    });
    // If /sensordata is requested, send the sensor data array as a json object
    server.on("/sensordata", HTTP_GET, []() {
        JsonDocument doc;
        JsonArray data = doc.to<JsonArray>();
        for (const SensorData sensorData : sensorDataVec) {
            JsonObject obj = data.add<JsonObject>();
            obj["time"] = sensorData.time;
            obj["temperature"] = sensorData.temperature;
        }
        String output;
        serializeJson(doc, output);
        server.send(200, "application/json", output);
    });
    
    Serial.println("API setup complete, server started");
    server.begin();
}

void loop() {
    server.handleClient();
    timeClient.update();

    int time = timeClient.getMinutes();

    // Add sensor data to the array every 15 minutes
    if (time % 5 == 0 && lastDataAdd != time) {
        Serial.println("Adding sensor data..");
        SensorData sensorData;
        sensorData.time = timeClient.getEpochTime();
        sensorData.temperature = bme.readTemperature();
        sensorDataVec.push_back(sensorData);
        // Update the last data add time
        lastDataAdd = time;
    }
}
