# your_project_folder/pages/6_One_on_One_Meetings.py
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
# For now, let's make it a bit more robust
if 'employee_names' not in st.session_state:
    # This is a temporary placeholder.
    # In a real app, you'd populate this from your 'Employee Directory' data.
    st.session_state.employee_names = ["Alice Smith", "Bob Johnson", "Charlie Brown", "Diana Prince", "Eve Adams"]

employee_names = st.session_state.employee_names


# --- Section: Schedule New One-on-One Meeting ---
st.header("🗓️ Schedule a New Meeting")
with st.form("meeting_scheduler_form"):
    col1, col2 = st.columns(2)
    with col1:
        selected_employee = st.selectbox("Select Employee", employee_names, key="schedule_employee")
        meeting_date = st.date_input("Meeting Date", datetime.now().date(), key="schedule_date") # .date() to get just the date part
    with col2:
        # Defaulting time to current hour for convenience
        current_hour = datetime.now().strftime("%H")
        meeting_time_str = st.text_input("Meeting Time (e.g., 10:00 AM or 14:30)", f"{current_hour}:00", key="schedule_time")
        meeting_purpose = st.text_area("Meeting Purpose/Topic", key="schedule_purpose")

    submitted = st.form_submit_button("Schedule Meeting")
    if submitted:
        try:
            # Combine date and time
            # Try parsing with both 12-hour (AM/PM) and 24-hour formats
            try:
                meeting_datetime = datetime.strptime(f"{meeting_date} {meeting_time_str}", "%Y-%m-%d %I:%M %p")
            except ValueError:
                meeting_datetime = datetime.strptime(f"{meeting_date} {meeting_time_str}", "%Y-%m-%d %H:%M")


            new_meeting = {
                "id": len(st.session_state.meetings) + 1, # Simple ID generation
                "employee": selected_employee,
                "datetime": meeting_datetime,
                "purpose": meeting_purpose,
                "agenda": "", # Placeholder for agenda
                "mom": ""     # Placeholder for Minutes of Meeting
            }
            st.session_state.meetings.append(new_meeting)
            st.success(f"Meeting with **{selected_employee}** scheduled for **{meeting_datetime.strftime('%Y-%m-%d %I:%M %p')}**!")
            # Rerun to clear form after submission (optional, but good UX)
            st.rerun()
        except ValueError:
            st.error("Invalid time format. Please use HH:MM AM/PM (e.g., 10:00 AM) or HH:MM (e.g., 14:30).")

st.markdown("---") # Separator

# --- Section: Upcoming Meetings ---
st.header("📋 Upcoming Meetings")
if st.session_state.meetings:
    # Sort meetings by date and time
    sorted_meetings = sorted(st.session_state.meetings, key=lambda x: x['datetime'])

    meetings_df = pd.DataFrame(sorted_meetings)
    # Ensure 'datetime' column is datetime type for operations
    meetings_df['datetime'] = pd.to_datetime(meetings_df['datetime'])

    meetings_df['Meeting Time'] = meetings_df['datetime'].dt.strftime('%Y-%m-%d %I:%M %p')
    meetings_df['Status'] = meetings_df['datetime'].apply(lambda x: "Upcoming" if x > datetime.now() else "Past")

    # Display only relevant columns and upcoming meetings by default
    # Filter for upcoming meetings to show first
    upcoming_df = meetings_df[meetings_df['Status'] == 'Upcoming'].copy()
    past_df = meetings_df[meetings_df['Status'] == 'Past'].copy()

    if not upcoming_df.empty:
        st.subheader("Currently Scheduled Meetings")
        st.dataframe(upcoming_df[['Meeting Time', 'employee', 'purpose', 'Status', 'id']],
                     hide_index=True,
                     column_config={
                         "id": st.column_config.Column("Meeting ID", width="small"),
                         "employee": "Employee",
                         "purpose": "Purpose"
                     })
    else:
        st.info("No upcoming meetings scheduled.")

    if not past_df.empty:
        with st.expander("View Past Meetings"):
            st.dataframe(past_df[['Meeting Time', 'employee', 'purpose', 'Status', 'id']],
                         hide_index=True,
                         column_config={
                             "id": st.column_config.Column("Meeting ID", width="small"),
                             "employee": "Employee",
                             "purpose": "Purpose"
                         })
else:
    st.info("No meetings scheduled yet. Use the form above to schedule one!")

st.markdown("---") # Separator

