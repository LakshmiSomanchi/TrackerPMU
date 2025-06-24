# TrackerPMU/data_manager.py
import streamlit as st
import pandas as pd
from datetime import date

@st.cache_resource(ttl=3600) # Cache the resource for 1 hour
def get_initial_employee_data():
    """Loads and caches the initial comprehensive employee data."""
    employee_full_details = {
        "Rupesh Mukherjee": {"Title": "Associate Practice Leader", "Department": "PMU", "Reporting To": "N/A", "Email": "rupeshmukherjee@example.com", "Phone": "91-9876543210", "Status": "Employee"},
        "Shifali Sharma": {"Title": "Project Manager", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Email": "shifali@example.com", "Phone": "91-89221943", "Status": "Employee"},
        "Kuntal Dutta": {"Title": "Senior Manager - Field", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Email": "kuntal@example.com", "Phone": "91-9932032059", "Status": "Employee"},
        "Sachin WadapaLliwar": {"Title": "Manager - Field", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Email": "sachinw@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Dr. Guru Mohan Reddy": {"Title": "Assistant Manager - Field", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Email": "gurumohan@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "K Balaji": {"Title": "Senior Associate - Field", "Department": "PMU", "Reporting To": "Dr. Ramakrishna", "Email": "kbalaji@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Bhavya Kharoo": {"Title": "Employee", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "bhavya@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Gautam Bagada": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta", "Email": "gautam@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Ajay Vaghela": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta", "Email": "ajay@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Samadhan Bangale": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta", "Email": "samadhan@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Prabodh Pate": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta", "Email": "prabodh@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Ramalakshmi Somanchi": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "ramalakshmi@example.com", "Phone": "+91-9392799155", "Status": "Employee"},
        "Aditya Yuvaraj": {"Title": "Assistant Manager", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar", "Email": "aditya@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Bhushan Sananse": {"Title": "Assistant Manager", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar", "Email": "bhushan@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Nilesh Rajkumar Dhanwate": {"Title": "Senior executive", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "nilesh@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Ranu Laoddha": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "ranu@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Pari Sharma": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "pari@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Muskan Kaushal": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "muskan@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Kriti Suneha": {"Title": "Employee", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "kriti@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Nikhitha VK": {"Title": "Employee", "Department": "PMU", "Reporting To": "Shifali Sharma", "Email": "nikhitha@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Sandeep GS": {"Title": "Employee", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar", "Email": "sandeep@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Aniket Grover": {"Title": "Assistant Manager - Field", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar", "Email": "aniket@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Subhrat Ghoshal": {"Title": "Senior Executive - Field", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar", "Email": "subhrat@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Hrushikesh Tilekar": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar", "Email": "hrushikesh@example.com", "Phone": "(555) 555-5555", "Status": "Employee"},
        "Jhelum Chowdhury": {"Title": "Consultant", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Email": "jhelum@example.com", "Phone": "(555) 555-5555", "Status": "Contractor"},
        "Jaweriah Hazrana": {"Title": "Research analyst", "Department": "PMU", "Reporting To": "Jhelum Chowdhury", "Email": "jaweriah@example.com", "Phone": "(555) 555-5555", "Status": "Contractor"},
        "Dr. Ramakrishna": {"Title": "Consultant", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Email": "ramakrishna@example.com", "Phone": "(555) 555-5555", "Status": "Contractor"},
    }
    return employee_full_details

@st.cache_data(ttl=3600) # Cache the data for 1 hour
def get_initial_tasks_data():
    """Loads and caches the initial task data."""
    tasks_data = {
        # Employees from the provided images, ensuring all exist
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
        "Dr. Ramakrishna": [],

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

    # Ensure all listed employees have an entry, even if empty
    all_employees = sorted(list(get_initial_employee_data().keys()))
    for emp_name in all_employees:
        if emp_name not in tasks_data:
            tasks_data[emp_name] = []

    return tasks_data

@st.cache_data(ttl=3600) # Cache attendance data for 1 hour
def get_initial_attendance_data():
    """Loads and caches initial attendance data."""
    return {} # Start with an empty dictionary for attendance

def get_next_task_id(current_tasks_data):
    """Calculates the next available task ID."""
    max_id = 0
    for employee_tasks in current_tasks_data.values():
        for task in employee_tasks:
            if task['id'] > max_id:
                max_id = task['id']
    return max_id + 1 if max_id > 0 else 1
