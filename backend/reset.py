from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()

# Agent outputs
cur.execute("DELETE FROM agent_decisions")
cur.execute("DELETE FROM notifications")

# Maintenance workflow
cur.execute("DELETE FROM maintenance_schedule")
cur.execute("DELETE FROM service_bookings")

# Deliveries
cur.execute("DELETE FROM delivery_schedule")

# Predictions (optional)
cur.execute("DELETE FROM predictions")

# Make all service slots available again
cur.execute("""
UPDATE service_slots
SET available = 1
""")

conn.commit()
conn.close()

print("TEST ENVIRONMENT RESET")