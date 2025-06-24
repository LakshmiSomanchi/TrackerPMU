# your_project_folder/pages/4_Programs_Dashboard.py
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Programs Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Programs Dashboard")
st.markdown("Overview and management of current projects/programs, including budget and spent tracking.")

# --- Session State Initialization for Program Data ---
# Structure: {program_name: {"budget": float, "tasks": [{"id": int, "name": str, "spent": float, "description": str}]}}
if 'programs_data' not in st.session_state:
    st.session_state.programs_data = {
        "Project Phoenix": {
            "budget": 100000.00,
            "tasks": [
                {"id": 1, "name": "Market Research", "spent": 15000.00, "description": "Conduct survey and analyze market trends."},
                {"id": 2, "name": "Product Design", "spent": 25000.00, "description": "Develop UI/UX mockups and prototypes."},
                {"id": 3, "name": "Team Recruitment", "spent": 10000.00, "description": "Hire specialized personnel for development."}
            ]
        },
        "Operation Dragon": {
            "budget": 75000.00,
            "tasks": [
                {"id": 1, "name": "Infrastructure Setup", "spent": 12000.00, "description": "Set up cloud servers and databases."},
                {"id": 2, "name": "Security Audit", "spent": 8000.00, "description": "Perform comprehensive security vulnerability assessment."}
            ]
        },
        "Initiative Horizon": {
            "budget": 50000.00,
            "tasks": [] # No tasks initially
        }
    }

# --- Helper function to calculate total spent and remaining budget ---
def calculate_program_financials(program_name):
    program = st.session_state.programs_data[program_name]
    total_spent = sum(task['spent'] for task in program['tasks'])
    remaining_budget = program['budget'] - total_spent
    return total_spent, remaining_budget

# --- Display Programs Overview ---
st.header("📈 Program Financial Overview")
if st.session_state.programs_data:
    overview_data = []
    for program_name, program_details in st.session_state.programs_data.items():
        total_spent, remaining_budget = calculate_program_financials(program_name)
        overview_data.append({
            "Program": program_name,
            "Budget": f"₹ {program_details['budget']:,.2f}",
            "Spent": f"₹ {total_spent:,.2f}",
            "Remaining": f"₹ {remaining_budget:,.2f}"
        })
    overview_df = pd.DataFrame(overview_data)
    st.dataframe(overview_df, hide_index=True)
else:
    st.info("No programs defined yet. Use the section below to add a new program.")

st.markdown("---")

# --- Add/Manage Programs Section ---
st.header("➕ Add/Manage Programs")
program_names = sorted(list(st.session_state.programs_data.keys()))

with st.expander("Add New Program"):
    with st.form("add_program_form"):
        new_program_name = st.text_input("New Program Name", key="new_program_name_input")
        new_program_budget = st.number_input("Initial Program Budget (₹)", min_value=0.00, value=0.00, step=1000.00, key="new_program_budget_input")
        add_program_button = st.form_submit_button("Add Program")

        if add_program_button:
            if new_program_name and new_program_name not in st.session_state.programs_data:
                st.session_state.programs_data[new_program_name] = {
                    "budget": new_program_budget,
                    "tasks": []
                }
                st.success(f"Program '{new_program_name}' added with budget ₹ {new_program_budget:,.2f}.")
                st.rerun()
            elif new_program_name:
                st.warning(f"Program '{new_program_name}' already exists.")
            else:
                st.error("Program name cannot be empty.")

