# your_project_folder/Home.py
import streamlit as st
import os # Import os module to handle file paths

st.set_page_config(
    page_title="PMU Management Suite",
    page_icon="🏢",
    layout="wide"
)

# --- Header Section ---
st.title("🏢 Welcome to the PMU Management Suite!")
st.markdown("---")

# --- Introduction Section ---
st.write("""
This application is designed to help the Project Management Unit (PMU) streamline various operations,
from task tracking to employee management and attendance.
""")

st.info("💡 **Tip:** Navigate using the sidebar to explore different sections!")

# --- Modules Overview Section (More Visual) ---
st.header("Explore Our Modules:")

col1, col2, col3 = st.columns(3) # Create three columns for module cards

with col1:
    st.subheader("📊 Task Tracker")
    st.write("Manage individual employee tasks with Kanban cards.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Organize, prioritize, and track progress.</p>", unsafe_allow_html=True)

with col2:
    st.subheader("👥 Employee Directory")
    st.write("View a comprehensive list of all team members.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Quick access to contact and role information.</p>", unsafe_allow_html=True)

with col3:
    st.subheader("🧑‍🏫 Employee Flashcards")
    st.write("See detailed, card-like views of each employee.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Individual profiles for focused insights.</p>", unsafe_allow_html=True)

# New row of columns for the remaining modules
col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("📈 Programs Dashboard")
    st.write("Get an overview of current and ongoing projects/programs.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Track progress and key metrics at a glance.</p>", unsafe_allow_html=True)

    # --- HERE'S WHERE WE ADD THE WIREFRAME IMAGE ---
    st.markdown("##### Wireframe Preview:")
    try:
        # Construct the path to your image
        # os.path.join handles differences in path separators across operating systems
        image_path = os.path.join("assets", "programs_dashboard_wireframe.png")
        st.image(image_path, caption="Programs Dashboard Wireframe (Design Preview)", use_column_width=True)
        st.caption("This is a design mockup from Figma. Actual implementation may vary.")
    except FileNotFoundError:
        st.warning("Wireframe image not found. Please ensure 'programs_dashboard_wireframe.png' is in the 'assets' folder.")
    # --- END OF WIREFRAME ADDITION ---

with col5:
    st.subheader("✍️ Attendance Marker")
    st.write("Mark your daily attendance easily.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Simple and efficient daily check-ins.</p>", unsafe_allow_html=True)

with col6:
    st.subheader("🛠️ Integrations")
    st.write("Future planned integrations to enhance workflow.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Connecting with other essential tools.</p>", unsafe_allow_html=True)


st.markdown("---")

# --- Next Steps / Roadmap Section ---
st.header("Future Roadmap:")
st.markdown("""
Our journey to a fully-featured PMU Management Suite continues. Here's what's next:
""")

phase_col1, phase_col2, phase_col3 = st.columns(3)

with phase_col1:
    st.markdown("#### **🚀 Phase 2: Core Module Implementation**")
    st.markdown("""
    - Implementing Employee Directory, Flashcards.
    - Setting up Programs Dashboard placeholder.
    - Foundation for Attendance Marker.
    """)

with phase_col2:
    st.markdown("#### **💾 Phase 3: Persistent Data Storage**")
    st.markdown("""
    - Transition from in-memory data to a robust database solution.
    - Ensuring all data (tasks, employees, attendance) is saved permanently.
    """)

with phase_col3:
    st.markdown("#### **📍 Phase 4: Advanced Attendance & Reporting**")
    st.markdown("""
    - Enhancing Attendance with Geotagging (researching Streamlit compatibility).
    - Developing a proper Calendar/Minutes of Meeting (MoM) system.
    """)

st.markdown("---")

# --- Footer ---
st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f0f2f6;
    color: #555;
    text-align: center;
    padding: 10px;
    font-size: 0.8em;
    border-top: 1px solid #e6e6e6;
}
</style>
<div class="footer">
    <p>PMU Management Suite © 2025 | Developed with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
