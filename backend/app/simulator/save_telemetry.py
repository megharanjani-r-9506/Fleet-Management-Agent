from app.database.db import get_connection


def save_telemetry(data):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO telemetry (
            vehicle_id,
            ambient_temp,
            engine_temp,
            engine_rpm,
            engine_load,
            operating_hours,
            mileage
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["vehicle_id"],
            data["ambient_temp"],
            data["engine_temp"],
            data["engine_rpm"],
            data["engine_load"],
            data["operating_hours"],
            data["mileage"]
        ))

        conn.commit()

    except Exception as e:
        print("Telemetry save error:", e)

    finally:
        conn.close()