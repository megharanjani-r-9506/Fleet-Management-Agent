import plotly.express as px
import streamlit as st

from api_client import (
    get_bookings,
    get_deliveries,
    get_maintenance,
    get_predictions,
    get_service_slots,
    get_vehicles,
    get_decisions,
    get_notifications , 
    generate_telemetry,  
    reset_demo,
    run_ai_agents
)

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Fleet Maintenance Dashboard",
    layout="wide"
)

st.title("🚚 AI Fleet Maintenance Management System")

button1, button2, button3 = st.columns(3)

# -----------------------------
# RESET DEMO
# -----------------------------
with button1:

    if st.button("🔄 Reset Demo", use_container_width=True):

        response = reset_demo()

        if response.status_code == 200:
            st.success("Demo reset successfully!")
            st.rerun()
        else:
            st.error("Reset failed.")

# -----------------------------
# GENERATE TELEMETRY
# -----------------------------
with button2:

    if st.button("🚚 Generate Telemetry", use_container_width=True):

        response = generate_telemetry()

        if response.status_code == 200:
            st.success("Telemetry generated successfully!")
            st.rerun()
        else:
            st.error("Telemetry generation failed.")

# -----------------------------
# RUN AI AGENTS
# -----------------------------
with button3:

    if st.button("🧠 Run AI Agents", use_container_width=True):

        response = run_ai_agents()

        if response.status_code == 200:
            st.success("AI Agents executed successfully!")
            st.rerun()
        else:
            st.error("Failed to execute AI Agents.")


#-----------------------------
# LOAD DATA
# -----------------------------
vehicles_df = get_vehicles()
predictions_df = get_predictions()
maintenance_df = get_maintenance()
bookings_df = get_bookings()
deliveries_df = get_deliveries()
slots_df = get_service_slots()
decisions_df = get_decisions()
notifications_df = get_notifications()   # ✅ FIXED (was missing usage)

# -----------------------------
# SAFETY CHECK
# -----------------------------
if predictions_df is None or predictions_df.empty:
    st.warning("No prediction data available")
    st.stop()

# -----------------------------
# LATEST STATE PER VEHICLE
# -----------------------------
latest_predictions = (
    predictions_df
    .sort_values("id")
    .groupby("vehicle_id", as_index=False)
    .tail(1)
)

# -----------------------------
# KPI CALCULATIONS
# -----------------------------
total_vehicles = len(vehicles_df)

healthy_count = (latest_predictions["risk_level"] == "Healthy").sum()
monitor_count = (latest_predictions["risk_level"] == "Monitor").sum()
maintenance_count = (latest_predictions["risk_level"] == "Maintenance Required").sum()
critical_count = (latest_predictions["risk_level"] == "Critical").sum()

booking_count = len(bookings_df) if bookings_df is not None else 0

# -----------------------------
# KPI UI
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Vehicles", total_vehicles)
col2.metric("Healthy", healthy_count)
col3.metric("Monitor", monitor_count)
col4.metric("Maintenance", maintenance_count)
col5.metric("Bookings", booking_count)

st.divider()

# -----------------------------
# CHARTS ROW 1
# -----------------------------
chart1, chart2 = st.columns(2)

with chart1:
    st.subheader("Fleet Risk Distribution")

    risk_chart = px.pie(
        latest_predictions,
        names="risk_level",
        title="Current Fleet Status"
    )

    st.plotly_chart(risk_chart, use_container_width=True)

with chart2:
    st.subheader("Maintenance Priority")

    if maintenance_df is not None and not maintenance_df.empty and "priority" in maintenance_df.columns:

        priority_counts = (
            maintenance_df["priority"]
            .value_counts()
            .reset_index()
        )

        priority_counts.columns = ["priority", "count"]

        priority_chart = px.bar(
            priority_counts,
            x="priority",
            y="count",
            title="Maintenance Priority Distribution"
        )

        st.plotly_chart(priority_chart, use_container_width=True)

    else:
        st.info("No maintenance data available")

# -----------------------------
# CHARTS ROW 2
# -----------------------------
chart3, chart4 = st.columns(2)

with chart3:
    st.subheader("Health Score Trend")

    trend_chart = px.line(
        predictions_df.sort_values("id"),
        x="predicted_at",
        y="health_score",
        color="vehicle_id",
        markers=True
    )

    st.plotly_chart(trend_chart, use_container_width=True)

with chart4:
    st.subheader("Failure Probability Trend")

    failure_chart = px.line(
        predictions_df.sort_values("id"),
        x="predicted_at",
        y="failure_probability",
        color="vehicle_id",
        markers=True
    )

    st.plotly_chart(failure_chart, use_container_width=True)

# -----------------------------
# SERVICE SLOT UTILIZATION
# -----------------------------
st.subheader("Service Slot Utilization")

if slots_df is not None and not slots_df.empty and "available" in slots_df.columns:

    available_slots = len(slots_df[slots_df["available"] == 1])
    booked_slots = len(slots_df[slots_df["available"] == 0])

    slot_chart = px.pie(
        names=["Booked", "Available"],
        values=[booked_slots, available_slots],
        hole=0.55,
        title="Workshop Capacity"
    )

    st.plotly_chart(slot_chart, use_container_width=True)

else:
    st.info("No service slot data available")

# -----------------------------
# DELIVERY OVERVIEW
# -----------------------------
st.subheader("Delivery Assignments")

if deliveries_df is not None and not deliveries_df.empty and "vehicle_id" in deliveries_df.columns:

    delivery_chart = px.bar(
        deliveries_df,
        x="vehicle_id",
        color="route",
        title="Scheduled Deliveries"
    )

    st.plotly_chart(delivery_chart, use_container_width=True)

else:
    st.info("No delivery data available")

# -----------------------------
# 🧠 AGENT DECISIONS
# -----------------------------
st.subheader("🧠 AI Agent Decisions")

if decisions_df is not None and not decisions_df.empty:

    st.dataframe(
        decisions_df.sort_values("created_at", ascending=False),
        use_container_width=True
    )

    st.subheader("Decision Distribution")

    decision_chart = px.histogram(
        decisions_df,
        x="decision",
        title="Agent Decision Types"
    )

    st.plotly_chart(decision_chart, use_container_width=True)

else:
    st.info("No agent decisions available")

# -----------------------------
# 🔔 NOTIFICATIONS (NEW + FIXED)
# -----------------------------
st.subheader("🔔 System Notifications")

if notifications_df is not None and not notifications_df.empty:

    st.dataframe(
        notifications_df.sort_values("created_at", ascending=False),
        use_container_width=True
    )

    st.subheader("Notification Types")

    notif_chart = px.histogram(
        notifications_df,
        x="title",
        title="Notification Summary"
    )

    st.plotly_chart(notif_chart, use_container_width=True)

else:
    st.info("No notifications available")

# -----------------------------
# TABLES
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Latest Vehicle Status",
    "Maintenance Schedule",
    "Service Bookings",
    "Delivery Schedule"
])

with tab1:
    st.dataframe(latest_predictions, use_container_width=True)

with tab2:
    st.dataframe(maintenance_df, use_container_width=True)

with tab3:
    st.dataframe(bookings_df, use_container_width=True)

with tab4:
    st.dataframe(deliveries_df, use_container_width=True)