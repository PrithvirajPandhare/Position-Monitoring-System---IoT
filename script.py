import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np

# Create flowchart for the code logic
fig, ax = plt.subplots(1, 1, figsize=(12, 16))
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis('off')

# Define flowchart shapes and connections
def draw_flowchart_box(ax, x, y, width, height, text, box_type='process'):
    if box_type == 'start_end':
        # Oval shape for start/end
        ellipse = patches.Ellipse((x + width/2, y + height/2), width, height, 
                                 facecolor='lightgreen', edgecolor='black')
        ax.add_patch(ellipse)
    elif box_type == 'decision':
        # Diamond shape for decision
        diamond = patches.Polygon([(x + width/2, y), (x + width, y + height/2), 
                                 (x + width/2, y + height), (x, y + height/2)],
                                facecolor='lightyellow', edgecolor='black')
        ax.add_patch(diamond)
    else:
        # Rectangle for process
        rect = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1",
                            facecolor='lightblue', edgecolor='black')
        ax.add_patch(rect)
    
    # Add text
    ax.text(x + width/2, y + height/2, text, ha='center', va='center', 
            fontsize=9, wrap=True)

def draw_arrow(ax, x1, y1, x2, y2):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', lw=1.5, color='black'))

# Draw flowchart elements
draw_flowchart_box(ax, 3.5, 18.5, 3, 1, 'START', 'start_end')
draw_arrow(ax, 5, 18.5, 5, 17.5)

draw_flowchart_box(ax, 2, 16.5, 6, 1, 'Initialize I2C Communication\nSetup MPU6050 & OLED Display')
draw_arrow(ax, 5, 16.5, 5, 15.5)

draw_flowchart_box(ax, 2, 14.5, 6, 1, 'Calibrate MPU6050 Sensor\nCalculate Error Values')
draw_arrow(ax, 5, 14.5, 5, 13.5)

draw_flowchart_box(ax, 2, 12.5, 6, 1, 'Display Initialization Message\non OLED Screen')
draw_arrow(ax, 5, 12.5, 5, 11.5)

# Main loop starts
draw_flowchart_box(ax, 2, 10.5, 6, 1, 'Read Accelerometer Data\n(AccX, AccY, AccZ)')
draw_arrow(ax, 5, 10.5, 5, 9.5)

draw_flowchart_box(ax, 2, 8.5, 6, 1, 'Calculate Roll & Pitch Angles\nfrom Accelerometer')
draw_arrow(ax, 5, 8.5, 5, 7.5)

draw_flowchart_box(ax, 2, 6.5, 6, 1, 'Read Gyroscope Data\n(GyroX, GyroY, GyroZ)')
draw_arrow(ax, 5, 6.5, 5, 5.5)

draw_flowchart_box(ax, 2, 4.5, 6, 1, 'Apply Complementary Filter\nFuse Gyro + Accel Data')
draw_arrow(ax, 5, 4.5, 5, 3.5)

draw_flowchart_box(ax, 2, 2.5, 6, 1, 'Update OLED Display\nShow Roll, Pitch, Yaw')
draw_arrow(ax, 5, 2.5, 5, 1.5)

draw_flowchart_box(ax, 2, 0.5, 6, 1, 'Send Data to Cloud\n(ThingsBoard/Serial)')

# Loop back arrow
draw_arrow(ax, 8.2, 1, 9, 1)
draw_arrow(ax, 9, 1, 9, 11)
draw_arrow(ax, 9, 11, 8.2, 11)

# Add loop label
ax.text(9.5, 6, 'MAIN\nLOOP', ha='center', va='center', fontsize=10, 
        bbox=dict(boxstyle="round,pad=0.3", facecolor='orange'))

plt.title('IoT Position Monitoring System - Code Flowchart', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('iot_flowchart.png', dpi=300, bbox_inches='tight')
plt.show()