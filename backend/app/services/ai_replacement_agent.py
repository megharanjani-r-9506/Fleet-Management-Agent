import os
import json

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def choose_replacement_vehicle(
    vehicle_id,
    risk_level,
    delivery_date,
    candidates
):

    prompt = f"""
You are an AI Fleet Replacement Agent.

A vehicle requires maintenance and must be removed from service.

Vehicle:
{vehicle_id}

Risk Level:
{risk_level}

Delivery Date:
{delivery_date}

Candidate Vehicles:
{json.dumps(candidates, indent=2)}

Your objectives:

Minimize delivery disruption.
Maintain fleet availability.
Minimize operational risk.
Avoid creating future scheduling conflicts.
Balance workload across the fleet.

Candidate vehicle data includes workload and future commitments.

Evaluate all candidates and choose the best replacement vehicle.

Return ONLY valid JSON:

{{
"vehicle_id": "",
"confidence": 0,
"reason": ""
}}
"""

    response = model.generate_content(prompt)

    result = response.text.strip()

    # Remove markdown if Gemini adds it
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:
        return json.loads(result)

    except Exception as e:

        print(
            f"[AI] JSON Parse Error: {e}"
        )

        print(
            f"[AI] Raw Response: {result}"
        )

        # Safe fallback
        return {
            "vehicle_id": candidates[0]["vehicle_id"],
            "reason": "Fallback selection due to parsing error."
        }

if __name__ == "__main__":

    candidates = [
        {
            "vehicle_id": "TRK001",
            "future_deliveries": 3,
            "maintenance_booked": False,
            "risk_level": "Monitor"
        },
        {
            "vehicle_id": "TRK004",
            "future_deliveries": 0,
            "maintenance_booked": False,
            "risk_level": "Healthy"
        },
        {
            "vehicle_id": "TRK005",
            "future_deliveries": 0,
            "maintenance_booked": True,
            "risk_level": "Maintenance Required"
        }
    ]

    result = choose_replacement_vehicle(
        vehicle_id="TRK003",
        risk_level="Critical",
        delivery_date="2026-06-21",
        candidates=candidates
    )

    print(result)