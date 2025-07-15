import streamlit as st

st.set_page_config(
    page_title="PMU Management Suite",
    page_icon="🏢",
    layout="wide" 
)


st.title("🏢 Welcome to the PMU Management Suite!")
st.markdown("---") 


st.write("""
This application is designed to help the Project Management Unit (PMU) streamline various operations,
from task tracking to employee management and attendance.
""")

st.info("💡 **Tip:** Navigate using the sidebar to explore different sections!")


st.header("Explore Our Modules:")

col1, col2, col3 = st.columns(3) 

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


col4, col5, col6 = st.columns(3)

with col4:
    st.subheader("📈 Programs Dashboard")
    st.write("Get an overview of current and ongoing projects/programs.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Track progress and key metrics at a glance.</p>", unsafe_allow_html=True)

   
    st.markdown("---") 
    st.markdown("### View Design Resources:")
    st.markdown("""
    Want to explore interactive design kits that inspire some of our layouts?
    Check out the **[Bloo Lo-Fi Wireframe Kit on Figma Community](https://www.figma.com/community/file/1119385966966606048/Bloo-Lo-Fi-Wireframe-Kit--Community-)**
    """)


with col5:
    st.subheader("✍️ Attendance Marker")
    st.write("Mark your daily attendance easily.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Simple and efficient daily check-ins.</p>", unsafe_allow_html=True)

with col6:
    st.subheader("🛠️ Integrations")
    st.write("Future planned integrations to enhance workflow.")
    st.markdown("<p style='font-size: smaller; color: gray;'>Connecting with other essential tools.</p>", unsafe_allow_html=True)


st.markdown("---")


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

st.markdown("""
<style>
.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #f0f2f6; /* Streamlit's default background for a subtle look */
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
