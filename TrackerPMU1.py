import streamlit as st
import pandas as pd
from datetime import date

# --- Global Data Storage (In-memory for now) ---
# This dictionary will store our tasks.
# Key: employee_name
# Value: List of task dictionaries
# Each task dictionary: {'id', 'name', 'description', 'status', 'due_date'}
tasks_data = {
    # Employees from the provided images
    "Rupesh Mukherjee": [],
    "Shifali Sharma": [],
    "Kuntal Dutta": [],
    "Sachin WadapaLliwar": [],
    "Dr. Guru Mohan Reddy": [],
    "K Balaji": [],
    "Bhavya Kharoo": [],
    "Gautam Bagada": [],
    "Ajay Vaghela": [],
    "Samadhan Bangale": [],
    "Prabodh Pate": [],
    "Ramalakshmi Somanchi": [],
    "Aditya Yuvaraj": [],
    "Bhushan Sananse": [],
    "Nilesh Rajkumar Dhanwate": [],
    "Ranu Laoddha": [],
    "Pari Sharma": [],
    "Muskan Kaushal": [],
    "Kriti Suneha": [],
    "Nikhitha VK": [],
    "Sandeep GS": [],
    "Aniket Grover": [],
    "Subhrat Ghoshal": [],
    "Hrushikesh Tilekar": [],

    # Contractors from the provided images
    "Jhelum Chowdhury": [],
    "Jaweriah Hazrana": [],
    "Dr. Ramakrishna": [], # This replaces the previous placeholder for Dr. Ramakrishnan

    # Added some initial tasks for demonstration, feel free to remove or modify
    "Rupesh Mukherjee": [
        {"id": 1, "name": "Finalize Project Alpha Scope", "description": "Meet with stakeholders to define final project scope.", "status": "To Do", "due_date": date(2025, 7, 10)},
        {"id": 2, "name": "Q3 Planning Review", "description": "Review Q3 plans with department heads.", "status": "In Progress", "due_date": date(2025, 7, 15)},
    ],
    "Shifali Sharma": [
        {"id": 3, "name": "Onboard New PM", "description": "Complete onboarding for the new project manager.", "status": "In Progress", "due_date": date(2025, 6, 28)},
        {"id": 4, "name": "Update Risk Register", "description": "Review and update project risk register for all active programs.", "status": "To Do", "due_date": date(2025, 7, 5)},
    ],
    "Kuntal Dutta": [
        {"id": 5, "name": "Client X Meeting Prep", "description": "Prepare agenda and presentation for Client X meeting.", "status": "Done", "due_date": date(2025, 6, 20)},
    ]
}

# Add tasks_data to Streamlit's session state to persist it across reruns
if 'tasks' not in st.session_state:
    st.session_state.tasks = tasks_data

# Determine the next available ID by finding the max ID from all tasks
if 'next_task_id' not in st.session_state:
    max_id = 0
    # Make sure to handle cases where an employee might not have tasks yet
    for employee_tasks in st.session_state.tasks.values():
        for task in employee_tasks:
            if task['id'] > max_id:
                max_id = task['id']
    st.session_state.next_task_id = max_id + 1 if max_id > 0 else 1 # Start from 1 if no initial tasks


# --- Helper Functions ---
def add_task(employee_name, task_name, description, due_date):
    """Adds a new task for the given employee."""
    new_task = {
        "id": st.session_state.next_task_id,
        "name": task_name,
        "description": description,
        "status": "To Do",  # New tasks start as 'To Do'
        "due_date": due_date
    }
    # Ensure the employee exists in the tasks_data dictionary
    if employee_name not in st.session_state.tasks:
        st.session_state.tasks[employee_name] = []
    st.session_state.tasks[employee_name].append(new_task)
    st.session_state.next_task_id += 1
    st.success(f"Task '{task_name}' added for {employee_name}!")

