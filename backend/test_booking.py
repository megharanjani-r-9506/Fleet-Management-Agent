from app.database.db import get_connection

c = get_connection()
cur = c.cursor()

cur.execute("""
INSERT INTO maintenance_schedule 
(vehicle_id, risk_level, recommendation, priority, status)
VALUES ('TEST_SLOT','Critical','Test booking','High','Pending')
""")

c.commit()
c.close()

print("Inserted")