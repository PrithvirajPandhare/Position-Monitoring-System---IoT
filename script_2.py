# Create comprehensive project data structure
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
        {"name": "ESP32 Development Board", "quantity": 1, "purpose": "Main microcontroller"},
        {"name": "MPU6050 IMU Sensor", "quantity": 1, "purpose": "6-axis motion sensing"},
        {"name": "SSD1306 OLED Display (128x64)", "quantity": 1, "purpose": "Real-time data display"},
        {"name": "Breadboard", "quantity": 1, "purpose": "Prototyping connections"},
        {"name": "Jumper Wires", "quantity": "Set", "purpose": "Component connections"},
        {"name": "USB Cable", "quantity": 1, "purpose": "Programming and power"},
        {"name": "Power Supply (Optional)", "quantity": 1, "purpose": "Standalone operation"}
    ],
    
    "software_tools": [
        {"name": "Arduino IDE", "purpose": "Code development and upload"},
        {"name": "Wokwi Simulator", "purpose": "Circuit simulation and testing"},
        {"name": "ThingsBoard", "purpose": "IoT cloud platform"},
        {"name": "Git/GitHub", "purpose": "Version control and documentation"},
        {"name": "Libraries", "list": ["Wire.h", "Adafruit_MPU6050.h", "Adafruit_SSD1306.h", "WiFi.h", "PubSubClient.h"]}
    ],
    
    "cloud_environment": {
        "platform": "ThingsBoard Community Edition",
        "features": ["Device management", "Real-time dashboards", "Data visualization", "Telemetry storage"],
        "connectivity": "MQTT protocol over WiFi",
        "data_format": "JSON telemetry messages"
    }
}

# Create a detailed component table
import pandas as pd

# Hardware components table
hw_df = pd.DataFrame(project_data["hardware_components"])
print("HARDWARE COMPONENTS:")
print("=" * 50)
print(hw_df.to_string(index=False))
print("\n")

# Software tools table
sw_df = pd.DataFrame(project_data["software_tools"])
print("SOFTWARE TOOLS:")
print("=" * 50)
for idx, row in sw_df.iterrows():
    print(f"• {row['name']}: {row['purpose']}")
    if 'list' in row and pd.notna(row['list']):
        for lib in row['list']:
            print(f"  - {lib}")
print("\n")

# Save project data to CSV
hw_df.to_csv('hardware_components.csv', index=False)
sw_df.to_csv('software_tools.csv', index=False)

print("Files created:")
print("- hardware_components.csv")
print("- software_tools.csv")
print("- iot_flowchart.png")
print("- iot_architecture.png")