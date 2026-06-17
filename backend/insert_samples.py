from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
INSERT INTO maintenance_schedule
(vehicle_id, risk_level, recommendation, priority, status)
VALUES
('TEST001', 'Critical', 'Immediate maintenance', 'High', 'Pending')
""")

cur.execute("""
INSERT INTO maintenance_schedule
(vehicle_id, risk_level, recommendation, priority, status)
VALUES
('TEST002', 'Maintenance Required', 'Schedule maintenance', 'Medium', 'Pending')
""")

cur.execute("""
INSERT INTO maintenance_schedule
(vehicle_id, risk_level, recommendation, priority, status)
VALUES
('TEST003', 'Monitor', 'Observe vehicle', 'Low', 'Pending')
""")

conn.commit()
conn.close()

print("Test records inserted")