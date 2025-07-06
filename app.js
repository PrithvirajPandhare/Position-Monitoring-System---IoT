// IoT Position and Orientation Monitoring System
// Real-time data simulation and visualization

class IoTDashboard {
    constructor() {
        // Initialize sensor data
        this.sensorData = {
            roll: 0,
            pitch: 0,
            yaw: 0,
            accelX: 0,
            accelY: 0,
            accelZ: 9.81,
            gyroX: 0,
            gyroY: 0,
            gyroZ: 0,
            temperature: 25.4
        };

        // System status
        this.systemStatus = {
            deviceOnline: true,
            wifiConnected: true,
            cloudConnected: true,
            isMonitoring: true,
            dataRate: 10,
            batteryLevel: 85,
            uptime: 3600,
            totalSamples: 36000
        };

        // Animation and timing
        this.updateInterval = null;
        this.chartUpdateInterval = null;
        this.timeAccumulator = 0;
        
        // Chart data storage
        this.historicalData = {
            labels: [],
            roll: [],
            pitch: [],
            yaw: []
        };

        // Initialize the dashboard
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeChart();
        this.startDataSimulation();
        this.updateTimestamp();
        this.updateSystemInfo();
        
        // Start real-time updates
        setInterval(() => this.updateTimestamp(), 1000);
        setInterval(() => this.updateSystemStats(), 5000);
    }

    setupEventListeners() {
        // Control buttons
        document.getElementById('startStopBtn').addEventListener('click', () => {
            this.toggleMonitoring();
        });

        document.getElementById('resetBtn').addEventListener('click', () => {
            this.resetData();
        });

        document.getElementById('exportBtn').addEventListener('click', () => {
            this.exportData();
        });

        document.getElementById('calibrateBtn').addEventListener('click', () => {
            this.startCalibration();
        });

        // Time range selector for chart
        document.getElementById('timeRange').addEventListener('change', (e) => {
            this.updateChartTimeRange(e.target.value);
        });
    }

