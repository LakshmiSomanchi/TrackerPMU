import streamlit as st
import pandas as pd # Used for data structure, not direct DataFrame operations here

st.set_page_config(layout="wide", page_title="Employee Flashcards")

st.title("Employee Flashcards")
st.markdown("---")

# Re-defining employee data here for now. Will be centralized in Phase 3.
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

# Number of columns for flashcards (e.g., 3 cards per row)
num_columns = 3
cols = st.columns(num_columns)
col_idx = 0

for name, details in employee_full_details.items():
    with cols[col_idx]:
        st.markdown(f"### {name}")
        # Placeholder for headshot. In a real app, you'd load images from a path.
        st.image("https://via.placeholder.com/100", caption="Headshot", width=100) # Generic placeholder image
        st.write(f"**Title:** {details.get('Title', 'N/A')}")
        st.write(f"**Department:** {details.get('Department', 'N/A')}")
        st.write(f"**Status:** {details.get('Status', 'N/A')}")
        st.write(f"**Reporting To:** {details.get('Reporting To', 'N/A')}")
        st.write(f"**Email:** {details.get('Email', 'N/A')}")
        st.write(f"**Phone:** {details.get('Phone', 'N/A')}")
        st.markdown("---") # Separator between cards
    col_idx = (col_idx + 1) % num_columns

st.markdown("---")
st.info("These flashcards offer a more detailed view of each team member.")
