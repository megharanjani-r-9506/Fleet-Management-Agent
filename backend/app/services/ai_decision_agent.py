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


def make_maintenance_decision(
    vehicle_id,
    risk_level,
    has_delivery,
    replacement_available,
    failure_probability,
    upcoming_delivery_count,
    replacement_vehicle_count
):

    prompt = f"""
You are an AI Fleet Operations Manager.

Fleet Situation:
- Vehicle ID: {vehicle_id}
- Risk Level: {risk_level}
- Failure Probability: {failure_probability}%
- Upcoming Deliveries: {upcoming_delivery_count}
- Replacement Vehicles Available: {replacement_vehicle_count}
- Has Immediate Delivery: {has_delivery}
- Replacement Available: {replacement_available}

Your objectives:
1. Ensure vehicle safety.
2. Minimize delivery disruption.
3. Minimize operational downtime.
4. Maintain fleet efficiency.

Decision Priority Rules:

1. Critical Risk + Immediate Delivery + Replacement Available
   -> Delivery Reassigned

2. Critical Risk + Immediate Delivery + No Replacement
   -> Hold Delivery

3. Critical Risk + No Delivery
   -> Schedule Maintenance

4. Maintenance Required + Immediate Delivery
   -> Schedule After Delivery

5. Maintenance Required + No Delivery
   -> Schedule Maintenance

6. Monitor or Healthy
   -> No Action Required

These rules have HIGH priority and should only be overridden if there is a strong operational reason.
You must choose ONE action:
- Delivery Reassigned
- Hold Delivery
- Schedule Maintenance
- Schedule After Delivery
- Maintenance Delayed
- No Action Required

Consider:
Failure Probability Guidelines:

    0-30%
    Low Risk

    31-60%
    Moderate Risk

    61-85%
    High Risk

    86-100%
    Critical Risk

    A moderate-risk vehicle may continue operating if delivery commitments are important and maintenance can safely be delayed.

    A high-risk vehicle should be considered for maintenance soon.

    A critical-risk vehicle should generally be removed from service immediately.
- Critical vehicles may require immediate action.
- Deliveries are important business commitments.
- Replacement availability reduces disruption.
- Delaying maintenance may increase future risk.
- Holding deliveries impacts customer commitments.

Evaluate the situation as a real fleet operations manager.

Return ONLY valid JSON:
{{
  "decision": "",
  "confidence": 0,
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

    pass
