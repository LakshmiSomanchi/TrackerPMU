import streamlit as st
from datetime import datetime
import json
import os
import pytz 
st.set_page_config(layout="wide", page_title="Attendance Marker")

st.title("⏰ Attendance Marker")
st.markdown("---")

ATTENDANCE_FILE = "attendance_records.json" 


if 'attendance_records' not in st.session_state:
    st.session_state.attendance_records = {} 

employee_names = sorted([
    "Rupesh Mukherjee", "Shifali Sharma", "Kuntal Dutta", "Sachin WadapaLliwar",
    "Dr. Guru Mohan Reddy", "K Balaji", "Bhavya Kharoo", "Gautam Bagada",
    "Ajay Vaghela", "Samadhan Bangale", "Prabodh Pate", "Ramalakshmi Somanchi",
    "Aditya Yuvaraj", "Bhushan Sananse", "Nilesh Rajkumar Dhanwate",
    "Ranu Laddha", "Pari Sharma", "Muskan Kaushal", "Kriti Suneha",
    "Nikhitha VK", "Sandeep GS", "Aniket Grover", "Subhrat Ghoshal",
    "Hrushikesh Tilekar", "Jhelum Chowdhury", "Jaweriah Hazrana", "Dr. Ramakrishna"
])

selected_employee_attendance = st.selectbox("Select Your Name for Attendance", employee_names)
st.markdown("---")

st.subheader("Mark Your Attendance")

india_tz = pytz.timezone('Asia/Kolkata')
current_time_ist = datetime.now(india_tz)

current_location_input = st.text_input("Enter your Current Location", "Pune, Maharashtra, India")
st.info(f"Current Date & Time (IST): **{current_time_ist.strftime('%Y-%m-%d %H:%M:%S')}**")

col1, col2 = st.columns(2)

with col1:
    if st.button("Check In 👋"):
        if selected_employee_attendance:
            record = {
                "timestamp": current_time_ist.isoformat(),
                "type": "Check-In",
                "location": current_location_input
            }
            if selected_employee_attendance not in st.session_state.attendance_records:
                st.session_state.attendance_records[selected_employee_attendance] = []
            st.session_state.attendance_records[selected_employee_attendance].append(record)
            st.success(f"Checked In for {selected_employee_attendance} at {current_time_ist.strftime('%H:%M:%S')} from {current_location_input}!")
        else:
            st.error("Please select your name.")

with col2:
    if st.button("Check Out 👋"):
        if selected_employee_attendance:
            record = {
                "timestamp": current_time_ist.isoformat(),
                "type": "Check-Out",
                "location": current_location_input
            }
            if selected_employee_attendance not in st.session_state.attendance_records:
                st.session_state.attendance_records[selected_employee_attendance] = []
            st.session_state.attendance_records[selected_employee_attendance].append(record)
            st.success(f"Checked Out for {selected_employee_attendance} at {current_time_ist.strftime('%H:%M:%S')} from {current_location_input}!")
        else:
            st.error("Please select your name.")

st.markdown("---")
st.subheader(f"Attendance History for {selected_employee_attendance}")

if selected_employee_attendance in st.session_state.attendance_records and st.session_state.attendance_records[selected_employee_attendance]:
    
    attendance_df = pd.DataFrame(st.session_state.attendance_records[selected_employee_attendance])
    attendance_df['timestamp'] = pd.to_datetime(attendance_df['timestamp']) 
    attendance_df = attendance_df.sort_values(by='timestamp', ascending=False)
    st.dataframe(attendance_df, use_container_width=True)
else:
    st.info("No attendance records found for this employee yet.")

st.markdown("---")
st.markdown("""
**Note on Geotagging:**
Direct and precise geotagging in a free Streamlit Cloud environment can be challenging due to browser security policies (HTTPS required, user permissions).
For a production system, you would typically use:
-   **Client-side JavaScript:** To get browser location (requires secure context - HTTPS).
-   **Backend processing:** To store and verify location data.
-   **Integration with APIs:** For more robust location services.
For now, we are using a manual text input for location.
""")
