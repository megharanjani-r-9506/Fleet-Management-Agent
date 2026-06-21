import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "megharanjanir@gmail.com"
SENDER_PASSWORD = "wgoe vxpo pbbl ravh"
RECEIVER_EMAIL = "rudhramegha9506@gmail.com"


def send_email(subject, message):

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        server.quit()

        print("[EMAIL] Sent successfully")

    except Exception as e:
        print("[EMAIL ERROR]", e)

def build_delivery_reassigned_email(
    vehicle_id,
    replacement_vehicle,
    route,
    delivery_date
):

    return f"""
🚚 DELIVERY REASSIGNED

Vehicle:
{vehicle_id}

Status:
A critical maintenance risk was detected.

Action Taken:
Delivery has been reassigned to {replacement_vehicle}.

Delivery Details:
• Route: {route}
• Delivery Date: {delivery_date}

System Status:
✓ Delivery reassigned successfully
✓ Customer commitment maintained
✓ Vehicle scheduled for maintenance
"""


def build_maintenance_email(
    vehicle_id
):

    return f"""
🛠️ MAINTENANCE APPROVED

Vehicle:
{vehicle_id}

Status:
Maintenance has been approved and scheduled.

Actions Taken:
✓ Vehicle removed from active service
✓ Maintenance booking created
✓ Fleet schedule updated

Recommendation:
Complete maintenance before returning the vehicle to operational duty.
"""


def build_delivery_hold_email(
    vehicle_id
):

    return f"""
⛔ DELIVERY HELD

Vehicle:
{vehicle_id}

Status:
No suitable replacement vehicle was available.

Action Required:
Fleet manager review recommended.

System Status:
✓ Delivery paused
✓ Alert generated
"""

def build_maintenance_deferred_email(
    vehicle_id
):

    return f"""
📅 MAINTENANCE DEFERRED

Vehicle:
{vehicle_id}

Status:
Maintenance has been temporarily deferred.

Reason:
An active delivery commitment must be completed before maintenance can begin.

System Status:
✓ Delivery retained
✓ Maintenance postponed
✓ Vehicle remains under monitoring
"""


def build_maintenance_delayed_email(
    vehicle_id
):

    return f"""
⚠️ MAINTENANCE DELAYED

Vehicle:
{vehicle_id}

Status:
Maintenance could not be scheduled immediately.

Action Required:
Fleet manager review recommended.

System Status:
✓ Vehicle flagged for attention
✓ Maintenance not yet scheduled
"""