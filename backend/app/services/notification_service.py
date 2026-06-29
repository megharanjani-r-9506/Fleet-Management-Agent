import os
import resend
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

RECEIVER_EMAIL = os.getenv("EMAIL_RECEIVER")



def send_email(subject, message):

    try:
        resend.Emails.send({
            "from": "Fleet AI <onboarding@resend.dev>",
            "to": RECEIVER_EMAIL,
            "subject": subject,
            "text": message
        })

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

if __name__ == "__main__":
    send_email(
        "Fleet AI Test",
        "Hello! This is a test email from Fleet AI."
    )