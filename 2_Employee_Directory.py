import streamlit as st
import pandas as pd

st.set_page_config(layout="wide", page_title="Employee Directory")

st.title("👥 Employee Directory")
st.markdown("---")

# This data should ideally come from a persistent source, but for now, we'll re-define
# a basic employee list. In Phase 3, all this data will be loaded from a single source.
employee_list_data = {
    "Rupesh Mukherjee": {"Title": "Associate Practice Leader", "Department": "PMU", "Reporting To": "N/A"},
    "Shifali Sharma": {"Title": "Project Manager", "Department": "PMU", "Reporting To": "Rupesh Mukherjee"},
    "Kuntal Dutta": {"Title": "Senior Manager - Field", "Department": "PMU", "Reporting To": "Rupesh Mukherjee"},
    "Sachin WadapaLliwar": {"Title": "Manager - Field", "Department": "PMU", "Reporting To": "Rupesh Mukherjee"},
    "Dr. Guru Mohan Reddy": {"Title": "Assistant Manager - Field", "Department": "PMU", "Reporting To": "Rupesh Mukherjee"},
    "K Balaji": {"Title": "Senior Associate - Field", "Department": "PMU", "Reporting To": "Dr. Ramakrishna"},
    "Bhavya Kharoo": {"Title": "Employee", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Gautam Bagada": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta"},
    "Ajay Vaghela": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta"},
    "Samadhan Bangale": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta"},
    "Prabodh Pate": {"Title": "Employee", "Department": "PMU", "Reporting To": "Kuntal Dutta"},
    "Ramalakshmi Somanchi": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Aditya Yuvaraj": {"Title": "Assistant Manager", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar"},
    "Bhushan Sananse": {"Title": "Assistant Manager", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar"},
    "Nilesh Rajkumar Dhanwate": {"Title": "Senior executive", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Ranu Laoddha": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Pari Sharma": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Muskan Kaushal": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Kriti Suneha": {"Title": "Employee", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Nikhitha VK": {"Title": "Employee", "Department": "PMU", "Reporting To": "Shifali Sharma"},
    "Sandeep GS": {"Title": "Employee", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar"},
    "Aniket Grover": {"Title": "Assistant Manager - Field", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar"},
    "Subhrat Ghoshal": {"Title": "Senior Executive - Field", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar"},
    "Hrushikesh Tilekar": {"Title": "Associate - Field", "Department": "PMU", "Reporting To": "Sachin WadapaLliwar"},
    "Jhelum Chowdhury": {"Title": "Consultant", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Status": "Contractor"},
    "Jaweriah Hazrana": {"Title": "Research analyst", "Department": "PMU", "Reporting To": "Jhelum Chowdhury", "Status": "Contractor"},
    "Dr. Ramakrishna": {"Title": "Consultant", "Department": "PMU", "Reporting To": "Rupesh Mukherjee", "Status": "Contractor"},
}

# Convert the dictionary to a pandas DataFrame for easy display
employees_df = pd.DataFrame.from_dict(employee_list_data, orient='index')
employees_df.index.name = "Name" # Set the index name to "Name"
employees_df = employees_df.reset_index() # Convert index to a column

st.dataframe(employees_df, use_container_width=True)

st.markdown("---")
st.info("This directory provides a quick overview of all personnel. Flashcards offer more detail.")
