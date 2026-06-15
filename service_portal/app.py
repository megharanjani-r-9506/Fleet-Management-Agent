import streamlit as st
from db_reader import get_service_slots, get_bookings

st.set_page_config(
    page_title="Service Booking Portal",
    layout="wide"
)

st.title("🔧 Fleet Service Booking Portal")

slots_df = get_service_slots()
bookings_df = get_bookings()

st.subheader("Available Service Slots")

st.dataframe(
    slots_df,
    use_container_width=True
)

st.divider()

st.subheader("Current Bookings")

st.dataframe(
    bookings_df,
    use_container_width=True
)