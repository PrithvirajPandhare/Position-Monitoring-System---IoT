# IoT Position and Orientation Monitoring System

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
