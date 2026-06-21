# Fleet-Management-Agent
An Agentic AI system that monitors fleet vehicle health, predicts potential failures, and recommends preventive maintenance actions to reduce downtime and operational costs.

//to reset slots
python -c "from app.database.db import get_connection; c=get_connection(); cur=c.cursor(); cur.execute('DELETE FROM service_bookings'); cur.execute('UPDATE service_slots SET available = 1'); c.commit(); c.close(); print('reset complete')"

// to view slots
 python -c "from app.database.db import get_connection; c=get_connection(); cur=c.cursor(); cur.execute('SELECT service_date, service_time, available FROM service_slots'); print(cur.fetchall()); c.close()"           

// to run frontend
 streamlit run app.py  

// to run backend
 uvicorn app.main:app --reload --port 8000          

// to run simulator to generate-data
 python -m app.simulator.generate_data                                                                          
 // to run the agent
 python -m app.agent.fleet_graph


System explained in simple terms (no jargon):

Fleet Management System — What it does
1. Vehicle health monitoring

System continuously checks each vehicle and assigns a status like:

Healthy
Monitor
Maintenance Required
Critical

👉 This tells you which vehicles are safe and which need attention.

2. Maintenance scheduling (auto system)

When a vehicle needs maintenance:

The system automatically finds a service slot
Books it without manual work
Marks it as “Booked” in database

👉 No manual scheduling needed.

3. Smart slot allocation (capacity-aware)

System:

Checks available workshop slots
Avoids overbooking a day
Distributes vehicles across multiple days

👉 Ensures workshop is never overloaded.

4. Delivery conflict detection

Before booking maintenance, it checks:

Does this vehicle have a delivery scheduled?

If YES:

It detects a conflict
Decides what to do next
5. Replacement vehicle system

If a vehicle has a delivery + maintenance conflict:

System searches for another available truck
If found → delivery is reassigned
If not → delivery is held

👉 Prevents delivery failure.

6. Decision engine (AI brain of system)

Your system automatically decides:

Should maintenance proceed?
Should delivery be moved?
Should delivery be stopped?
Should maintenance be delayed?

👉 This is the “thinking brain” of your system.

7. Universal conflict engine

Before booking anything, it checks:

maintenance conflict
delivery conflict
scheduling conflicts

👉 Prevents double-booking or bad scheduling.

8. Priority-based handling

System gives priority like:

Critical (urgent)
Maintenance Required
Monitor
Healthy

👉 Critical vehicles are handled first.

9. Automatic decision logging

Every action is saved:

Why a decision was made
What happened to the vehicle
What action was taken

👉 You get full traceability.

10. Notifications system

System alerts managers when:

Delivery is reassigned
Delivery is held
Conflict is detected

👉 So humans stay informed automatically.

11. Dashboard (visual control panel)

You can see:

Vehicle health
Maintenance status
Bookings
Deliveries
AI decisions
Slot utilization

👉 Full system visibility in one place.


----------------------------------
Test cases
---------------------------------

1. Test Normal Maintenance Booking

from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("DELETE FROM maintenance_schedule WHERE vehicle_id='TRK003'")

cur.execute("""
INSERT INTO maintenance_schedule
(vehicle_id,risk_level,recommendation,priority,status)
VALUES
('TRK003','Maintenance Required',
'Routine Maintenance','Medium','Pending')
""")

conn.commit()
conn.close()

print("TEST 1 CREATED")
print("Expected:")
print("- Slot allocated")
print("- Booking created")
print("- Status -> Booked")

2. Test Critical Vehicle Reassignment

from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("DELETE FROM maintenance_schedule")
cur.execute("DELETE FROM delivery_schedule")

cur.execute("""
INSERT INTO delivery_schedule
(vehicle_id,delivery_date,route,status)
VALUES
('CRIT003','2026-06-20','Mumbai Route','Scheduled')
""")

cur.execute("""
INSERT INTO maintenance_schedule
(vehicle_id,risk_level,recommendation,priority,status)
VALUES
('CRIT003','Critical',
'Immediate Maintenance','High','Pending')
""")

conn.commit()
conn.close()

print("TEST 2 CREATED")
print("Expected:")
print("- Delivery conflict")
print("- Replacement found")
print("- Delivery reassigned")

3. Test Hold Delivery

from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("DELETE FROM maintenance_schedule")
cur.execute("DELETE FROM delivery_schedule")

delivery_date = "2026-06-20"

vehicles = [
    "CRIT003",
    "TRK001",
    "TRK002",
    "TRK003",
    "TRK004",
    "TRK005"
]

for vehicle in vehicles:

    cur.execute("""
    INSERT INTO delivery_schedule
    (vehicle_id,delivery_date,route,status)
    VALUES (?,?,?,?)
    """, (
        vehicle,
        delivery_date,
        f"Route-{vehicle}",
        "Scheduled"
    ))

cur.execute("""
INSERT INTO maintenance_schedule
(vehicle_id,risk_level,recommendation,priority,status)
VALUES
('CRIT003','Critical',
'Immediate Maintenance','High','Pending')
""")

conn.commit()
conn.close()

print("TEST 3 CREATED")
print("Expected:")
print("- No replacement vehicle")
print("- Hold Delivery decision")

4. Test Maintenance Required With Delivery

from app.database.db import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("DELETE FROM maintenance_schedule")

cur.execute("""
INSERT INTO delivery_schedule
(vehicle_id,delivery_date,route,status)
VALUES
('TRK005','2026-06-20','Chennai Route','Scheduled')
""")

cur.execute("""
INSERT INTO maintenance_schedule
(vehicle_id,risk_level,recommendation,priority,status)
VALUES
('TRK005',
'Maintenance Required',
'Engine Service',
'Medium',
'Pending')
""")

conn.commit()
conn.close()

print("TEST 4 CREATED")
print("Expected:")
print("- Schedule After Delivery")
print("- No immediate booking")

// reset db
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