import streamlit as st

st.set_page_config(layout="wide", page_title="Programs Dashboard")

st.title("📊 Programs Dashboard")
st.markdown("---")

st.header("Current & Ongoing Programs")

st.info("""
This section will be developed to track high-level programs and workstreams.
You will be able to:
* View a list of all active programs.
* See their current status, key milestones, and associated workplans.
* Track overall progress and updates.
""")

st.subheader("Upcoming Development:")
st.markdown("- Define the data structure for programs (Name, Description, Status, Lead, Start Date, End Date, Key Deliverables).")
st.markdown("- Implement forms for adding and updating programs.")
st.markdown("- Link tasks from the 'Task Tracker' to specific programs.")

# Placeholder for displaying programs
st.subheader("Example Programs (Placeholder)")
st.write("- **Program Alpha:** Focusing on digital transformation initiatives.")
st.write("- **Program Beta:** Expanding market reach in new regions.")
st.write("- **Program Gamma:** Enhancing internal operational efficiency.")

st.markdown("---")
st.info("This module will provide a higher-level view of all projects and strategic initiatives.")
