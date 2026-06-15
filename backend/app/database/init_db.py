from app.database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id TEXT PRIMARY KEY,
        vehicle_type TEXT,
        status TEXT
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS telemetry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    ambient_temp REAL,
    engine_temp REAL,
    engine_rpm REAL,
    engine_load REAL,
    operating_hours INTEGER,
    mileage REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
    
    cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    health_score REAL,
    failure_probability REAL,
    risk_level TEXT,
    predicted_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS maintenance_schedule (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id TEXT,
    risk_level TEXT,
    recommendation TEXT,
    priority TEXT,
    status TEXT
)
""")

    conn.commit()
    conn.close()

    print("Vehicles table created successfully!")

if __name__ == "__main__":
    create_tables()