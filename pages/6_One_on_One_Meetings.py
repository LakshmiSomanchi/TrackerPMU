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

if 'meetings' not in st.session_state:
    st.session_state.meetings = []

employee_names = sorted([
    "Rupesh Mukherjee",
    "Shifali Sharma",
    "Kuntal Dutta",
    "Sachin WadapaLliwar",
    "Dr. Guru Mohan Reddy",
    "K Balaji",
    "Bhavya Kharoo",
    "Gautam Bagada",
    "Ajay Vaghela",
    "Samadhan Bangale",
    "Prabodh Pate",
    "Ramalakshmi Somanchi",
    "Aditya Yuvaraj",
    "Bhushan Sananse",
    "Nilesh Rajkumar Dhanwate",
    "Ranu Laddha",
    "Pari Sharma",
    "Muskan Kaushal",
    "Kriti Suneha",
    "Nikhitha VK",
    "Sandeep GS",
    "Aniket Grover",
    "Subhrat Ghoshal",
    "Hrushikesh Tilekar",
    "Jhelum Chowdhury",
    "Jaweriah Hazrana",
    "Dr. Ramakrishna"
])

st.header("🗓️ Schedule a New Meeting")
if employee_names:
    with st.form("meeting_scheduler_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_employee = st.selectbox("Select Employee", employee_names, key="schedule_employee")
            meeting_date = st.date_input("Meeting Date", datetime.now().date(), key="schedule_date")
        with col2:
            current_hour = datetime.now().strftime("%H")
            meeting_time_str = st.text_input("Meeting Time (e.g., 10:00 AM or 14:30)", f"{current_hour}:00", key="schedule_time")
            meeting_purpose = st.text_area("Meeting Purpose/Topic", key="schedule_purpose")

        submitted = st.form_submit_button("Schedule Meeting")
        if submitted:
            try:
                time_formats = ["%I:%M %p", "%H:%M"] 
                parsed_time = None
                for fmt in time_formats:
                    try:
                        parsed_time = datetime.strptime(meeting_time_str, fmt).time()
                        break
                    except ValueError:
                        continue

                if parsed_time is None:
                    raise ValueError("Invalid time format.")

                meeting_datetime = datetime.combine(meeting_date, parsed_time)

                new_meeting = {
                    "id": len(st.session_state.meetings) + 1, 
                    "employee": selected_employee,
                    "datetime": meeting_datetime,
                    "purpose": meeting_purpose,
                    "agenda": "", 
                    "mom": ""  
                }
                st.session_state.meetings.append(new_meeting)
                st.success(f"Meeting with **{selected_employee}** scheduled for **{meeting_datetime.strftime('%Y-%m-%d %I:%M %p')}**!")
                st.rerun() 
            except ValueError as e:
                st.error(f"Error scheduling meeting: {e}. Please use HH:MM AM/PM (e.g., 10:00 AM) or HH:MM (e.g., 14:30).")
else:
    st.warning("No employee names defined in this page. Please add names to the 'employee_names' list.")

st.markdown("---") 


st.header("📋 Upcoming Meetings")
if st.session_state.meetings:
    
    sorted_meetings = sorted(st.session_state.meetings, key=lambda x: x['datetime'])

    meetings_df = pd.DataFrame(sorted_meetings)
    
    meetings_df['datetime'] = pd.to_datetime(meetings_df['datetime'])

    meetings_df['Meeting Time'] = meetings_df['datetime'].dt.strftime('%Y-%m-%d %I:%M %p')
    meetings_df['Status'] = meetings_df['datetime'].apply(lambda x: "Upcoming" if x > datetime.now() else "Past")
  
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

st.markdown("---") 

st.header("📝 Meeting Agenda & MoM Taker")
if st.session_state.meetings:
    sorted_meetings_for_mom = sorted(st.session_state.meetings, key=lambda x: x['datetime'], reverse=True) # Show recent first

    meeting_options = [
        f"{m['datetime'].strftime('%Y-%m-%d %I:%M %p')} - {m['employee']} (ID: {m['id']})"
        for m in sorted_meetings_for_mom
    ]
    if meeting_options:
        selected_meeting_display = st.selectbox("Select Meeting to Manage", meeting_options, key="mom_select")

        selected_meeting_id = None
        try:
            if "(ID: " in selected_meeting_display:
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
                    
                    delete_button = st.form_submit_button("Delete Meeting", help="Permanently delete this meeting.", type="secondary", key="delete_meeting_btn")

                if save_button:
                    
                    for i, m in enumerate(st.session_state.meetings):
                        if m['id'] == current_meeting['id']:
                            st.session_state.meetings[i]['agenda'] = updated_agenda
                            st.session_state.meetings[i]['mom'] = updated_mom
                            break
                    st.success("Agenda and MoM saved successfully!")
                    st.rerun() 
                elif delete_button:
                    
                    st.session_state.meetings = [m for m in st.session_state.meetings if m['id'] != current_meeting['id']]
                    st.warning(f"Meeting with {current_meeting['employee']} deleted.")
                    st.rerun() 
        else:
            if selected_meeting_id is not None:
                st.error("Selected meeting not found in the current list.")
    else:
        st.info("No meetings available to manage. Schedule one first.")
else:
    st.info("Schedule a meeting first to manage its agenda and MoM.")

st.markdown("---") 


st.header("📅 Individual Employee Calendar")
if employee_names:
    selected_employee_calendar = st.selectbox("Select Employee to View Calendar", employee_names, key="calendar_employee")

    if st.session_state.meetings:
        employee_meetings = [m for m in st.session_state.meetings if m['employee'] == selected_employee_calendar]
        if employee_meetings:
            employee_meetings_df = pd.DataFrame(employee_meetings)
            employee_meetings_df['datetime'] = pd.to_datetime(employee_meetings_df['datetime']) 
            employee_meetings_df['Meeting Time'] = employee_meetings_df['datetime'].dt.strftime('%Y-%m-%d %I:%M %p')
            employee_meetings_df['Status'] = employee_meetings_df['datetime'].apply(lambda x: "Upcoming" if x > datetime.now() else "Past")

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
    st.info("No employee names available to display calendar. Please add names to the 'employee_names' list in this file.")
