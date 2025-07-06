# Create IoT System Architecture Diagram
fig, ax = plt.subplots(1, 1, figsize=(14, 10))
ax.set_xlim(0, 14)
ax.set_ylim(0, 10)
ax.axis('off')

# Define color scheme
device_color = '#4CAF50'
connectivity_color = '#2196F3'
cloud_color = '#FF9800'
app_color = '#9C27B0'

# Device Layer
device_rect = Rectangle((1, 7), 3, 2.5, facecolor=device_color, alpha=0.3, edgecolor='black')
ax.add_patch(device_rect)
ax.text(2.5, 8.7, 'DEVICE LAYER', ha='center', fontweight='bold', fontsize=12)
ax.text(2.5, 8.3, '• ESP32/Arduino', ha='center', fontsize=10)
ax.text(2.5, 8.0, '• MPU6050 IMU', ha='center', fontsize=10)
ax.text(2.5, 7.7, '• OLED Display', ha='center', fontsize=10)
ax.text(2.5, 7.4, '• Power Supply', ha='center', fontsize=10)

# Connectivity Layer
conn_rect = Rectangle((5.5, 7), 3, 2.5, facecolor=connectivity_color, alpha=0.3, edgecolor='black')
ax.add_patch(conn_rect)
ax.text(7, 8.7, 'CONNECTIVITY', ha='center', fontweight='bold', fontsize=12)
ax.text(7, 8.3, '• WiFi/Bluetooth', ha='center', fontsize=10)
ax.text(7, 8.0, '• I2C Protocol', ha='center', fontsize=10)
ax.text(7, 7.7, '• MQTT/HTTP', ha='center', fontsize=10)
ax.text(7, 7.4, '• Serial Comm', ha='center', fontsize=10)

# Cloud Layer
cloud_rect = Rectangle((10, 7), 3, 2.5, facecolor=cloud_color, alpha=0.3, edgecolor='black')
ax.add_patch(cloud_rect)
ax.text(11.5, 8.7, 'CLOUD LAYER', ha='center', fontweight='bold', fontsize=12)
ax.text(11.5, 8.3, '• ThingsBoard', ha='center', fontsize=10)
ax.text(11.5, 8.0, '• Data Storage', ha='center', fontsize=10)
ax.text(11.5, 7.7, '• Analytics', ha='center', fontsize=10)
ax.text(11.5, 7.4, '• Visualization', ha='center', fontsize=10)

# Data Processing Layer
proc_rect = Rectangle((3, 4.5), 8, 1.5, facecolor='#E0E0E0', alpha=0.5, edgecolor='black')
ax.add_patch(proc_rect)
ax.text(7, 5.7, 'DATA PROCESSING LAYER', ha='center', fontweight='bold', fontsize=12)
ax.text(7, 5.3, 'Sensor Fusion • Complementary Filter • Position Calculation • Real-time Analysis', ha='center', fontsize=10)

# Application Layer
app_rect = Rectangle((5.5, 2), 3, 1.5, facecolor=app_color, alpha=0.3, edgecolor='black')
ax.add_patch(app_rect)
ax.text(7, 3.2, 'APPLICATION', ha='center', fontweight='bold', fontsize=12)
ax.text(7, 2.8, '• Web Dashboard', ha='center', fontsize=10)
ax.text(7, 2.5, '• Mobile App', ha='center', fontsize=10)
ax.text(7, 2.2, '• Alerts/Notifications', ha='center', fontsize=10)

# User Interface
user_rect = Rectangle((5.5, 0.2), 3, 1, facecolor='#FFC107', alpha=0.3, edgecolor='black')
ax.add_patch(user_rect)
ax.text(7, 0.8, 'USER INTERFACE', ha='center', fontweight='bold', fontsize=12)
ax.text(7, 0.4, 'Real-time Monitoring & Control', ha='center', fontsize=10)

# Add arrows to show data flow
# Device to Connectivity
ax.annotate('', xy=(5.3, 8.2), xytext=(4.2, 8.2),
            arrowprops=dict(arrowstyle='->', lw=2, color='blue'))

# Connectivity to Cloud
ax.annotate('', xy=(9.8, 8.2), xytext=(8.7, 8.2),
            arrowprops=dict(arrowstyle='->', lw=2, color='blue'))

# Bidirectional data flow arrows
ax.annotate('', xy=(7, 6.8), xytext=(7, 6.2),
            arrowprops=dict(arrowstyle='->', lw=2, color='green'))
ax.annotate('', xy=(7, 4.3), xytext=(7, 3.7),
            arrowprops=dict(arrowstyle='->', lw=2, color='green'))
ax.annotate('', xy=(7, 1.8), xytext=(7, 1.4),
            arrowprops=dict(arrowstyle='->', lw=2, color='green'))

# Add feedback arrow
ax.annotate('', xy=(4.5, 2.7), xytext=(4.5, 7.5),
            arrowprops=dict(arrowstyle='->', lw=1.5, color='red', linestyle='dashed'))
ax.text(3.5, 5, 'Feedback\n& Control', ha='center', fontsize=9, color='red', rotation=90)

plt.title('IoT Position Monitoring System - Architecture Diagram', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('iot_architecture.png', dpi=300, bbox_inches='tight')
plt.show()