# --- Section: Meeting Agenda & MoM Taker ---
st.header("📝 Meeting Agenda & MoM Taker")
if st.session_state.meetings:
    # Create a list of meeting options for the selectbox
    # Ensure sorted_meetings is available or re-sort it
    sorted_meetings_for_mom = sorted(st.session_state.meetings, key=lambda x: x['datetime'], reverse=True) # Show recent first

    meeting_options = [
        f"{m['datetime'].strftime('%Y-%m-%d %I:%M %p')} - {m['employee']} (ID: {m['id']})"
        for m in sorted_meetings_for_mom
    ]
    if meeting_options:
        selected_meeting_display = st.selectbox("Select Meeting to Manage", meeting_options, key="mom_select")

        # Find the selected meeting object
        # Extract ID more robustly, handling cases where ID might not be at the very end
        try:
            selected_meeting_id_str = selected_meeting_display.split("(ID: ")[1].split(")")[0]
            selected_meeting_id = int(selected_meeting_id_str)
        except (IndexError, ValueError):
            st.error("Could not parse meeting ID. Please re-select or check data integrity.")
            selected_meeting_id = None

        current_meeting = None
        if selected_meeting_id is not None:
            current_meeting = next((m for m in st.session_state.meetings if m['id'] == selected_meeting_id), None)

        if current_meeting:
            st.subheader(f"Managing Meeting with {current_meeting['employee']} on {current_meeting['datetime'].strftime('%Y-%m-%d %I:%M %p')}")
            st.markdown(f"**Purpose:** {current_meeting['purpose']}")

            with st.form("agenda_mom_form"):
                st.markdown("#### Agenda")
                updated_agenda = st.text_area(
                    "Write/Edit Agenda Items (e.g., - Review Q1 goals, - Discuss project roadmap)",
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

                col_save, col_delete = st.columns([1, 1])
                with col_save:
                    save_button = st.form_submit_button("Save Agenda and MoM")
                with col_delete:
                    delete_button = st.form_submit_button("Delete Meeting", help="Permanently delete this meeting.", type="secondary")

                if save_button:
                    # Update the selected meeting in session state
                    for i, m in enumerate(st.session_state.meetings):
                        if m['id'] == current_meeting['id']:
                            st.session_state.meetings[i]['agenda'] = updated_agenda
                            st.session_state.meetings[i]['mom'] = updated_mom
                            break
                    st.success("Agenda and MoM saved successfully!")
                    st.rerun() # Rerun to refresh display
                elif delete_button:
                    # Remove the meeting from session state
                    st.session_state.meetings = [m for m in st.session_state.meetings if m['id'] != current_meeting['id']]
                    st.warning(f"Meeting with {current_meeting['employee']} deleted.")
                    st.rerun() # Rerun to update the list
        else:
            if selected_meeting_id is not None: # Only show error if ID was correctly parsed but meeting not found
                st.error("Selected meeting not found in the current list.")
    else:
        st.info("No meetings available to manage. Schedule one first.")
else:
    st.info("Schedule a meeting first to manage its agenda and MoM.")

st.markdown("---") # Separator

# --- Section: Individual Employee Calendar View ---
st.header("📅 Individual Employee Calendar")
if employee_names: # Ensure there are employees to select
    selected_employee_calendar = st.selectbox("Select Employee to View Calendar", employee_names, key="calendar_employee")

    if st.session_state.meetings:
        employee_meetings = [m for m in st.session_state.meetings if m['employee'] == selected_employee_calendar]
        if employee_meetings:
            employee_meetings_df = pd.DataFrame(employee_meetings)
            employee_meetings_df['datetime'] = pd.to_datetime(employee_meetings_df['datetime']) # Ensure datetime type
            employee_meetings_df['Meeting Time'] = employee_meetings_df['datetime'].dt.strftime('%Y-%m-%d %I:%M %p')
            employee_meetings_df['Status'] = employee_meetings_df['datetime'].apply(lambda x: "Upcoming" if x > datetime.now() else "Past")

            # Display only relevant columns for the calendar view
            st.dataframe(employee_meetings_df[['Meeting Time', 'purpose', 'agenda', 'mom', 'Status']], hide_index=True,
                         column_config={
                             "purpose": "Purpose",
                             "agenda": "Agenda",
                             "mom": "Minutes of Meeting"
                         })
        else:
            st.info(f"No meetings found for **{selected_employee_calendar}**.")
    else:
        st.info("No meetings scheduled yet to display in calendars.")
else:
    st.info("No employee names available to display calendar. Please add employees via 'Employee Directory' if implemented.")
