/*
  IoT Position and Orientation Monitoring System

  Author: [Your Name]
  Date: July 2025

  Description:
  This system monitors object position and orientation using MPU6050 IMU sensor
  and displays real-time data on OLED screen. Data is also transmitted to 
  ThingsBoard cloud platform via WiFi.

  Hardware Components:
  - ESP32 Development Board
  - MPU6050 6-axis IMU Sensor  
  - SSD1306 OLED Display (128x64)

  Connections:
  MPU6050:     ESP32:
  VCC    -->   3.3V
  GND    -->   GND
  SCL    -->   GPIO22 (SCL)
  SDA    -->   GPIO21 (SDA)

  OLED:        ESP32:
  VCC    -->   3.3V
  GND    -->   GND
  SCL    -->   GPIO22 (SCL)
  SDA    -->   GPIO21 (SDA)
*/

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Display settings
#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
#define OLED_ADDRESS 0x3C

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// ThingsBoard settings
const char* tb_server = "demo.thingsboard.io";
const char* tb_token = "YOUR_DEVICE_TOKEN";
const int tb_port = 1883;

// Initialize sensors and display
Adafruit_MPU6050 mpu;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

// Sensor variables
float AccX, AccY, AccZ;
float GyroX, GyroY, GyroZ;
float roll, pitch, yaw = 0;
float AccErrorX = 0, AccErrorY = 0;
float GyroErrorX = 0, GyroErrorY = 0, GyroErrorZ = 0;

// Timing variables
unsigned long previousTime = 0;
unsigned long currentTime = 0;
float elapsedTime = 0;

// Complementary filter coefficient
float alpha = 0.96;

// Display update timing
unsigned long lastDisplayUpdate = 0;
const unsigned long displayInterval = 100; // Update every 100ms

// Cloud update timing
unsigned long lastCloudUpdate = 0;
const unsigned long cloudInterval = 1000; // Send to cloud every 1 second

void setup() {
  Serial.begin(115200);
  Serial.println("Initializing IoT Position Monitoring System...");

  // Initialize I2C
  Wire.begin(21, 22); // SDA, SCL pins for ESP32

  // Initialize MPU6050
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");

  // Configure MPU6050
  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  // Initialize OLED display
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDRESS)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("IoT Position Monitor");
  display.println("Initializing...");
  display.display();
  delay(2000);

  // Calibrate IMU
  Serial.println("Calibrating IMU sensors...");
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("Calibrating IMU...");
  display.println("Keep device still");
  display.display();

  calculateIMUError();

  // Initialize WiFi
  WiFi.begin(ssid, password);
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("Connecting to WiFi...");
  display.display();

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  // Initialize MQTT
  mqttClient.setServer(tb_server, tb_port);

  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("System Ready!");
  display.println("WiFi: Connected");
  display.print("IP: ");
  display.println(WiFi.localIP());
  display.display();
  delay(2000);

  Serial.println("System initialization complete!");
  currentTime = millis();
}

void loop() {
  // Read sensor data
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Get current time
  previousTime = currentTime;
  currentTime = millis();
  elapsedTime = (currentTime - previousTime) / 1000.0;

  // Read accelerometer data (in m/s²)
  AccX = a.acceleration.x;
  AccY = a.acceleration.y;
  AccZ = a.acceleration.z;

  // Calculate roll and pitch from accelerometer
  float accAngleX = (atan(AccY / sqrt(pow(AccX, 2) + pow(AccZ, 2))) * 180 / PI) - AccErrorX;
  float accAngleY = (atan(-1 * AccX / sqrt(pow(AccY, 2) + pow(AccZ, 2))) * 180 / PI) - AccErrorY;

  // Read gyroscope data (in rad/s, convert to deg/s)
  GyroX = g.gyro.x * 180 / PI - GyroErrorX;
  GyroY = g.gyro.y * 180 / PI - GyroErrorY;
  GyroZ = g.gyro.z * 180 / PI - GyroErrorZ;

  // Integrate gyroscope data
  float gyroAngleX = roll + GyroX * elapsedTime;
  float gyroAngleY = pitch + GyroY * elapsedTime;
  yaw = yaw + GyroZ * elapsedTime;

  // Apply complementary filter
  roll = alpha * gyroAngleX + (1 - alpha) * accAngleX;
  pitch = alpha * gyroAngleY + (1 - alpha) * accAngleY;

  // Update display
  if (millis() - lastDisplayUpdate >= displayInterval) {
    updateDisplay();
    lastDisplayUpdate = millis();
  }

  // Send data to cloud
  if (millis() - lastCloudUpdate >= cloudInterval) {
    sendToCloud();
    lastCloudUpdate = millis();
  }

  // Print to serial monitor
  Serial.print("Roll: "); Serial.print(roll, 2);
  Serial.print("° | Pitch: "); Serial.print(pitch, 2);
  Serial.print("° | Yaw: "); Serial.print(yaw, 2);
  Serial.println("°");

  delay(10); // Small delay for stability
}

