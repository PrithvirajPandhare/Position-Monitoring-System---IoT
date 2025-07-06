/*
  IoT Position Monitor - Wokwi Simulation Version

  Simplified version for Wokwi simulation without WiFi components
  Click on the MPU6050 sensor to change orientation values
*/

#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1

Adafruit_MPU6050 mpu;
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

float roll = 0, pitch = 0, yaw = 0;
float AccErrorX = 0, AccErrorY = 0;
float GyroErrorX = 0, GyroErrorY = 0, GyroErrorZ = 0;
unsigned long previousTime = 0;
float alpha = 0.96;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) delay(10);
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("IoT Position Monitor");
  display.println("Wokwi Simulation");
  display.println("Click MPU6050 sensor");
  display.println("to change values!");
  display.display();
  delay(3000);

  Serial.println("System Ready - Click MPU6050 to interact!");
  previousTime = millis();
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  unsigned long currentTime = millis();
  float elapsedTime = (currentTime - previousTime) / 1000.0;
  previousTime = currentTime;

  // Calculate angles from accelerometer
  float accAngleX = (atan(a.acceleration.y / sqrt(pow(a.acceleration.x, 2) + pow(a.acceleration.z, 2))) * 180 / PI);
  float accAngleY = (atan(-1 * a.acceleration.x / sqrt(pow(a.acceleration.y, 2) + pow(a.acceleration.z, 2))) * 180 / PI);

  // Get gyroscope data in degrees/sec
  float GyroX = g.gyro.x * 180 / PI;
  float GyroY = g.gyro.y * 180 / PI;
  float GyroZ = g.gyro.z * 180 / PI;

  // Integrate gyroscope
  float gyroAngleX = roll + GyroX * elapsedTime;
  float gyroAngleY = pitch + GyroY * elapsedTime;
  yaw = yaw + GyroZ * elapsedTime;

  // Apply complementary filter
  roll = alpha * gyroAngleX + (1 - alpha) * accAngleX;
  pitch = alpha * gyroAngleY + (1 - alpha) * accAngleY;

  // Update display
  display.clearDisplay();
  display.setTextSize(1);
  display.setCursor(0, 0);
  display.println("Position Monitor");
  display.drawLine(0, 10, SCREEN_WIDTH, 10, WHITE);

  display.setCursor(0, 15);
  display.print("Roll:  ");
  display.print(roll, 1);
  display.println("°");

  display.setCursor(0, 25);
  display.print("Pitch: ");
  display.print(pitch, 1);
  display.println("°");

  display.setCursor(0, 35);
  display.print("Yaw:   ");
  display.print(yaw, 1);
  display.println("°");

  display.setCursor(0, 50);
  display.print("Accel: ");
  display.print(sqrt(pow(a.acceleration.x,2) + pow(a.acceleration.y,2) + pow(a.acceleration.z,2)), 1);
  display.println(" m/s²");

  display.display();

  // Serial output
  Serial.print("Roll: "); Serial.print(roll, 2);
  Serial.print("° | Pitch: "); Serial.print(pitch, 2);
  Serial.print("° | Yaw: "); Serial.print(yaw, 2);
  Serial.println("°");

  delay(50);
}