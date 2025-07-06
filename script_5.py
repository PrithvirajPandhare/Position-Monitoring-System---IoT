# Create Wokwi simulation configuration
wokwi_config = {
    "diagram.json": {
        "version": 1,
        "author": "IoT Expert",
        "editor": "wokwi",
        "parts": [
            {
                "type": "wokwi-esp32-devkit-v1",
                "id": "esp",
                "top": 0,
                "left": 0,
                "attrs": {}
            },
            {
                "type": "wokwi-mpu6050",
                "id": "mpu1",
                "top": -48,
                "left": 144,
                "attrs": {}
            },
            {
                "type": "wokwi-ssd1306",
                "id": "oled1",
                "top": -120,
                "left": 288,
                "attrs": {}
            }
        ],
        "connections": [
            ["esp:3V3", "mpu1:VCC", "red", []],
            ["esp:GND.1", "mpu1:GND", "black", []],
            ["esp:D21", "mpu1:SDA", "green", []],
            ["esp:D22", "mpu1:SCL", "blue", []],
            ["esp:3V3", "oled1:VCC", "red", []],
            ["esp:GND.1", "oled1:GND", "black", []],
            ["esp:D21", "oled1:SDA", "green", []],
            ["esp:D22", "oled1:SCL", "blue", []]
        ]
    }
}

# Create simplified Arduino code for Wokwi (without WiFi for simulation)
wokwi_code = '''/*
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
}'''

# Save Wokwi files
import json

with open('wokwi_diagram.json', 'w') as f:
    json.dump(wokwi_config["diagram.json"], f, indent=2)

with open('wokwi_sketch.ino', 'w') as f:
    f.write(wokwi_code)

# Create project documentation template
documentation = """# IoT Position and Orientation Monitoring System

## Project Overview

This project implements a real-time IoT system for monitoring object position and orientation using an MPU6050 IMU sensor, with visualization on an OLED display and cloud connectivity via ThingsBoard.

## Aim

To design and implement a comprehensive IoT solution that:
- Monitors 6-axis motion data (accelerometer + gyroscope)
- Provides real-time visual feedback via OLED display
- Implements sensor fusion using complementary filter
- Enables remote monitoring through cloud connectivity
- Serves as an educational platform for IoT development

## Problem Statement

Traditional position monitoring systems lack:
1. **Real-time visualization** - Users need immediate feedback
2. **Cost-effective solutions** - Expensive commercial systems limit accessibility
3. **Cloud integration** - Remote monitoring capabilities are essential
4. **Educational value** - Learning platforms for IoT development
5. **Accurate sensor fusion** - Combining multiple sensor data effectively

## Solution Scope

### Hardware Integration
- **ESP32 Microcontroller**: Main processing unit with WiFi capability
- **MPU6050 IMU Sensor**: 6-axis motion sensing (3-axis accelerometer + 3-axis gyroscope)
- **SSD1306 OLED Display**: Real-time data visualization (128x64 pixels)
- **I2C Communication**: Efficient sensor and display connectivity

### Software Implementation
- **Arduino IDE Development**: Code development and deployment
- **Sensor Fusion Algorithm**: Complementary filter for accurate orientation
- **Real-time Processing**: Continuous data acquisition and processing
- **Cloud Connectivity**: MQTT protocol for ThingsBoard integration

### Simulation Environment
- **Wokwi Platform**: Online circuit simulation and testing
- **Virtual Hardware**: Test code without physical components
- **Interactive Interface**: Click-to-modify sensor values

## Required Components

### Hardware Components
| Component | Quantity | Purpose |
|-----------|----------|---------|
| ESP32 Development Board | 1 | Main microcontroller with WiFi |
| MPU6050 IMU Sensor | 1 | 6-axis motion sensing |
| SSD1306 OLED Display (128x64) | 1 | Real-time data display |
| Breadboard | 1 | Prototyping connections |
| Jumper Wires | 10-15 | Component connections |
| USB Cable | 1 | Programming and power |

### Software Tools
| Tool | Purpose |
|------|---------|
| Arduino IDE | Code development and upload |
| Wokwi Simulator | Circuit simulation and testing |
| ThingsBoard CE | IoT cloud platform |
| Git/GitHub | Version control and documentation |

### Cloud Environment
- **Platform**: ThingsBoard Community Edition
- **Protocol**: MQTT over WiFi
- **Data Format**: JSON telemetry messages
- **Features**: Real-time dashboards, device management, data storage

## Circuit Connections

```
ESP32 Connections:
==================

MPU6050 IMU Sensor:
VCC  --> 3.3V
GND  --> GND
SCL  --> GPIO 22 (I2C Clock)
SDA  --> GPIO 21 (I2C Data)

OLED Display (SSD1306):
VCC  --> 3.3V
GND  --> GND
SCL  --> GPIO 22 (I2C Clock) [Shared]
SDA  --> GPIO 21 (I2C Data)  [Shared]
```

## Code Implementation

### Key Features
- **Sensor Calibration**: Automatic error correction during startup
- **Complementary Filter**: Combines accelerometer and gyroscope data
- **Real-time Display**: Updates OLED every 100ms
- **Cloud Transmission**: Sends data to ThingsBoard every 1 second
- **Error Handling**: Connection monitoring and recovery

### Algorithm Flow
1. **Initialization**: Setup I2C, sensors, display, and WiFi
2. **Calibration**: Calculate sensor error offsets
3. **Data Acquisition**: Read accelerometer and gyroscope values
4. **Sensor Fusion**: Apply complementary filter algorithm
5. **Display Update**: Show current orientation on OLED
6. **Cloud Transmission**: Send telemetry data via MQTT

## Wokwi Simulation

The project includes a Wokwi simulation that allows testing without physical hardware:

1. **Access**: Visit wokwi.com and create new project
2. **Setup**: Import the diagram.json and sketch.ino files
3. **Interaction**: Click on MPU6050 sensor to modify values
4. **Observation**: Watch real-time updates on the OLED display

## ThingsBoard Setup

1. **Account Creation**: Register at demo.thingsboard.io
2. **Device Registration**: Create new device and obtain access token
3. **Dashboard Configuration**: Setup visualization widgets
4. **Data Monitoring**: View real-time telemetry data

## Implementation Steps

### Phase 1: Hardware Assembly
1. Connect components according to circuit diagram
2. Verify connections and power supply
3. Test basic connectivity

### Phase 2: Software Development
1. Install required Arduino libraries
2. Upload and test basic sensor reading code
3. Implement OLED display functionality
4. Add sensor fusion algorithm

### Phase 3: Cloud Integration
1. Setup WiFi connectivity
2. Configure ThingsBoard connection
3. Implement MQTT data transmission
4. Test end-to-end functionality

### Phase 4: Testing and Validation
1. Calibrate sensors in different orientations
2. Verify display accuracy
3. Test cloud connectivity and data flow
4. Document performance metrics

## Expected Outcomes

- **Real-time Monitoring**: Live display of roll, pitch, yaw angles
- **Cloud Visualization**: Remote access to orientation data
- **Educational Value**: Complete IoT development experience
- **Scalability**: Foundation for more complex motion monitoring systems

## Future Enhancements

- **Magnetometer Integration**: Add compass functionality
- **Data Logging**: Store historical movement patterns
- **Mobile App**: Dedicated smartphone interface
- **Machine Learning**: Pattern recognition and prediction
- **Multi-device Network**: Monitor multiple objects simultaneously

## Documentation Files

- `iot_position_monitor.ino` - Complete ESP32 Arduino code
- `wokwi_sketch.ino` - Simplified simulation code
- `wokwi_diagram.json` - Wokwi circuit configuration
- `hardware_components.csv` - Component list
- `software_tools.csv` - Software requirements
- `circuit_connections.txt` - Wiring guide

## Demo Video Script

1. **Introduction**: Project overview and objectives
2. **Hardware Setup**: Component connections and assembly
3. **Code Explanation**: Key algorithms and features
4. **Wokwi Simulation**: Online testing demonstration
5. **Real Hardware Test**: Live sensor data and OLED display
6. **Cloud Integration**: ThingsBoard dashboard demonstration
7. **Conclusion**: Results and future possibilities

---
*This project demonstrates practical IoT development skills including sensor integration, real-time processing, cloud connectivity, and comprehensive documentation.*
"""