void updateDisplay() {
  display.clearDisplay();

  // Title
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Position Monitor");

  // Draw separator line
  display.drawLine(0, 10, SCREEN_WIDTH, 10, WHITE);

  // Roll value
  display.setCursor(0, 15);
  display.print("Roll:  ");
  display.print(roll, 1);
  display.println("°");

  // Pitch value
  display.setCursor(0, 25);
  display.print("Pitch: ");
  display.print(pitch, 1);
  display.println("°");

  // Yaw value
  display.setCursor(0, 35);
  display.print("Yaw:   ");
  display.print(yaw, 1);
  display.println("°");

  // Connection status
  display.setCursor(0, 50);
  if (WiFi.status() == WL_CONNECTED) {
    display.print("WiFi: OK");
  } else {
    display.print("WiFi: DISCONNECTED");
  }

  display.setCursor(0, 57);
  if (mqttClient.connected()) {
    display.print("Cloud: CONNECTED");
  } else {
    display.print("Cloud: OFFLINE");
  }

  display.display();
}

void sendToCloud() {
  if (!mqttClient.connected()) {
    reconnectMQTT();
  }

  if (mqttClient.connected()) {
    // Create JSON payload
    StaticJsonDocument<200> doc;
    doc["roll"] = round(roll * 100) / 100.0;
    doc["pitch"] = round(pitch * 100) / 100.0;
    doc["yaw"] = round(yaw * 100) / 100.0;
    doc["temperature"] = 25.0; // You can add actual temp from MPU6050
    doc["timestamp"] = millis();

    char buffer[256];
    serializeJson(doc, buffer);

    // Publish to ThingsBoard
    String topic = "v1/devices/me/telemetry";
    mqttClient.publish(topic.c_str(), buffer);

    Serial.println("Data sent to cloud: " + String(buffer));
  }

  mqttClient.loop();
}

void reconnectMQTT() {
  while (!mqttClient.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (mqttClient.connect("ESP32Client", tb_token, "")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void calculateIMUError() {
  // Calculate accelerometer error (200 readings)
  int c = 0;
  while (c < 200) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    AccErrorX += (atan((a.acceleration.y) / sqrt(pow((a.acceleration.x), 2) + pow((a.acceleration.z), 2))) * 180 / PI);
    AccErrorY += (atan(-1 * (a.acceleration.x) / sqrt(pow((a.acceleration.y), 2) + pow((a.acceleration.z), 2))) * 180 / PI);
    c++;
    delay(5);
  }
  AccErrorX = AccErrorX / 200;
  AccErrorY = AccErrorY / 200;

  c = 0;
  // Calculate gyroscope error (200 readings)
  while (c < 200) {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    GyroErrorX += (g.gyro.x * 180 / PI);
    GyroErrorY += (g.gyro.y * 180 / PI);
    GyroErrorZ += (g.gyro.z * 180 / PI);
    c++;
    delay(5);
  }
  GyroErrorX = GyroErrorX / 200;
  GyroErrorY = GyroErrorY / 200;
  GyroErrorZ = GyroErrorZ / 200;

  Serial.println("IMU Calibration Complete");
  Serial.print("AccErrorX: "); Serial.println(AccErrorX);
  Serial.print("AccErrorY: "); Serial.println(AccErrorY);
  Serial.print("GyroErrorX: "); Serial.println(GyroErrorX);
  Serial.print("GyroErrorY: "); Serial.println(GyroErrorY);
  Serial.print("GyroErrorZ: "); Serial.println(GyroErrorZ);
}