def update_task_status(employee_name, task_id, new_status):
    """Updates the status of a specific task."""
    # We iterate through all tasks globally because task_id is unique across employees
    found = False
    for tasks_list in st.session_state.tasks.values():
        for task in tasks_list:
            if task['id'] == task_id:
                task['status'] = new_status
                found = True
                st.success(f"Task '{task['name']}' status updated to '{new_status}'!")
                return # Exit once found and updated
    if not found:
        st.error("Task not found.")

def delete_task(employee_name, task_id):
    """Deletes a task for a given employee."""
    if employee_name in st.session_state.tasks:
        initial_len = len(st.session_state.tasks[employee_name])
        st.session_state.tasks[employee_name] = [
            task for task in st.session_state.tasks[employee_name] if task['id'] != task_id
        ]
        if len(st.session_state.tasks[employee_name]) < initial_len:
            st.success("Task deleted successfully!")
        else:
            st.warning("Task not found for this employee.")
    else:
        st.warning("Employee not found.")


# --- Streamlit App Layout ---
st.set_page_config(layout="wide", page_title="Project Task Tracker")

st.title("🚀 Project Management Task Tracker")
st.markdown("---")

# Employee Selection
# Ensure that all employees from the initial tasks_data are in the dropdown
employee_names = sorted(list(st.session_state.tasks.keys()))
if not employee_names:
    st.warning("No employees loaded. Please add employees to the initial data.")
    st.stop() # Stop execution if no employees are present

selected_employee = st.sidebar.selectbox("Select Employee", employee_names)
st.sidebar.markdown("---")

# Add New Task Form
st.sidebar.header(f"Add New Task for {selected_employee}")
with st.sidebar.form("new_task_form"):
    task_name = st.text_input("Task Name", key="new_task_name")
    description = st.text_area("Description", key="new_task_description")
    due_date = st.date_input("Due Date", min_value=date.today(), value=date.today(), key="new_task_due_date")
    submit_button = st.form_submit_button("Add Task")

    if submit_button:
        if task_name:
            add_task(selected_employee, task_name, description, due_date)
            st.rerun() # Rerun to update the display
        else:
            st.error("Task Name cannot be empty.")

st.sidebar.markdown("---")
st.sidebar.info("Select an employee to view and manage their tasks. Use the form above to add new tasks.")

# --- Main Content Area: Kanban Board ---
st.header(f"Kanban Board for {selected_employee}")

if selected_employee not in st.session_state.tasks or not st.session_state.tasks[selected_employee]:
    st.info(f"{selected_employee} currently has no tasks. Add one using the sidebar form!")
else:
    # Filter tasks for the selected employee
    employee_tasks = st.session_state.tasks[selected_employee]

    # Group tasks by status
    status_columns = st.columns(3) # To Do, In Progress, Done
    kanban_statuses = ["To Do", "In Progress", "Done"]

    for i, status in enumerate(kanban_statuses):
        with status_columns[i]:
            st.subheader(status)
            st.markdown("---") # Separator for visual clarity

            tasks_in_status = [task for task in employee_tasks if task['status'] == status]

            if not tasks_in_status:
                st.info("No tasks here!")
            else:
                for task in tasks_in_status:
                    with st.expander(f"**{task['name']}**"):
                        st.markdown(f"**Description:** {task['description']}")
                        st.markdown(f"**Due Date:** {task['due_date'].strftime('%Y-%m-%d')}")
                        st.markdown(f"**Task ID:** `{task['id']}`") # For easy reference in updating

                        # Dropdown to change status
                        new_status = st.selectbox(
                            "Change Status",
                            kanban_statuses,
                            index=kanban_statuses.index(task['status']),
                            key=f"status_select_{task['id']}" # Unique key for each selectbox
                        )
                        if new_status != task['status']:
                            update_task_status(selected_employee, task['id'], new_status)
                            st.rerun() # Rerun to reflect the status change

                        # Delete task button
                        if st.button("Delete Task", key=f"delete_button_{task['id']}"):
                            delete_task(selected_employee, task['id'])
                            st.rerun() # Rerun to remove the deleted task