    startDataSimulation() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }

        this.updateInterval = setInterval(() => {
            if (this.systemStatus.isMonitoring) {
                this.generateRealisticsensorData();
                this.updateUI();
                this.update3DVisualization();
                this.updateHistoricalData();
            }
        }, 100); // 10 Hz update rate
    }

    generateRealisticsensorData() {
        const time = this.timeAccumulator += 0.1;
        
        // Generate realistic orientation data with smooth movements
        this.sensorData.roll = 30 * Math.sin(time * 0.3) + 5 * Math.sin(time * 1.2) + this.addNoise(2);
        this.sensorData.pitch = 25 * Math.cos(time * 0.25) + 3 * Math.cos(time * 1.5) + this.addNoise(2);
        this.sensorData.yaw = 45 * Math.sin(time * 0.2) + 10 * Math.sin(time * 0.8) + this.addNoise(3);

        // Clamp orientation values to realistic ranges
        this.sensorData.roll = Math.max(-90, Math.min(90, this.sensorData.roll));
        this.sensorData.pitch = Math.max(-90, Math.min(90, this.sensorData.pitch));
        this.sensorData.yaw = ((this.sensorData.yaw % 360) + 360) % 360;

        // Generate accelerometer data based on orientation
        const rollRad = this.sensorData.roll * Math.PI / 180;
        const pitchRad = this.sensorData.pitch * Math.PI / 180;
        
        this.sensorData.accelX = 9.81 * Math.sin(rollRad) + this.addNoise(0.5);
        this.sensorData.accelY = 9.81 * Math.sin(pitchRad) + this.addNoise(0.5);
        this.sensorData.accelZ = 9.81 * Math.cos(rollRad) * Math.cos(pitchRad) + this.addNoise(0.5);

        // Generate gyroscope data (angular velocity)
        this.sensorData.gyroX = 20 * Math.cos(time * 0.4) + this.addNoise(5);
        this.sensorData.gyroY = 15 * Math.sin(time * 0.6) + this.addNoise(5);
        this.sensorData.gyroZ = 10 * Math.sin(time * 0.3) + this.addNoise(5);

        // Temperature with slight variations
        this.sensorData.temperature = 25.4 + 2 * Math.sin(time * 0.05) + this.addNoise(0.2);

        // Update system stats
        this.systemStatus.totalSamples += 1;
    }

    addNoise(amplitude) {
        return (Math.random() - 0.5) * amplitude;
    }

    updateUI() {
        // Update orientation gauges
        this.updateGauge('roll', this.sensorData.roll, -90, 90);
        this.updateGauge('pitch', this.sensorData.pitch, -90, 90);
        this.updateGauge('yaw', this.sensorData.yaw, 0, 360);

        // Update accelerometer bars
        this.updateBar('accelX', this.sensorData.accelX, -20, 20);
        this.updateBar('accelY', this.sensorData.accelY, -20, 20);
        this.updateBar('accelZ', this.sensorData.accelZ, -20, 20);

        // Update gyroscope bars
        this.updateBar('gyroX', this.sensorData.gyroX, -100, 100);
        this.updateBar('gyroY', this.sensorData.gyroY, -100, 100);
        this.updateBar('gyroZ', this.sensorData.gyroZ, -100, 100);

        // Update temperature
        document.getElementById('temperatureValue').textContent = 
            this.sensorData.temperature.toFixed(1) + '°C';

        // Update orientation display values
        document.getElementById('rollDisplay').textContent = 
            this.sensorData.roll.toFixed(1) + '°';
        document.getElementById('pitchDisplay').textContent = 
            this.sensorData.pitch.toFixed(1) + '°';
        document.getElementById('yawDisplay').textContent = 
            this.sensorData.yaw.toFixed(1) + '°';

        // Update data rate
        document.getElementById('dataRate').textContent = 
            this.systemStatus.dataRate + ' Hz';
    }

    updateGauge(type, value, min, max) {
        const percentage = ((value - min) / (max - min)) * 100;
        const gauge = document.getElementById(type + 'Gauge');
        const valueElement = document.getElementById(type + 'Value');
        
        gauge.style.setProperty('--gauge-percent', percentage + '%');
        valueElement.textContent = value.toFixed(1) + '°';
    }

    updateBar(type, value, min, max) {
        const percentage = Math.abs(value) / Math.max(Math.abs(min), Math.abs(max)) * 100;
        const bar = document.getElementById(type + 'Bar');
        const valueElement = document.getElementById(type + 'Value');
        
        bar.style.width = Math.min(100, percentage) + '%';
        valueElement.textContent = value.toFixed(2);
    }

    update3DVisualization() {
        const cube = document.getElementById('orientationCube');
        const { roll, pitch, yaw } = this.sensorData;
        
        // Apply 3D rotation transform
        cube.style.transform = 
            `rotateX(${pitch}deg) rotateY(${yaw}deg) rotateZ(${roll}deg)`;
    }

    updateHistoricalData() {
        const now = new Date();
        const timeLabel = now.toLocaleTimeString();
        
        // Add new data point
        this.historicalData.labels.push(timeLabel);
        this.historicalData.roll.push(this.sensorData.roll);
        this.historicalData.pitch.push(this.sensorData.pitch);
        this.historicalData.yaw.push(this.sensorData.yaw);
        
        // Keep only last 60 data points (6 seconds at 10Hz)
        const maxPoints = 60;
        if (this.historicalData.labels.length > maxPoints) {
            this.historicalData.labels.shift();
            this.historicalData.roll.shift();
            this.historicalData.pitch.shift();
            this.historicalData.yaw.shift();
        }
        
        // Update chart every 10 data points
        if (this.historicalData.labels.length % 10 === 0) {
            this.updateChart();
        }
    }

    initializeChart() {
        const ctx = document.getElementById('orientationChart').getContext('2d');
        
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Roll (°)',
                    data: [],
                    borderColor: '#1FB8CD',
                    backgroundColor: 'rgba(31, 184, 205, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                }, {
                    label: 'Pitch (°)',
                    data: [],
                    borderColor: '#FFC185',
                    backgroundColor: 'rgba(255, 193, 133, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                }, {
                    label: 'Yaw (°)',
                    data: [],
                    borderColor: '#B4413C',
                    backgroundColor: 'rgba(180, 65, 60, 0.1)',
                    borderWidth: 2,
                    fill: false,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    intersect: false,
                    mode: 'index'
                },
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            padding: 20
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Time'
                        },
                        ticks: {
                            maxTicksLimit: 10
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Angle (degrees)'
                        },
                        min: -180,
                        max: 180
                    }
                },
                elements: {
                    point: {
                        radius: 0,
                        hoverRadius: 5
                    }
                }
            }
        });
    }

    updateChart() {
        if (!this.chart) return;
        
        this.chart.data.labels = [...this.historicalData.labels];
        this.chart.data.datasets[0].data = [...this.historicalData.roll];
        this.chart.data.datasets[1].data = [...this.historicalData.pitch];
        this.chart.data.datasets[2].data = [...this.historicalData.yaw];
        
        this.chart.update('none'); // No animation for real-time updates
    }

    updateTimestamp() {
        const now = new Date();
        document.getElementById('currentTime').textContent = 
            now.toLocaleString();
    }

    updateSystemInfo() {
        document.getElementById('deviceId').textContent = 'ESP32-001';
        document.getElementById('firmwareVersion').textContent = '1.0.0';
        document.getElementById('batteryLevel').textContent = 
            this.systemStatus.batteryLevel + '%';
        document.getElementById('totalSamples').textContent = 
            this.systemStatus.totalSamples.toLocaleString();
        document.getElementById('packetsPerMin').textContent = 
            (this.systemStatus.dataRate * 60).toLocaleString();
        
        // Update uptime
        this.systemStatus.uptime += 5;
        const hours = Math.floor(this.systemStatus.uptime / 3600);
        const minutes = Math.floor((this.systemStatus.uptime % 3600) / 60);
        document.getElementById('uptime').textContent = `${hours}h ${minutes}m`;
    }

    updateSystemStats() {
        // Simulate occasional status changes
        if (Math.random() < 0.05) { // 5% chance
            this.simulateStatusChange();
        }
        
        // Update battery level (slowly decreasing)
        if (Math.random() < 0.1) {
            this.systemStatus.batteryLevel = Math.max(20, this.systemStatus.batteryLevel - 1);
        }
        
        this.updateSystemInfo();
    }

    simulateStatusChange() {
        const statusElements = [
            'deviceStatus',
            'connectionStatus', 
            'dataStreamStatus'
        ];
        
        const randomStatus = statusElements[Math.floor(Math.random() * statusElements.length)];
        const element = document.getElementById(randomStatus);
        const dot = element.querySelector('.status-dot');
        const label = element.querySelector('.status-label');
        
        // Temporarily change to warning state
        dot.className = 'status-dot status-dot--warning';
        label.textContent = 'Reconnecting...';
        
        // Return to normal after 2 seconds
        setTimeout(() => {
            dot.className = 'status-dot status-dot--success';
            switch (randomStatus) {
                case 'deviceStatus':
                    label.textContent = 'Device Online';
                    break;
                case 'connectionStatus':
                    label.textContent = 'ThingsBoard Connected';
                    break;
                case 'dataStreamStatus':
                    label.textContent = 'Data Stream Active';
                    break;
            }
        }, 2000);
    }

    toggleMonitoring() {
        this.systemStatus.isMonitoring = !this.systemStatus.isMonitoring;
        const button = document.getElementById('startStopBtn');
        const text = document.getElementById('startStopText');
        
        if (this.systemStatus.isMonitoring) {
            text.textContent = 'Stop Monitoring';
            button.className = 'btn btn--primary';
            this.startDataSimulation();
        } else {
            text.textContent = 'Start Monitoring';
            button.className = 'btn btn--secondary';
            if (this.updateInterval) {
                clearInterval(this.updateInterval);
            }
        }
    }

    resetData() {
        // Reset historical data
        this.historicalData = {
            labels: [],
            roll: [],
            pitch: [],
            yaw: []
        };
        
        // Reset sensor data to initial state
        this.sensorData = {
            roll: 0,
            pitch: 0,
            yaw: 0,
            accelX: 0,
            accelY: 0,
            accelZ: 9.81,
            gyroX: 0,
            gyroY: 0,
            gyroZ: 0,
            temperature: 25.4
        };
        
        // Reset system stats
        this.systemStatus.totalSamples = 0;
        this.timeAccumulator = 0;
        
        // Update UI
        this.updateUI();
        this.update3DVisualization();
        if (this.chart) {
            this.updateChart();
        }
        
        // Show feedback
        this.showNotification('Data reset successfully', 'success');
    }

    exportData() {
        const data = {
            timestamp: new Date().toISOString(),
            currentData: this.sensorData,
            historicalData: this.historicalData,
            systemStatus: this.systemStatus
        };
        
        const blob = new Blob([JSON.stringify(data, null, 2)], {
            type: 'application/json'
        });
        
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `iot-sensor-data-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showNotification('Data exported successfully', 'success');
    }

    startCalibration() {
        const button = document.getElementById('calibrateBtn');
        const status = document.getElementById('calibrationStatus');
        
        button.disabled = true;
        button.textContent = 'Calibrating...';
        status.textContent = 'In Progress';
        status.className = 'status status--warning';
        
        // Simulate calibration process
        setTimeout(() => {
            button.disabled = false;
            button.textContent = 'Recalibrate';
            status.textContent = 'Complete';
            status.className = 'status status--success';
            
            this.showNotification('Calibration completed', 'success');
        }, 3000);
    }

    updateChartTimeRange(range) {
        // This would typically filter historical data by time range
        // For demo purposes, we'll just show a notification
        this.showNotification(`Chart updated to show ${range}`, 'info');
    }

    showNotification(message, type = 'info') {
        // Create a simple notification system
        const notification = document.createElement('div');
        notification.className = `status status--${type}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 1000;
            padding: 12px 16px;
            border-radius: 6px;
            font-size: 14px;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        
        // Add animation styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.style.animation = 'slideIn 0.3s ease reverse';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new IoTDashboard();
});