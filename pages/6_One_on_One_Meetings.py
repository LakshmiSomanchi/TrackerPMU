# your_project_folder/pages/2_One_on_One_Meetings.py
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="One-on-One Meetings",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 One-on-One Meeting Management")
st.markdown("Streamline your one-on-one discussions with employees.")

# --- Session State Initialization for Meeting Data ---
# This dictionary will store our meeting data.
# In a real app, this would come from a database or persistent storage.
if 'meetings' not in st.session_state:
    st.session_state.meetings = []

# Placeholder for employee names.
# In a real app, you'd load this from your Employee Directory data.
employee_names = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Eve Adams"]

# --- Section: Schedule New One-on-One Meeting ---
st.header("🗓️ Schedule a New Meeting")
with st.form("meeting_scheduler_form"):
    col1, col2 = st.columns(2)
    with col1:
        selected_employee = st.selectbox("Select Employee", employee_names, key="schedule_employee")
        meeting_date = st.date_input("Meeting Date", datetime.now(), key="schedule_date")
    with col2:
        meeting_time_str = st.text_input("Meeting Time (e.g., 10:00 AM)", "09:00 AM", key="schedule_time")
        meeting_purpose = st.text_area("Meeting Purpose/Topic", key="schedule_purpose")

    submitted = st.form_submit_button("Schedule Meeting")
    if submitted:
        try:
            # Combine date and time
            meeting_datetime_str = f"{meeting_date} {meeting_time_str}"
            meeting_datetime = datetime.strptime(meeting_datetime_str, "%Y-%m-%d %I:%M %p")

            new_meeting = {
                "id": len(st.session_state.meetings) + 1, # Simple ID generation
                "employee": selected_employee,
                "datetime": meeting_datetime,
                "purpose": meeting_purpose,
                "agenda": "", # Placeholder for agenda
                "mom": ""     # Placeholder for Minutes of Meeting
            }
            st.session_state.meetings.append(new_meeting)
            st.success(f"Meeting with {selected_employee} scheduled for {meeting_datetime.strftime('%Y-%m-%d %I:%M %p')}!")
        except ValueError:
            st.error("Invalid time format. Please use HH:MM AM/PM (e.g., 10:00 AM).")

---

# --- Section: Upcoming Meetings ---
st.header("📋 Upcoming Meetings")
if st.session_state.meetings:
    # Sort meetings by date and time
    sorted_meetings = sorted(st.session_state.meetings, key=lambda x: x['datetime'])

    meetings_df = pd.DataFrame(sorted_meetings)
    meetings_df['Datetime'] = meetings_df['datetime'].dt.strftime('%Y-%m-%d %I:%M %p')
    meetings_df['Status'] = meetings_df['datetime'].apply(lambda x: "Upcoming" if x > datetime.now() else "Past")

    # Display only relevant columns and upcoming meetings by default
    st.dataframe(meetings_df[['Datetime', 'employee', 'purpose', 'Status', 'id']],
                 hide_index=True,
                 column_config={
                     "id": st.column_config.Column("Meeting ID", width="small")
                 })
else:
    st.info("No meetings scheduled yet. Use the form above to schedule one!")

---

# --- Section: Meeting Agenda & MoM Taker ---
st.header("📝 Meeting Agenda & MoM Taker")
if st.session_state.meetings:
    # Create a list of meeting options for the selectbox
    meeting_options = [
        f"{m['datetime'].strftime('%Y-%m-%d %I:%M %p')} - {m['employee']} (ID: {m['id']})"
        for m in sorted_meetings
    ]
    selected_meeting_display = st.selectbox("Select Meeting to Manage", meeting_options, key="mom_select")

    # Find the selected meeting object
    selected_meeting_id = int(selected_meeting_display.split("(ID: ")[1][:-1])
    current_meeting = next((m for m in st.session_state.meetings if m['id'] == selected_meeting_id), None)

    if current_meeting:
        st.subheader(f"Managing Meeting with {current_meeting['employee']} on {current_meeting['datetime'].strftime('%Y-%m-%d %I:%M %p')}")

        with st.form("agenda_mom_form"):
            st.markdown("#### Agenda")
            updated_agenda = st.text_area(
                "Write/Edit Agenda Items (e.g., - Review Q1 goals)",
                value=current_meeting['agenda'],
                height=150,
                key="agenda_input"
            )

            st.markdown("#### Minutes of Meeting (MoM)")
            updated_mom = st.text_area(
                "Record Key Discussions and Action Items",
                value=current_meeting['mom'],
                height=250,
                key="mom_input"
            )

            save_button = st.form_submit_button("Save Agenda and MoM")
            if save_button:
                # Update the selected meeting in session state
                for i, m in enumerate(st.session_state.meetings):
                    if m['id'] == current_meeting['id']:
                        st.session_state.meetings[i]['agenda'] = updated_agenda
                        st.session_state.meetings[i]['mom'] = updated_mom
                        break
                st.success("Agenda and MoM saved successfully!")
    else:
        st.error("Selected meeting not found.")
else:
    st.info("Schedule a meeting first to manage its agenda and MoM.")

---

# --- Section: Individual Employee Calendar View ---
st.header("📅 Individual Employee Calendar")
selected_employee_calendar = st.selectbox("Select Employee to View Calendar", employee_names, key="calendar_employee")

if st.session_state.meetings:
    employee_meetings = [m for m in st.session_state.meetings if m['employee'] == selected_employee_calendar]
    if employee_meetings:
        employee_meetings_df = pd.DataFrame(employee_meetings)
        employee_meetings_df['Datetime'] = employee_meetings_df['datetime'].dt.strftime('%Y-%m-%d %I:%M %p')
        employee_meetings_df['Status'] = employee_meetings_df['datetime'].apply(lambda x: "Upcoming" if x > datetime.now() else "Past")
        st.dataframe(employee_meetings_df[['Datetime', 'purpose', 'agenda', 'Status']], hide_index=True)
    else:
        st.info(f"No meetings found for {selected_employee_calendar}.")
else:
    st.info("No meetings scheduled yet to display in calendars.")
