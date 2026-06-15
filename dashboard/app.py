import streamlit as st
from db_reader import get_predictions, get_maintenance

st.set_page_config(
    page_title="Fleet Maintenance Dashboard",
    layout="wide"
)

st.title("🚚 AI Fleet Maintenance Management System")

# Load data
df = get_predictions()
maintenance_df = get_maintenance()

# ======================
# Fleet Metrics
# ======================

total_vehicles = len(df)
critical_count = len(df[df["risk_level"] == "Critical"])
monitor_count = len(df[df["risk_level"] == "Monitor"])
healthy_count = len(df[df["risk_level"] == "Healthy"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vehicles", total_vehicles)
col2.metric("Critical", critical_count)
col3.metric("Monitor", monitor_count)
col4.metric("Healthy", healthy_count)

# ======================
# Predictions Section
# ======================

st.divider()

st.subheader("📊 Recent Vehicle Predictions")

st.dataframe(
    df,
    use_container_width=True
)

# ======================
# Maintenance Queue
# ======================

st.divider()

st.subheader("🔧 Maintenance Queue")

st.dataframe(
    maintenance_df,
    use_container_width=True
)