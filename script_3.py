# Create comprehensive project data structure (fixed)
project_data = {
    "aim": """To design and implement a real-time IoT system for monitoring the position and 
orientation of objects using accelerometer and gyroscope sensors, with real-time data 
visualization on an OLED display and cloud-based monitoring capabilities.""",
    
    "problem_statement": """Traditional position and orientation monitoring systems often lack:
1. Real-time visualization capabilities
2. Cost-effective implementation for educational/research purposes
3. Cloud-based remote monitoring features
4. Accurate sensor fusion algorithms
5. User-friendly interfaces for data interpretation""",
    
    "scope": """This project encompasses:
- Hardware integration of MPU6050 IMU sensor with ESP32/Arduino
- Real-time data processing using complementary filter for sensor fusion
- OLED display for immediate visual feedback
- Cloud connectivity for remote monitoring via ThingsBoard
- Simulation environment using Wokwi for testing and validation
- Documentation and demonstration materials""",
    
    "hardware_components": [
        {"name": "ESP32 Development Board", "quantity": "1", "purpose": "Main microcontroller with WiFi"},
        {"name": "MPU6050 IMU Sensor", "quantity": "1", "purpose": "6-axis motion sensing (3-axis accelerometer + 3-axis gyroscope)"},
        {"name": "SSD1306 OLED Display (128x64)", "quantity": "1", "purpose": "Real-time data display via I2C"},
        {"name": "Breadboard", "quantity": "1", "purpose": "Prototyping connections"},
        {"name": "Jumper Wires (Male-to-Male)", "quantity": "10-15", "purpose": "Component connections"},
        {"name": "USB Cable (Micro-USB)", "quantity": "1", "purpose": "Programming and power supply"},
        {"name": "External Power Supply (Optional)", "quantity": "1", "purpose": "Standalone operation (5V/3.3V)"}
    ],
    
    "software_tools": [
        {"name": "Arduino IDE", "purpose": "Code development, compilation, and upload"},
        {"name": "Wokwi Online Simulator", "purpose": "Circuit simulation and code testing"},
        {"name": "ThingsBoard CE", "purpose": "IoT cloud platform for data visualization"},
        {"name": "Git/GitHub", "purpose": "Version control and project documentation"},
        {"name": "Arduino Libraries", "purpose": "Wire.h, Adafruit_MPU6050.h, Adafruit_SSD1306.h"},
        {"name": "WiFi Libraries", "purpose": "WiFi.h, PubSubClient.h for MQTT communication"}
    ]
}

# Create detailed component tables
import pandas as pd

# Hardware components table
hw_df = pd.DataFrame(project_data["hardware_components"])
print("HARDWARE COMPONENTS REQUIRED:")
print("=" * 60)
print(hw_df.to_string(index=False))
print("\n")

# Software tools table
sw_df = pd.DataFrame(project_data["software_tools"])
print("SOFTWARE TOOLS AND LIBRARIES:")
print("=" * 60)
print(sw_df.to_string(index=False))
print("\n")

# Cloud environment details
print("CLOUD ENVIRONMENT SETUP:")
print("=" * 60)
print("Platform: ThingsBoard Community Edition")
print("Protocol: MQTT over WiFi")
print("Data Format: JSON telemetry messages")
print("Features: Real-time dashboards, device management, data storage")
print("\n")

# Project scope breakdown
print("PROJECT SCOPE BREAKDOWN:")
print("=" * 60)
print("1. HARDWARE INTEGRATION")
print("   - ESP32 with MPU6050 sensor via I2C")
print("   - OLED display for real-time visualization")
print("   - Power management and connectivity")
print("\n2. SOFTWARE DEVELOPMENT")
print("   - Sensor calibration and data acquisition")
print("   - Complementary filter implementation")
print("   - Real-time display updates")
print("   - Cloud connectivity and data transmission")
print("\n3. SIMULATION AND TESTING")
print("   - Wokwi circuit simulation")
print("   - Code validation and debugging")
print("   - Performance optimization")
print("\n4. DOCUMENTATION")
print("   - Circuit diagrams and schematics")
print("   - Code documentation and flowcharts")
print("   - User manual and demo video")

# Save to CSV files
hw_df.to_csv('hardware_components.csv', index=False)
sw_df.to_csv('software_tools.csv', index=False)

print("\n\nFILES GENERATED:")
print("=" * 30)
print("✓ hardware_components.csv")
print("✓ software_tools.csv") 
print("✓ iot_flowchart.png")
print("✓ iot_architecture.png")