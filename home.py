# your_project_folder/Home.py
import streamlit as st

st.set_page_config(
    page_title="PMU Management Suite",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Welcome to the PMU Management Suite!")

st.markdown("""
This application is designed to help the Project Management Unit (PMU) streamline various operations,
from task tracking to employee management and attendance.

**Navigate using the sidebar to explore different sections:**

* **Task Tracker:** Manage individual employee tasks with Kanban cards.
* **Employee Directory:** View a list of all team members.
* **Employee Flashcards:** See detailed, card-like views of each employee.
* **Programs Dashboard:** An overview of current and ongoing projects/programs.
* **Attendance Marker:** Mark your daily attendance.

---
""")

st.info("Choose a module from the sidebar to get started!")

st.markdown("### Next Steps:")
st.markdown("- **Phase 2:** Implementing Employee Directory, Flashcards, Programs placeholder, and Attendance marker foundation.")
st.markdown("- **Phase 3:** Adding persistent storage for all data.")
st.markdown("- **Phase 4:** Enhancing Attendance with Geotagging (if feasible with Streamlit's free tier) and a proper Calendar/MoM system.")

# You can add more introductory content or a dashboard summary here later