# --- Select Program to Manage ---
st.markdown("### Select a Program to Manage Details")
if program_names:
    selected_program = st.selectbox("Choose a Program", program_names, key="selected_program_details")

    if selected_program:
        current_program = st.session_state.programs_data[selected_program]
        total_spent_for_selected, remaining_budget_for_selected = calculate_program_financials(selected_program)

        st.subheader(f"Details for: {selected_program}")
        st.write(f"**Budget:** ₹ {current_program['budget']:,.2f}")
        st.write(f"**Total Spent:** ₹ {total_spent_for_selected:,.2f}")
        st.write(f"**Remaining Budget:** ₹ {remaining_budget_for_selected:,.2f}")

        st.markdown("#### Update Program Budget")
        with st.form(f"update_budget_form_{selected_program}"):
            updated_budget = st.number_input("New Program Budget (₹)", min_value=0.00, value=current_program['budget'], step=1000.00, key=f"update_budget_{selected_program}")
            update_budget_button = st.form_submit_button("Update Budget")
            if update_budget_button:
                st.session_state.programs_data[selected_program]['budget'] = updated_budget
                st.success(f"Budget for '{selected_program}' updated to ₹ {updated_budget:,.2f}.")
                st.rerun()

        st.markdown("#### Tasks Under This Program")
        # Display tasks in a DataFrame
        if current_program['tasks']:
            tasks_df = pd.DataFrame(current_program['tasks'])
            tasks_df['Spent'] = tasks_df['spent'].apply(lambda x: f"₹ {x:,.2f}")
            st.dataframe(tasks_df[['id', 'name', 'description', 'Spent']], hide_index=True)
        else:
            st.info(f"No tasks defined for '{selected_program}' yet.")

        # --- Add New Task to Program ---
        st.markdown("##### Add New Task")
        with st.form(f"add_task_form_{selected_program}"):
            new_task_name = st.text_input("Task Name", key=f"new_task_name_{selected_program}")
            new_task_description = st.text_area("Task Description", key=f"new_task_desc_{selected_program}")
            initial_spent = st.number_input("Initial Spent for Task (₹)", min_value=0.00, value=0.00, step=100.00, key=f"initial_spent_{selected_program}")
            add_task_button = st.form_submit_button("Add Task")

            if add_task_button:
                if new_task_name:
                    next_task_id = max([t['id'] for t in current_program['tasks']]) + 1 if current_program['tasks'] else 1
                    new_task = {
                        "id": next_task_id,
                        "name": new_task_name,
                        "description": new_task_description,
                        "spent": initial_spent
                    }
                    st.session_state.programs_data[selected_program]['tasks'].append(new_task)
                    st.success(f"Task '{new_task_name}' added to '{selected_program}'.")
                    st.rerun()
                else:
                    st.error("Task name cannot be empty.")

        # --- Update Spent for Existing Task ---
        if current_program['tasks']:
            st.markdown("##### Update Spent for an Existing Task")
            task_options = [f"{t['name']} (ID: {t['id']})" for t in current_program['tasks']]
            selected_task_display = st.selectbox("Select Task to Update Spent", task_options, key=f"select_task_to_update_{selected_program}")

            if selected_task_display:
                selected_task_id = int(selected_task_display.split("(ID: ")[1][:-1])
                current_task = next((t for t in current_program['tasks'] if t['id'] == selected_task_id), None)

                if current_task:
                    with st.form(f"update_task_spent_form_{selected_program}_{selected_task_id}"):
                        st.write(f"**Task:** {current_task['name']}")
                        st.write(f"**Current Spent:** ₹ {current_task['spent']:,.2f}")
                        new_spent_amount = st.number_input("New Spent Amount (₹)", min_value=0.00, value=current_task['spent'], step=100.00, key=f"new_spent_amount_{selected_program}_{selected_task_id}")
                        update_spent_button = st.form_submit_button("Update Task Spent")

                        if update_spent_button:
                            for i, task in enumerate(st.session_state.programs_data[selected_program]['tasks']):
                                if task['id'] == selected_task_id:
                                    st.session_state.programs_data[selected_program]['tasks'][i]['spent'] = new_spent_amount
                                    break
                            st.success(f"Spent for task '{current_task['name']}' updated to ₹ {new_spent_amount:,.2f}.")
                            st.rerun()
                else:
                    st.error("Selected task not found.")
        else:
            st.info("Add tasks first to update their spent amounts.")
else:
    st.info("No programs available to manage. Add a new program above.")
