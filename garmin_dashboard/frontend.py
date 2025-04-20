import streamlit as st

from garmin_dashboard import charts

st.title("Garmin Dashboard")


st.subheader("Resting Heart Rate")
st.pyplot(charts.resting_heart_rate())

st.subheader("Sleep")
st.pyplot(charts.sleep())


st.subheader("Body Battery")
st.pyplot(charts.body_battery())
