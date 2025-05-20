import sqlite3

def init_db():
    # Connect to (or create) the database
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()
    
    # Create sensor_data table with all sensor fields
    c.execute('''CREATE TABLE IF NOT EXISTS sensor_data
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  timestamp TEXT NOT NULL,
                  air_temp REAL NOT NULL,
                  humidity REAL NOT NULL,
                  soil_moisture_1 REAL NOT NULL,
                  soil_moisture_2 REAL NOT NULL,
                  soil_moisture_3 REAL NOT NULL,
                  soil_temp_1 REAL NOT NULL,
                  soil_temp_2 REAL NOT NULL,
                  soil_temp_3 REAL NOT NULL,
                  light REAL NOT NULL)''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == "__main__":
    init_db()