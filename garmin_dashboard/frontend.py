import streamlit as st

from garmin_dashboard import charts

st.title("Garmin Dashboard")

st.subheader("Steps")
st.pyplot(charts.chart_body_battery())
