import sqlite3
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# Route to handle sensor data POST requests
@app.route('/api/sensor', methods=['POST'])
def receive_sensor_data():
    try:
        data = request.get_json()
        required_fields = ['air_temp', 'humidity', 'soil_moisture_1', 'soil_moisture_2', 
                          'soil_moisture_3', 'soil_temp_1', 'soil_temp_2', 'soil_temp_3', 'light']
        
        # Check for missing fields
        for field in required_fields:
            if field not in data or data[field] is None:
                return jsonify({'error': f'Missing or invalid {field}'}), 400
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn = sqlite3.connect('sensor_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO sensor_data 
                     (timestamp, air_temp, humidity, soil_moisture_1, soil_moisture_2, 
                      soil_moisture_3, soil_temp_1, soil_temp_2, soil_temp_3, light) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (timestamp, data['air_temp'], data['humidity'], 
                   data['soil_moisture_1'], data['soil_moisture_2'], data['soil_moisture_3'],
                   data['soil_temp_1'], data['soil_temp_2'], data['soil_temp_3'], data['light']))
        conn.commit()
        conn.close()
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to serve the web interface
@app.route('/')
def index():
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    c.execute('''SELECT timestamp, air_temp, humidity, soil_moisture_1, soil_moisture_2, 
                        soil_moisture_3, soil_temp_1, soil_temp_2, soil_temp_3, light 
                 FROM sensor_data ORDER BY timestamp DESC LIMIT 100''')
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)