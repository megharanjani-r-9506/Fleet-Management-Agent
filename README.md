# Fleet-Management-Agent
An Agentic AI system that monitors fleet vehicle health, predicts potential failures, and recommends preventive maintenance actions to reduce downtime and operational costs.

//to reset slots
python -c "from app.database.db import get_connection; c=get_connection(); cur=c.cursor(); cur.execute('DELETE FROM service_bookings'); cur.execute('UPDATE service_slots SET available = 1'); c.commit(); c.close(); print('reset complete')"

// to view slots
 python -c "from app.database.db import get_connection; c=get_connection(); cur=c.cursor(); cur.execute('SELECT service_date, service_time, available FROM service_slots'); print(cur.fetchall()); c.close()"           