with open('PROJECT_DOCUMENTATION.md', 'w') as f:
    f.write(documentation)

print("All project files generated successfully!")
print("\nGenerated Files:")
print("=" * 40)
print("📄 Documentation:")
print("   ✓ PROJECT_DOCUMENTATION.md")
print("   ✓ circuit_connections.txt")
print("   ✓ hardware_components.csv")
print("   ✓ software_tools.csv")
print("\n💻 Code Files:")
print("   ✓ iot_position_monitor.ino (Full ESP32 code)")
print("   ✓ wokwi_sketch.ino (Simulation code)")
print("\n🔧 Simulation:")
print("   ✓ wokwi_diagram.json (Circuit configuration)")
print("\n📊 Diagrams:")
print("   ✓ iot_flowchart.png")
print("   ✓ iot_architecture.png")

print("\n\n🚀 Next Steps:")
print("1. Upload wokwi files to wokwi.com for simulation")
print("2. Assemble hardware according to circuit_connections.txt")
print("3. Update WiFi credentials in iot_position_monitor.ino")
print("4. Setup ThingsBoard account and update device token")
print("5. Test and demonstrate the system")

# Create a simple GitHub repository structure
github_structure = """
IoT-Position-Monitoring-System/
├── README.md
├── docs/
│   ├── PROJECT_DOCUMENTATION.md
│   ├── circuit_connections.txt
│   ├── hardware_components.csv
│   └── software_tools.csv
├── src/
│   ├── iot_position_monitor.ino
│   └── libraries_required.txt
├── simulation/
│   ├── wokwi_sketch.ino
│   ├── wokwi_diagram.json
│   └── simulation_guide.md
├── images/
│   ├── iot_flowchart.png
│   ├── iot_architecture.png
│   ├── circuit_diagram.png
│   └── demo_screenshots/
├── demo/
│   ├── demo_video.mp4
│   └── demo_script.md
└── LICENSE
"""

with open('github_structure.txt', 'w') as f:
    f.write("Suggested GitHub Repository Structure:\n")
    f.write("=" * 40 + "\n")
    f.write(github_structure)

print("\n📁 GitHub repository structure saved to github_structure.txt")