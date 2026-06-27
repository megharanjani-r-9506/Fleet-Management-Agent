import os
import json

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("GEMINI_API_KEY:", os.getenv("GEMINI_API_KEY"))

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def choose_maintenance_slot(
    vehicle_id,
    risk_level,
    available_slots
):

    prompt = f"""
You are an AI Fleet Maintenance Scheduler.

Vehicle:
{vehicle_id}

Risk Level:
{risk_level}

Available Slots:
{json.dumps(available_slots, indent=2)}

Rules:

1. Critical vehicles should get earliest slot.
2. Maintenance Required vehicles should get an early slot.
3. Avoid unnecessary delays.
4. Choose exactly ONE slot.

Return ONLY JSON.

{{
    "slot_id": 0,
    "reason": ""
}}
"""

    response = model.generate_content(prompt)

    result = response.text.strip()

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return json.loads(result)

if __name__ == "__main__":

    slots = [
        {
            "slot_id": 1,
            "date": "2026-06-21",
            "time": "09:00"
        },
        {
            "slot_id": 2,
            "date": "2026-06-22",
            "time": "10:00"
        }
    ]

    result = choose_maintenance_slot(
        "TRK003",
        "Critical",
        slots
    )

    print(result)